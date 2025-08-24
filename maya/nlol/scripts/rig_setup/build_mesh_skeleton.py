import tomllib
from importlib import reload
from pathlib import Path

from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

reload(rig_folder_path)

rig_folderpath = rig_folder_path.rig_folderpath

mesh_filepath = rig_folderpath / "model.ma"
skeleton_filepath = rig_folderpath / "skeleton.ma"
skin_weights_filepath = rig_folderpath / "skin_weights.xml"


class BuildMeshSkeleton:
    """Import mesh and skeleton, then build into skeletal mesh."""

    def __init__(self, rig_data_filepath: str | Path):
        self.rig_data_filepath = rig_data_filepath
        self._rig_data = None

        self.logger = get_logger()

    @property
    def rig_data(self) -> dict:
        """Returns dictionary from "rig_object_data.toml." """
        if self._rig_data is None:
            with open(self.rig_data_filepath, "rb") as f:
                self._rig_data = tomllib.load(f)
        return self._rig_data

    @property
    def rig_name(self) -> str:
        """Returns rig_name variable from toml."""
        return self.rig_data.get("rig_name")

    @property
    def unreal_rig(self) -> str:
        """Returns unreal_rig variable from toml."""
        return self.rig_data.get("unreal_rig")

    def import_mesh_skeleton(self):
        """Import model geometry and skeleton into new Maya scene."""
        cmds.file(mesh_filepath, i=True)
        cmds.file(skeleton_filepath, i=True)

    def build_skeletalmesh(self):
        """Skin the model geometry to the skeleton.
        Create parent group for this new skeletal mesh.
        """
        if not mesh_filepath.is_file() or not skeleton_filepath.is_file():
            msg = '"model.ma" and/or "skeleton.ma" not in rig folder. '
            "Skipping import. Proceeding to rig phase."
            self.logger.info(msg)
            return

        dialog_result = cmds.confirmDialog(
            title="Confirm",
            message="Create New \nCharacter Scene?",
            button=["Yes", "No"],
            defaultButton="Yes",
            cancelButton="No",
            dismissString="No",
            icon="question",
            bgc=(0.2, 0.2, 0.2),
        )
        if dialog_result == "No":
            msg = 'Canceling import for "model.ma" and "skeleton.ma". Proceeding to rig phase.'
            self.logger.info(msg)
            return

        # force open new maya file
        cmds.file(force=True, new=True)

        # import mesh and skeleton
        self.import_mesh_skeleton()

        # get root skeleton joint
        top_nodes = cmds.ls(assemblies=True)
        root_joint = [nd for nd in top_nodes if cmds.objectType(nd) == "joint"]
        skeleton_root = root_joint[0]

        # get model geometry
        mesh_shapes = cmds.ls(type="mesh")
        meshes = cmds.listRelatives(mesh_shapes, parent=True)
        meshes = list(set(meshes))  # remove duplicates (from Origin geo)

        # ---------- create top skeletal mesh group ----------
        if self.rig_name:
            skeletalmesh_grp_name = f"{self.rig_name}_skeletalMeshGrp"
        else:
            skeletalmesh_grp_name = "main_skeletalMeshGrp"

        skeletalmesh_grp = cmds.group(empty=True, name=skeletalmesh_grp_name)
        if self.unreal_rig:
            cmds.setAttr(f"{skeletalmesh_grp}.rotateX", -90)

        # parent meshes and skeleton to top group
        cmds.parent(skeleton_root, skeletalmesh_grp)
        for mesh in meshes:
            cmds.parent(mesh, skeletalmesh_grp)

        # --------------- bind skin ---------------
        for mesh in meshes:
            # create default bind skin between root joint and mesh
            new_skin_cluster = cmds.skinCluster(skeleton_root, mesh)
            # weight all joints to root joint to simplify and avoid skin transfer glitches
            cmds.skinPercent(
                new_skin_cluster[0],
                mesh,
                transformValue=(skeleton_root, 1.0),
            )

            # import and apply user pre-saved weights
            cmds.deformerWeights(
                skin_weights_filepath.name,
                im=True,
                method="index",
                deformer=new_skin_cluster[0],
                path=skin_weights_filepath.parent,
            )

            # apply normalize weights (default for "Import Weights...")
            cmds.skinCluster(new_skin_cluster, edit=True, forceNormalizeWeights=True)

        # ---------- all joints scale compensate off ----------
        # prevents double scaling issues later on
        all_rig_joints = [skeleton_root]
        skeleton_root_children = cmds.listRelatives(skeleton_root, allDescendents=True)
        all_rig_joints.extend(skeleton_root_children)

        for jnt in all_rig_joints:
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)
