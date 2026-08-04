import re
import tomllib
from importlib import reload
from pathlib import Path

from maya import cmds, mel
from nlol.core import general_utils
from nlol.core.rig_setup import common_build_functions
from nlol.defaults.rig_folder_path import rig_folderpath
from nlol.utilities.nlol_maya_logger import get_logger

reload(general_utils)
reload(common_build_functions)

swap_side_str = general_utils.swap_side_str
get_top_parent = general_utils.get_top_parent
CommonBuildFunctions = common_build_functions.CommonBuildFunctions


class ConnectBlendShapes:
    """Connect mesh blendshapes and/or rig controls via set driven keys.
    Drive with other rig controls/ attributes.
    Set up connections via toml config file; "blendshape_setdrivenkeys.toml".
    Store blendshapes under single meshes in "blendshapes.ma".
    Default file location is in main nLol rig folder.
    """

    def __init__(
        self,
        blendshapes_filepath: Path | None = None,
        setdrivenkeys_filepath: Path | None = None,
    ):
        """Initialize class.

        Args:
            blendshapes_filepath: Custom filepath location for maya file containing blendshapes.
                Otherwise uses default.
            setdrivenkeys_filepath: Custom filepath location for set drive key config file.
                Otherwise uses default location.

        """
        self.blendshapes_filepath = blendshapes_filepath or (rig_folderpath() / "blendshapes.ma")
        self.setdrivenkeys_filepath = setdrivenkeys_filepath or (
            rig_folderpath() / "blendshape_setdrivenkeys.toml"
        )

        self.logger = get_logger()

    def build_import(self):
        """Create setup for rig blendshapes.
        --------------------------------------------------
        Import and transfer blendshapes from "blendshapes.ma".
        Useful for face blendshape setup.
        """
        self.blendshapes_file_import()
        meshes_with_blendshapes = self.find_transfer_blendshapes()
        self.cleanup_leftovers()

        return meshes_with_blendshapes

    def build_connect(self, meshes_with_blendshapes: list[str]):
        """Finish setup for rig blendshapes.
        --------------------------------------------------
        Connects blendshapes to ctrls from "rig_helpers.ma" or
        connect to ctrls built from a rig module.

        Args:
            meshes_with_blendshapes: Scene mesh transforms that have a connected blendshape node.

        """
        top_ctrl_grps = self.setdrivenkey_connections(meshes_with_blendshapes)
        self.top_grouping(top_ctrl_grps)

    def blendshapes_file_import(self):
        """Import blendshapes file containing meshes with blendshape nodes
        holding the blendshape weights.
        The meshes will have the string "BlendShapes" in name, but otherwise,
        be named same as original mesh.
        """
        if not Path(self.blendshapes_filepath).is_file():
            msg = '"blendshapes.ma" not in rig folder. Skipping import...\n'
            self.logger.info(msg)
            msg = f"File not found: {self.blendshapes_filepath}"
            self.logger.debug(msg)

            return

        cmds.file(self.blendshapes_filepath, i=True)

    def find_transfer_blendshapes(self) -> list[str]:
        """Find blendshape meshes and there matches.
        Then transfer blendshapes to the matching meshes.

        Returns:
            List of scene mesh transforms with blendshapes.
            Meshes that found a match and had blendshapes applied from imported meshes.

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

        return matching_meshes

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

    def setdrivenkey_connections(self, meshes_with_blendshapes: list[str]) -> str:
        """Connect blendshapes or other object attributes to transform ctrls
        via set driven keys.

        Args:
            meshes_with_blendshapes: Scene mesh transforms that have a connected blendshape node.

        Returns:
            Scene top grp for setdrivenkey ctrls.

        """
        if not Path(self.setdrivenkeys_filepath).is_file():
            msg = (
                '"blendshape_setdrivenkeys.toml" not in rig folder. '
                "Skipping blendshape setdrivenkey setup..."
            )
            self.logger.info(msg)

            msg = f"File not found: {self.setdrivenkeys_filepath}"
            self.logger.debug(msg)

            return None

        with open(self.setdrivenkeys_filepath, "rb") as f:
            toml_data = tomllib.load(f)
        # ----- base values -----
        # get blendshape nodes from meshes
        try:
            blendshape_objs = meshes_with_blendshapes  # get mesh names from already imported
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
        start_in_tangent_type = toml_data.get("start_in_tangent_type", "linear")
        start_out_tangent_type = toml_data.get("start_out_tangent_type", "linear")
        mid_in_tangent_type = toml_data.get("mid_in_tangent_type", "auto")
        mid_out_tangent_type = toml_data.get("mid_out_tangent_type", "auto")
        end_in_tangent_type = toml_data.get("end_in_tangent_type", "linear")
        end_out_tangent_type = toml_data.get("end_out_tangent_type", "linear")

        # data list
        setdrivenkeys_data = toml_data["setdrivenkeys"]

        # ----- get mirrored "setdrivenkeys" -----
        right_setdrivenkeys_data = []
        for data in setdrivenkeys_data:
            mirror_right = data.get("mirror_right")
            mirror_right_invert = data.get("mirror_right_invert")
            if mirror_right:
                blendshape_attr = swap_side_str(data.get("blendshape_attr", ""))
                object_attr = swap_side_str(data.get("object_attr", ""))
                transform_crv = swap_side_str(data.get("transform_crv", ""))
                transform_crv_attr = swap_side_str(data.get("transform_crv_attr", ""))

                crv_end = data.get("crv_end")
                crv_end = crv_end or 1.0
                if mirror_right_invert:
                    crv_end = -crv_end  # invert float

                blendshape_fix_attrs = swap_side_str(data.get("blendshape_fix_attrs", ""))

                right_dict = data.copy()  # copy original mod dict
                right_dict_updates = {
                    "blendshape_attr": blendshape_attr,
                    "object_attr": object_attr,
                    "transform_crv": transform_crv,
                    "crv_end": crv_end,
                    "blendshape_fix_attrs": blendshape_fix_attrs,
                }
                right_dict.update(
                    {key: value for key, value in right_dict_updates.items() if key in data},
                )

                right_setdrivenkeys_data.append(right_dict)
        setdrivenkeys_data.extend(right_setdrivenkeys_data)

        # ----- iterate through "setdrivenkeys" -----
        active_transform_values = {}  # transform data for transformLimits
        crv_top_grps = []
        for data in setdrivenkeys_data:
            blendshape_attr = data.get("blendshape_attr", "")
            object_attr = data.get("object_attr", "")
            transform_crv = data.get("transform_crv", "")
            crv_attr = data.get("crv_attr", "")
            transform_crv_attr = data.get("transform_crv_attr", "")

            blendshape_start = data.get("blendshape_start")
            blendshape_mid = data.get("blendshape_mid")
            blendshape_end = data.get("blendshape_end")
            object_start = data.get("object_start")
            object_mid = data.get("object_mid")
            object_end = data.get("object_end")
            crv_start = data.get("crv_start")
            crv_mid = data.get("crv_mid")
            crv_end = data.get("crv_end")
            blendshape_fix_attrs = data.get("blendshape_fix_attrs", "").split(",")
            blendshape_fix_attrs = [txt.strip() for txt in blendshape_fix_attrs if txt.strip()]

            if (transform_crv_attr and transform_crv) or (transform_crv_attr and crv_attr):
                msg = (
                    '"Check file: "blenshape_setdrivenkeys.toml"\n'
                    'Cannot have "transform_crv_attr" with "transform_crv"/"crv_attr" parameters.\n'
                    f"{transform_crv_attr = }\n"
                    f"{transform_crv = }\n"
                    f"{crv_attr = }\n"
                )
                self.logger.error(msg)
                raise ValueError(msg)
            if transform_crv_attr:
                transform_crv_attr_split = transform_crv_attr.split(".")
                transform_crv = transform_crv_attr_split[0]
                crv_attr = ".".join(transform_crv_attr_split[1:])

            if (blendshape_start and object_start) or (blendshape_end and object_end):
                msg = (
                    '"Check file: "blendshape_setdrivenkeys.toml"\n'
                    'Cannot have "blendshape_start/end" and "object_start/end" parameters.\n'
                    f"{blendshape_start = }\n"
                    f"{blendshape_end = }\n"
                    f"{object_start = }\n"
                    f"{object_end = }"
                )
                self.logger.error(msg)
                raise ValueError(msg)
            blendshape_start = blendshape_start or object_start or 0.0
            blendshape_mid = blendshape_mid or object_mid or None
            blendshape_end = blendshape_end or object_end or 1.0
            crv_start = crv_start or 0.0
            crv_mid = crv_mid or None
            crv_end = crv_end or 1.0

            if object_attr and blendshape_attr:
                msg = (
                    '"Check file: "blenshape_setdrivenkeys.toml"\n'
                    'Cannot have "object_attr" and "blendshape_attr" paremeters together.\n'
                    f"{object_attr = }\n"
                    f"{blendshape_attr = }"
                )
                self.logger.error(msg)
                raise ValueError(msg)

            # key object transform based on crv positions
            if object_attr:  # example: "mouthCorner_left_ctrl.translateY"
                if cmds.objExists(object_attr):
                    cmds.setDrivenKeyframe(  # start key
                        object_attr,
                        currentDriver=f"{transform_crv}.{crv_attr}",
                        value=blendshape_start,
                        driverValue=crv_start,
                        inTangentType=start_in_tangent_type,
                        outTangentType=start_out_tangent_type,
                    )
                    if blendshape_mid:
                        cmds.setDrivenKeyframe(  # middle key
                            object_attr,
                            currentDriver=f"{transform_crv}.{crv_attr}",
                            value=blendshape_mid,
                            driverValue=crv_mid,
                            inTangentType=mid_in_tangent_type,
                            outTangentType=mid_out_tangent_type,
                        )
                    cmds.setDrivenKeyframe(  # end key
                        object_attr,
                        currentDriver=f"{transform_crv}.{crv_attr}",
                        value=blendshape_end,
                        driverValue=crv_end,
                        inTangentType=end_in_tangent_type,
                        outTangentType=end_out_tangent_type,
                    )
                    active_transform_values.setdefault(f"{transform_crv}.{crv_attr}", []).extend(
                        [crv_start, crv_end],
                    )
                else:
                    msg = f'Does not exist. Skipping connection: "{object_attr}"'
                    self.logger.info(msg)

            if not blendshape_nds or not blendshape_attr:  # skip
                continue
            # key blendshape weights based on crv positions
            for blendshape_nd in blendshape_nds:
                if cmds.objExists(f"{blendshape_nd}.{blendshape_attr}"):
                    cmds.setDrivenKeyframe(  # start key
                        f"{blendshape_nd}.{blendshape_attr}",
                        currentDriver=f"{transform_crv}.{crv_attr}",
                        value=blendshape_start,
                        driverValue=crv_start,
                        inTangentType=start_in_tangent_type,
                        outTangentType=start_out_tangent_type,
                    )
                    if blendshape_mid:
                        cmds.setDrivenKeyframe(  # middle key
                            f"{blendshape_nd}.{blendshape_attr}",
                            currentDriver=f"{transform_crv}.{crv_attr}",
                            value=blendshape_mid,
                            driverValue=crv_mid,
                            inTangentType=mid_in_tangent_type,
                            outTangentType=mid_out_tangent_type,
                        )
                    cmds.setDrivenKeyframe(  # end key
                        f"{blendshape_nd}.{blendshape_attr}",
                        currentDriver=f"{transform_crv}.{crv_attr}",
                        value=blendshape_end,
                        driverValue=crv_end,
                        inTangentType=end_in_tangent_type,
                        outTangentType=end_out_tangent_type,
                    )
                    active_transform_values.setdefault(f"{transform_crv}.{crv_attr}", []).extend(
                        [crv_start, crv_end],
                    )
                else:
                    msg = (
                        f'Does not exist. Skipping connection: "{blendshape_nd}.{blendshape_attr}"'
                    )
                    self.logger.debug(msg)

                # connect corrective blendshape weights
                for fix_attr in blendshape_fix_attrs:
                    if cmds.objExists(f"{blendshape_nd}.{fix_attr}"):
                        multiply_nd = cmds.listConnections(
                            f"{blendshape_nd}.{fix_attr}",
                            source=True,
                            type="multiply",
                        )
                        if multiply_nd:  # if mult node, get attached set range node
                            setrange_nd = list(
                                set(
                                    cmds.listConnections(
                                        multiply_nd,
                                        source=True,
                                        type="setRange",
                                    ),
                                ),
                            )
                            multiply_nd = multiply_nd[0]
                            setrange_nd = setrange_nd[0]
                        else:
                            multiply_nd = cmds.createNode(
                                "multiply",
                                name=f"{fix_attr}Multiply",
                            )
                            setrange_nd = cmds.createNode(
                                "setRange",
                                name=f"{fix_attr}SetRange",
                            )
                            cmds.connectAttr(f"{multiply_nd}.output", f"{blendshape_nd}.{fix_attr}")
                            cmds.connectAttr(f"{setrange_nd}.outValueX", f"{multiply_nd}.input[0]")
                            cmds.connectAttr(f"{setrange_nd}.outValueY", f"{multiply_nd}.input[1]")
                            cmds.connectAttr(f"{setrange_nd}.outValueZ", f"{multiply_nd}.input[2]")
                            cmds.setAttr(f"{setrange_nd}.valueX", 1.0)
                            cmds.setAttr(f"{setrange_nd}.valueY", 1.0)
                            cmds.setAttr(f"{setrange_nd}.valueZ", 1.0)
                            cmds.setAttr(f"{setrange_nd}.maxX", 1.0)
                            cmds.setAttr(f"{setrange_nd}.maxY", 1.0)
                            cmds.setAttr(f"{setrange_nd}.maxZ", 1.0)

                        # transform crv (ctrl) to setRange node, to control corrective blendshape
                        crv_attr_axis = (crv_attr[-1]).capitalize()
                        cmds.connectAttr(
                            f"{transform_crv}.{crv_attr}",
                            f"{setrange_nd}.value{crv_attr_axis}",
                        )
                        crv_start_end = [crv_start, crv_end]  # set negative end values to Min
                        low_val, high_val = min(crv_start_end), max(crv_start_end)
                        cmds.setAttr(f"{setrange_nd}.oldMin{crv_attr_axis}", low_val)
                        cmds.setAttr(f"{setrange_nd}.oldMax{crv_attr_axis}", high_val)
                        # reverse min max range if crv_end in negative
                        if low_val < 0:
                            cmds.setAttr(f"{setrange_nd}.min{crv_attr_axis}", 1.0)
                            cmds.setAttr(f"{setrange_nd}.max{crv_attr_axis}", 0.0)

            # get top grps for parenting
            crv_top_grp = get_top_parent(transform_crv)
            crv_top_grps.append(crv_top_grp)

        # ----- set transform limits -----
        # lock and hide attrs first
        for transform_crv_attr in active_transform_values:
            transform_crv = transform_crv_attr.split(".")[0]
            lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
            for axis in "XYZ":
                cmds.setAttr(f"{transform_crv}.translate{axis}", **lock_hide_kwargs)
                cmds.setAttr(f"{transform_crv}.rotate{axis}", **lock_hide_kwargs)
                cmds.setAttr(f"{transform_crv}.scale{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{transform_crv}.visibility", **lock_hide_kwargs)

        for transform_crv_attr, values in active_transform_values.items():
            transform_crv = transform_crv_attr.split(".")[0]
            crv_attr = transform_crv_attr.split(".")[1]
            low_val, high_val = min(values), max(values)
            self.logger.debug(f"{transform_crv_attr = }")
            self.logger.debug(f"{values = }")
            self.logger.debug(f"{low_val = }")
            self.logger.debug(f"{high_val = }")

            # unlock and show attr to limit
            cmds.setAttr(transform_crv_attr, keyable=True, lock=False)

            # enable and set limit values on attr
            if crv_attr in ["translateY", "ty"]:
                cmds.transformLimits(
                    transform_crv,
                    translationY=[low_val, high_val],
                    enableTranslationY=[1, 1],
                )
            elif crv_attr in ["translateX", "tx"]:
                cmds.transformLimits(
                    transform_crv,
                    translationX=[low_val, high_val],
                    enableTranslationX=[1, 1],
                )
            elif crv_attr in ["translateZ", "tz"]:
                cmds.transformLimits(
                    transform_crv,
                    translationZ=[low_val, high_val],
                    enableTranslationZ=[1, 1],
                )

        # ----- remove duplicate top group strings -----
        top_ctrl_grps = list(set(crv_top_grps))

        return top_ctrl_grps

    def top_grouping(self, top_ctrl_grps: str):
        """Parent ctrl grp to top rig grp.

        Args:
            top_ctrl_grps: Main ctrl grp.

        """
        CommonBuildFunctions().top_rig_grouping(top_ctrl_grps)

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
