from importlib import reload

from nlol.scripts.rig_modules import biped_foot_submod, biped_limb_mod
from nlol.utilities import utils_maya

reload(biped_limb_mod)
reload(biped_foot_submod)

BipedLimbModule = biped_limb_mod.BipedLimbModule
BipedFootModule = biped_foot_submod.BipedFootModule

cap = utils_maya.cap


class BipedLegModule(BipedLimbModule):
    """Setup biped leg rig module."""

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list[str],
        upper_twist_joints: list[str],
        lower_twist_joints: list[str],
        main_object_names: list[str] | None = None,
        upper_twist_name: str | None = None,
        lower_twist_name: str | None = None,
        foot_locators: list[str] | None = None,
        invert_toe_wiggle: bool = False,
        invert_toe_spin: bool = False,
        invert_foot_lean: bool = False,
        invert_foot_tilt: bool = False,
        invert_foot_roll: bool = False,
    ):
        """Initialize leg rig module.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: The mirror direction string in the toml file.
            main_joints: The main skinned joints.
            upper_twist_joints: Main skinned twist joints for upper segment.
            lower_twist_joints: Main skinned twist joints for lower segment.
            main_object_names: Main object names to be used instead of raw joint names.
            upper_twist_name: Main upper twist object name instead of raw joint names.
            lower_twist_name: Main lower twist object name instead of raw joint names.
            foot_locators: Locators determining position rotation of reverse foot ctrls.
                Requires 4 locators; toe end, heel, lateral foot side and medial foot side,
                listed in that order. Or use the pre-determined locator names and skip the arg,
                if character just has the bipedal left and right leg.

        """
        self.foot_locators = foot_locators
        self.invert_toe_wiggle = invert_toe_wiggle
        self.invert_toe_spin = invert_toe_spin
        self.invert_foot_lean = invert_foot_lean
        self.invert_foot_tilt = invert_foot_tilt
        self.invert_foot_roll = invert_foot_roll

        mod_name = rig_module_name
        mirr_side = mirror_direction
        if not main_object_names:
            main_object_names = [
                f"upper{cap(mod_name)}",
                f"lower{cap(mod_name)}",
                f"ankle{cap(mod_name)}",
                f"toe{cap(mod_name)}",
            ]
        if not upper_twist_name:
            upper_twist_name = f"upper{cap(mod_name)}Twist"
        if not lower_twist_name:
            lower_twist_name = f"lower{cap(mod_name)}Twist"

        if len(main_object_names) != 4:
            msg = (
                'Must be 4 "main_object_names" to match number of main joints in leg rig module: '
                f"{mod_name}, {mirr_side}"
            )
            self.logger.error(msg)
            raise ValueError(msg)

        super().__init__(
            rig_module_name=rig_module_name,
            mirror_direction=mirror_direction,
            main_joints=main_joints,
            upper_twist_joints=upper_twist_joints,
            lower_twist_joints=lower_twist_joints,
            main_object_names=main_object_names,
            upper_twist_name=upper_twist_name,
            lower_twist_name=lower_twist_name,
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
                foot_locators=self.foot_locators,
                invert_toe_wiggle=self.invert_toe_wiggle,
                invert_toe_spin=self.invert_toe_spin,
                invert_foot_lean=self.invert_foot_lean,
                invert_foot_tilt=self.invert_foot_tilt,
                invert_foot_roll=self.invert_foot_roll,
            )
            self.foot_module.build()

        return self.limb_top_grp
