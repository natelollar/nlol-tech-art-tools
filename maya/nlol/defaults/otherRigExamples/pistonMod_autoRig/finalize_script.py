"""finalize_script.py"""

from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


def main():
    """Optional script to help finalize and cleanup rig."""
    # -----
    logger.info("Running finalize script...")

    base_ctrl = "hydroPistonBase_ctrl"
    top_geo_ctrl = "exampleTop_ctrlGeo"
    bot_geo_ctrl = "exampleBot_ctrlGeo"

    if cmds.objExists(top_geo_ctrl):
        cmds.parent(top_geo_ctrl, base_ctrl)  # parent example geo to base ctrl
        cmds.editDisplayLayerMembers("defaultLayer", top_geo_ctrl)  # remove from layer
    if cmds.objExists(bot_geo_ctrl):
        cmds.parent(bot_geo_ctrl, base_ctrl)
        cmds.editDisplayLayerMembers("defaultLayer", bot_geo_ctrl)

    # -----
    logger.info("Finalize script finished.")


if __name__ == "__main__":
    main()
