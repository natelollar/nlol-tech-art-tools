"""finalize_script.py"""

from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


def main():
    """Optional script to help finalize and cleanup rig."""
    # -----
    logger.info("Running finalize script...")

    # neck to fk
    cmds.setAttr("neckSwch_ctrl.fkIkBlend", 1)

    # -----
    logger.info("Finalize script finished.")


if __name__ == "__main__":
    main()
