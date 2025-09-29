from maya.api import OpenMaya

from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def axis_facing_direction(object: str, world_space_direction: str) -> str:
    """Find which object axis most aims in the given world space direction.
    Useful for finding joint axis facing most rear in world space direction.

    Args:
        object: Object to get axis from. A joint for example.
        world_space_direction: The world space direction that defines
            which object axis is mostly facing it.
            Accepted args: "x", "y", "z", "-x", "-y", "-z"

    Returns:
        Most aligned axis. Same strings as "world_space_direction" arg.

    """
    axis_map = {
        "x": (1, 0, 0),
        "-x": (-1, 0, 0),
        "y": (0, 1, 0),
        "-y": (0, -1, 0),
        "z": (0, 0, 1),
        "-z": (0, 0, -1),
    }
    # world space target direction vector
    target_direction = OpenMaya.MVector(axis_map[world_space_direction.lower()])

    # object world matrix
    object_world_matrix = OpenMaya.MMatrix(
        [cmds.getAttr(f"{object}.worldMatrix")[i : i + 4] for i in range(0, 16, 4)],
    )

    # find most aligned axis with dot product
    max_dot_product = -1.0
    most_aligned_axis = None
    for axis in axis_map:
        # local axis to world space
        object_world_axis = (OpenMaya.MVector(axis_map[axis]) * object_world_matrix).normal()
        # measure alignment with target direction
        dot_product = object_world_axis * target_direction

        if dot_product > max_dot_product:
            max_dot_product = dot_product
            most_aligned_axis = axis

    return most_aligned_axis


def axis_facing_child(object_parent: str, object_child: str) -> str:
    """Get the parent object axis most facing its child object.
    Useful for getting the main axis facing down the chain for a joint.

    Args:
        object_parent: Parent object being analyzed to find the main axis
                facing the child object.
        object_child: Child object for the parent object to aim at
            to find the closest aiming axis.

    Returns:
        Object axis most facing its child object.

    """
    axis_map = {
        "x": (1, 0, 0),
        "-x": (-1, 0, 0),
        "y": (0, 1, 0),
        "-y": (0, -1, 0),
        "z": (0, 0, 1),
        "-z": (0, 0, -1),
    }
    parent_position = OpenMaya.MVector(cmds.getAttr(f"{object_parent}.worldMatrix")[12:15])
    child_position = OpenMaya.MVector(cmds.getAttr(f"{object_child}.worldMatrix")[12:15])

    # calculate direction from parent to child
    target_direction = (child_position - parent_position).normal()

    # parent objects world matrix
    parent_world_matrix = OpenMaya.MMatrix(
        [cmds.getAttr(f"{object_parent}.worldMatrix")[i : i + 4] for i in range(0, 16, 4)],
    )

    # find most aligned axis with dot product
    max_dot_product = -1.0
    most_aligned_axis = None
    for axis in axis_map:
        # local axis to world space
        object_world_axis = (OpenMaya.MVector(axis_map[axis]) * parent_world_matrix).normal()
        # measure alignment with target direction
        dot_product = object_world_axis * target_direction

        if dot_product > max_dot_product:
            max_dot_product = dot_product
            most_aligned_axis = axis

    return most_aligned_axis


def query_main_axis(
    parent_jnt: str,
    child_jnt: str,
    mod_name: str = "",
    mirr_side: str = "",
) -> str | None:
    """Get down the joint chain main axis.
    Query the main axis facing down the joint chain.
    """
    down_chain_axis = axis_facing_child(
        object_parent=parent_jnt,
        object_child=child_jnt,
    )
    if down_chain_axis not in ["x", "-x"]:
        error_msg = (
            f'Main axis pointing down the "{mod_name}{mirr_side}"'
            f' chain is "{down_chain_axis}".\n'
            'Main axis should be "x" or "-x".\n  '
            f'Rig module "{mod_name}{mirr_side}" did not build.',
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    return down_chain_axis


def axis_facing_child_snap(
    object_parent: str | None = None,
    object_child: str | None = None,
    translate_only: bool = False,
) -> str:
    """Snap child to the closest pointing parent axis. If the closest
    pointing parent axis is X, for instance, 0 out all values except
    X translate in relation to the parent object.

    Args:
        object_parent: Same as axis_facing_child().
        object_child: Same as axis_facing_child().
        translate_only: Snap only the child objects translate.
            Leave rotate alone.

    Returns:
        Same as axis_facing_child().

    """
    current_parent = cmds.listRelatives(object_child, parent=True)
    if not isinstance(current_parent, list) or current_parent[0] != object_parent:
        current_parent = None

    most_aligned_axis = axis_facing_child(object_parent, object_child)

    axis_string = "xyz"
    main_axis_string = most_aligned_axis.replace("-", "")
    non_max_axis_string = axis_string.replace(main_axis_string, "")

    # zero out values that are not the main axis
    if not current_parent:  # avoid parenting if already parent
        cmds.parent(object_child, object_parent)
    for axis in non_max_axis_string:
        cmds.setAttr(f"{object_child}.translate{axis.upper()}", 0)
    # zero out all rotation values for perfect max axis alignment
    if not translate_only:
        cmds.setAttr(f"{object_child}.rotate", 0, 0, 0)
        if cmds.objExists(f"{object_child}.jointOrient"):
            cmds.setAttr(f"{object_child}.jointOrient", 0, 0, 0)
        if cmds.objExists(f"{object_child}.rotateAxis"):
            cmds.setAttr(f"{object_child}.rotateAxis", 0, 0, 0)

    # if not originally parented, unparent from axis parent
    if not current_parent:
        cmds.parent(object_child, world=True)

    return most_aligned_axis


def snap_to_closest_axis(translate_only: bool = False) -> None:
    """Snap first selected objects to last selected.
    Use the last selected objects closest pointing parent
    axis to snap to.

    Args:
        translate_only: Same as axis_facing_child_snap().

    """
    selected = cmds.ls(selection=True)
    parent_object = selected[-1]
    children_objects = selected[:-1]
    for obj in children_objects:
        most_aligned_axis = axis_facing_child_snap(parent_object, obj, translate_only)
        print(f'snapped "{obj}" to "{most_aligned_axis}"')

    cmds.select(clear=True)
