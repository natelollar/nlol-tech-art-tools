"""List of animation variables to be called by shelf and menu."""

from importlib import reload

from nlol.core.rig_tools import random_generator

reload(random_generator)

random_colors_dull = random_generator.random_colors_dull


def build_animation_list():
    """Create a dictionary list of animation men and shelf buttons, and their attributes."""
    random_clrs = random_colors_dull()

    shelf_separator = {
        "label": "=" * 35,
        "image": "nlol_separator_03_blue.png",
        "annotation": "Separator.",
        "command": 'print("Separator.")',
        "sourceType": "python",
    }

    animation_list = [
        shelf_separator,
        {
            "label": "Save Transforms for Selected",
            "image": "pythonFamily.png",
            "annotation": "Save translate/rotate/scale for selected objects to json file.",
            "imageOverlayLabel": "SvTrs",
            "backgroundColor": random_clrs[30],
            "command": "from nlol.core.standalone import transforms_save_load\n"
            "from importlib import reload\nreload(transforms_save_load)\n"
            "transforms_save_load.save_transforms()",
            "sourceType": "python",
        },
        {
            "label": "Load Transforms for Selected",
            "image": "pythonFamily.png",
            "annotation": "Load translate/rotate/scale for selected objects from json file.",
            "imageOverlayLabel": "LdTrs",
            "backgroundColor": random_clrs[31],
            "command": "from nlol.core.standalone import transforms_save_load\n"
            "from importlib import reload\nreload(transforms_save_load)\n"
            "transforms_save_load.load_transforms()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Save Keyframe for Selected",
            "image": "pythonFamily.png",
            "annotation": "Save current keyframe data for selected objects.",
            "imageOverlayLabel": "SvKfm",
            "backgroundColor": random_clrs[0],
            "command": "from nlol.core.animation_tools import keyframe_export_import\n"
            "from importlib import reload\nreload(keyframe_export_import)\n"
            "keyframe_export_import.KeyframeExportImport().get_keyframe_data()",
            "sourceType": "python",
        },
        {
            "label": "Load Keyframe Data (to Saved)",
            "image": "pythonFamily.png",
            "annotation": "Load keyframe data for SAVED objects on current frame.",
            "imageOverlayLabel": "LdKfm",
            "backgroundColor": random_clrs[1],
            "command": "from nlol.core.animation_tools import keyframe_export_import\n"
            "from importlib import reload\nreload(keyframe_export_import)\n"
            "keyframe_export_import.KeyframeExportImport().apply_keyframe_data()",
            "sourceType": "python",
        },
        {
            "label": "Load Keyframe Data (to Selected)",
            "image": "pythonFamily.png",
            "annotation": "Load keyframe data for SELECTED objects on current frame.",
            "imageOverlayLabel": "LdSlct",
            "backgroundColor": random_clrs[2],
            "command": "from nlol.core.animation_tools import keyframe_export_import\n"
            "from importlib import reload\nreload(keyframe_export_import)\n"
            "keyframe_export_import.KeyframeExportImport().apply_keyframe_data_to_selected()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Save All Keyframes for Selected",
            "image": "pythonFamily.png",
            "annotation": "Save all keyframe data for selected objects within animation range.",
            "imageOverlayLabel": "SvAll",
            "backgroundColor": random_clrs[3],
            "command": "from nlol.core.animation_tools import keyframe_export_import\n"
            "from importlib import reload\nreload(keyframe_export_import)\n"
            "keyframe_export_import.KeyframeExportImport().get_keyframe_data_all()",
            "sourceType": "python",
        },
        {
            "label": "Load All Keyframes",
            "image": "pythonFamily.png",
            "annotation": "Load keyframe data for SAVED objects for all frames "
            "in the saved animation playback range. "
            "Key each saved attribute value on each frame where it was saved.",
            "imageOverlayLabel": "LdAll",
            "backgroundColor": random_clrs[4],
            "command": "from nlol.core.animation_tools import keyframe_export_import\n"
            "from importlib import reload\nreload(keyframe_export_import)\n"
            "keyframe_export_import.KeyframeExportImport().apply_keyframe_data_all()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Mirror Opposite Ctrl",
            "image": "pythonFamily.png",
            "annotation": 'Mirror selected ctrl/s "left to right" or "right to left". '
            "OPPOSITE ctrl will be mirrored.",
            "imageOverlayLabel": "MrrOpp",
            "backgroundColor": random_clrs[5],
            "command": "from nlol.core.animation_tools import mirror_ctrls\n"
            "from importlib import reload\nreload(mirror_ctrls)\n"
            "mirror_ctrls.mirror_selected_ctrls(to_other_side=True)",
            "sourceType": "python",
        },
        {
            "label": "Mirror Selected Ctrl",
            "image": "pythonFamily.png",
            "annotation": 'Mirror selected ctrl/s "left to right" or "right to left". '
            "SELECTED ctrl will be mirrored.",
            "imageOverlayLabel": "MrrSel",
            "backgroundColor": random_clrs[6],
            "command": "from nlol.core.animation_tools import mirror_ctrls\n"
            "from importlib import reload\nreload(mirror_ctrls)\n"
            "mirror_ctrls.mirror_selected_ctrls()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Add Mirror Attributes",
            "image": "pythonFamily.png",
            "annotation": 'Add mirror attributes to selected objects. Example: ".mirrorTranslateX"',
            "imageOverlayLabel": "AddMir",
            "backgroundColor": random_clrs[20],
            "command": "from nlol.core.animation_tools import mirror_attrs_export_import\n"
            "from importlib import reload\nreload(mirror_attrs_export_import)\n"
            "mirror_attrs_export_import.MirrorAttrsExportImport().add_mirror_attrs()",
            "sourceType": "python",
        },
        {
            "label": "Save Mirror Attributes (Generic)",
            "image": "pythonFamily.png",
            "annotation": "Save mirror attributes for selected ctrls to generic defaults folder. "
            '"nlol/core/defaults/". '
            "Select all objects when saving. Saving is not additive.",
            "imageOverlayLabel": "SvMrGn",
            "backgroundColor": random_clrs[40],
            "command": "from nlol.core.animation_tools import mirror_attrs_export_import\n"
            "from importlib import reload\nreload(mirror_attrs_export_import)\n"
            "mirror_attrs_export_import.MirrorAttrsExportImport(use_generic_filepath=True).get_save_mirror_attrs()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Save Mirror Attributes",
            "image": "pythonFamily.png",
            "annotation": "Save mirror attributes for selected ctrls to rig folder. "
            "Recommended to select all ctrls when saving. Will load back in when rebuilding rig. ",
            "imageOverlayLabel": "SvMrAt",
            "backgroundColor": random_clrs[21],
            "command": "from nlol.core.animation_tools import mirror_attrs_export_import\n"
            "from importlib import reload\nreload(mirror_attrs_export_import)\n"
            "mirror_attrs_export_import.MirrorAttrsExportImport().get_save_mirror_attrs()",
            "sourceType": "python",
        },
        {
            "label": "Load Mirror Attributes",
            "image": "pythonFamily.png",
            "annotation": 'Load mirror attrs from saved "mirror_attributes.json" in rig folder.',
            "imageOverlayLabel": "LdMrAt",
            "backgroundColor": random_clrs[24],
            "command": "from nlol.core.animation_tools import mirror_attrs_export_import\n"
            "from importlib import reload\nreload(mirror_attrs_export_import)\n"
            "mirror_attrs_export_import.MirrorAttrsExportImport().apply_mirror_attrs()",
            "sourceType": "python",
        },
        {
            "label": "Show Mirror Attributes",
            "image": "pythonFamily.png",
            "annotation": "Show mirror attributes in channel box for selected ctrls. ",
            "imageOverlayLabel": "ShwMrr",
            "backgroundColor": random_clrs[23],
            "command": "from nlol.core.animation_tools import mirror_attrs_export_import\n"
            "from importlib import reload\nreload(mirror_attrs_export_import)\n"
            "mirror_attrs_export_import.MirrorAttrsExportImport().show_hide_mirror_attrs()",
            "sourceType": "python",
        },
        {
            "label": "Hide Mirror Attributes",
            "image": "pythonFamily.png",
            "annotation": "Hide mirror attributes in channel box for selected ctrls.",
            "imageOverlayLabel": "HidMrr",
            "backgroundColor": random_clrs[24],
            "command": "from nlol.core.animation_tools import mirror_attrs_export_import\n"
            "from importlib import reload\nreload(mirror_attrs_export_import)\n"
            "mirror_attrs_export_import.MirrorAttrsExportImport().show_hide_mirror_attrs(show_attrs=False)",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Temp Locator",
            "image": "pythonFamily.png",
            "annotation": "Create temporary locator at world origin. "
            "Useful for creating temp pivot with multi parent constraint.",
            "imageOverlayLabel": "TmpLoc",
            "backgroundColor": random_clrs[25],
            "command": "from nlol.core.rig_components import create_locators\n"
            "from importlib import reload\nreload(create_locators)\n"
            "create_locators.temp_locator()",
            "sourceType": "python",
        },
        {
            "label": "Multi Parent Constraint",
            "image": "pythonFamily.png",
            "annotation": "Useful for constraining multiple ctrls to a single locator "
            "for a temporary pivot. Constrains to last selected object.",
            "imageOverlayLabel": "MltPrt",
            "backgroundColor": random_clrs[26],
            "command": "from nlol.core.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.multi_parent_const()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Source Target Connect (Anim Retarget)",
            "image": "pythonFamily.png",
            "annotation": "Connect source and target ctrls for anim retarget."
            'Using the "retarget_data.toml" in the nLol rig or default folder.',
            "imageOverlayLabel": "SrcTrg",
            "backgroundColor": random_clrs[27],
            "command": "from nlol.core.animation_tools import retarget_animation\n"
            "from importlib import reload\nreload(retarget_animation)\n"
            "retarget_animation.RetargetAnimation().apply_ctrl_connections()",
            "sourceType": "python",
        },
        {
            "label": "Delete Connections (Anim Retarget)",
            "image": "pythonFamily.png",
            "annotation": "Delete constraint connections created for anim retarget.",
            "imageOverlayLabel": "DelCon",
            "backgroundColor": random_clrs[28],
            "command": "from nlol.core.animation_tools import retarget_animation\n"
            "from importlib import reload\nreload(retarget_animation)\n"
            "retarget_animation.RetargetAnimation().delete_ctrl_connections()",
            "sourceType": "python",
        },
        {
            "label": "Copy Keyframes (Anim Retarget)",
            "image": "pythonFamily.png",
            "annotation": "Bake keyframes from source to target controls. "
            "Only bake on attributes and frames with keyframe data. "
            "Copy over tangent data.",
            "imageOverlayLabel": "CpyKey",
            "backgroundColor": random_clrs[29],
            "command": "from nlol.core.animation_tools import retarget_animation\n"
            "from importlib import reload\nreload(retarget_animation)\n"
            "retarget_animation.RetargetAnimation().copy_keyframes()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Animation Save Load UI",
            "image": "pythonFamily.png",
            "annotation": "UI for saving and loading animation data for selected objects.",
            "imageOverlayLabel": "KeyUI",
            "backgroundColor": random_clrs[30],
            "command": "from nlol.core.ui import anim_saver_ui\nanim_saver_ui.reload_tool()",
            "sourceType": "python",
        },
    ]

    return animation_list
