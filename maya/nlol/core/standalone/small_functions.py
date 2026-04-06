import math

import shiboken6
from PySide6.QtWidgets import QApplication

from maya import cmds
from nlol.core.rig_tools import show_attributes
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def select_all_ctrls(rig_group_string: str = "_rigGrp") -> list[str]:
    """Select all ctrl curves underneath rig, selected,
    or specified group. Uses string "ctrl" to narrow result.

    Args:
        rig_group_string: Either main rig group name or
            string within main rig group identifying it.

    Returns:
        All rig ctrls or selected and their descendents.

    """
    selection = cmds.ls(selection=True)
    if selection:
        all_ctrls = cmds.listRelatives(selection, allDescendents=True) + selection
    else:
        top_nodes = cmds.ls(assemblies=True)
        rig_grps = [node for node in top_nodes if rig_group_string in node]
        all_ctrls = cmds.listRelatives(rig_grps, allDescendents=True)

    all_ctrls = [
        ctrl
        for ctrl in all_ctrls
        if cmds.listRelatives(ctrl, shapes=True, type="nurbsCurve") and "ctrl" in ctrl.lower()
    ]

    cmds.select(all_ctrls)

    return all_ctrls


def reset_all_ctrls(all_keyable: bool = False) -> None:
    """Reset all rig ctrls or selected ctrls and their descendents.
    This resets ctrl transforms translate, rotate, scale, and other custom attributes.
    Resets to queryable default values.

    Args:
        all_keyable: Choose to reset all queryable keyable attributes instead of just
        the smaller list of specified attributes. For instance, resets parent spaces too.

    """
    all_ctrls = select_all_ctrls()

    standard_attrs = (
        "translateX",
        "translateY",
        "translateZ",
        "rotateX",
        "rotateY",
        "rotateZ",
        "scaleX",
        "scaleY",
        "scaleZ",
    )
    custom_attrs = (
        "toeWiggle",
        "toeSpin",
        "lean",
        "tilt",
        "roll",
        "softFalloff",
        "soft",
        "startTwistBlend",
        "stretch",
    )
    basic_attrs = standard_attrs + custom_attrs

    for ctrl in all_ctrls:
        if all_keyable:
            attrs = cmds.listAttr(ctrl, keyable=True) or []
        else:
            attrs = basic_attrs

        for attr in attrs:
            if attr not in standard_attrs:
                if not cmds.attributeQuery(attr, node=ctrl, exists=True):
                    continue
            default_value = cmds.attributeQuery(attr, node=ctrl, listDefault=True)
            if default_value and cmds.getAttr(f"{ctrl}.{attr}", settable=True):
                cmds.setAttr(f"{ctrl}.{attr}", *default_value)


def select_shapes():
    selection = cmds.ls(selection=True)

    selection_shapes = []
    for obj in selection:
        shps = cmds.listRelatives(obj, shapes=True)
        selection_shapes.extend(shps)

    cmds.select(selection_shapes)


def select_shapes_show_attrs():
    """Select curve shapes and show useful curve shape attributes."""
    selection = cmds.ls(selection=True)

    selection_shapes = []
    for obj in selection:
        shps = cmds.listRelatives(obj, shapes=True)
        selection_shapes.extend(shps)

    cmds.select(selection_shapes)
    show_attributes.ShowAttributes().show_curve_attrs()


def get_selection_type():
    """Get Maya object type for selected."""
    selection = cmds.ls(selection=True)
    for obj in selection:
        selection_type = cmds.objectType(obj)
        print(obj, selection_type)


def rename_joints():
    new_name = "exampleName"
    selection = cmds.ls(selection=True)
    for i, jnt in enumerate(selection, 1):
        cmds.rename(jnt, f"{new_name}_{i:02d}_jnt")


def rename_skincluster():
    """Rename skin cluster based on selected nLol mesh name.
    Select skinned objects in scene and quickly rename their skin_clusters.
    Selected object name should be "<name>_<direction>_<id>_<type>".
    """
    mesh_selection = cmds.ls(selection=True)

    for i, mesh in enumerate(mesh_selection, 1):
        mesh_type_name = mesh.split("_")[-1]
        skincluster_name = mesh.replace(mesh_type_name, "skinCluster")

        mesh_history = cmds.listHistory(mesh)
        skincluster = cmds.ls(mesh_history, type="skinCluster")[0]

        cmds.rename(skincluster, skincluster_name)


def renumber_joints():
    """Rename number id's for nLol naming convention.
    For selected number chain, will rename numerically starting from one.
    Useful if removing joint from chain and need to renumber joints.
    """
    selection = cmds.ls(selection=True)
    for i, obj in enumerate(selection, 1):
        name_id = obj.split("_")[-2]
        name_numbers = name_id[-2:]
        new_name = obj.replace(name_numbers, f"{i:02d}")
        cmds.rename(obj, new_name)


def print_selected_list(string_format: bool = False):
    """Print list of selected Maya objects as python formatted list
    or as string formatted list.
    """
    selection = cmds.ls(selection=True)
    obj_list = []
    if string_format:
        obj_list = ", ".join(selection)
        print(f'\n"{obj_list}"')
    else:
        for obj in selection:
            obj_list.append(obj)
        print(f"\n{obj_list}")


def query_skinned_joints():
    """Select skinned joints from first selected mesh object."""
    first_select = cmds.ls(selection=True)[0]
    skinned_joint = cmds.skinCluster(first_select, query=True, influence=True)
    logger.info(f"Joints skinned to: {first_select}\n{skinned_joint}")
    cmds.select(skinned_joint)


def center_all_windows():
    """Move Maya windows to center of primary screen.
    Helpful after changing monitors and losing windows.
    """
    for widget in QApplication.allWidgets():
        if shiboken6.isValid(widget) and widget.isWindow() and not widget.isHidden():
            widget.move(
                QApplication.primaryScreen().availableGeometry().center() - widget.rect().center(),
            )
            widget.showNormal()  # Restores the widget after it has been maximized or minimized.


def distance_between(object_1: str, object_2: str, use_bbox: bool = False) -> float:
    """Calculate distance between to object pivots in 3D space. Optionally,
    use bounding box center to calculate distance between.

    Args:
        object_1: Starting object for distance measurement.
        object_2: Ending object for distance measurement.
        use_bbox: Use bounding box center point instead of rotate pivot for start and end points.

    Returns:
        Distance between the two objects.

    """
    if use_bbox:
        # xmin, ymin, zmin, xmax, ymax, zmax
        bbox_1 = cmds.exactWorldBoundingBox(object_1)
        bbox_2 = cmds.exactWorldBoundingBox(object_2)

        pos_1 = (
            (bbox_1[0] + bbox_1[3]) / 2,
            (bbox_1[1] + bbox_1[4]) / 2,
            (bbox_1[2] + bbox_1[5]) / 2,
        )
        pos_2 = (
            (bbox_2[0] + bbox_2[3]) / 2,
            (bbox_2[1] + bbox_2[4]) / 2,
            (bbox_2[2] + bbox_2[5]) / 2,
        )
    else:
        pos_1 = cmds.xform(object_1, query=True, worldSpace=True, rotatePivot=True)
        pos_2 = cmds.xform(object_2, query=True, worldSpace=True, rotatePivot=True)

    # euclidean distance formula, distance formula, pythagorean distance
    distance = math.sqrt(
        (pos_2[0] - pos_1[0]) ** 2 + (pos_2[1] - pos_1[1]) ** 2 + (pos_2[2] - pos_1[2]) ** 2,
    )

    return distance


def hide_shape_transforms(shape_types: str | list[str]) -> None:
    """Hide transform of shape type."""
    if isinstance(shape_types, str):
        shape_types = [shape_types]

    for shape_type in shape_types:
        shapes = cmds.ls(type=shape_type)
        transforms = [cmds.listRelatives(shp, parent=True)[0] for shp in shapes]
        for transform in transforms:
            cmds.setAttr(f"{transform}.visibility", 0)


def hide_rig_clutter():
    """Hide rig clutter after showing entire hierarchy."""
    hide_shape_transforms(["distanceDimShape"])


def multi_parent_const():
    """Parent multiple objects to a single object.
    Useful for constraining multiple ctrls to a single locator
    for a temporary pivot. Constrain to last selected object.
    """
    selected = cmds.ls(sl=True)
    for obj in selected:
        if obj != selected[-1]:
            cmds.parentConstraint(selected[-1], obj, maintainOffset=True, weight=1.0)
