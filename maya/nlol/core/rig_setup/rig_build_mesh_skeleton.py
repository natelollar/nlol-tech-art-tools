from importlib import reload

from maya import cmds
from nlol.core.rig_setup import build_mesh_skeleton
from nlol.defaults.rig_folder_path import rig_folderpath

reload(build_mesh_skeleton)


def run_mesh_skeleton_build(show_confirmation: bool = True):
    """Build just the skeletal mesh, no rig.

    Args:
        show_confirmation: Show confirmation window popup.

    """
    rig_data_filepath = rig_folderpath() / "rig_object_data.toml"

    # ----------
    # also imports "rig_helpers.ma"
    build_mesh_skeleton.BuildMeshSkeleton(rig_data_filepath, show_confirmation).build_skeletalmesh()

    # ----------
    cmds.select(clear=True)
    cmds.flushUndo()
