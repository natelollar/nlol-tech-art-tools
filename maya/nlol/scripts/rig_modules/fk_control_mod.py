from importlib import reload

from maya import cmds
from nlol.scripts.rig_components import (
    clean_constraints,
    create_control_groups,
    create_nurbs_curves,
)
from nlol.utilities.nlol_maya_logger import get_logger

reload(create_nurbs_curves)
reload(create_control_groups)
reload(clean_constraints)

CreateCurves = create_nurbs_curves.CreateCurves
create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
scale_constr = clean_constraints.scale_constr


class FkControlModule:
    """For building a basic fk control setup as a rig module."""

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str | None = None,
        main_joints: list | None = None,
        constraint: bool = True,
        hide_and_lock: bool = False,
    ):
        """Args:
        rig_module_name: Custom name for the rig module.
        mirror_direction: Name for mirror side.
        main_joints: Where to position the control.
            And joint to parent contrain to control unless "constraint=False".
        constraint: Whether to connect the control and joint
            with a parent and scale constraint. Useful if parenting another control
            to this control instead of a joint.
        hide_and_lock: Whether to hide the control and lock the attributes.
            Useful for a world control mainly used for parent space switching.

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"

        self.main_joints = main_joints

        self.constraint = constraint
        self.hide_and_lock = hide_and_lock

        self.logger = get_logger()

    def create_fk_ctrl(self) -> str:
        """Create simple fk control for selected joint or object.

        Returns:
            Top control group.

        """
        ctrl_name = f"{self.mod_name}{self.mirr_side}ctrl"
        fk_control = CreateCurves(
            name=ctrl_name,
            size=1,
            curve_type="box_curve",
        ).nurbs_curve
        fk_control_group = create_ctrl_grps(fk_control)[0]

        if self.main_joints:
            cmds.matchTransform(fk_control_group, self.main_joints[0])
            # if locator used from rig_helpers.ma, delete it
            if cmds.objectType(self.main_joints) != "joint":
                obj_shp = cmds.listRelatives(self.main_joints[0], shapes=True)
                if cmds.objectType(obj_shp) == "locator":
                    cmds.delete(self.main_joints[0])

        if self.constraint:  # parent constrain joint to control
            if not self.main_joints:
                error_msg = f'{ctrl_name}: Missing "joints" key. Need "joints" to constrain.'
                self.logger.error(error_msg)
                raise ValueError(error_msg)
            parent_constr(fk_control, self.main_joints[0])
            scale_constr(fk_control, self.main_joints[0])

        if self.hide_and_lock:  # lock attributes and hide control
            cmds.setAttr(f"{fk_control}.translate", lock=True)
            cmds.setAttr(f"{fk_control}.rotate", lock=True)
            cmds.setAttr(f"{fk_control}.scale", lock=True)
            cmds.setAttr(f"{fk_control}.visibility", 0)

        # hide visibility attribute
        cmds.setAttr(f"{fk_control}.visibility", lock=True, keyable=False, channelBox=False)

        # assign instance variables
        self.fk_control_group = fk_control_group

        return fk_control_group
