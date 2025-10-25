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
