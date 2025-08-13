from maya import cmds


def create_ctrl_grps(control: str) -> str:
    """Create groups for control curves.
    This includes the parent group, parent switch group,
    and offset group. Creates a single set of groups for one control.

    Args:
        Control to be parented.

    Returns:
        Group names.

    """
    control_group = cmds.group(empty=True, name=f"{control}Grp")
    global_group = cmds.group(empty=True, name=f"{control}PrntGrp", relative=True)
    switch_group = cmds.group(empty=True, name=f"{control}PrntSwchGrp", relative=True)
    offset_group = cmds.group(empty=True, name=f"{control}OffsetGrp", relative=True)

    cmds.parent(control, offset_group)
    cmds.parent(offset_group, switch_group)
    cmds.parent(switch_group, global_group)
    cmds.parent(global_group, control_group)

    return control_group, switch_group, offset_group
