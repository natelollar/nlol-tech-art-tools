import re
import tomllib
from importlib import reload
from pathlib import Path

from maya import cmds, mel
from nlol.core import general_utils
from nlol.core.rig_setup import common_build_functions
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

reload(general_utils)
reload(common_build_functions)
reload(rig_folder_path)

swap_side_str = general_utils.swap_side_str
get_top_parent = general_utils.get_top_parent
CommonBuildFunctions = common_build_functions.CommonBuildFunctions

rig_folderpath = rig_folder_path.rig_folderpath
default_blendshapes_filepath = rig_folderpath / "blendshapes.ma"
default_setdrivenkeys_filepath = rig_folderpath / "blendshape_setdrivenkeys.toml"


class ConnectBlendShapes:
    def __init__(
        self,
        blendshapes_filepath: Path = default_blendshapes_filepath,
        setdrivenkeys_filepath: Path = default_setdrivenkeys_filepath,
    ):
        self.blendshapes_filepath = blendshapes_filepath
        self.setdrivenkeys_filepath = setdrivenkeys_filepath

        self.logger = get_logger()

    def build(self):
        """Create setup for rig blendshapes.
        --------------------------------------------------
        Import and transfer blendshapes from "blendshapes.ma".
        Connect blendshapes to ctrls from "rig_helpers.ma".
        Useful for face blendshape setup.
        """
        cmds.undoInfo(openChunk=True)
        try:
            self.blendshapes_file_import()
            self.find_transfer_blendshapes()
            top_ctrl_grp = self.setdrivenkey_connections()
            self.top_grouping(top_ctrl_grp)
            self.cleanup_leftovers()
        finally:
            cmds.undoInfo(closeChunk=True)

    def blendshapes_file_import(self):
        """Import blendshapes file containing meshes with blendshape nodes
        holding the blendshape weights.
        The meshes will have the string "BlendShapes" in name, but otherwise,
        be named same as original mesh.
        """
        if not Path(self.blendshapes_filepath).is_file():
            msg = (
                '"blendshapes.ma" not in rig folder. Skipping blendshape import.\n'
                f'File not found: "{self.blendshapes_filepath}".'
            )
            self.logger.info(msg)
            return

        cmds.file(self.blendshapes_filepath, i=True)

    def find_transfer_blendshapes(self):
        """Find blendshape meshes and there matches.
        Then transfer blendshapes to the matching meshes.
        """
        mesh_shps = cmds.ls(type="mesh", noIntermediate=True)
        meshes = [cmds.listRelatives(shp, parent=True)[0] for shp in mesh_shps]
        blendshape_meshes = [mesh for mesh in meshes if "blendshape" in mesh.lower()]
        matching_meshes = []
        for mesh in blendshape_meshes:
            matching_mesh = re.sub(r"blendshapes?", "", mesh, flags=re.IGNORECASE)
            matching_meshes.append(matching_mesh)

        if len(blendshape_meshes) != len(matching_meshes):
            msg = (
                f"Not finding matches for blendshape meshes: {blendshape_meshes}\n"
                'Blendshapes meshes should contain "BlendShapes" string'
                " and otherwise match target mesh string."
            )
            self.logger.error(msg)
            raise ValueError(msg)

        for source_mesh, target_mesh in zip(blendshape_meshes, matching_meshes, strict=False):
            if cmds.objExists(target_mesh):
                self.transfer_blendshapes(source_mesh, target_mesh)
            else:
                self.logger.warning(
                    f'Target mesh not exist: "{target_mesh}". Skipping blendshape transfer.',
                )

        # instance variables
        self.meshes_with_blendshapes = matching_meshes

    def transfer_blendshapes(self, source_mesh, target_mesh):
        """Transfer blendshapes from "source mesh" to "target mesh".
        These two meshes should have identical topology.
        Helpful if saving blendshapes in separate file from main model.

        Args:
            source_mesh: Source mesh with blendshape node.
            target_mesh: Mesh to have blendshape node weights copied to.

        """
        # get source blendshape node
        source_blendshape_nd = cmds.ls(cmds.listHistory(source_mesh), type="blendShape")[0]
        source_blendshapes = cmds.listAttr(f"{source_blendshape_nd}.weight", multi=True)

        # create target blendshape node
        target_blendshape_nd = cmds.blendShape(target_mesh, frontOfChain=True)[0]

        # transfer blendshapes
        for i, blendshape in enumerate(source_blendshapes):
            cmds.setAttr(f"{source_blendshape_nd}.{blendshape}", 1)
            blendshape_duplicate = cmds.duplicate(source_mesh)[0]
            cmds.setAttr(f"{source_blendshape_nd}.{blendshape}", 0)

            cmds.blendShape(
                target_blendshape_nd,
                edit=True,
                target=(target_mesh, i, blendshape_duplicate, 1.0),
            )
            cmds.aliasAttr(blendshape, f"{target_blendshape_nd}.weight[{i}]")
            cmds.delete(blendshape_duplicate)

        # delete old source mesh
        cmds.delete(source_mesh)

        # rename blendshape node after deleting source
        blendshape_nd_name = f"{target_mesh}BlendShape"
        cmds.rename(target_blendshape_nd, blendshape_nd_name)

    def setdrivenkey_connections(self) -> str:
        """Connect blendshapes or other object attributes to transform ctrls
        via set driven keys.

        Returns:
            Top grp for setdrivenkey ctrls.

        """
        if not Path(self.setdrivenkeys_filepath).is_file():
            msg = (
                '"blendshape_setdrivenkeys.toml" not in rig folder. '
                "Skipping blendshape setdrivenkey connections.\n"
                f'File not found: "{self.setdrivenkeys_filepath}".'
            )
            self.logger.info(msg)
            return None

        with open(self.setdrivenkeys_filepath, "rb") as f:
            toml_data = tomllib.load(f)
        # ----- base values -----
        # get blendshape nodes from meshes
        try:
            blendshape_objs = self.meshes_with_blendshapes  # get mesh names from already imported
        except Exception:
            blendshape_objs = toml_data.get("blendshape_objs", "")  # get mesh names from toml
            blendshape_objs = blendshape_objs.split(",")
            blendshape_objs = [txt.strip() for txt in blendshape_objs if txt.strip()]
        blendshape_nds = []
        if blendshape_objs:
            for obj in blendshape_objs:
                obj_shp = cmds.listRelatives(obj, shapes=True)
                blendshape_nd = cmds.listConnections(obj_shp, type="blendShape")
                blendshape_nds.extend(blendshape_nd)
        blendshape_nds = list(set(blendshape_nds))
        # set driven key in/out tangents
        in_tangent_type = toml_data.get("inTangentType", "linear")
        out_tangent_type = toml_data.get("outTangentType", "linear")

        # data list
        setdrivenkeys_data = toml_data["setdrivenkeys"]

        # ----- get top ctrl grp -----
        first_crv = setdrivenkeys_data[0]["transform_crv"]
        top_ctrl_grp = get_top_parent(first_crv)

        # ----- get mirrored "setdrivenkeys" -----
        right_setdrivenkeys_data = []
        for data in setdrivenkeys_data:
            mirror_right = data.get("mirror_right")
            mirror_right_invert = data.get("mirror_right_invert")
            if mirror_right:
                blendshape_attr = swap_side_str(data.get("blendshape_attr", ""))
                object_attr = swap_side_str(data.get("object_attr"))
                transform_crv = swap_side_str(data["transform_crv"])

                crv_end = data.get("crv_end")
                crv_end = crv_end or 1.0
                if mirror_right_invert:
                    crv_end = -crv_end  # invert float

                data_dict = {
                    "blendshape_attr": blendshape_attr,
                    "object_attr": object_attr,
                    "transform_crv": transform_crv,
                    "crv_attr": data["crv_attr"],
                    "blendshape_start": data.get("blendshape_start"),
                    "blendshape_end": data.get("blendshape_end"),
                    "crv_start": data.get("crv_start"),
                    "crv_end": crv_end,
                }
                right_setdrivenkeys_data.append(data_dict)
        setdrivenkeys_data.extend(right_setdrivenkeys_data)

        # ----- iterate through "setdrivenkeys" -----
        for data in setdrivenkeys_data:
            blendshape_attr = data.get("blendshape_attr", "")
            object_attr = data.get("object_attr")
            transform_crv = data["transform_crv"]
            crv_attr = data["crv_attr"]
            blendshape_start = data.get("blendshape_start")
            blendshape_end = data.get("blendshape_end")
            crv_start = data.get("crv_start")
            crv_end = data.get("crv_end")

            blendshape_start = blendshape_start or 0.0
            blendshape_end = blendshape_end or 1.0
            crv_start = crv_start or 0.0
            crv_end = crv_end or 1.0

            if object_attr and blendshape_attr:
                msg = (
                    'Cannot have "object_attr" and "blendshape_attr" paremeters together. '
                    f"{object_attr = } "
                    f"{blendshape_attr = }"
                )
                self.logger.error(msg)
                raise ValueError(msg)

            if object_attr:
                # start
                cmds.setDrivenKeyframe(
                    object_attr,
                    currentDriver=f"{transform_crv}.{crv_attr}",
                    value=blendshape_start,
                    driverValue=crv_start,
                    inTangentType=in_tangent_type,
                    outTangentType=out_tangent_type,
                )
                # end
                cmds.setDrivenKeyframe(
                    object_attr,
                    currentDriver=f"{transform_crv}.{crv_attr}",
                    value=blendshape_end,
                    driverValue=crv_end,
                    inTangentType=in_tangent_type,
                    outTangentType=out_tangent_type,
                )

            if not blendshape_nds:  # skip
                continue
            for blendshape_nd in blendshape_nds:
                if cmds.objExists(f"{blendshape_nd}.{blendshape_attr}"):
                    # start
                    cmds.setDrivenKeyframe(
                        f"{blendshape_nd}.{blendshape_attr}",
                        currentDriver=f"{transform_crv}.{crv_attr}",
                        value=blendshape_start,
                        driverValue=crv_start,
                        inTangentType=in_tangent_type,
                        outTangentType=out_tangent_type,
                    )
                    # end
                    cmds.setDrivenKeyframe(
                        f"{blendshape_nd}.{blendshape_attr}",
                        currentDriver=f"{transform_crv}.{crv_attr}",
                        value=blendshape_end,
                        driverValue=crv_end,
                        inTangentType=in_tangent_type,
                        outTangentType=out_tangent_type,
                    )
                else:
                    msg = (
                        f'Does not exist. Skipping connection: "{blendshape_nd}.{blendshape_attr}"'
                    )
                    self.logger.info(msg)

        return top_ctrl_grp

    def top_grouping(self, top_ctrl_grp: str):
        """Parent ctrl grp to top rig grp.

        Args:
            top_ctrl_grp: Main ctrl grp.

        """
        CommonBuildFunctions().top_rig_grouping(top_ctrl_grp)

    def cleanup_leftovers(self):
        """Remove unused nodes, specifically,
        leftover materials from blendshape mesh import.
        Also, remove leftover display layers.
        """
        # remove duplicate materials
        mel.eval("MLdeleteUnused;")

        # remove leftover layers
        scene_display_lyrs = cmds.ls(type="displayLayer")
        for lyr in scene_display_lyrs:
            if lyr not in ["defaultLayer", "geo_lyr", "joints_lyr"]:
                cmds.delete(lyr)
