from maya.api import OpenMaya as om
from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


def get_closest_vert_from_list(source_vert: str, target_verts: list) -> tuple[str, list]:
    """Args:
        source_vert: Main vert to compare target verts to.
        target_vert: List of verts to search through.

    Returns:
        Closest vert to source vert and closest vert "xyz" position.

    """
    source_vert_pos = cmds.xform(source_vert, query=True, worldSpace=True, translation=True)
    source_point = om.MPoint(
        float(source_vert_pos[0]),
        float(source_vert_pos[1]),
        float(source_vert_pos[2]),
    )  # (x, y, z, w)

    closest_vert = None
    closest_vert_pos = None
    min_distance = float("inf")
    for target_vert in target_verts:
        target_vert_pos = cmds.xform(target_vert, query=True, worldSpace=True, translation=True)
        target_point = om.MPoint(
            float(target_vert_pos[0]),
            float(target_vert_pos[1]),
            float(target_vert_pos[2]),
        )
        distance = source_point.distanceTo(target_point)
        if distance < min_distance:
            min_distance = distance
            closest_vert = target_vert
            closest_vert_pos = target_vert_pos

    return closest_vert, closest_vert_pos


def vert_snapper(guess_source_verts: bool = True) -> None:
    """Snap first selected object vertices to closest vertices on
    second selected object. Can select mesh objects or vertices.
    Two mesh objects required.

    Args:
        guess_source_verts: Find closest target verts and limit to number of target verts.
        Useful when not selecting specific verts and just select source and target meshes.

    """
    selected = cmds.ls(selection=True)

    # get selected objects. keep selection order.
    objects = []
    for obj in selected:
        if ".vtx" in obj:
            obj = obj.split(".")[0]
        elif cmds.objectType(obj) == "transform":
            shapes = cmds.listRelatives(obj, shapes=True)
            if cmds.objectType(shapes[0]) == "mesh":
                obj = obj
        objects.append(obj)
    objects = list(dict.fromkeys(objects))  # remove dup

    # first and second selected variables
    first_selected = objects[0]
    second_selected = objects[1]

    # get verts for first and second selected
    vert_dict = {}
    for sel in [first_selected, second_selected]:
        vert_objs = []
        for obj in selected:
            if sel in obj:
                vert_objs.append(obj)
        vert_dict[sel] = vert_objs

    # get list of verts for each or just object name
    first_sel_verts = vert_dict[first_selected]
    if len(first_sel_verts) == 1 and ".vtx" not in first_sel_verts[0]:
        first_sel_verts = [f"{first_sel_verts[0]}.vtx[:]"]
    first_sel_verts = cmds.ls(first_sel_verts, flatten=True)

    second_sel_verts = vert_dict[second_selected]
    if len(second_sel_verts) == 1 and ".vtx" not in second_sel_verts[0]:
        second_sel_verts = [f"{second_sel_verts[0]}.vtx[:]"]
    second_sel_verts = cmds.ls(second_sel_verts, flatten=True)

    # find closest target verts and limit to number of target verts
    # if more target verts, no reason to limit source by target
    if guess_source_verts and not (len(second_sel_verts) > len(first_sel_verts)):
        closest_source_verts = []
        for vert in second_sel_verts:
            closest_vert, _ = get_closest_vert_from_list(vert, first_sel_verts)
            closest_source_verts.append(closest_vert)
        first_sel_verts = closest_source_verts

    logger.debug(first_sel_verts)
    logger.debug(second_sel_verts)
    logger.debug(len(first_sel_verts))
    logger.debug(len(second_sel_verts))

    # snap verts
    for vert in first_sel_verts:
        _, closest_vert_pos = get_closest_vert_from_list(vert, second_sel_verts)
        cmds.xform(vert, worldSpace=True, translation=closest_vert_pos)
