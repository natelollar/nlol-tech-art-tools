from importlib import reload

from maya import cmds
from nlol.shelves_menus import nurbs_curve_list, rigging_list
from nlol.utilities.nlol_maya_logger import get_logger

reload(nurbs_curve_list)
reload(rigging_list)


def main_menu():
    """Create nLol Maya menu equivilent to the nLol Maya shelf.
    Contains tech are tools, including rigging tools.
    """
    logger = get_logger()

    nlol_menu_name = "nlol_tools_menu"

    # check if menu already exists
    if cmds.menu(nlol_menu_name, exists=True):
        cmds.deleteUI(nlol_menu_name)

    # ----- nlol menu -----
    nlol_menu = cmds.menu(nlol_menu_name, label="nLol Tools", parent="MayaWindow", tearOff=True)
    # ----- divider -----
    cmds.menuItem(
        "rigging_tools_divider",
        divider=True,
        dividerLabel="Rig Tools",
        parent=nlol_menu,
    )
    # ----- submenus -----
    nurbs_curve_submenu = cmds.menuItem(
        "nurbs_curve_submenu",
        label="Nurbs Curves",
        parent=nlol_menu,
        tearOff=True,
        subMenu=True,
    )
    rigging_submenu = cmds.menuItem(
        "rigging_submenu",
        label="Rigging",
        parent=nlol_menu,
        tearOff=True,
        subMenu=True,
    )

    # add the nurbs curve menu items
    curve_menu_list = nurbs_curve_list.build_curve_list()
    for menu in curve_menu_list:
        kwargs = {
            key: menu[key]
            for key in ["label", "annotation", "image", "command"]
            if key in menu and menu[key] not in (None, "")
        }
        kwargs["parent"] = nurbs_curve_submenu
        cmds.menuItem(**kwargs)

    # add the rigging menu items
    rigging_menu_list = rigging_list.build_rigging_list()
    for menu in rigging_menu_list:
        kwargs = {
            key: menu[key]
            for key in ["label", "annotation", "image", "command"]
            if key in menu and menu[key] not in (None, "")
        }
        kwargs["parent"] = rigging_submenu
        cmds.menuItem(**kwargs)

    logger.info(f"Reloaded menu: {nlol_menu_name}")
