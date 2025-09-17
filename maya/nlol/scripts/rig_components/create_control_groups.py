from maya import cmds


def create_ctrl_grps(control: str, aux_offset_group: bool = False) -> str:
    """Create groups for control curves.
    This includes the parent group, parent switch group,
    and offset group. Creates a single set of groups for one control.

    Args:
        control: Control to be parented under groups.
        aux_offset_group: Add an additional offset group. "aux" standing for "auxiliary".
            Useful for adding extra connections.

    Returns:
        Group names.

    """
    offset_group = cmds.group(empty=True, name=f"{control}OffsetGrp")
    if aux_offset_group:
        aux_offset_group = cmds.group(empty=True, name=f"{control}AuxOffsetGrp")
    parent_switch_group = cmds.group(empty=True, name=f"{control}PrntSwchGrp")
    parent_group = cmds.group(empty=True, name=f"{control}PrntGrp")
    top_group = cmds.group(empty=True, name=f"{control}Grp")

    cmds.parent(control, offset_group)
    if aux_offset_group:
        cmds.parent(offset_group, aux_offset_group)
        cmds.parent(aux_offset_group, parent_switch_group)
    else:
        cmds.parent(offset_group, parent_switch_group)
    cmds.parent(parent_switch_group, parent_group)
    cmds.parent(parent_group, top_group)

    return_groups = (top_group, parent_group, parent_switch_group, offset_group)
    if aux_offset_group:
        return return_groups + (aux_offset_group,)
    return return_groups
