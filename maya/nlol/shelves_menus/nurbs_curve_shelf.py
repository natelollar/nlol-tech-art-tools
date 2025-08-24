from importlib import reload

from maya import cmds
from nlol.shelves_menus import nurbs_curve_list
from nlol.utilities.nlol_maya_logger import get_logger
reload(nurbs_curve_list)


def update_nurbs_curve_shelf():
    logger = get_logger()

    shelf_name = "nlNurbsCurves"

    # get top shelf layout
    top_shelf = cmds.shelfTabLayout("ShelfLayout", query=True, fullPathName=True)

    # delete shelf if exists
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    # create shelf
    cmds.shelfLayout(shelf_name, parent=top_shelf)

    shelf_list = nurbs_curve_list.build_curve_list()
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
                "sourceType",
            ]
            if key in shelf and shelf[key] not in (None, "")
        }
        kwargs["parent"] = shelf_name
        cmds.shelfButton(**kwargs)

    logger.info(f"Created shelf: {shelf_name}")
