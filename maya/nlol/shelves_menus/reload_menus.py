from importlib import reload

from maya import cmds
from nlol.shelves_menus import nurbs_curve_list, rigging_list

reload(nurbs_curve_list)
reload(rigging_list)


def main_menu():
    nlol_menu_name = "nlol_tools_menu"

    # check if menu already exists
    if cmds.menu(nlol_menu_name, exists=True):
        cmds.deleteUI(nlol_menu_name)

    # nlol menu
    nlol_menu = cmds.menu(nlol_menu_name, label="nLol Tools", parent="MayaWindow", tearOff=True)
    # divider
    cmds.menuItem(
        "rigging_tools_divider",
        divider=True,
        dividerLabel="Rig Tools",
        parent=nlol_menu,
    )
    # nurbs curve menu
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
    for menu in nurbs_curve_list.NURBS_CURVE_LIST:
        cmds.menuItem(
            label=menu["label"],
            annotation=menu["annotation"],
            image=menu["image"],
            command=menu["command"],
            parent=nurbs_curve_submenu,
        )

    # add the rigging menu items
    for menu in rigging_list.RIGGING_LIST:
        # dict comp to account for menu items not needing all the args
        kwargs = {
            key: menu[key]
            for key in ["label", "annotation", "image", "command"]
            if key in menu and menu[key] not in (None, "")
        }
        kwargs["parent"] = rigging_submenu
        cmds.menuItem(**kwargs)

    print(f"Reloaded menu: {nlol_menu_name}")
