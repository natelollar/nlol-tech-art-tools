from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger


def update_reload_shelf():
    """Update or add shelf with reload buttons."""
    logger = get_logger()

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
        command="from nlol.shelves_menus import rigging_shelf, nurbs_curve_shelf, utility_shelf\n"
        "from importlib import reload\n"
        "reload(rigging_shelf)\nrigging_shelf.update_rigging_shelf()\n"
        "reload(nurbs_curve_shelf)\nnurbs_curve_shelf.update_nurbs_curve_shelf()\n"
        "reload(utility_shelf)\nutility_shelf.update_utility_shelf()\n",
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
        "reload(reload_menus)\nreload_menus.main_menu()\n",
        sourceType="python",
        parent=shelf_name,
    )

    logger.info(f"Created shelf: {shelf_name}")
