"""Smaller functions helpful for rigging."""

import random as rd

from maya import cmds
from nlol.scripts.rig_tools.show_attributes import ShowAttributes


def axis_locator(
    objects: str | list[str] | None = None,
    locator_name: str | None = None,
    local_scale: tuple[float, float, float] = (10, 10, 10),
    color_rgb: tuple[float, float, float] | None = None,
) -> tuple[list[str], list[str]]:
    """Create locator at selected joints for manual axis alignment.
    Parent locator under joint.

    Args:
        objects: Joints or objects to parent locators under.
        local_scale: Optional base name for the locators.
        local_scale: Visuale scale in viewport.
        color_rgb: Tuple with 0-1.0 "r, g, b" values.

    Returns:
        List of locator names and list of objects parented to.

    """
    if objects:
        objects = [objects] if isinstance(objects, str) else objects
    else:
        objects = cmds.ls(sl=True)

    locator_list = []
    original_locator_name = locator_name
    for i, obj in enumerate(objects, 1):
        r, g, b = (
            color_rgb if color_rgb else (rd.uniform(0, 1.0), rd.uniform(0, 1.0), rd.uniform(0, 1.0))
        )
        if not original_locator_name:
            current_locator_name = "localAxis_" + obj
        elif len(objects) > 1:
            current_locator_name = f"{original_locator_name}{i}"
        else:
            current_locator_name = original_locator_name

        locator = cmds.spaceLocator(name=current_locator_name)[0]
        locator_shape = cmds.listRelatives(locator, shapes=True)[0]
        cmds.setAttr(f"{locator_shape}.localScale", local_scale[0], local_scale[1], local_scale[2])
        cmds.setAttr(f"{locator_shape}.useObjectColor", 2)
        cmds.setAttr(f"{locator_shape}.wireColorRGB", r, g, b)
        ShowAttributes(target_objects=locator_shape).show_curve_attrs()

        cmds.parent(locator, obj, relative=True)

        locator_list.append(locator)

    return locator_list, objects


def locator_snap_parent(
    objects: str | list[str] | None = None,
    locator_name: str | None = None,
    local_scale: tuple[float, float, float] = (10, 10, 10),
    color_rgb: tuple[float, float, float] | None = None,
) -> list[str]:
    """Snap locator to object, then apply parent and scale constraint.
    Useful if need to parent to joint without directly parenting under joint.
    If not objects, uses default selection.

    Args:
        Same as axis_locator().

    Returns:
        List of locator names.

    """
    locator_list, objects = axis_locator(objects, locator_name, local_scale, color_rgb)

    for loc, obj in zip(locator_list, objects, strict=False):
        cmds.parent(loc, world=True)
        cmds.parentConstraint(obj, loc)
        cmds.scaleConstraint(obj, loc)

    return locator_list


def locator_snap(
    objects: str | list[str] | None = None,
    locator_name: str | None = None,
    local_scale: tuple[float, float, float] = (10, 10, 10),
    color_rgb: tuple[float, float, float] | None = None,
    translate_only: bool = False,
) -> list[str]:
    """Similar to axis_locator().
    Snap locator to object, but leave it unparented.

    Args:
        Same as axis_locator().

    Returns:
        List of locator names.

    """
    locator_list, objects = axis_locator(objects, locator_name, local_scale, color_rgb)

    for loc in locator_list:
        cmds.parent(loc, world=True) #unparent
        if translate_only:
            cmds.setAttr(f"{loc}.rotate", 0, 0, 0)

    return locator_list


def axis_locator_del():
    """Delete locators used for manual axis alignment."""
    loc_shapes = cmds.ls("localAxis_*", type="locator")
    loc_transforms = cmds.listRelatives(loc_shapes, parent=1)

    for loc in loc_transforms:
        cmds.delete(loc)
