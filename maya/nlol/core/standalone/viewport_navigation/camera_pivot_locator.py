from maya import cmds
from nlol.core.rig_components import create_nurbs_curves
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def create_curve_locator(small_locator: bool = False):
    """Create locator shaped curve to show camera tumble pivot location."""
    if not cmds.objExists("cam_pivot_loc"):
        if small_locator:
            cam_locator = create_nurbs_curves.CreateCurves(
                name="cam_pivot_loc",
                color_rgb=(0.2, 0.2, 0.2),
                size=0.05,
            ).locator_curve()
        else:
            cam_locator = create_nurbs_curves.CreateCurves(
                name="cam_pivot_loc",
                color_rgb=(0.9, 0.2, 0.0),
                line_width=3.0,
            ).locator_curve()

        cmds.connectAttr("perspShape.tumblePivot", f"{cam_locator}.translate")
    else:
        logger.info("Camera pivot locator already in scene.")


def delete_curve_locator():
    """Delete locator shaped curve."""
    if cmds.objExists("cam_pivot_loc"):
        cmds.delete("cam_pivot_loc")
        logger.info('Deleted "cam_pivot_loc".')
    else:
        logger.info('"cam_pivot_loc" does not exist.')
