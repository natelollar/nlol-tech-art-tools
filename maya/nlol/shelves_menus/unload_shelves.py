from maya import mel


def remove_nlol_shelves():
    """Remove the nlol shelves from Maya."""
    reload_shelf = "nlReload"
    animation_shelf = "nlAnimTools"
    modeling_shelf = "nlModelTools"
    nurbs_curves_shelf = "nlNurbsCurves"
    rigging_shelf = "nlRigTools"
    utility_shelf = "nlUtils"

    try:
        mel.eval(f"deleteShelfTab {reload_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {reload_shelf}.")
    try:
        mel.eval(f"deleteShelfTab {animation_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {animation_shelf}.")
    try:
        mel.eval(f"deleteShelfTab {modeling_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {modeling_shelf}.")
    try:
        mel.eval(f"deleteShelfTab {nurbs_curves_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {nurbs_curves_shelf}.")
    try:
        mel.eval(f"deleteShelfTab {rigging_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {rigging_shelf}.")
    try:
        mel.eval(f"deleteShelfTab {utility_shelf};")
    except Exception:
        print(f"Failed to delete shelf: {utility_shelf}.")
