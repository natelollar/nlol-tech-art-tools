from importlib import reload

from maya import cmds
from nlol.core.rig_setup import (
    build_blendshapes,
    build_display_layers,
    build_finalize_script,
    build_flexi_to_cloth,
    build_mesh_skeleton,
    build_rig_modules,
    parent_space_switching,
    save_control_curves,
)
from nlol.core.rig_tools import mirror_attrs_export_import
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

reload(mirror_attrs_export_import)
reload(build_blendshapes)
reload(build_display_layers)
reload(build_display_layers)
reload(build_finalize_script)
reload(build_flexi_to_cloth)
reload(build_mesh_skeleton)
reload(build_rig_modules)
reload(parent_space_switching)
reload(save_control_curves)
reload(rig_folder_path)

rig_folderpath = rig_folder_path.rig_folderpath
rig_data_filepath = rig_folderpath / "rig_object_data.toml"
blendshapes_filepath = rig_folderpath / "blendshapes.ma"
setdrivenkeys_filepath = rig_folderpath / "blendshape_setdrivenkeys.toml"
rig_ps_filepath = rig_folderpath / "rig_parent_spaces.toml"
rig_ctrl_crvs_filepath = rig_folderpath / "rig_control_curves.json"
mirror_attrs_filepath = rig_folderpath / "mirror_attributes.json"
display_lyrs_filepath = rig_folderpath / "rig_display_layers.toml"
finalize_script_filepath = rig_folderpath / "finalize_script.py"

logger = get_logger()


def run_rig_build():
    """Build entire rig."""
    # code modules that import files and cannot be undone
    # ----- skeletal mesh, import "rig_helpers.ma" -----
    build_mesh_skeleton.BuildMeshSkeleton(rig_data_filepath).build_skeletalmesh()
    # ----- blendshape setup -----
    build_blendshapes.ConnectBlendShapes(blendshapes_filepath, setdrivenkeys_filepath).build()
    # clear undo after importing
    cmds.select(clear=True)
    cmds.flushUndo()

    # ----------
    # code module that can be undone
    cmds.undoInfo(openChunk=True)  # easily undo up to the import
    try:
        # ----- cloth -----
        # "*Settings.json", "collision_meshes.json"
        build_flexi_to_cloth.FlexiToCloth().build()
        # ----- rig modules -----
        build_rig_modules.build_modules(rig_data_filepath)
        # ----- ctrl shapes -----
        save_control_curves.SaveControlCurves(rig_ctrl_crvs_filepath).apply_curve_attributes()
        # ----- parent spaces -----
        parent_space_switching.ParentSpacing(rig_ps_filepath).build()
        # # ----- load mirror attributes -----
        mirror_attrs_export_import.MirrorAttrsExportImport(
            mirror_attrs_filepath,
        ).apply_mirror_attrs()
        # ----- display layers -----
        build_display_layers.BuildDisplayLayers(display_lyrs_filepath).build()
        # ----- finalize script -----
        build_finalize_script.run_finalize_script(finalize_script_filepath)
    except Exception:
        raise
    finally:
        cmds.undoInfo(closeChunk=True)
        cmds.select(clear=True)
