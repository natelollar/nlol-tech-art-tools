from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger
from nlol.utilities.utils_maya import cap

logger = get_logger()


class ExampleModule:
    def __init__(self, rig_module_name: str, mirror_direction: str, main_joints: list[str]):
        """Create rig module..."""
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints

    def build(self):
        """Entry point. Run method to build rig module.
        --------------------------------------------------

        Returns:
            Top group for rig module.

        """
        self.build_top_groups()
        self.build_main()

        return self.mod_top_grp

    def build_top_groups(self):
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

    def build_main(self):
        """Create rig module components, connections, features..."""
        return 0
