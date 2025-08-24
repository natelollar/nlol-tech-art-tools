from importlib import reload

from maya import cmds
from nlol.scripts.rig_tools import better_duplicate
from nlol.utilities.nlol_maya_logger import get_logger

reload(better_duplicate)

duplicate_curve = better_duplicate.duplicate_curve


def replace_crv_shps():
    """Replace last selected curves with first selected curve.
    This will replace the curve shapes underneath each curve transform.
    Useful for updating rig control shapes.
    """
    logger = get_logger()

    selection = cmds.ls(selection=True)
    new_curve = selection[0]

    cmds.undoInfo(openChunk=True)
    try:
        for current_crv in selection[1:]:
            new_curve_duplicate = duplicate_curve(new_curve)
            cmds.matchTransform(new_curve_duplicate, current_crv)

            current_crv_shapes = cmds.listRelatives(current_crv, shapes=True)
            new_curve_dup_shapes = cmds.listRelatives(new_curve_duplicate, shapes=True)

            cmds.delete(current_crv_shapes)

            cmds.parent(new_curve_dup_shapes, current_crv, relative=True, shape=True)

            parented_shapes = cmds.listRelatives(current_crv, shapes=True)
            for new_shp in parented_shapes:
                new_shp = cmds.rename(new_shp, f"{current_crv}Shape")

            cmds.delete(new_curve_duplicate)

    except Exception:
        logger.exception("An error occured replacing the curves.")
    finally:
        cmds.undoInfo(closeChunk=True)
        cmds.select(clear=True)
