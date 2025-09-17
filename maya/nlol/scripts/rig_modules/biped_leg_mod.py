from importlib import reload

from nlol.scripts.rig_modules import biped_foot_submod, biped_limb_mod

reload(biped_limb_mod)
reload(biped_foot_submod)

BipedLimbModule = biped_limb_mod.BipedLimbModule
BipedFootModule = biped_foot_submod.BipedFootModule

main_new_names = "upperLeg, lowerLeg, ankle, toe"
upper_twist_new_name = "upperLegTwist"
lower_twist_new_name = "lowerLegTwist"


class BipedLegModule(BipedLimbModule):
    """Setup biped leg rig module."""

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list,
        upper_twist_joints: list,
        lower_twist_joints: list,
    ):
        """Initialize leg rig module.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: The mirror direction string in the toml file.
            main_joints: The main skinned joints.
            upper_twist_joints: Main skinned twist joints for upper segment.
            lower_twist_joints: Main skinned twist joints for lower segment.

        """
        super().__init__(
            rig_module_name=rig_module_name,
            mirror_direction=mirror_direction,
            main_joints=main_joints,
            upper_twist_joints=upper_twist_joints,
            lower_twist_joints=lower_twist_joints,
            main_object_names=main_new_names,
            upper_twist_name=upper_twist_new_name,
            lower_twist_name=lower_twist_new_name,
        )

    def build(self) -> str:
        """Build the leg rig module.
        --------------------------------------------------

        Returns:
            Top most group for leg rig module.

        """
        self.limb_module = super().build()
        if self.limb_module:
            self.foot_module = BipedFootModule(
                limb_module=self,
            )
            self.foot_module.build()

        return self.limb_top_grp
