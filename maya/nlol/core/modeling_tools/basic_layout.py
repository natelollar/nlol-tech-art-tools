import math

from maya import cmds


def grid_layout(spread: float = 100) -> None:
    """Arrange selected objects in a grid pattern.

    Args:
        spread: How far apart each object.

    """
    obj_sel = cmds.ls(sl=True)
    if not obj_sel:
        cmds.warning("No objects selected.")
        return

    num_obj = len(obj_sel)
    grid_size = math.ceil(num_obj**0.5)

    grid_pattern = [(x * spread, z * spread) for x in range(grid_size) for z in range(grid_size)]

    for obj, (x, z) in zip(obj_sel, grid_pattern, strict=False):
        cmds.setAttr(f"{obj}.translate", x, 0, z)


def duplicate_replace(
    delete_tartget_objs: bool = True,
    instance_target_obs: bool = True,
    source_as_first_new_target: bool = True,
) -> None:
    """Replace selected objects with first selected.
    Maintain target object tranforms.

    Args:
        delete_tartget_objs: Delete target objects when replacing with source objects.
        instance_target_obs: Instance instead of duplicate source object.
        source_as_first_new_target: Use source object as first object to
            replace first target object, instead of duplicating.

    """
    selected = cmds.ls(selection=True)
    source_obj = selected[0]
    target_objs = selected[1:]

    for i, obj in enumerate(target_objs):
        if source_as_first_new_target and i == 0:
            new_source_obj = source_obj
        elif instance_target_obs:
            new_source_obj = cmds.instance(source_obj)
        else:
            new_source_obj = cmds.duplicate(source_obj)
        cmds.matchTransform(new_source_obj, obj)
        if delete_tartget_objs:
            cmds.delete(obj)
