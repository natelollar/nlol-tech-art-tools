from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


class SpaceSwitchMatch:
    """Switch rig ctrl parent spaces while maintaining world space transforms."""

    def run(self, ctrl_parentspace_data: list[dict[str, dict[str, int]]]):
        """Run space switch matching on multiple ctrls.

        Args:
            ctrl_parentspace_data: List of ctrls and new parent spaces to switch to.

        """
        # rig_ctrl = "ikAnkleFrontLeg_left_ctrl"
        # new_parentspaces = {"parentSpaces": 3}
        for rig_ctrl, new_parentspaces in ctrl_parentspace_data.items():
            self.switch_match(rig_ctrl, new_parentspaces)

    def switch_match(self, rig_ctrl: str, new_parentspaces: dict[str, int]):
        """Switch parent spaces while keeping same world space transforms.
        Allows switching a ctrls parent space without moving it.

        Args:
            rig_ctrl: Rig control to switch parent spaces for.
            new_parentspaces: Dictionary with parent space attribute names
                and parent space index values.

        """
        # match locator to ctrl transforms
        tmp_locator = cmds.spaceLocator(name="spaceSwitchTemp_loc")[0]
        cmds.matchTransform(tmp_locator, rig_ctrl)

        # update parent spaces
        for parentspace, parentspace_value in new_parentspaces.items():
            if cmds.objExists(f"{rig_ctrl}.{parentspace}"):
                cmds.setAttr(f"{rig_ctrl}.{parentspace}", parentspace_value)
            else:
                msg = f"Parent space doet not exist: {rig_ctrl}.{parentspace}"
                logger.info(msg)

        # match ctrl to original transforms
        cmds.matchTransform(rig_ctrl, tmp_locator)
        cmds.delete(tmp_locator)
