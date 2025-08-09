from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.scripts.rig_components import create_control_groups, create_nurbs_curves

reload(create_nurbs_curves)
reload(create_control_groups)

CreateCurves = create_nurbs_curves.CreateCurves
create_ctrl_grps = create_control_groups.create_ctrl_grps


class FkControlModule:
    """For building a basic fk control setup as a rig module."""

    def __init__(
        self,
        rig_data_filepath: str | Path,
        rig_module: str,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list,
    ):
        self.rig_data_filepath = rig_data_filepath
        self.rig_module = rig_module
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"

        self.main_joints = main_joints

    def create_fk_ctrl(self) -> str:
        """Create simple fk control for selected joint or object.

        Returns:
            Top control group.

        """
        fk_control = CreateCurves(
            name=f"{self.mod_name}{self.mirr_side}ctrl",
            size=5,
            curve_type="box_curve",
        ).nurbs_curve
        fk_control_group = create_ctrl_grps(fk_control)[0]

        # snap control group to joint object
        cmds.matchTransform(fk_control_group, self.main_joints[0])

        # parent constrain joint to control
        cmds.parentConstraint(fk_control, self.main_joints[0])
        cmds.scaleConstraint(fk_control, self.main_joints[0])

        return fk_control_group
