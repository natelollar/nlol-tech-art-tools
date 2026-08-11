"""finalize_script.py"""

from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


def main():
    """Optional script to help finalize and cleanup rig."""
    # -----
    logger.info("Running finalize script...")

    # ----- connect fk/ik blend to elbow aim toggle -----
    aim_reverse_nd = cmds.createNode(
            "reverse",
            name="elbowAimBlend_reverse",
        )
    cmds.connectAttr("armSwch_ctrl.fkIkBlend", f"{aim_reverse_nd}.inputX", force=True)
    cmds.connectAttr(f"{aim_reverse_nd}.outputX", "fkElbowParent_ctrl.aimToggle", force=True)

    # -----
    logger.info("Finalize script finished.")


if __name__ == "__main__":
    main()
