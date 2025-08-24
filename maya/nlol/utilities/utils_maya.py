import sys
from functools import wraps

from PySide6 import QtWidgets
from shiboken6 import wrapInstance

from maya import OpenMayaUI as omui
from maya import cmds


def query_maya_windows():
    """Print Maya Qt window names."""
    # list main window
    main_window_pointer = omui.MQtUtil.mainWindow()
    main_window = wrapInstance(int(main_window_pointer), QtWidgets.QMainWindow)
    print(f"Main Window: {main_window.objectName()}")

    # list other windows
    # windows = cmds.lsUI(controlLayouts=True)
    shelf_windows = cmds.lsUI(type="shelfTabLayout")
    for win in shelf_windows:
        print(f"'shelfTabLayout' window: {win}")


def get_sys_path():
    """Print python system paths."""
    for path in sys.path:
        print(path)


def get_selected_type():
    objects = cmds.ls(selection=True)
    for obj in objects:
        obj_type = cmds.objectType(obj)
        print(obj_type)


def cap(text: str) -> str:
    """Capitalize only first letter in a string."""
    return text[0].upper() + text[1:] if text else text


def snake_to_camel(text: str) -> str:
    """Converts snake_case to camelCase."""
    components = text.split("_")
    return components[0] + "".join(cap(comp) for comp in components[1:])


def add_divider_attribue(
    control_name: str,
    divider_amount: int = 10,
    divider_symbol: str = "_",
) -> None:
    """Attribute to place above added attributes in channel box.
    Helpful for organizing and viewing channel box attributes.
    Attribute appears as a line in the channel box.
    """
    divider_string = divider_amount * divider_symbol
    cmds.addAttr(
        control_name,
        longName=divider_string,
        niceName=divider_string,
        attributeType="enum",
        enumName=divider_string,
    )
    cmds.setAttr(f"{control_name}.{divider_string}", channelBox=True)


def maya_undo(func):
    """Groups executed maya commands into single undo chunk.
    Wrap functions or methods, not classes.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            return func(*args, **kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)

    return wrapper


def left_to_right_str(text_str: str) -> str:
    """Replace left string characters with right characters.
    Currently, replaces any `_left_` with `_right_` and the suffix `_l` with `_r`.
    Example: Replaces `_left_` with `_right_` in `ikHand_left_ctrl`.
    Specifically works with a string or string list.
    Example: `hand_l` or `indexFinger_left_01_ctrl` or
    `pinky_metacarpal_l, pinky_01_l, pinky_02_l, pinky_03_l`

    Args:
        text_str: Input string text containing left characters.

    Returns:
        New string text for right side.

    """
    if not text_str:
        return text_str
    text_str = text_str.replace("_left_", "_right_")
    text_str = text_str.replace("_l,", "_r,")
    text_str = f"{text_str[:-2]}_r" if text_str.endswith("_l") else text_str
    return text_str
