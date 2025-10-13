from maya import cmds


def create_ctrl_grps(control: str, aux_offset_grp: bool = False) -> str:
    """Create groups for control curves.
    This includes the parent group, parent switch group,
    and offset group. Creates a single set of groups for one control.

    Args:
        control: Control to be parented under groups.
        aux_offset_grp: Add an additional offset group. "aux" standing for "auxiliary".
            Useful for adding extra connections.

    Returns:
        Group names.

    """
    offset_grp = cmds.group(empty=True, name=f"{control}OffsetGrp")
    if aux_offset_grp:
        aux_offset_grp = cmds.group(empty=True, name=f"{control}AuxOffsetGrp")
    parent_switch_grp = cmds.group(empty=True, name=f"{control}PrntSwchGrp")
    parent_grp = cmds.group(empty=True, name=f"{control}PrntGrp")
    top_grp = cmds.group(empty=True, name=f"{control}Grp")

    cmds.parent(control, offset_grp)
    if aux_offset_grp:
        cmds.parent(offset_grp, aux_offset_grp)
        cmds.parent(aux_offset_grp, parent_switch_grp)
    else:
        cmds.parent(offset_grp, parent_switch_grp)
    cmds.parent(parent_switch_grp, parent_grp)
    cmds.parent(parent_grp, top_grp)

    return_grps = (top_grp, parent_grp, parent_switch_grp, offset_grp)
    if aux_offset_grp:
        return return_grps + (aux_offset_grp,)
    return return_grps
