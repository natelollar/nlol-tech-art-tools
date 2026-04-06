from maya import cmds


def create_ctrl_grps(control: str, aux_offset_grp: int | bool = False) -> tuple[str]:
    """Create groups for control curves.
    This includes the parent group, parent switch group,
    and offset group/s. Creates a single set of groups for one control.

    Args:
        control: Control to be parented under groups.
        aux_offset_grp: Add additional offset groups. "aux" standing for "auxiliary".
            Useful for adding extra connections. Enter "True" for one extra group,
            or an integer for multiple extra groups.

    Returns:
        Group names.

    """
    offset_grp = cmds.group(empty=True, name=f"{control}OffsetGrp")
    aux_offset_grps = []

    if aux_offset_grp is True:
        aux_offset_grp = cmds.group(empty=True, name=f"{control}AuxOffsetGrp")
        aux_offset_grps = [aux_offset_grp]
    elif isinstance(aux_offset_grp, int):
        for i in range(1, aux_offset_grp + 1):
            grp = cmds.group(empty=True, name=f"{control}Aux{i:02d}OffsetGrp")
            aux_offset_grps.append(grp)
        for i, grp in enumerate(aux_offset_grps[1:]):
            cmds.parent(grp, aux_offset_grps[i])

    parent_switch_grp = cmds.group(empty=True, name=f"{control}PrntSwchGrp")
    parent_grp = cmds.group(empty=True, name=f"{control}PrntGrp")
    top_grp = cmds.group(empty=True, name=f"{control}Grp")

    cmds.parent(control, offset_grp)
    if aux_offset_grps:
        cmds.parent(offset_grp, aux_offset_grps[-1])
        cmds.parent(aux_offset_grps[0], parent_switch_grp)
    else:
        cmds.parent(offset_grp, parent_switch_grp)

    cmds.parent(parent_switch_grp, parent_grp)
    cmds.parent(parent_grp, top_grp)

    return_grps = (top_grp, parent_grp, parent_switch_grp, offset_grp)
    return return_grps + tuple(aux_offset_grps)
