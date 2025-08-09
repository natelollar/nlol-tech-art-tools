from maya import cmds
from maya.api import OpenMaya


def apply_hinge_vector(
    limb_joints: list | tuple,
    control_object: str,
    control_object_distance: str,
) -> None:
    """Find and apply correct limb hinge vector to a control object based on three joints.
    Useful for finding and applying initial pole vector control transformations
    when creating an ik limb and need the pole vector control rotation perfectly aligned
    to the triangular plane between the three joints.
    Used on leg or arm limbs, for example.

    Args:
        limb_joints: Three joints. Start, middle hinge, and end joints.
        control_object: The control curve or control group
            to apply middle hinge vector transforms to.
        control_object_distance: The distance away from the middle hinge joint
            to place the control object at. An offset from the hinge joint.

    """
    # length of limb in translate x
    limb_length = cmds.getAttr(f"{limb_joints[1]}.translateX") + cmds.getAttr(
        f"{limb_joints[2]}.translateX",
    )
    # length of limb upperhalf in translate x
    limb_length_upperhalf = cmds.getAttr(f"{limb_joints[1]}.translateX")
    # divide sum of limb_length by limb_length_upperhalf for better mid value, around 2
    limb_length_mid_value = limb_length / limb_length_upperhalf

    # vector positions of start, middle, and end joints of limb
    start_joint_vector = OpenMaya.MVector(
        cmds.xform(limb_joints[0], query=True, rotatePivot=True, worldSpace=True),
    )
    mid_joint_vector = OpenMaya.MVector(
        cmds.xform(limb_joints[1], query=True, rotatePivot=True, worldSpace=True),
    )
    end_joint_vector = OpenMaya.MVector(
        cmds.xform(limb_joints[2], query=True, rotatePivot=True, worldSpace=True),
    )

    # find vector of pole vector hinge
    start_to_end_vector = end_joint_vector - start_joint_vector
    start_to_end_mid = start_to_end_vector / limb_length_mid_value
    mid_vector = start_joint_vector + start_to_end_mid
    mid_vector_to_mid_joint_vector = mid_joint_vector - mid_vector
    mid_vector_to_mid_joint_vector_scaled = (
        mid_vector_to_mid_joint_vector * control_object_distance
    )  # control distance from hinge joint
    mid_point_to_knee_point = mid_vector + mid_vector_to_mid_joint_vector_scaled

    # final vector. avoids knee changing position on creation.
    cmds.xform(control_object, translation=mid_point_to_knee_point)

    # point the control group at the middle hinge joint
    myAimConst = cmds.aimConstraint(
        limb_joints[1],
        control_object,
        offset=(0, 0, 0),
        weight=1,
        aimVector=(0, 0, -1),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 1, 0),
    )
    cmds.delete(myAimConst)
