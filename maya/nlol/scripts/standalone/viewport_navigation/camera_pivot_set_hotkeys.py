from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def cam_pivot_to_mouse_hotkey(create_empty_hotkey: bool = False):
    """Set "camera_pivot_to_mouse" tool to "alt+f" hotkey."""
    # remove runTimeCommand if exists
    if cmds.runTimeCommand("CameraPivotToMouse", exists=True):
        cmds.runTimeCommand("CameraPivotToMouse", edit=True, delete=True)
    # ----- create runTimeCommand -----
    cmds.runTimeCommand(
        "CameraPivotToMouse",
        annotation="Move camera tumble pivot to closest position under mouse. "
        "Raycasts from mouse into viewport. Uses mesh shapes for raycast intersection. "
        'Meant to work with "tumble_tool_settings" set with shelf button. ',
        category="Custom Scripts",
        command="from nlol.scripts.standalone.viewport_navigation "
        "import camera_pivot_to_mouse\n"
        "from importlib import reload\nreload(camera_pivot_to_mouse)\n"
        "camera_pivot_to_mouse.pivot_to_mouse()",
        commandLanguage="python",
    )
    # ----- set hotkey to runTimeCommand -----
    if create_empty_hotkey:  # set empty for when deleting hotkey
        cmds.hotkey(keyShortcut="f", altModifier=True, name="")
    else:
        # requires "NameCommand" suffix for some odd reason
        # suffix required or "alt+f" doesn't get added
        cmds.hotkey(keyShortcut="f", altModifier=True, name="CameraPivotToMouseNameCommand")

    # query resulting hotkey
    hotkey_query = cmds.hotkey("f", query=True, keyShortcut=True, altModifier=True, name=True)
    logger.info(f"hotkey_query: {hotkey_query}")


def delete_cam_mouse_hotkey():
    """Delete "camera_pivot_to_mouse" hotkey. Leaving the remaining hotkey empty."""
    # recreate empty version of hotkey first
    cam_pivot_to_mouse_hotkey(create_empty_hotkey=True)

    if cmds.runTimeCommand("CameraPivotToMouse", exists=True):
        cmds.runTimeCommand("CameraPivotToMouse", edit=True, delete=True)

    cmds.hotkey("f", keyShortcut=True, altModifier=True, name="")

    # query resulting hotkey
    hotkey_query = cmds.hotkey("f", query=True, keyShortcut=True, altModifier=True, name=True)
    logger.info(f"hotkey_query: {hotkey_query}")


def cam_pivot_to_selected_hotkey(create_empty_hotkey: bool = False):
    """Set "camera_pivot_to_selected" tool to "shift+f" hotkey."""
    # remove runTimeCommand if exists
    if cmds.runTimeCommand("CameraPivotToSelected", exists=True):
        cmds.runTimeCommand("CameraPivotToSelected", edit=True, delete=True)
    # ----- create runTimeCommand -----
    cmds.runTimeCommand(
        "CameraPivotToSelected",
        annotation="Set camera tumble pivot to selected objects pivot. "
        "For example, useful when rotating around a specific joint in a joint chain. "
        'Meant to work with "tumble_tool_settings" set with shelf button. ',
        category="Custom Scripts",
        command="from nlol.scripts.standalone.viewport_navigation "
        "import camera_pivot_to_selected\n"
        "from importlib import reload\nreload(camera_pivot_to_selected)\n"
        "camera_pivot_to_selected.set_camera_pivot_to_selected()",
        commandLanguage="python",
    )
    # ----- set hotkey to runTimeCommand -----
    if create_empty_hotkey:
        cmds.hotkey(keyShortcut="f", shiftModifier=True, name="")
    else:
        cmds.hotkey(keyShortcut="f", shiftModifier=True, name="CameraPivotToSelectedNameCommand")

    hotkey_query = cmds.hotkey("f", query=True, keyShortcut=True, shiftModifier=True, name=True)
    logger.info(f"hotkey_query: {hotkey_query}")


def delete_cam_selected_hotkey():
    """Delete "camera_pivot_to_selected" hotkey. Leaving the remaining hotkey empty."""
    cam_pivot_to_selected_hotkey(create_empty_hotkey=True)

    if cmds.runTimeCommand("CameraPivotToSelected", exists=True):
        cmds.runTimeCommand("CameraPivotToSelected", edit=True, delete=True)

    cmds.hotkey("f", keyShortcut=True, shiftModifier=True, name="")

    hotkey_query = cmds.hotkey("f", query=True, keyShortcut=True, shiftModifier=True, name=True)
    logger.info(f"hotkey_query: {hotkey_query}")
