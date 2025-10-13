from importlib import reload

from maya import cmds
from nlol.core.rig_setup import (
    build_display_layers,
    build_flexi_to_cloth,
    build_mesh_skeleton,
    build_rig_modules,
    parent_space_switching,
    save_control_curves,
)
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_folder_path)
reload(build_display_layers)
reload(build_flexi_to_cloth)
reload(build_mesh_skeleton)
reload(build_rig_modules)
reload(parent_space_switching)
reload(save_control_curves)

rig_folderpath = rig_folder_path.rig_folderpath
rig_data_filepath = rig_folderpath / "rig_object_data.toml"
rig_ps_filepath = rig_folderpath / "rig_parent_spaces.toml"
rig_ctrl_crvs_filepath = rig_folderpath / "rig_control_curves.json"
display_lyrs_filepath = rig_folderpath / "rig_display_layers.toml"

logger = get_logger()


def run_rig_build():
    """Build entire rig."""
    # ----- skeletal mesh, import "rig_helpers.ma" -----
    build_mesh_skeleton.BuildMeshSkeleton(rig_data_filepath).build_skeletalmesh()
    # clear undo after importing
    cmds.select(clear=True)
    cmds.flushUndo()

    # ----------
    cmds.undoInfo(openChunk=True)  # easily undo up to the import
    try:
        # ----- cloth -----
        # "*Settings.json", "collision_meshes.json"
        build_flexi_to_cloth.FlexiToCloth().build()
        # ----- rig modules -----
        build_rig_modules.build_modules(rig_data_filepath)
        # ----- parent spaces -----
        parent_space_switching.ParentSpacing(rig_ps_filepath).build()
        # ----- ctrl shapes -----
        save_control_curves.SaveControlCurves(rig_ctrl_crvs_filepath).apply_curve_attributes()
        # ----- display layers -----
        build_display_layers.BuildDisplayLayers(display_lyrs_filepath).build()
    except Exception:
        raise
    finally:
        cmds.undoInfo(closeChunk=True)
        cmds.select(clear=True)
