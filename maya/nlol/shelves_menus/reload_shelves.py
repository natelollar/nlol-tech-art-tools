from maya import cmds, mel
from nlol.shelves_menus import nurbs_curve_shelf, rigging_shelf


def update_nlol_shelves():
    shelf_name = "nlReload"

    # get top shelf layout
    top_shelf = cmds.shelfTabLayout("ShelfLayout", query=True, fullPathName=True)

    # delete shelf if exists
    if cmds.shelfLayout(shelf_name, exists=True):
        cmds.deleteUI(shelf_name, layout=True)

    # create shelf
    cmds.shelfLayout(shelf_name, parent=top_shelf)

    # add shelf buttons
    cmds.shelfButton(
        label="Reload nlol Shelves",
        image="refresh.png",
        annotation="Reload nlol Shelves.",
        imageOverlayLabel="",
        backgroundColor=(0.3, 0.3, 0.0),
        command="from nlol.shelves_menus import rigging_shelf, nurbs_curve_shelf\n"
        "from importlib import reload\n"
        "reload(rigging_shelf)\n"
        "rigging_shelf.update_rigging_shelf()\n"
        "reload(nurbs_curve_shelf)\n"
        "nurbs_curve_shelf.update_nurbs_curve_shelf()",
        sourceType="python",
        parent=shelf_name,
    )

    cmds.shelfButton(
        label="Reload nLol Menu",
        image="refresh.png",
        flipY=True,
        annotation="Reload nLol Menus.",
        backgroundColor=(0.4, 0.3, 0.0),
        command="from nlol.shelves_menus import reload_menus\n"
        "from importlib import reload\n"
        "reload(reload_menus)\n"
        "reload_menus.main_menu()\n",
        sourceType="python",
        parent=shelf_name,
    )

    print(f"Created shelf: {shelf_name}")

    # create other shelves too for initial setup
    rigging_shelf.update_rigging_shelf()
    nurbs_curve_shelf.update_nurbs_curve_shelf()

    # save all shelves.  otherwise restarting maya may change shelves.
    # save all shelves under main top shelf
    mel.eval("saveAllShelves $gShelfTopLevel;")
