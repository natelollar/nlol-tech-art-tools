from importlib import reload

from maya import mel
from nlol.shelves_menus import nurbs_curve_shelf, reload_shelf, rigging_shelf, utility_shelf

reload(reload_shelf)
reload(nurbs_curve_shelf)
reload(rigging_shelf)
reload(utility_shelf)


def update_nlol_shelves():
    """Reload nLol shelves."""
    reload_shelf.update_reload_shelf()
    rigging_shelf.update_rigging_shelf()
    nurbs_curve_shelf.update_nurbs_curve_shelf()
    utility_shelf.update_utility_shelf()

    # save all shelves.  otherwise restarting maya may change shelves.
    # save all shelves under main top shelf
    mel.eval("saveAllShelves $gShelfTopLevel;")
