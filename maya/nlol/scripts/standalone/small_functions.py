from maya import cmds
from nlol.scripts.rig_tools import show_attributes


def select_shapes():
    selection = cmds.ls(selection=True)

    selection_shapes = []
    for obj in selection:
        shps = cmds.listRelatives(obj, shapes=True)
        selection_shapes.extend(shps)

    cmds.select(selection_shapes)

def select_shapes_show_attrs():
    """Select curve shapes and show useful curve shape attributes."""
    selection = cmds.ls(selection=True)

    selection_shapes = []
    for obj in selection:
        shps = cmds.listRelatives(obj, shapes=True)
        selection_shapes.extend(shps)

    cmds.select(selection_shapes)
    show_attributes.ShowAttributes().show_curve_attrs()

def get_selection_type():
    selection = cmds.ls(selection=True)
    selection_type = cmds.objectType(selection)
    print(selection_type)


def select_all_controls(main_rig_group: str = "rig_allGrp"):
    """Select all control curves underneath selected group
    or specified group.
    """
    selection = cmds.ls(selection=True)
    if selection:
        #control_group = selection[0]
        control_group = selection
    else:
        control_group = main_rig_group

    all_ctrls = cmds.listRelatives(control_group, allDescendents=True)
    all_ctrls = [
        ctrl
        for ctrl in all_ctrls
        if cmds.listRelatives(ctrl, shapes=True, type="nurbsCurve") and "ctrl" in ctrl.lower()
    ]

    cmds.select(all_ctrls)
