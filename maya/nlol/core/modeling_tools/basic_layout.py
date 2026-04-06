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
