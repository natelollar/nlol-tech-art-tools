from maya import cmds


def remove_nlol_menus():
    """Remove the nLol Menus from Maya."""
    menu_name = "nlol_tools_menu"

    if cmds.menu(menu_name, exists=True):
        cmds.deleteUI(menu_name)
        print(f"Menu removed: {menu_name}")

