from importlib import reload

from maya import cmds
from nlol.scripts.rig_tools import better_duplicate
from nlol.utilities.utils_maya import maya_undo

reload(better_duplicate)

duplicate_curve = better_duplicate.duplicate_curve


@maya_undo
def mirror_curves(
    original_side: str = "left",
    flipped_side: str = "right",
    mirror_axis: str = "x",
) -> None:
    """Mirror rig control curve shapes across axis.
    Mirrors to absolute position, so controls with
    non-perfect mirroring will have to be adjusted.
    """
    selection = cmds.ls(selection=True)

    for crv in selection:
        cmds.select(crv)

        # list locked attr to unlock and relock later
        crv_locked_attr = cmds.listAttr(crv, locked=True)
        if crv_locked_attr:
            for attr in crv_locked_attr:
                cmds.setAttr(f"{crv}.{attr}", lock=False, keyable=True, channelBox=True)

        # duplicate, delete children, unparent
        crv_dup = duplicate_curve(crv)
        crv_dup_childs = cmds.listRelatives(crv_dup, allDescendents=True, type="transform")
        cmds.delete(crv_dup_childs)
        cmds.Unparent(crv_dup)

        # parent duplicated ctrl under world origin grp, then flip across axis
        world_grp = cmds.group(empty=True)
        cmds.parent(crv_dup, world_grp)
        cmds.setAttr(f"{world_grp}.scale{mirror_axis.upper()}", -1)
        cmds.Unparent(crv_dup)
        cmds.delete(world_grp)

        # find opposite side ctrl of orignal duplicated
        crv_opp = crv.replace(original_side, flipped_side)

        # unlock all attributes
        if crv_locked_attr:
            for attr in crv_locked_attr:
                cmds.setAttr(f"{crv_opp}.{attr}", lock=False, keyable=True, channelBox=True)

        # get shape of opposite side ctrl to delete later
        crv_opp_shape = cmds.listRelatives(crv_opp, shapes=True)
        # parent under opposite ctrl and freeze attributes to get same exact trans, rot, scale
        cmds.parent(crv_dup, crv_opp)
        cmds.makeIdentity(crv_dup, apply=True)
        cmds.Unparent(crv_dup)

        # find shape of duplicated ctrl
        crv_dup_shape = cmds.listRelatives(crv_dup, shapes=True)
        # parent flipped shape under other side ctrl
        cmds.parent(crv_dup_shape, crv_opp, relative=True, shape=True)
        cmds.delete(crv_dup)  # delete unused duplicate transform
        cmds.delete(crv_opp_shape)  # delete old shape under opposite ctrl

        # rename new shape after opposite ctrl parent
        for shp in crv_dup_shape:
            cmds.rename(shp, f"{crv_opp}Shape")

        # relock and hide attritues
        if crv_locked_attr:
            for attr in crv_locked_attr:
                cmds.setAttr(f"{crv}.{attr}", lock=True, keyable=False, channelBox=False)
                cmds.setAttr(f"{crv_opp}.{attr}", lock=True, keyable=False, channelBox=False)

        cmds.select(crv_opp)
