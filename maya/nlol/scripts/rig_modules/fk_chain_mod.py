from importlib import reload

from maya import cmds
from nlol.scripts.rig_components import (
    clean_constraints,
    create_control_groups,
    create_nurbs_curves,
)

reload(create_nurbs_curves)
reload(create_control_groups)
reload(clean_constraints)

CreateCurves = create_nurbs_curves.CreateCurves
create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
scale_constr = clean_constraints.scale_constr


class FkChainModule:
    """For building a basic fk contrl chain setup as a rig module."""

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list,
    ):
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints

    def build_fk_ctrl_chain(self) -> str:
        """Create a basic chain of fk controls along a joint chain.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: Name for mirror side.
            main_joints: Joints to snap the controls to,
                and then parent and scale constrain to controls.

        Returns:
            Top control group.

        """
        fk_ctrl_grps = []
        fk_ctrls = []
        for i, jnt in enumerate(self.main_joints, 1):
            fk_ctrl = create_nurbs_curves.CreateCurves(
                name=f"{self.mod_name}{self.mirr_side}{i:02d}_ctrl",
                size=1,
                color_rgb=(1, 0, 0),
            ).box_curve()

            fk_ctrl_grp = create_ctrl_grps(fk_ctrl)[0]

            cmds.matchTransform(fk_ctrl_grp, jnt)

            parent_constr(fk_ctrl, jnt)
            scale_constr(fk_ctrl, jnt)

            cmds.setAttr(f"{fk_ctrl}.visibility", lock=True, keyable=False, channelBox=False)

            fk_ctrl_grps.append(fk_ctrl_grp)
            fk_ctrls.append(fk_ctrl)

        # parent controls into hierarchy
        for grp, ctrl in zip(fk_ctrl_grps[1:], fk_ctrls, strict=False):
            cmds.parent(grp, ctrl)

        return fk_ctrl_grps[0]
