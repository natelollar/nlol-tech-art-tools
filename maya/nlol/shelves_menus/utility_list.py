"""List of utility variables to be called by shelf and menu."""

from importlib import reload

from nlol.core.rig_tools import random_generator

reload(random_generator)

random_colors_dull = random_generator.random_colors_dull


def build_utility_list():
    """Create a dictionary list of utility menu and shelf buttons, and their attributes."""
    random_clrs = random_colors_dull()

    shelf_separator = {
        "label": "=" * 35,
        "image": "nlol_separator_03_blue.png",
        "annotation": "Separator.",
        "command": 'print("Separator.")',
        "sourceType": "python",
    }

    utility_list = [
        shelf_separator,
        {
            "label": 'Set Hotkey for "Camera Pivot To Mouse"',
            "image": "pythonFamily.png",
            "annotation": 'Set hotkey for "Camera Pivot To Mouse" to "alt+f". '
            "Double click shelf button to delete hotkey. "
            'Meant to work with "tumble_tool_settings" set with shelf button. ',
            "imageOverlayLabel": "MsHtky",
            "backgroundColor": random_clrs[0],
            "command": "from nlol.core.standalone.viewport_navigation "
            "import camera_pivot_set_hotkeys\n"
            "from importlib import reload\nreload(camera_pivot_set_hotkeys)\n"
            "camera_pivot_set_hotkeys.cam_pivot_to_mouse_hotkey()",
            "doubleClickCommand": "from nlol.core.standalone.viewport_navigation "
            "import camera_pivot_set_hotkeys\n"
            "from importlib import reload\nreload(camera_pivot_set_hotkeys)\n"
            "camera_pivot_set_hotkeys.delete_cam_mouse_hotkey()",
            "sourceType": "python",
        },
        {
            "label": 'Set Hotkey for "Camera Pivot To Selected"',
            "image": "pythonFamily.png",
            "annotation": 'Set hotkey for "Camera Pivot To Selected" to "shift+f". '
            "Double click shelf button to delete hotkey. "
            'Meant to work with "tumble_tool_settings" set with shelf button. ',
            "imageOverlayLabel": "SlHtky",
            "backgroundColor": random_clrs[1],
            "command": "from nlol.core.standalone.viewport_navigation "
            "import camera_pivot_set_hotkeys\n"
            "from importlib import reload\nreload(camera_pivot_set_hotkeys)\n"
            "camera_pivot_set_hotkeys.cam_pivot_to_selected_hotkey()",
            "doubleClickCommand": "from nlol.core.standalone.viewport_navigation "
            "import camera_pivot_set_hotkeys\n"
            "from importlib import reload\nreload(camera_pivot_set_hotkeys)\n"
            "camera_pivot_set_hotkeys.delete_cam_selected_hotkey()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Create Camera Pivot Locator",
            "image": "pythonFamily.png",
            "annotation": "Create locator curve to show camera tumble pivot.",
            "imageOverlayLabel": "CamLoc",
            "backgroundColor": random_clrs[2],
            "command": "from nlol.core.standalone.viewport_navigation "
            "import camera_pivot_locator\n"
            "from importlib import reload\nreload(camera_pivot_locator)\n"
            "camera_pivot_locator.create_curve_locator()",
            "doubleClickCommand": "from nlol.core.standalone.viewport_navigation "
            "import camera_pivot_locator\n"
            "from importlib import reload\nreload(camera_pivot_locator)\n"
            "camera_pivot_locator.delete_curve_locator()",
            "sourceType": "python",
        },
        {
            "label": "Create Small Camera Pivot Locator",
            "image": "pythonFamily.png",
            "annotation": "Create small locator curve to show camera tumble pivot.",
            "imageOverlayLabel": "LocSml",
            "backgroundColor": random_clrs[3],
            "command": "from nlol.core.standalone.viewport_navigation "
            "import camera_pivot_locator\n"
            "from importlib import reload\nreload(camera_pivot_locator)\n"
            "camera_pivot_locator.create_curve_locator(small_locator=True)",
            "doubleClickCommand": "from nlol.core.standalone.viewport_navigation "
            "import camera_pivot_locator\n"
            "from importlib import reload\nreload(camera_pivot_locator)\n"
            "camera_pivot_locator.delete_curve_locator()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Set Camera Tumble Tool Settings",
            "image": "pythonFamily.png",
            "annotation": "Set camera tumble tool settings "
            'needed for "camera_pivot_to_mouse" tool. '
            'These settings can be set manually in "View < Camera Tools < Tumble Tool".',
            "imageOverlayLabel": "TmblSt",
            "backgroundColor": random_clrs[4],
            "command": "from nlol.core.standalone.viewport_navigation "
            "import tumble_tool_settings\n"
            "from importlib import reload\nreload(tumble_tool_settings)\n"
            "tumble_tool_settings.apply_tumble_settings()",
            "sourceType": "python",
        },
        {
            "label": "Reset Tumble Tool Settings",
            "image": "pythonFamily.png",
            "annotation": "Reset camera tumble tool settings to default values. "
            'These settings can be set manually in "View < Camera Tools < Tumble Tool".',
            "imageOverlayLabel": "RstTmbl",
            "backgroundColor": random_clrs[5],
            "command": "from nlol.core.standalone.viewport_navigation "
            "import tumble_tool_settings\n"
            "from importlib import reload\nreload(tumble_tool_settings)\n"
            "tumble_tool_settings.reset_tumble_settings()",
            "sourceType": "python",
        },
    ]

    return utility_list
