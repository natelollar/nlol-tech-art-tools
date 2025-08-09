from maya import cmds
from nlol.shelves_menus.nurbs_curve_list import NURBS_CURVE_LIST


def update_nurbs_curve_shelf():
    shelf_name = "nlNurbsCurves"

    # get top shelf layout
    top_shelf = cmds.shelfTabLayout("ShelfLayout", query=True, fullPathName=True)

    # delete shelf if exists
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    # create shelf
    cmds.shelfLayout(shelf_name, parent=top_shelf)

    for shelf in NURBS_CURVE_LIST:
        cmds.shelfButton(
            label=shelf["label"],
            image=shelf["image"],
            annotation=shelf["annotation"],
            imageOverlayLabel=shelf["imageOverlayLabel"],
            backgroundColor=shelf["backgroundColor"],
            command=shelf["command"],
            sourceType=shelf["sourceType"],
            parent=shelf_name,
        )

    print(f"Created shelf: {shelf_name}")
