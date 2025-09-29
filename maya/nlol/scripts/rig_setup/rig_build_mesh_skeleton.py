from importlib import reload

from maya import cmds
from nlol.defaults import rig_folder_path
from nlol.scripts.rig_setup import build_mesh_skeleton

reload(build_mesh_skeleton)
reload(rig_folder_path)

rig_folderpath = rig_folder_path.rig_folderpath
rig_data_filepath = rig_folderpath / "rig_object_data.toml"


def run_mesh_skeleton_build():
    """Build just the skeletal mesh, no rig."""
    # ----------
    # also imports "rig_helpers.ma"
    build_mesh_skeleton.BuildMeshSkeleton(rig_data_filepath).build_skeletalmesh()

    # ----------
    cmds.select(clear=True)
    cmds.flushUndo()
