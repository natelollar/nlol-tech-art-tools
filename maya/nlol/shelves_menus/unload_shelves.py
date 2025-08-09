from maya import mel


def remove_nlol_shelves():
    """Remove the nlol shelves from Maya."""
    reload_shelf = "nlReload"
    rigging_shelf = "nlRigTools"
    nurbs_curves_shelf = "nlNurbsCurves"

    try:
        mel.eval(f"deleteShelfTab {reload_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {reload_shelf}.")
    try:
        mel.eval(f"deleteShelfTab {rigging_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {rigging_shelf}.")
    try:
        mel.eval(f"deleteShelfTab {nurbs_curves_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {nurbs_curves_shelf}.  Likely does not exist.")
