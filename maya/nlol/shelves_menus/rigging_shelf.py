from maya import cmds
from nlol.shelves_menus.rigging_list import RIGGING_LIST


def update_rigging_shelf():
    shelf_name = "nlRigTools"

    # get top shelf layout
    top_shelf = cmds.shelfTabLayout("ShelfLayout", query=True, fullPathName=True)

    # delete shelf if exists
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    # create shelf
    cmds.shelfLayout(shelf_name, parent=top_shelf)

    for shelf in RIGGING_LIST:
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

    print(f"Created shelf: {shelf_name}")
