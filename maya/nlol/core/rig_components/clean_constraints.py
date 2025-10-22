from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger


def parent_constr(
    targets: str | list[str],
    object: str,
    skip_tran: bool | None = None,
    skip_rot: bool | None = None,
    offset: bool | None = None,
    interp_type: int | None = None,
) -> str:
    """Parent constraint with clean name.
    Eliminates the need to name the constraint every time.
    Simpler arg set up.

    Args:
        targets: Parent objects.
        object: Child object.
        skip_tran: Whether to skip constraining translate.
        skip_rot: Whether to skip constraining rotate.
        offset: Whether to maintain offset when constraining.
        interp_type: "No Flip", "Average", "Shortest", "Longest", "Cache".

    Returns:
        The name of the constraint.

    """
    logger = get_logger()

    skip_tran = ("x", "y", "z") if skip_tran else ()
    skip_rot = ("x", "y", "z") if skip_rot else ()
    offset = True if offset else False
    name = f"{object}ParentConstraint"
    if skip_tran:
        name = f"{object}RotateConstraint"
    elif skip_rot:
        name = f"{object}TranslateConstraint"

    if skip_tran and skip_rot:
        error_msg = 'Cannot have both "skip_tran" and "skip_tran" for "parent_constr"'
        logger.error(error_msg)
        raise TypeError(error_msg)

    constraint = cmds.parentConstraint(
        targets,
        object,
        name=name,
        skipTranslate=skip_tran,
        skipRotate=skip_rot,
        maintainOffset=offset,
    )[0]

    if interp_type is not None:
        cmds.setAttr(f"{constraint}.interpType", interp_type)

    return constraint


def point_constr(
    targets: str | list[str],
    object: str,
    offset: bool | None = None,
) -> str:
    """Similar to parent_constr except uses pointConstraint."""
    offset = True if offset else False
    constraint = cmds.pointConstraint(
        targets,
        object,
        name=f"{object}PointConstraint",
        maintainOffset=offset,
    )[0]
    return constraint


def orient_constr(
    targets: str | list[str],
    object: str,
    offset: bool | None = None,
) -> str:
    """Similar to parent_constr except uses orientConstraint."""
    offset = True if offset else False
    constraint = cmds.orientConstraint(
        targets,
        object,
        name=f"{object}OrientConstraint",
        maintainOffset=offset,
    )[0]
    return constraint


def scale_constr(
    targets: str | list[str],
    object: str,
    offset: bool | None = None,
) -> str:
    """Similar to parent_constr except uses scaleConstraint."""
    offset = True if offset else False
    constraint = cmds.scaleConstraint(
        targets,
        object,
        name=f"{object}ScaleConstraint",
        maintainOffset=offset,
    )[0]
    return constraint


def aim_constr(
    targets: str | list[str],
    object: str,
    world_up_object: str,
    world_up_type: str = "object",
    aim_vector: str = "z",
    up_vector: str = "x",
    offset: bool | None = None,
) -> str:
    """Aim constraint with clean name.
    Eliminates the need to name the constraint every time.
    Simpler arg set up.

    Args:
        targets: Parent objects. Normally just one target parent.
        object: Child object.
        world_up_object: Object constraining up axis vector.
        aim_vector: Single string character of aiming axis vector. "x" or "y" or "z".
            Can also add negative sign to string. "-x" or "-y" or "-z".
        up_vector: Similar to aim_vector, only for up axis vector.
        offset: Whether to maintain offset when constraining.

    Returns:
        The name of the constraint.

    """
    axis_vectors = {
        "x": (1, 0, 0),
        "y": (0, 1, 0),
        "z": (0, 0, 1),
        "-x": (-1, 0, 0),
        "-y": (0, -1, 0),
        "-z": (0, 0, -1),
    }

    offset = True if offset else False
    constraint = cmds.aimConstraint(
        targets,
        object,
        worldUpObject=world_up_object,
        worldUpType=world_up_type,
        aimVector=axis_vectors[aim_vector.lower()],
        upVector=axis_vectors[up_vector.lower()],
        maintainOffset=offset,
        name=f"{object}AimConstraint",
    )[0]

    return constraint
