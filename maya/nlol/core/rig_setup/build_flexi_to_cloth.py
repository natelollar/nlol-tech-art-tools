import json
from importlib import reload

from maya import cmds, mel
from nlol.core.rig_components import create_control_groups, create_nurbs_curves
from nlol.defaults import rig_folder_path
from nlol.core import general_utils
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_folder_path)

create_ctrl_grps = create_control_groups.create_ctrl_grps
add_divider_attribue = general_utils.add_divider_attribue

rig_folderpath = rig_folder_path.rig_folderpath
cloth_data_folderpath = rig_folderpath / "cloth_data"
collision_mesh_filepath = cloth_data_folderpath / "collision_meshes.json"


class FlexiToCloth:
    """Create nCloth blendshape setup for flexi/ribbon geometry.
    Create ctrl for toggling on/off.
    """

    def __init__(self):
        self.logger = get_logger()

    def build(self):
        """Entry point. Run this method.
        --------------------------------------------------
        """
        # check if cloth data in rig folder
        cloth_verts_filepaths = list(cloth_data_folderpath.glob("*DynamicConstraint.json"))
        if not list(cloth_verts_filepaths):
            msg = (
                '"*DynamicConstraint.json" files not in rig "cloth_data" folder. '
                "Skipping cloth setup."
            )
            self.logger.info(msg)
            return

        # run main methods
        cmds.undoInfo(openChunk=True)
        try:
            self.build_top_grps()
            self.build_aux_ctrl()
            self.build_main()
        finally:
            cmds.undoInfo(closeChunk=True)

    def build_top_grps(self):
        """Create top groups for organization."""
        self.top_grp = cmds.group(empty=True, name="nClothMain_grp")
        self.components_grp = cmds.group(empty=True, name="nClothComponents_grp")

        cmds.parent(self.components_grp, self.top_grp)

        top_nodes = cmds.ls(assemblies=True)
        for obj in top_nodes:
            if "_rigGrp" in obj:
                cmds.parent(self.top_grp, obj)  # parent to main rig group

        for grp in [self.top_grp, self.components_grp]:
            for axis in "XYZ":
                cmds.setAttr(f"{grp}.translate{axis}", lock=True)
                cmds.setAttr(f"{grp}.rotate{axis}", lock=True)
                cmds.setAttr(f"{grp}.scale{axis}", lock=True)
        cmds.setAttr(f"{self.components_grp}.visibility", 0)

    def build_main(self, apply_cloth_settings: bool = True) -> None:
        """Create nCloth setup for rigging. Constrains cloth mesh to attach meshes with
        "Point to Surface". Multiple cloth meshes and attach meshes allowed.
        Save cloth data to cloth_data folder first. Save data with save_vertex_ids(),
        save_collision_meshes() if collision needed, and optionally save_ncloth_settings().

        This will set up nCloth for each "*DynamicConstraint.json" in cloth_data folder.
        Each dictionary in list returned from get_saved_vertex_ids() contains
        vertex ids, vertex/cloth mesh, and constraint/attach mesh. Also, the "collision_meshes.json"
        contains collision mesh names. And any "*Settings.json" in cloth_data folder contain
        saved nCloth settings that are applied at the end.

        Args:
            apply_cloth_settings: Use pre-saved nCloth settings in cloth_data folder.

        """
        self.ncloth_attr_index = 0
        flexi_mesh_current = None
        nucleus_nd = None
        attach_mesh_datas = self.get_saved_vertex_ids()
        # ----- iterate through cloth data -----
        # constrain cloth verts to meshes
        for attach_mesh_data in attach_mesh_datas:
            flexi_mesh = attach_mesh_data["vertex_mesh"]
            flexi_mesh_shp = cmds.listRelatives(flexi_mesh, shapes=True)[0]
            if flexi_mesh != flexi_mesh_current:  # if new mesh for cloth, not just new attach mesh
                # ----- duplicate for blendshape -----
                flexi_base_name = flexi_mesh.split("_")[0]
                cloth_mesh = flexi_mesh.replace(flexi_base_name, f"{flexi_base_name}Cloth")
                if not cmds.objExists(cloth_mesh):
                    cmds.duplicate(flexi_mesh, name=cloth_mesh)
                # top grp parenting
                cmds.parent(cloth_mesh, self.top_grp)
            attach_vertices = attach_mesh_data["attach_vertices"]
            attach_vertices = [vert.replace(flexi_mesh, cloth_mesh) for vert in attach_vertices]
            attach_mesh = attach_mesh_data["attach_mesh"]
            cloth_mesh_shp = cmds.listRelatives(cloth_mesh, shapes=True)[0]
            attach_mesh_shp = cmds.listRelatives(attach_mesh, shapes=True)[0]
            # top grp parenting
            cmds.parent(attach_mesh, self.top_grp)
            cmds.setAttr(f"{attach_mesh}.visibility", 0)

            # ----- apply nCloth -----
            # skip if already created for another attach mesh
            if not cmds.listConnections(cloth_mesh_shp, type="nCloth"):
                cmds.select(nucleus_nd)
                cmds.select(cloth_mesh, add=True)
                mel.eval("createNCloth 0;")  # 0 is Local Space Output
                cmds.select(clear=True)
                self.logger.debug(f'nCloth generated for: "{cloth_mesh_shp}"')

            # ----- constrain verts to attach object -----
            # apply point to surface constraint
            cmds.select(attach_vertices)
            cmds.select(attach_mesh, add=True)
            mel.eval("createNConstraint pointToSurface 0;")  # 0 is Use Sets off

            # ----- find and name nodes -----
            # name ncloth and nucleus nodes
            ncloth_nd = cmds.listConnections(cloth_mesh_shp, type="nCloth")[0]
            ncloth_nd = cmds.rename(ncloth_nd, f"{cloth_mesh}NCloth")
            ncloth_nd_shp = cmds.listConnections(cloth_mesh_shp, type="nCloth", shapes=True)[0]
            self.logger.debug(f"{ncloth_nd = }")  # nCloth
            if not nucleus_nd:  # if not identified and renamed yet for rig
                nucleus_nd = cmds.listConnections(ncloth_nd_shp, type="nucleus")[0]
                nucleus_nd = cmds.rename(nucleus_nd, "main_nucleus")
                # nucleus settings
                cmds.setAttr(f"{nucleus_nd}.spaceScale", 0.01)  # global scale: unreal/meters
                # top grp parenting
                cmds.parent(nucleus_nd, self.components_grp)
                self.logger.debug(f"{nucleus_nd = }")  # nucleus

            # name nRigid and dynamicConstraint nodes
            nrigid_nd = cmds.listConnections(attach_mesh_shp, type="nRigid")[0]
            nrigid_nd = cmds.rename(nrigid_nd, f"{attach_mesh}NRigid")
            nrigid_nd_shp = cmds.listConnections(attach_mesh_shp, type="nRigid", shapes=True)[0]
            ncomponent_nd = cmds.listConnections(nrigid_nd_shp, type="nComponent")[0]
            ncomponent_nd = cmds.rename(ncomponent_nd, f"{attach_mesh}NComponent")
            dynamicconst_nd = cmds.listConnections(ncomponent_nd, type="dynamicConstraint")[0]
            dynamicconst_nd = cmds.rename(dynamicconst_nd, f"{attach_mesh}DynamicConstraint")
            self.logger.debug(f"{nrigid_nd = }")  # nRigid
            self.logger.debug(f"{nrigid_nd_shp = }")  # nRigid shape
            self.logger.debug(f"{ncomponent_nd = }")  # nComponent
            self.logger.debug(f"{dynamicconst_nd = }")  # dynamicConstraint

            # ----- cloth settings -----
            # nCloth preset
            try:
                preset_filename = "thickLeather.mel"  # thickLeather, burlap
                ncloth_preset = (
                    f"{cmds.internalVar(mayaInstallDir=True)}"
                    f"/presets/attrPresets/nCloth/{preset_filename}"
                )
                mel.eval(f'applyPresetToNode "{ncloth_nd_shp}" "" "" "{ncloth_preset}" 1;')
            except Exception as e:
                self.logger.warning(f"Failed to find or apply nCloth preset: {ncloth_preset}\n{e}")

            # other settings
            cmds.setAttr(f"{ncloth_nd_shp}.inputMeshAttract", 0.10)

            # ----- output cloth mesh blendshape -----
            if flexi_mesh != flexi_mesh_current:
                output_cloth_mesh_shp = cmds.listConnections(
                    f"{ncloth_nd_shp}.outputMesh",
                    plugs=True,
                )[0]
                output_cloth_mesh_shp = output_cloth_mesh_shp.split(".")[0]
                mesh_shp_new_name = flexi_mesh_shp.replace(
                    flexi_base_name,
                    f"{flexi_base_name}OutputCloth",
                )
                output_cloth_mesh_shp = cmds.rename(output_cloth_mesh_shp, mesh_shp_new_name)
                blendshape_nd = f"{output_cloth_mesh_shp}BlendShape"
                cmds.blendShape(
                    output_cloth_mesh_shp,
                    flexi_mesh,
                    name=blendshape_nd,
                )
                cmds.setAttr(f"{blendshape_nd}.{output_cloth_mesh_shp}", 0.5)
                # set current flexi mesh
                flexi_mesh_current = flexi_mesh

            # ----- aux ctrl attrs -----
            self.aux_ctrl_ncloth_attrs(ncloth_nd_shp, blendshape_nd, output_cloth_mesh_shp)

            # ----- top grp parenting -----
            if cmds.listRelatives(ncloth_nd, parent=True) != [self.components_grp]:
                cmds.parent(ncloth_nd, self.components_grp)
            cmds.parent(nrigid_nd, self.components_grp)
            cmds.parent(dynamicconst_nd, self.components_grp)

        # ----- add collision meshes -----
        if collision_mesh_filepath.is_file():
            collision_mesh_data = self.get_saved_collision_meshes()
            collision_meshes = collision_mesh_data["collision_meshes"]
            self.logger.debug(f"{collision_meshes = }")
            cmds.select(nucleus_nd)
            cmds.select(collision_meshes, add=True)
            mel.eval("makeCollideNCloth;")
            # rename nRigid objects base on coll meshes
            for obj in collision_meshes:
                obj_shp = cmds.listRelatives(obj, shapes=True)[0]
                nrigid_nd = cmds.listConnections(obj_shp, type="nRigid")[0]
                nrigid_nd = cmds.rename(nrigid_nd, f"{obj}NRigid")
                # top grp parenting
                cmds.parent(nrigid_nd, self.components_grp)
                cmds.parent(obj, self.top_grp)
                cmds.setAttr(f"{obj}.visibility", 0)
        else:
            self.logger.info('No "collision_meshes.json" in cloth_data rig folder.')

        # ----- aux ctrl attrs -----
        self.aux_ctrl_nucleus_attrs(nucleus_nd)

        # ----- apply saved nCloth settings -----
        self.apply_ncloth_settings()

        # ----- extend playback timeline -----
        cmds.playbackOptions(minTime=0, maxTime=300)

    def get_saved_vertex_ids(self) -> list[dict]:
        """Query json data for nCloth mesh vertex IDs, vertex mesh and attach mesh.
        Get this data for all the attach meshes in the cloth_data folder for this rig.

        Returns:
            Returns same data as save_vertex_ids() except for multiple attach meshes in a list.

        """
        cloth_verts_filepaths = list(cloth_data_folderpath.glob("*DynamicConstraint.json"))
        if not list(cloth_verts_filepaths):
            msg = f'No json dynamicConstraint filepaths in: "{cloth_data_folderpath}"'
            self.logger.error(msg)
            raise ValueError(msg)

        attach_mesh_datas = []
        for cloth_verts_filepath in cloth_verts_filepaths:
            with open(cloth_verts_filepath) as f:
                attach_mesh_data = json.load(f)
                attach_mesh_datas.append(attach_mesh_data)

        return attach_mesh_datas

    def save_vertex_ids(self):
        """Save selected mesh vertex IDs, vertex mesh and attach mesh.
        Select vertices from cloth mesh, then select mesh object to attach to
        and run this method to save selection data.
        """
        attach_mesh_data = self.get_selected_vertex_ids()
        attach_mesh = attach_mesh_data["attach_mesh"]
        cloth_data_folderpath.mkdir(exist_ok=True)
        cloth_verts_filepath = cloth_data_folderpath / f"{attach_mesh}DynamicConstraint.json"

        self.logger.debug(f"{cloth_verts_filepath = }")
        with open(cloth_verts_filepath, "w") as f:
            json.dump(attach_mesh_data, f, indent=4)

    def get_selected_vertex_ids(self) -> dict[str, list[str] | str]:
        """Get selected vertex IDs and selected mesh to attach verts to.
        The queried data is based on current selection in Maya.

        Returns:
            Dictionary of selected vertex IDs, vertex mesh, and mesh to attach vertices too.

        """
        selected = cmds.ls(selection=True)

        attach_mesh_data = {}
        attach_mesh_data.setdefault("attach_vertices", [])
        vertex_meshes = []
        attach_meshes = []
        for obj in selected:
            if ".vtx" in obj:
                mesh = obj.split(".")[0]
                vertex_meshes.append(mesh)
                attach_mesh_data["attach_vertices"].append(obj)
            elif "." not in obj:
                attach_meshes.append(obj)

        errors = []
        if len(set(vertex_meshes)) != 1:
            errors.append("Vertices selected from more than one mesh (or none). ")
        if len(attach_meshes) != 1:
            errors.append("More than one attach mesh selected (or none). ")
        if errors:
            errors.append(
                "Select vertices from one mesh and select one other mesh for attaching to.",
            )
            error_msg = "\n".join(errors)
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # add vert mesh
        attach_mesh_data["vertex_mesh"] = vertex_meshes[0]
        attach_mesh_data["attach_mesh"] = attach_meshes[0]

        return attach_mesh_data

    def get_saved_collision_meshes(self) -> dict[str, list[str]]:
        """Query "collision_meshes.json" from cloth_data folder.

        Returns:
            Dict with list of collision mesh names.

        """
        if not collision_mesh_filepath.is_file():
            msg = f'No "collision_meshes.json" found: {collision_mesh_filepath}'
            self.logger.error(msg)
            raise ValueError(msg)

        with open(collision_mesh_filepath) as f:
            collision_mesh_data = json.load(f)

        return collision_mesh_data

    def save_collision_meshes(self):
        """Save collision mesh names to json.
        Separate from this method, add actual collision meshes to "rig_helpers.ma".
        They can be skinned to joints.
        """
        collision_mesh_data = self.get_selected_collision_meshes()
        cloth_data_folderpath.mkdir(exist_ok=True)

        with open(collision_mesh_filepath, "w") as f:
            json.dump(collision_mesh_data, f, indent=4)

    def get_selected_collision_meshes(self) -> dict[str, list[str]]:
        """Query selected collision objects and add to dictionary.

        Returns:
            Dict with selected collision objects.

        """
        selected = cmds.ls(selection=True)

        collision_mesh_data = {}
        collision_mesh_data.setdefault("collision_meshes", [])
        for obj in selected:
            obj_shp = cmds.listRelatives(obj, shapes=True)[0]
            if cmds.objectType(obj_shp) == "mesh":
                collision_mesh_data["collision_meshes"].append(obj)

        if not collision_mesh_data["collision_meshes"]:
            msg = "No collision meshes added. Must select at least one mesh object."
            self.logger.error(msg)
            raise ValueError(msg)

        return collision_mesh_data

    def apply_ncloth_settings(self):
        """Apply saved nCloth settings from "*Settings.json" files in cloth_data folder."""
        ncloth_settings = self.get_saved_ncloth_settings()
        for settings in ncloth_settings:
            for obj_attr, value in settings.items():
                try:
                    if isinstance(value, list) and any(isinstance(v, (list, tuple)) for v in value):
                        value = value[0]
                        if not value:
                            continue
                        cmds.setAttr(obj_attr, *value)
                    else:
                        cmds.setAttr(obj_attr, value)
                except Exception:
                    self.logger.debug(f"Failed to set nCloth attribute: {obj_attr = }, {value}")

    def get_saved_ncloth_settings(self) -> list[dict]:
        """Get saved nCloth settings for nCloth objects.
        These settings will be in "*Settings.json" files in the cloth_data folder.

        Returns:
            A list of saved settings for nCloth objects.

        """
        ncloth_settings_filepaths = list(cloth_data_folderpath.glob("*Settings.json"))
        if not list(ncloth_settings_filepaths):
            msg = f'No custom cloth settings in: "{cloth_data_folderpath}"'
            self.logger.debug(msg)

        ncloth_settings = []
        for settings_file in ncloth_settings_filepaths:
            with open(settings_file) as f:
                settings = json.load(f)
                ncloth_settings.append(settings)

        return ncloth_settings

    def save_ncloth_settings(self):
        """Save nCloth settings to a json file per nCloth object."""
        ncloth_settings = self.get_selected_cloth_settings()
        cloth_data_folderpath.mkdir(exist_ok=True)

        for obj in ncloth_settings.keys():
            ncloth_settings_filepath = cloth_data_folderpath / f"{obj}Settings.json"
            with open(ncloth_settings_filepath, "w") as f:
                json.dump(ncloth_settings[obj], f, indent=4)

    def get_selected_cloth_settings(self) -> dict[str, dict]:
        """Get nCloth settings from selected nCloth objects.
        Currently, supports "keyable" settings.

        Returns:
            Dictionary with nCloth settings for each selected nCloth object.

        """
        selected = cmds.ls(selection=True)

        ncloth_settings = {}
        for obj in selected:
            obj_shp = cmds.listRelatives(obj, shapes=True)[0]
            attrs = cmds.listAttr(obj_shp, keyable=True)  # settable=True, visible=True

            ncloth_settings.setdefault(obj_shp, {})
            for attr in attrs:
                try:
                    value = cmds.getAttr(f"{obj_shp}.{attr}")
                    ncloth_settings[obj_shp][f"{obj_shp}.{attr}"] = value
                except Exception:
                    pass

        return ncloth_settings

    def build_aux_ctrl(self):
        """Create cloth auxiliary ctrl."""
        self.aux_ctrl = create_nurbs_curves.CreateCurves(
            name="nClothAux_ctrl",
            size=1,
            color_rgb=(0.2, 0.1, 0.7),
        ).box_curve()
        self.aux_ctrl_grp = create_ctrl_grps(self.aux_ctrl)[0]

        # lock and hide attrs
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{self.aux_ctrl}.translate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{self.aux_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{self.aux_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{self.aux_ctrl}.visibility", **lock_hide_kwargs)

        # top grp parenting
        cmds.parent(self.aux_ctrl_grp, self.top_grp)

    def aux_ctrl_nucleus_attrs(self, nucleus_nd) -> None:
        """Set up auxiliary ctrl attributes fot the nucleus node.

        Args:
            nucleus_nd: The nCloth nucleus node.

        """
        add_divider_attribue(control_name=self.aux_ctrl, divider_amount=10)
        cmds.addAttr(
            self.aux_ctrl,
            longName="nucleusEnable",
            attributeType="bool",
            defaultValue=False,
            keyable=True,
        )
        cmds.connectAttr(f"{self.aux_ctrl}.nucleusEnable", f"{nucleus_nd}.enable")
        cmds.addAttr(
            self.aux_ctrl,
            longName="nucleusSpaceScale",
            attributeType="double",
            defaultValue=0.01,
            keyable=True,
        )
        cmds.setAttr(f"{self.aux_ctrl}.nucleusSpaceScale", lock=True)
        cmds.connectAttr(f"{self.aux_ctrl}.nucleusSpaceScale", f"{nucleus_nd}.spaceScale")
        cmds.addAttr(
            self.aux_ctrl,
            longName="nucleusStartFrame",
            attributeType="double",
            defaultValue=1,
            keyable=True,
        )
        cmds.connectAttr(f"{self.aux_ctrl}.nucleusStartFrame", f"{nucleus_nd}.startFrame")

    def aux_ctrl_ncloth_attrs(self, ncloth_nd_shp, blendshape_nd, output_cloth_mesh_shp) -> None:
        """Set up auxiliary ctrl attributes fot nCloth components.

        Args:
            ncloth_nd_shp: nCloth node shape.
            blendshape_nd: Blendshape node being used for nCloth setup.
            output_cloth_mesh_shp: Output cloth mesh shape.

        """
        ncloth_base_nm = ncloth_nd_shp.split("_")[0]
        divider_attr_nm = f"_{ncloth_base_nm}_"
        if not cmds.objExists(f"{self.aux_ctrl}.{divider_attr_nm}"):
            cmds.addAttr(
                self.aux_ctrl,
                longName=divider_attr_nm,
                niceName=divider_attr_nm,
                attributeType="enum",
                enumName=divider_attr_nm,
            )
            cmds.setAttr(f"{self.aux_ctrl}.{divider_attr_nm}", channelBox=True)

            cmds.addAttr(
                self.aux_ctrl,
                longName=f"isDynamic{self.ncloth_attr_index}",
                attributeType="bool",
                defaultValue=True,
                keyable=True,
            )
            cmds.connectAttr(
                f"{self.aux_ctrl}.isDynamic{self.ncloth_attr_index}",
                f"{ncloth_nd_shp}.isDynamic",
            )

            cmds.addAttr(
                self.aux_ctrl,
                longName=f"blendShape{self.ncloth_attr_index}",
                attributeType="double",
                defaultValue=0,
                minValue=0,
                maxValue=1,
                keyable=True,
            )
            cmds.connectAttr(
                f"{self.aux_ctrl}.blendShape{self.ncloth_attr_index}",
                f"{blendshape_nd}.{output_cloth_mesh_shp}",
            )

            self.ncloth_attr_index += 1  # index skips over non-ncloth iterations
