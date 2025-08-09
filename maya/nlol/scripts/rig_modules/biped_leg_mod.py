from importlib import reload
from pathlib import Path

from nlol.scripts.rig_modules import biped_foot_mod, biped_limb_mod

reload(biped_limb_mod)
reload(biped_foot_mod)

BipedLimbModule = biped_limb_mod.BipedLimbModule
BipedFootModule = biped_foot_mod.BipedFootModule

main_new_names = "upperLeg, lowerLeg, ankle, toe"
upper_twist_new_name = "upperLegTwist"
lower_twist_new_name = "lowerLegTwist"


class BipedLegModule(BipedLimbModule):
    """Setup biped leg rig module."""

    def __init__(
        self,
        rig_data_filepath: str | Path,
        rig_module: str,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list,
        upper_twist_joints: list,
        lower_twist_joints: list,
    ):
        """Initialize leg rig module.

        Args:
            rig_data_filepath: Json filepath containing name strings and
                joint selection metadata for rig module.
            rig_module: Name of rig module being used in the json file.
            rig_module_name: Custom name for the rig module.
            mirror_direction: The mirror direction string in the json file.
            main_joints: The main skinned joints.
            upper_twist_joints: Main skinned twist joints for upper segment.
            lower_twist_joints: Main skinned twist joints for lower segment.

        """
        super().__init__(
            rig_data_filepath=rig_data_filepath,
            rig_module=rig_module,
            rig_module_name=rig_module_name,
            mirror_direction=mirror_direction,
            main_joints=main_joints,
            upper_twist_joints=upper_twist_joints,
            lower_twist_joints=lower_twist_joints,
            main_object_names=main_new_names,
            upper_twist_name=upper_twist_new_name,
            lower_twist_name=lower_twist_new_name,
        )

    def build_leg_module(self) -> str:
        """Build the leg rig module.

        Returns:
            Top most group for leg rig module.

        """
        self.limb_module = super().build_limb_module()
        if self.limb_module:
            self.foot_module = BipedFootModule(
                limb_module=self,
            )
            self.foot_module.build_foot_module()

        return self.limb_top_grp
