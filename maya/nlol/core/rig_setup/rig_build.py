from importlib import reload

from maya import cmds
from nlol.core.animation_tools import mirror_attrs_export_import
from nlol.core.rig_setup import (
    build_blendshapes,
    build_cloth_dynamics,
    build_display_layers,
    build_finalize_script,
    build_mesh_skeleton,
    build_rig_modules,
    check_data,
    parent_space_switching,
    save_control_curves,
)
from nlol.defaults.rig_folder_path import rig_folderpath
from nlol.utilities import check_registry
from nlol.utilities.nlol_maya_logger import get_logger
from nlol.utilities.nlol_maya_registry import get_registry

reload(mirror_attrs_export_import)
reload(build_blendshapes)
reload(build_display_layers)
reload(build_finalize_script)
reload(build_cloth_dynamics)
reload(build_mesh_skeleton)
reload(build_rig_modules)
reload(check_data)
reload(parent_space_switching)
reload(save_control_curves)
reload(check_registry)


registry = get_registry()
logger = get_logger()


def run_rig_build(show_confirmation: bool = True):
    """Build entire rig.

    Args:
        show_confirmation: Whether to show confirmation popup or
            start rig build immediately.

    """
    # -----
    rig_data_filepath = rig_folderpath() / "rig_object_data.toml"
    blendshapes_filepath = rig_folderpath() / "blendshapes.ma"
    setdrivenkeys_filepath = rig_folderpath() / "blendshape_setdrivenkeys.toml"
    rig_ps_filepath = rig_folderpath() / "rig_parent_spaces.toml"
    rig_ctrl_crvs_filepath = rig_folderpath() / "rig_control_curves.json"
    mirror_attrs_filepath = rig_folderpath() / "mirror_attributes.json"
    display_lyrs_filepath = rig_folderpath() / "rig_display_layers.toml"
    finalize_script_filepath = rig_folderpath() / "finalize_script.py"

    # -----
    logger.info("-------------------- START RIG BUILD... --------------------")

    # ----- clear registry data -----
    registry.clear_registry()

    # ----- custom rig build folderpath -----
    logger.info(f"Rig folder: {rig_folderpath()}")

    try:
        # ----- skeletal mesh, import "rig_helpers.ma" -----
        build_mesh_skeleton.BuildMeshSkeleton(
            rig_data_filepath,
            show_confirmation,
            full_rig_build=True,
        ).build_skeletalmesh()
        # ----- import apply blendshapes -----
        blendshapes_meshes = build_blendshapes.ConnectBlendShapes(
            blendshapes_filepath=blendshapes_filepath,
        ).build_import()
        # ----- cloth -----
        # "*Settings.json", "collision_meshes.json"
        build_cloth_dynamics.ClothDynamics().build()
        # ----- rig modules -----
        build_rig_modules.build_modules(rig_data_filepath)
        # ----- blendshape ctrl connections -----
        build_blendshapes.ConnectBlendShapes(
            setdrivenkeys_filepath=setdrivenkeys_filepath,
        ).build_connect(
            blendshapes_meshes,
        )
        # ----- ctrl shapes -----
        save_control_curves.SaveControlCurves(rig_ctrl_crvs_filepath).apply_curve_attributes()
        # ----- parent spaces -----
        parent_space_switching.ParentSpacing(rig_ps_filepath).build()
        # ----- load mirror attributes -----
        mirror_attrs_export_import.MirrorAttrsExportImport(
            mirror_attrs_filepath,
        ).apply_mirror_attrs()
        # ----- display layers -----
        build_display_layers.BuildDisplayLayers(display_lyrs_filepath).build()
        build_display_layers.collapse_display_layers()
        # ----- finalize script -----
        build_finalize_script.run_finalize_script(finalize_script_filepath)
    except InterruptedError as e:
        logger.info(e)
        return

    # ------------------------------
    cmds.select(clear=True)
    cmds.flushUndo()

    # ----- check data -----
    check_registry.verify_registry()
    check_data.verify_data()

    logger.info("-------------------- END RIG BUILD. --------------------")
