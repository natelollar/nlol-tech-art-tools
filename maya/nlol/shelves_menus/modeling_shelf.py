from importlib import reload

from maya import cmds
from nlol.shelves_menus import modeling_list
from nlol.utilities.nlol_maya_logger import get_logger

reload(modeling_list)


def update_modeling_shelf():
    """Update or add the modeling shelf."""
    logger = get_logger()

    shelf_name = "nlModelTools"

    # get top shelf layout
    top_shelf = cmds.shelfTabLayout("ShelfLayout", query=True, fullPathName=True)

    # delete shelf if exists
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    # create shelf
    cmds.shelfLayout(shelf_name, parent=top_shelf)

    shelf_list = modeling_list.build_modeling_list()
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
                # ----------
                "enable",
                "width",
                "height",
                "manage",
                "visible",
                "preventOverride",
                "enableBackground",
                "style", 
                "horizontal",
            ]
            if key in shelf and shelf[key] not in (None, "")
        }
        kwargs["parent"] = shelf_name
        cmds.shelfButton(**kwargs)

    logger.info(f"Created shelf: {shelf_name}")
