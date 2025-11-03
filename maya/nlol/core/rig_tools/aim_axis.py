from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def aim_axis_aim_constraint(
    freeze_transforms: bool = True,
    aim_vector: tuple = (1, 0, 0),
    up_Vector: tuple = (0, 1, 0),
    world_up_vector: tuple = (0, 1, 0),
):
    """Aim first object main axis at second object with aim constraint.
    Defaults to "x" aim axis and "y" up axis.

    Args:
        freeze_transforms: Freeze transforms before and after aiming object.
        aim_vector, up_Vector, world_up_vector: Standard Maya cmds args for aimConstraint.

    """
    selected = cmds.ls(selection=True)
    first_selected = selected[0]
    second_selected = selected[1]

    if freeze_transforms:
        cmds.makeIdentity(first_selected, apply=True)

    aim_const = cmds.aimConstraint(
        second_selected,
        first_selected,
        aimVector=aim_vector,
        upVector=up_Vector,
        worldUpType="vector",
        worldUpVector=world_up_vector,
    )[0]
    cmds.delete(aim_const)

    if freeze_transforms:
        cmds.makeIdentity(first_selected, apply=True)


def aim_axis_orient_joint():
    """Aim first joint main axis at second joint with "Skeleton < Orient Joint".
    Defaults to "x" main axis.
    """
    selected = cmds.ls(selection=True)
    try:
        first_selected = selected[0]
        second_selected = selected[1]
    except Exception:
        logger.warning("Must select 2 objects. First object aims at second object.")
    current_parent = cmds.listRelatives(second_selected, parent=True)
    # freeze transforms
    cmds.makeIdentity(first_selected, apply=True)

    cmds.parent(second_selected, first_selected)
    cmds.joint(
        first_selected,
        edit=True,
        orientJoint="xyz",  # "xzy",
        secondaryAxisOrient="yup",
        # autoOrientSecondaryAxis=True,
        zeroScaleOrient=True,
    )

    if current_parent:
        cmds.parent(second_selected, current_parent)
    else:
        cmds.parent(second_selected, world=True)

    # freeze transforms
    cmds.makeIdentity(first_selected, apply=True)

    cmds.select(clear=True)


def snap_alignment():
    """Snap first joint main axis to second joint.
    Aligns child joint first before using aim constraint.
    Maintains current joint positions.
    Defaults to "x" main axis.
    Steps: Move align child joint to main parent axis, then aim constrain,
    then move child back into position, then delete aim constraint and freeze transaforms.
    """
    selected = cmds.ls(selection=True)
    try:
        first_selected = selected[0]  # parent
        second_selected = selected[1]  # child
    except Exception:
        logger.warning("Must select 2 objects. First object aims at second object.")
    first_selected_parent = cmds.listRelatives(first_selected, parent=True)
    second_selected_parent = cmds.listRelatives(second_selected, parent=True)

    # query original position of child joint
    second_selected_position = cmds.xform(
        second_selected,
        query=True,
        worldSpace=True,
        translation=True,
    )

    # unparent
    for sel, prnt in zip(
        [first_selected, second_selected],
        [first_selected_parent, second_selected_parent],
        strict=False,
    ):
        if prnt:  # avoid warning
            cmds.parent(sel, world=True)
    # freeze transforms
    cmds.makeIdentity(first_selected, apply=True)
    cmds.makeIdentity(second_selected, apply=True)
    # parent child joint to parent joint
    cmds.parent(second_selected, first_selected)
    # zero out non-main axis translate values
    cmds.setAttr(f"{second_selected}.translateY", 0)
    cmds.setAttr(f"{second_selected}.translateZ", 0)
    # unparent child joint again
    cmds.parent(second_selected, world=True)

    # aim constrain. default values.
    # already aimed at, but add maintain offset to avoid axis moving
    aim_const = cmds.aimConstraint(
        second_selected,
        first_selected,
        aimVector=(1, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 1, 0),
        maintainOffset=True,
    )[0]
    # move child joint back into original position, with parent joint aiming
    cmds.xform(second_selected, worldSpace=True, translation=second_selected_position)
    # delete aim constraint
    cmds.delete(aim_const)
    # freeze transforms again
    cmds.makeIdentity(first_selected, apply=True)
    # reparent joints to original parents
    # both joints currently parented to the world
    for sel, prnt in zip(
        [first_selected, second_selected],
        [first_selected_parent, second_selected_parent],
        strict=False,
    ):
        if prnt:
            cmds.parent(sel, prnt)
