"""finalize_script.py"""

from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


def main():
    """Optional script to help finalize and cleanup rig."""
    # -----
    logger.info("Running finalize script...")

    # tmp constraints for rig mod example
    cmds.parentConstraint("pelvis_ctrl", "tailCloth_01_jnt", maintainOffset=True)
    cmds.scaleConstraint("pelvis_ctrl", "tailCloth_01_jnt")

    # show flexi surface joints
    cmds.setAttr("tailCloth_01_jnt.visibility", 1)

    # -----
    logger.info("Finalize script finished.")


if __name__ == "__main__":
    main()
