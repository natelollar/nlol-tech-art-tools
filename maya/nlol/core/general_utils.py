import sys
from functools import wraps

from PySide6 import QtWidgets
from shiboken6 import wrapInstance

from maya import OpenMayaUI as omui
from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


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


def swap_side_str(text_str) -> str:
    """Auto-detect and swap left/right character strings.
    Detects whether the string contains left or right indicators
    and swap to the opposite side.

    Args:
        text_str: Input string text with left or right characters.

    Returns:
        New string text with sides swapped, or original if no side detected.

    """
    if not text_str:
        return text_str

    original_text = text_str

    # detect side
    has_left = any(
        [
            "left" in text_str.lower(),
            text_str.endswith("_l"),
            text_str.startswith("l_"),
            "_l_" in text_str,
            "_l," in text_str,  # note commas in string
            ",l_" in text_str,
            " l_" in text_str,  # note whitespace in string
        ],
    )

    has_right = any(
        [
            "right" in text_str.lower(),
            text_str.endswith("_r"),
            text_str.startswith("r_"),
            "_r_" in text_str,
            "_r," in text_str,
            ",r_" in text_str,
            " r_" in text_str,
        ],
    )

    # determin direction
    if has_left and not has_right:
        from_side, to_side = "left", "right"
        from_abbr, to_abbr = "l", "r"
    elif has_right and not has_left:
        from_side, to_side = "right", "left"
        from_abbr, to_abbr = "r", "l"
    else:
        logger.debug(f"Could not determine side for: {original_text}")
        return text_str

    # perform replacements
    text_str = text_str.replace(from_side, to_side)
    text_str = text_str.replace(cap(from_side), cap(to_side))

    text_str = f"{text_str[:-2]}_{to_abbr}" if text_str.endswith(f"_{from_abbr}") else text_str
    text_str = f"{to_abbr}_{text_str[2:]}" if text_str.startswith(f"{from_abbr}_") else text_str

    text_str = text_str.replace(f"_{from_abbr}_", f"_{to_abbr}_")
    text_str = text_str.replace(f"_{from_abbr},", f"_{to_abbr},")  # note commas in strings
    text_str = text_str.replace(f",{from_abbr}_", f",{to_abbr}_")
    text_str = text_str.replace(f" {from_abbr}_", f" {to_abbr}_")  # note whitespace in strings

    return text_str


def left_to_right_str(text_str: str) -> str:
    """Replace left character strings with right character strings.
    Such as, replace any `left` with `right` and suffix `_l` with `_r`.
    Example: Replaces `left` with `right` in `ikHand_left_ctrl`.
    Specifically works with a string or string list.
    Example: `hand_l` or `indexFinger_left_01_ctrl` or
    `pinky_metacarpal_l, pinky_01_l, pinky_02_l, pinky_03_l`

    Args:
        text_str: Input string text containing left characters.

    Returns:
        New string text for right side.

    """
    return swap_side_str(text_str)


def invert_axis_string(text_str: str) -> str:
    """Invert axis "x", "y", or "z" to negative,
        or make negative axis positive.

    Args:
        text_str: Axis string.

    """
    return text_str.replace("-", "") if "-" in text_str else f"-{text_str}"


def get_top_parent(object) -> str:
    """Find top parent for object.
    For instance, finds the very top group in parent hierarchy.

    Args:
        object: Object to find top parent for.

    Returns:
        Very top parent of object.

    """
    object = cmds.ls(object, long=True)[0]

    while True:
        parent = cmds.listRelatives(object, parent=True, fullPath=True)
        if not parent:
            break
        object = parent[0]

    top_parent = object.split("|")[-1]

    return top_parent
