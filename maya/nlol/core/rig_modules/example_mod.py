from maya import cmds
from nlol.core.general_utils import cap
from nlol.utilities.nlol_maya_logger import get_logger
from nlol.utilities.nlol_maya_registry import get_registry

logger = get_logger()
registry = get_registry()


class ExampleModule:
    """Create rig module..."""

    def __init__(self, rig_module_name: str, mirror_direction: str, main_joints: list[str]) -> None:
        """Initialize class.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: Extra string describing mirror side. Ex. "left", "right".
            main_joints: The main skinned joints.

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints

        # -----
        msg = "Note message info."
        logger.info(msg)

        # -----
        test_obj = ["01", "02", "03"]
        registry.register_obj("test", test_obj)  # register object

        test_obj = registry.get_obj("test")  # get object later in rig build

    def build(self) -> str:
        """Entry point. Run method to build rig module.
        --------------------------------------------------

        Returns:
            Top Maya group for rig module.

        """
        self.setup_top_grps()
        self.build_main()

        return self.mod_top_grp

    def setup_top_grps(self) -> None:
        """Create top rig module groups for organization."""
        self.mod_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}grp",
        )
        self.fk_chain_top_grp = cmds.group(
            empty=True,
            name=f"fk{cap(self.mod_name)}{self.mirr_side}grp",
        )
        self.ik_chain_top_grp = cmds.group(
            empty=True,
            name=f"ik{cap(self.mod_name)}{self.mirr_side}grp",
        )
        cmds.parent(self.fk_chain_top_grp, self.mod_top_grp)
        cmds.parent(self.ik_chain_top_grp, self.mod_top_grp)

    def build_main(self) -> int:
        """Create rig module components, connections, features..."""
        return 0
