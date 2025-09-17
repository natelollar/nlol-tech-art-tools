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
        iteration_id: str = "",
        aux_offset_group: bool = False,
        return_all_groups: bool = False,
    ):
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.mirr_side = self.mirr_side.replace("__", "_")
        self.main_joints = main_joints
        self.iteration_id = iteration_id
        self.aux_offset_group = aux_offset_group
        self.return_all_groups = return_all_groups

    def build(self) -> str | tuple[list[str], list[str], list[str], list[str]]:
        """Build fk control chain rig module.
        --------------------------------------------------
        Create a basic chain of fk controls along a joint chain.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: Name for mirror side.
            main_joints: Joints to snap the controls to,
                and then parent and scale constrain to controls.
            iteration_id: Optional id if multiple fk chains being created.
                String that goes before number id.  Example: "a".
            aux_offset_group: An additional offset group useful for extra connections.
            return_all_groups: Return all the groups instead of just very top group.
                Helpful if using as rig sub-module.

        Returns:
            Fk control parent groups. Either the very top group or all the groups.
            Let method return only top group if using as a full rig module
            or all the groups if needed for sub-module connections.

        """
        fkctrls = []
        fkctrl_top_grps = []
        fkctrl_prnt_grps = []
        fkctrl_swch_grps = []
        fkctrl_offs_grps = []
        fkctrl_aux_grps = []
        for i, jnt in enumerate(self.main_joints, 1):
            fkctrl = create_nurbs_curves.CreateCurves(
                name=f"{self.mod_name}{self.mirr_side}{self.iteration_id}{i:02d}_ctrl",
                size=1,
                color_rgb=(1, 0, 0),
            ).box_curve()

            fkctrl_groups = create_ctrl_grps(control=fkctrl, aux_offset_group=self.aux_offset_group)
            fkctrl_aux_grp = None
            if len(fkctrl_groups) == 5:
                (
                    fkctrl_top_grp,
                    fkctrl_prnt_grp,
                    fkctrl_swch_grp,
                    fkctrl_offs_grp,
                    fkctrl_aux_grp,
                ) = fkctrl_groups
            else:
                fkctrl_top_grp, fkctrl_prnt_grp, fkctrl_swch_grp, fkctrl_offs_grp = fkctrl_groups

            cmds.matchTransform(fkctrl_top_grp, jnt)

            parent_constr(fkctrl, jnt)
            scale_constr(fkctrl, jnt)

            cmds.setAttr(f"{fkctrl}.visibility", lock=True, keyable=False, channelBox=False)

            fkctrls.append(fkctrl)
            fkctrl_top_grps.append(fkctrl_top_grp)
            fkctrl_prnt_grps.append(fkctrl_prnt_grp)
            fkctrl_swch_grps.append(fkctrl_swch_grp)
            fkctrl_offs_grps.append(fkctrl_offs_grp)
            if fkctrl_aux_grp:
                fkctrl_aux_grps.append(fkctrl_aux_grp)

        # parent controls into hierarchy
        for grp, ctrl in zip(fkctrl_top_grps[1:], fkctrls, strict=False):
            cmds.parent(grp, ctrl)

        if self.return_all_groups:
            return (
                fkctrl_top_grps,
                fkctrl_prnt_grps,
                fkctrl_swch_grps,
                fkctrl_offs_grps,
                fkctrl_aux_grps,
                fkctrls,
            )
        return fkctrl_top_grps[0]
