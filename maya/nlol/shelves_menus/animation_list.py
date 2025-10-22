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
            "label": "Apply All Keyframes",
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
    ]

    return animation_list
