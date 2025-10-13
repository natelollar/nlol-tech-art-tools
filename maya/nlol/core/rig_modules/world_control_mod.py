from nlol.core.rig_modules.fk_control_mod import FkControlModule
from nlol.utilities.nlol_maya_logger import get_logger


class WorldControlModule(FkControlModule):
    """Build a basic fk control setup. Place at world origin
    with world aligned axis. Hide the control and
    lock its transform and visiblity attributes.
    """

    def __init__(
        self,
        rig_module_name: str,
    ):
        super().__init__(
            rig_module_name=rig_module_name,
            constraint=False,
            hide_and_lock=True,
        )

        self.logger = get_logger()

    def build(self) -> str:
        """Create the world control rig module.
        --------------------------------------------------

        Returns:
            Top control group.

        """
        super().build()

        return self.fkctrl_grp
