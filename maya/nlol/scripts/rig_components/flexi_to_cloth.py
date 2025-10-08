"""Create nCloth blendshape for flexi geometry.
Create attribute for toggling this blendshape.
And function to toggle nCloth on/off for specific flexi geo.
"""

import json
from importlib import reload

from maya import cmds, mel
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_folder_path)

rig_folderpath = rig_folder_path.rig_folderpath
cloth_data_folderpath = rig_folderpath / "cloth_data"
collision_mesh_filepath = cloth_data_folderpath / "collision_meshes.json"
logger = get_logger()


class FlexiToCloth:
    def __init__(self):
        pass

    def build(self):
        """Entry point. Run this method.
        --------------------------------------------------
        """
        cmds.undoInfo(openChunk=True)
        try:
            self.main()
        finally:
            cmds.undoInfo(closeChunk=True)

    def main(self, apply_cloth_settings: bool = True):
        """Create nCloth setup for rigging. Constrains attach meshes with "Point to Surface".
        Multiple cloth meshes and attach meshes allowed.
        Save cloth data to cloth_data folder first. Save data with save_vertex_ids().

        Setup nCloth for each *DynamicConstraint json in cloth_data folder.
        Each dictionary in list returned from get_saved_vertex_ids() contains
        vertex ids, vertex/cloth mesh, and constraint/attach mesh.

        Args:
            apply_cloth_settings: Use pre-saved nCloth settings in cloth_data folder.

        """
        nucleus_nd = None
        attach_mesh_datas = self.get_saved_vertex_ids()
        # ----- iterate through cloth data -----
        # constrain cloth verts to meshes
        for attach_mesh_data in attach_mesh_datas:
            attach_vertices = attach_mesh_data["attach_vertices"]
            cloth_mesh = attach_mesh_data["vertex_mesh"]
            attach_mesh = attach_mesh_data["attach_mesh"]
            cloth_mesh_shp = cmds.listRelatives(cloth_mesh, shapes=True)[0]
            attach_mesh_shp = cmds.listRelatives(attach_mesh, shapes=True)[0]

            # ----- apply nCloth -----
            # skip if already created for another attach mesh.
            if not cmds.listConnections(cloth_mesh_shp, type="nCloth"):
                cmds.select(nucleus_nd)
                cmds.select(cloth_mesh, add=True)
                mel.eval("createNCloth 0;")  # 0 is Local Space Output
                cmds.select(clear=True)
                logger.debug(f'nCloth generated for: "{cloth_mesh_shp}"')
            # apply point to surface constraint
            cmds.select(attach_vertices)
            cmds.select(attach_mesh, add=True)
            mel.eval("createNConstraint pointToSurface 0;")  # 0 is Use Sets off
            # extend playback timeline
            cmds.playbackOptions(minTime=0, maxTime=1200)

            # ----- find and name nodes -----
            # name ncloth and nucleus nodes
            ncloth_nd = cmds.listConnections(cloth_mesh_shp, type="nCloth")[0]
            ncloth_nd = cmds.rename(ncloth_nd, f"{cloth_mesh}NCloth")
            ncloth_nd_shp = cmds.listConnections(cloth_mesh_shp, type="nCloth", shapes=True)[0]
            logger.debug(f"{ncloth_nd = }")  # nCloth
            if not nucleus_nd:  # if not identified and renamed yet for rig
                nucleus_nd = cmds.listConnections(ncloth_nd_shp, type="nucleus")[0]
                nucleus_nd = cmds.rename(nucleus_nd, "main_nucleus")
                # nucleus settings
                cmds.setAttr(f"{nucleus_nd}.spaceScale", 0.01)  # global scale: unreal/meters
                logger.debug(f"{nucleus_nd = }")  # nucleus

            # name nRigid and dynamicConstraint nodes
            nrigid_nd = cmds.listConnections(attach_mesh_shp, type="nRigid")[0]
            nrigid_nd = cmds.rename(nrigid_nd, f"{attach_mesh}NRigid")
            nrigid_nd_shp = cmds.listConnections(attach_mesh_shp, type="nRigid", shapes=True)[0]
            ncomponent_nd = cmds.listConnections(nrigid_nd_shp, type="nComponent")[0]
            ncomponent_nd = cmds.rename(ncomponent_nd, f"{attach_mesh}NComponent")
            dynamicconst_nd = cmds.listConnections(ncomponent_nd, type="dynamicConstraint")[0]
            dynamicconst_nd = cmds.rename(dynamicconst_nd, f"{attach_mesh}DynamicConstraint")
            logger.debug(f"{nrigid_nd = }")  # nRigid
            logger.debug(f"{nrigid_nd_shp = }")  # nRigid shape
            logger.debug(f"{ncomponent_nd = }")  # nComponent
            logger.debug(f"{dynamicconst_nd = }")  # dynamicConstraint

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
                logger.warning(f"Failed to find or apply nCloth preset: {ncloth_preset}\n{e}")

            # other settings
            cmds.setAttr(f"{ncloth_nd_shp}.inputMeshAttract", 0.10)

        # ----- add collision meshes -----
        collision_mesh_data = self.get_saved_collision_meshes()
        collision_meshes = collision_mesh_data["collision_meshes"]
        logger.debug(f"{collision_meshes = }")
        cmds.select(nucleus_nd)
        cmds.select(collision_meshes, add=True)
        mel.eval("makeCollideNCloth;")
        # rename nRigid objects base on coll meshes
        for obj in collision_meshes:
            obj_shp = cmds.listRelatives(obj, shapes=True)[0]
            nrigid_nd = cmds.listConnections(obj_shp, type="nRigid")[0]
            nrigid_nd = cmds.rename(nrigid_nd, f"{obj}NRigid")

        # ----- apply saved nCloth settings -----
        self.apply_ncloth_settings()

    def get_saved_vertex_ids(self) -> list[dict]:
        """Query json data for nCloth mesh vertex IDs, vertex mesh and attach mesh.
        Get this data for all the attach meshes in the cloth_data folder for this rig.

        Returns:
            Returns same data as save_vertex_ids() except for multiple attach meshes in a list.

        """
        cloth_verts_filepaths = list(cloth_data_folderpath.glob("*DynamicConstraint.json"))
        if not list(cloth_verts_filepaths):
            msg = f'No json dynamicConstraint filepaths in: "{cloth_data_folderpath}"'
            logger.error(msg)
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

        logger.debug(f"{cloth_verts_filepath = }")
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
            logger.error(error_msg)
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
            logger.error(msg)
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
            logger.error(msg)
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
                    logger.warning(f"Failed to set nCloth attribute: {obj_attr = }, {value}")

    def get_saved_ncloth_settings(self) -> list[dict]:
        """Get saved nCloth settings for nCloth objects.
        These settings will be in "*Settings.json" files in the cloth_data folder.

        Returns:
            A list of saved settings for nCloth objects.

        """
        ncloth_settings_filepaths = list(cloth_data_folderpath.glob("*Settings.json"))
        if not list(ncloth_settings_filepaths):
            msg = (
                f'No custom cloth settings in: "{cloth_data_folderpath}"\n'
                "Using default cloth setup."
            )
            logger.info(msg)

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
