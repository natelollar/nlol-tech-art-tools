"""Import "model.ma", "skeleton.ma", and "rig_helpers.ma" from asset's rig folder.
Also, setup skinning between skeleton and geo.
"""

import tomllib
from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.defaults import rig_folder_path
from nlol.core.rig_components import create_display_layers
from nlol.core.rig_tools import skin_export_import
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_folder_path)
reload(create_display_layers)
reload(skin_export_import)

objects_display_lyr = create_display_layers.objects_display_lyr

rig_folderpath = rig_folder_path.rig_folderpath
mesh_filepath = rig_folderpath / "model.ma"
skeleton_filepath = rig_folderpath / "skeleton.ma"
rig_helpers_filepath = rig_folderpath / "rig_helpers.ma"


class BuildMeshSkeleton:
    """Import mesh and skeleton, then build into skeletal mesh.
    Also, import rig helpers file.
    """

    def __init__(self, rig_data_filepath: str | Path | None = None):
        self.rig_data_filepath = rig_data_filepath
        self._rig_data = None

        self.logger = get_logger()

    @property
    def rig_data(self) -> dict:
        """Returns dictionary from "rig_object_data.toml." """
        if self._rig_data is None:
            if self.rig_data_filepath.is_file():
                with open(self.rig_data_filepath, "rb") as f:
                    self._rig_data = tomllib.load(f)
        return self._rig_data

    @property
    def rig_name(self) -> str:
        """Returns rig_name variable from toml."""
        if self.rig_data is None:
            return None
        return self.rig_data.get("rig_name")

    @property
    def unreal_rig(self) -> str:
        """Returns unreal_rig variable from toml."""
        if self.rig_data is None:
            return None
        return self.rig_data.get("unreal_rig")

    def import_mesh_skeleton_other(self):
        """Import model geometry and skeleton into new Maya scene.
        Also, import rig helpers file. Containing foot locators, flexi surface, etc.
        """
        cmds.file(mesh_filepath, i=True)
        cmds.file(skeleton_filepath, i=True)

        if rig_helpers_filepath.is_file():
            cmds.file(rig_helpers_filepath, i=True)
        else:
            msg = '"rig_helpers.ma" not in rig folder. Skipping import...'
            self.logger.info(msg)

        # remove leftover layers
        scene_display_lyrs = cmds.ls(type="displayLayer")
        for lyr in scene_display_lyrs:
            if lyr != "defaultLayer":
                cmds.delete(lyr)

    def build_skeletalmesh(self):
        """Skin the model geometry to the skeleton.
        Create parent group for this new skeletal mesh.
        """
        if not mesh_filepath.is_file() or not skeleton_filepath.is_file():
            msg = '"model.ma", and/or "skeleton.ma" not in rig folder. Skipping import..."'
            self.logger.info(msg)
            return

        yes_string = "Yes"
        no_string = "Use Current"
        dialog_result = cmds.confirmDialog(
            title="Confirm",
            message="Create New Character Scene?",
            button=[yes_string, no_string],
            defaultButton="Yes",
            cancelButton=no_string,
            dismissString=no_string,
            icon="question",
            bgc=(0.2, 0.2, 0.2),
        )
        if dialog_result == no_string:
            msg = 'Skipping import for "model.ma", "skeleton.ma" and "rig_helpers.ma".'
            self.logger.info(msg)
            return

        # force open new maya file
        cmds.file(force=True, new=True)

        # import mesh and skeleton and other files
        self.import_mesh_skeleton_other()

        # get root skeleton joint and other top joints
        top_nodes = cmds.ls(assemblies=True)
        top_joints = [nd for nd in top_nodes if cmds.objectType(nd) == "joint"]
        if len(top_joints) == 1:
            skeleton_root = top_joints[0]
            other_top_joints = []
        else:
            skeleton_roots = [rt_jnt for rt_jnt in top_joints if "root" in rt_jnt.lower()]
            if not skeleton_roots:
                msg = f'No top joints with "root" string: {top_joints}'
                self.logger.error(msg)
                raise ValueError(msg)
            if len(skeleton_roots) > 1:
                msg = f"More than one root joint: {skeleton_roots}"
                self.logger.error(msg)
                raise ValueError(msg)
            skeleton_root = skeleton_roots[0]
            top_joints.remove(skeleton_root)
            other_top_joints = top_joints

        # get model geometry
        mesh_shapes = cmds.ls(type="mesh")
        mesh_shapes.extend(cmds.ls(type="nurbsSurface"))
        meshes = cmds.listRelatives(mesh_shapes, parent=True)
        meshes = list(set(meshes))  # remove duplicates (from Origin geo)

        # --------------- top group parenting ---------------
        # create top skeletal mesh group
        if self.rig_name:
            skeletalmesh_grp = f"{self.rig_name}_skeletalMeshGrp"
        else:
            skeletalmesh_grp = "main_skeletalMeshGrp"
        if not cmds.objExists(skeletalmesh_grp):
            skeletalmesh_grp = cmds.group(empty=True, name=skeletalmesh_grp)
        if self.unreal_rig:
            cmds.setAttr(f"{skeletalmesh_grp}.rotateX", -90)
        # create top rig group
        if self.rig_name:
            main_rig_group = f"{self.rig_name}_rigGrp"
        else:
            main_rig_group = "main_rigGrp"
        if not cmds.objExists(main_rig_group):
            main_rig_group = cmds.group(empty=True, name=main_rig_group)

        # parent meshes and skeletons to top groups. hide joints and flexi meshes.
        cmds.parent(skeleton_root, skeletalmesh_grp)
        #cmds.setAttr(f"{skeleton_root}.visibility", 0)
        objects_display_lyr(  # skeleton_root to display layer
            objects=skeleton_root,
            display_layer="joints_lyr",
            reference=True,
        )
        if other_top_joints:
            cmds.parent(other_top_joints, main_rig_group)
            for top_jnts in other_top_joints:
                cmds.setAttr(f"{top_jnts}.visibility", 0)

        main_meshes = []
        for mesh in meshes:
            if "flexiSurface" in mesh:
                cmds.parent(mesh, main_rig_group)
                cmds.setAttr(f"{mesh}.visibility", 0)
            else:
                cmds.parent(mesh, skeletalmesh_grp)
                main_meshes.append(mesh)
        objects_display_lyr(  # main_meshes to display layer
            objects=main_meshes,
            display_layer="geo_lyr",
            reference=True,
        )

        # --------------- bind skin ---------------
        skin_export_import.import_skin_weights()

        # ----- all joints scale compensate off -----
        # prevents double scaling issues later on
        all_rig_joints = [skeleton_root]
        skeleton_root_children = cmds.listRelatives(skeleton_root, allDescendents=True)
        all_rig_joints.extend(skeleton_root_children)

        for jnt in all_rig_joints:
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)
