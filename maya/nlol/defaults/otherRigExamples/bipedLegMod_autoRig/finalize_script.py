"""finalize_script.py"""

from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


def main():
    """Optional script to help finalize and cleanup rig."""
    # -----
    logger.info("Running finalize script...")

    # set default attributes
    for side in ["left", "right"]:
        cmds.setAttr(f"ikAnkleLeg_{side}_ctrl.soft", 0.035)

    # -----
    logger.info("Finalize script finished.")


if __name__ == "__main__":
    main()
