from importlib import reload

from maya import cmds
from nlol.shelves_menus import animation_list
from nlol.utilities.nlol_maya_logger import get_logger

reload(animation_list)


def update_animation_shelf():
    """Update or add the animation shelf."""
    logger = get_logger()

    shelf_name = "nlAnimTools"

    top_shelf = cmds.shelfTabLayout("ShelfLayout", query=True, fullPathName=True)

    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    cmds.shelfLayout(shelf_name, parent=top_shelf)

    shelf_list = animation_list.build_animation_list()
    for shelf in shelf_list:
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
