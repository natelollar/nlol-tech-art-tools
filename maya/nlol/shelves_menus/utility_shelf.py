from importlib import reload

from maya import cmds
from nlol.shelves_menus import utility_list
from nlol.utilities.nlol_maya_logger import get_logger

reload(utility_list)


def update_utility_shelf():
    """Update or add utility shelf."""
    logger = get_logger()

    shelf_name = "nlUtils"

    # get top shelf layout
    top_shelf = cmds.shelfTabLayout("ShelfLayout", query=True, fullPathName=True)

    # delete shelf if exists
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    # create shelf
    cmds.shelfLayout(shelf_name, parent=top_shelf)

    shelf_list = utility_list.build_utility_list()
    for shelf in shelf_list:
        # dict comprehension to account for some shelf buttons not needing all the args
        kwargs = {
            key: shelf[key]
            for key in [
                "label",
                "image",
                "annotation",
                "imageOverlayLabel",
                "flexibleWidthType",
                "flexibleWidthValue",
                "backgroundColor",
                "highlightColor",
                "command",
                "doubleClickCommand",
                "sourceType",
                "menuItem",
                "menuItemPython",
            ]
            if key in shelf and shelf[key] not in (None, "")
        }
        kwargs["parent"] = shelf_name
        cmds.shelfButton(**kwargs)

    logger.info(f"Created shelf: {shelf_name}")
