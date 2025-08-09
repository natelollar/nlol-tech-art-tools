from importlib import reload

from maya import cmds
from nlol.scripts.rig_tools import show_attributes

reload(show_attributes)
ShowAttributes = show_attributes.ShowAttributes


def single_joint(
    name: str = "example_joint",
    radius: float = 1.0,
    color_rgb: list | tuple = (1.0, 0.4, 0.0),
    scale_compensate: bool = True,
    parent_snap: str | None = None,
    axis_parent_snap: str | None = None,
    position: tuple = (0, 0, 0),
) -> str:
    """Create single joint.

    Args:
        name: Joint name.
        radius: Joint radius (viewport size).
        color_rgb: RGB color values.
        scale_compensate: If true, parent scaling will not affect joint ".scale".  
            True by default in Maya.
        parent_snap: Object to snap the created joint to.  Does not parent under.
        axis_parent_snap: Same as align_to_object_axis().

    """
    # create joint
    cmds.select(clear=True)
    joint = cmds.joint(name=name, position=position)

    # size and color
    cmds.setAttr(".radius", radius)
    cmds.setAttr(".useObjectColor", 2)
    cmds.setAttr(".wireColorRGB", color_rgb[0], color_rgb[1], color_rgb[2])

    # scale compensate
    cmds.setAttr(".segmentScaleCompensate", scale_compensate)

    # show useful joint attributes
    cmds.select(joint)
    ShowAttributes().show_joint_attrs()

    # snap joint to parent object
    if parent_snap:
        cmds.parent(joint, parent_snap, relative=True)
        cmds.parent(joint, world=True)  # unparent

    # snap to parent objects closest pointing axis
    if axis_parent_snap:
        align_to_object_axis(joint, axis_parent_snap)

    return joint


def align_to_object_axis(child_object: str, axis_parent_snap: str) -> None:
    """Snap object to temp parents closest pointing axis, aka, main/ max axis.
    Parent will be temporary unless the child object is already parented to it.
    Useful for aligning joint chains perfectly.

    Args:
        child_object: Child object that will snap to temp parents closet axis.
            Useful for snapping to down the chain axis of a joint chain.
        axis_parent_snap: Parent to this object, then zero out all values except
            highest max translate. Then unparent. This aligns the child object to
            parent objects closest pointing axis. Does remain parented,
            unless already parented.

    """
    current_parent = cmds.listRelatives(child_object, parent=True)

    # snap to this parent objects main axis
    # temp parent unless already parented to
    cmds.parent(child_object, axis_parent_snap)
    # get highest translate value while parented
    joint_translate_values = cmds.getAttr(f"{child_object}.translate")[0]
    max_translate_axis_index = joint_translate_values.index(
        max(joint_translate_values, key=abs),
    )
    axis_string = "XYZ"
    max_axis_string = axis_string[max_translate_axis_index]
    non_max_axis_string = axis_string.replace(max_axis_string, "")

    # zero out values for axis' that are not the highest
    for axis in non_max_axis_string:
        cmds.setAttr(f"{child_object}.translate{axis}", 0)
    # zero out all rotation values for perfect max axis alignment
    cmds.setAttr(f"{child_object}.rotate", 0, 0, 0)
    cmds.setAttr(f"{child_object}.jointOrient", 0, 0, 0)
    cmds.setAttr(f"{child_object}.rotateAxis", 0, 0, 0)

    # if not originally parented to it, unparent from axis parent
    if not isinstance(current_parent, list) or current_parent[0] != axis_parent_snap:
        cmds.parent(child_object, world=True)
