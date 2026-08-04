import math

from maya import cmds
from nlol.utilities import nlol_maya_logger

logger = nlol_maya_logger.get_logger()


def check_prntswchgrp_scale() -> None:
    """Verify parent switch group default scale values."""
    parent_switch_grps = cmds.ls(
        "*PrntSwchGrp",
        "*:*PrntSwchGrp",
        "*:*:*PrntSwchGrp",
        type="transform",
        long=True,
    )
    for grp in parent_switch_grps:
        scale_attrs = list(cmds.getAttr(f"{grp}.scale")[0])
        default_scale_attrs = cmds.attributeQuery("scale", node=grp, listDefault=True)
        for scale_attr, default_scale_attr in zip(scale_attrs, default_scale_attrs, strict=False):
            if not math.isclose(scale_attr, default_scale_attr, abs_tol=0.00001):
                short_grp_name = cmds.ls(grp, shortNames=True)[0]
                msg = f"{short_grp_name}.scale = {scale_attrs}"
                logger.info(msg)
                break


def check_scene_objs_scale() -> None:
    """Verify scene objects default scale values."""
    scene_objs = cmds.ls(
        long=True,
    )
    for obj in scene_objs:
        if cmds.objExists(f"{obj}.scale"):
            scale_attrs = list(cmds.getAttr(f"{obj}.scale")[0])
            default_scale_attrs = cmds.attributeQuery("scale", node=obj, listDefault=True)
            for scale_attr, default_scale_attr in zip(
                scale_attrs,
                default_scale_attrs,
                strict=False,
            ):
                if not math.isclose(scale_attr, default_scale_attr, abs_tol=0.00001):
                    short_obj_name = cmds.ls(obj, shortNames=True)[0]
                    msg = f"{short_obj_name}.scale = {scale_attrs}"
                    logger.info(msg)
                    break


def verify_data() -> None:
    """Double check various values on rig objects."""
    # -----
    logger.info("Checking data...")

    # -----
    check_prntswchgrp_scale()
    # check_scene_objs_scale()

    # -----
    logger.info("Data checked.")


if __name__ == "__main__":
    verify_data()
