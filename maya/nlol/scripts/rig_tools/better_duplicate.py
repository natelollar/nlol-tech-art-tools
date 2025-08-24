from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger


def duplicate_curve(curve: str) -> str:
    """Duplicate wire color and line width too.

    Args:
        Curve to duplicate.

    Returns:
        New curve name.

    """
    logger = get_logger()

    dup_curve = cmds.duplicate(curve, name=f"{curve}_duplicate", renameChildren=True)[0]
    curve_shapes = cmds.listRelatives(curve, shapes=True)
    dup_curve_shapes = cmds.listRelatives(dup_curve, shapes=True)

    for crv_shp, dup_crv_shp in zip(curve_shapes, dup_curve_shapes, strict=False):
        use_object_color = cmds.getAttr(f"{crv_shp}.useObjectColor")
        object_color = cmds.getAttr(f"{crv_shp}.objectColor")
        wire_color_rgb = cmds.getAttr(f"{crv_shp}.wireColorRGB")[0]
        line_width = cmds.getAttr(f"{crv_shp}.lineWidth")
        if isinstance(use_object_color, list):
            error_msg = (
                f'"use_object_color" is list. Likely more than one curve shape named "{crv_shp}".'
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        use_object_color = cmds.setAttr(f"{dup_crv_shp}.useObjectColor", use_object_color)
        object_color = cmds.setAttr(f"{dup_crv_shp}.objectColor", object_color)
        wire_color_rgb = cmds.setAttr(f"{dup_crv_shp}.wireColorRGB", *wire_color_rgb)
        line_width = cmds.setAttr(f"{dup_crv_shp}.lineWidth", line_width)

    return dup_curve
