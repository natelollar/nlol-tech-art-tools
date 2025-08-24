from importlib import reload

from nlol.defaults import rig_folder_path
from nlol.scripts.rig_setup import (
    build_mesh_skeleton,
    build_rig_modules,
    parent_space_switching,
    save_control_curves,
)

from maya import cmds

reload(build_rig_modules)
reload(parent_space_switching)
reload(save_control_curves)
reload(rig_folder_path)
reload(build_mesh_skeleton)

rig_folderpath = rig_folder_path.rig_folderpath
rig_data_filepath = rig_folderpath / "rig_object_data.toml"
rig_ps_filepath = rig_folderpath / "rig_parent_spaces.toml"
rig_helpers_filepath = rig_folderpath / "rig_helpers.ma"
rig_ctrl_crvs_filepath = rig_folderpath / "rig_control_curves.json"


def run_rig_build():
    """Build entire rig."""
    # ----------
    build_mesh_skeleton.BuildMeshSkeleton(rig_data_filepath).build_skeletalmesh()
    # ----------
    cmds.file(rig_helpers_filepath, i=True)
    # ----------
    build_rig_modules.build_modules(rig_data_filepath)
    # ----------
    parent_space_switching.ParentSpacing(rig_ps_filepath).build_parent_spaces()
    # ----------
    save_control_curves.SaveControlCurves(rig_ctrl_crvs_filepath).apply_curve_attributes()

    # ----------
    cmds.select(clear=True)
    cmds.flushUndo()
