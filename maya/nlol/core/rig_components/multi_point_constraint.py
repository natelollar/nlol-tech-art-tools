from maya import cmds
from maya.api import OpenMaya


def multi_point_const(
    parent_objects: list[str],
    child_object: str,
    index_attribute: str,
) -> str:
    """Set up point constraint for parent space blending.
    This version of a the point constraint has proper parent object offsets.
    Also, sets up nodes to switch the offset based on an index of parent objects.

    Args:
        parent_objects: Targets for the point constrained object.
        child_control: Object being constrained. Often parent switch group or control.
        index_attribute: Control attribute that will switch offset values index.

    Returns:
        Point constraint name.

    """
    point_const = cmds.pointConstraint(
        parent_objects,
        child_object,
        name=f"{child_object}PointConstraint",
        weight=0,  # need 0 weight to prevent initial movement
    )[0]

    choice_nd = cmds.shadingNode("choice", asUtility=True, name=f"{child_object}Choice")

    for i, prnt_obj in enumerate(parent_objects):
        id_base_name = child_object.replace("_", f"_{i:02d}_", 2)
        id_base_name = id_base_name.replace(f"_{i:02d}_", "_", 1)

        colorconstant_nd = cmds.shadingNode(
            "colorConstant",
            asUtility=True,
            name=f"{id_base_name}ColorConstant",
        )
        pos_offset = local_position_offset(prnt_obj, child_object)
        cmds.setAttr(f"{colorconstant_nd}.inColor", *pos_offset)
        cmds.connectAttr(f"{colorconstant_nd}.outColor", f"{choice_nd}.input[{i}]")

    cmds.connectAttr(index_attribute, f"{choice_nd}.selector")
    cmds.connectAttr(f"{choice_nd}.output", f"{point_const}.offset")

    return point_const


def local_position_offset(parent_object: str, child_object: str):
    """Get child object position offset from parent object, from child object space."""
    child_obj_matrix = cmds.xform(child_object, query=True, matrix=True, worldSpace=True)
    child_obj_matrix_openmaya = OpenMaya.MMatrix(child_obj_matrix)
    # get child objects inverse matrix
    child_obj_matrix_inv = child_obj_matrix_openmaya.inverse()

    # parent object position
    parent_obj_pos = cmds.xform(parent_object, query=True, translation=True, worldSpace=True)
    parent_obj_pos.append(1)  # add 4th value to multiply by matrix
    parent_obj_pos_om = OpenMaya.MPoint(parent_obj_pos)

    # parent object's position in child objects local space
    parent_obj_pos_local = parent_obj_pos_om * child_obj_matrix_inv
    # invert distance
    # how far child is from parent, instead parent from child
    parent_obj_offset = [-parent_obj_pos_local.x, -parent_obj_pos_local.y, -parent_obj_pos_local.z]

    return [parent_obj_offset[0], parent_obj_offset[1], parent_obj_offset[2]]
