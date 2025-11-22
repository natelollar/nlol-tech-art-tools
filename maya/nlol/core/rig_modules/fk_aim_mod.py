from maya import cmds
from nlol.core.general_utils import add_divider_attribue, cap, invert_axis_string
from nlol.core.rig_components import clean_constraints, create_control_groups, create_nurbs_curves
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()

create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
scale_constr = clean_constraints.scale_constr
aim_constr = clean_constraints.aim_constr


class FkAimModule:
    """Fk ctrl that aims at specified object. Aiming can be toggled on/off via parent ctrl.
    Example use: Aiming wyvern wing elbow at pole vector ctrl.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list[str],
        aim_object: str,
        reverse_right_vectors: bool | None = None,
        aim_vector: str | None = None,
        up_vector: str | None = None,
    ):
        """Initialize rig module.
        Args:
            rig_module_name: Custom name for the rig module. For example, "elbow".
            mirror_direction: Name for mirror side. For example, "left" or "right".
            main_joints: Single joint to control with fk ctrl.
            aim_object:  Object/ctrl to aim the fk ctrl at.  
            reverse_right_vectors: Reverse the input aim vectors.
                For example, "-x" to "x", or "y" to "-y".
            aim_vector: Joint axis to aim at the aim_object. 
                For instance, with default "x", the ctrls "x" axis will aim at the aim_object.
            up_vector: Axis direction from the joint the world up object will be placed. 
                For example, with default "y", the world up crv will be placed 150 units
                above the joint in local "y" to help guide aiming.

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints
        self.aim_object = aim_object
        self.reverse_right_vectors = reverse_right_vectors
        self.aim_vector = aim_vector or "x"
        self.up_vector = up_vector or "y"

    def build(self):
        """Entry point. Run method to build rig module.
        --------------------------------------------------

        Returns:
            Top Maya group for rig module.

        """
        self.input_checks()
        self.setup_top_grps()
        self.setup_ctrls()
        self.setup_aim_crvs()
        self.setup_toggle_attr()

        return self.mod_top_grp

    def input_checks(self):
        """Check class args."""
        if len(self.main_joints) != 1:
            msg = f"({self.mod_name}, {self.mirr_side}): Takes a single joint."
            logger.error(msg)
            raise ValueError(msg)

    def setup_top_grps(self):
        """Create top rig module group for organization."""
        self.mod_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}grp",
        )

    def setup_ctrls(self):
        """Create and set up parent and fk ctrl."""
        # ----- parent ctrl -----
        self.parent_ctrl = create_nurbs_curves.CreateCurves(
            name=f"fk{cap(self.mod_name)}Parent{self.mirr_side}ctrl",
            size=1.0,
            color_rgb=(0.3, 0.0, 1),
        ).box_curve()
        self.parent_ctrl_grp, *_ = create_ctrl_grps(self.parent_ctrl)
        cmds.matchTransform(self.parent_ctrl_grp, self.main_joints[0])

        # ----- main fk ctrl -----
        self.fk_ctrl = create_nurbs_curves.CreateCurves(
            name=f"fk{cap(self.mod_name)}{self.mirr_side}ctrl",
            size=0.5,
            color_rgb=(1.0, 0.2, 0.0),
        ).box_curve()
        self.fk_ctrl_grp, *_, self.fk_ctrl_aux_grp = create_ctrl_grps(
            self.fk_ctrl,
            aux_offset_grp=True,
        )
        cmds.matchTransform(self.fk_ctrl_grp, self.main_joints[0])

        # ----- fk ctrl to parent ctrl -----
        cmds.parent(self.fk_ctrl_grp, self.parent_ctrl)

        # ----- constraints -----
        # constrain fk ctrl
        parent_constr(self.fk_ctrl, self.main_joints[0])
        scale_constr(self.fk_ctrl, self.main_joints[0])
        # constrain parent ctrl
        main_joints_parent = cmds.listRelatives(self.main_joints[0], parent=True)
        if main_joints_parent:
            parent_constr(main_joints_parent[0], self.parent_ctrl_grp, offset=True)
            scale_constr(main_joints_parent[0], self.parent_ctrl_grp)

        # ----- hide and lock -----
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{self.parent_ctrl}.translate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{self.parent_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{self.parent_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{self.parent_ctrl}.visibility", **lock_hide_kwargs)
        cmds.setAttr(f"{self.fk_ctrl}.visibility", **lock_hide_kwargs)

        # ----- organize -----
        cmds.parent(self.parent_ctrl_grp, self.mod_top_grp)

    def setup_aim_crvs(self):
        """Create aim curves and set up aim constraint."""
        # ----- reverse aim axis -----
        # reverse aim axis' vector for right side. example: "x" to "-x".
        if self.reverse_right_vectors:
            self.aim_vector = invert_axis_string(self.aim_vector)
            self.up_vector = invert_axis_string(self.up_vector)

        # ----- static aim crv -----
        static_aim_crv_name = f"{self.mod_name}StaticAim{self.mirr_side}crv"
        static_aim_crv = create_nurbs_curves.CreateCurves(
            name=static_aim_crv_name,
            size=1.0,
            color_rgb=(0.8, 0.2, 0.4),
        ).locator_curve()
        static_aim_crv_grp = cmds.group(static_aim_crv, name=f"{static_aim_crv}Grp")
        cmds.matchTransform(static_aim_crv_grp, self.aim_object)
        parent_constr(self.parent_ctrl, static_aim_crv_grp, offset=True)

        # ----- world up crv -----
        dist = 150
        world_up_crv_dist = {
            "x": (dist, 0, 0),
            "y": (0, dist, 0),
            "z": (0, 0, dist),
            "-x": (-dist, 0, 0),
            "-y": (0, -dist, 0),
            "-z": (0, 0, -dist),
        }

        world_up_crv_name = f"{self.mod_name}WorldUp{self.mirr_side}crv"
        world_up_crv = create_nurbs_curves.CreateCurves(
            name=world_up_crv_name,
            size=1.0,
            color_rgb=(0.8, 0.2, 0.4),
        ).locator_curve()
        world_up_crv_grp = cmds.group(world_up_crv, name=f"{world_up_crv}Grp")
        cmds.parent(world_up_crv_grp, self.main_joints[0], relative=True)  # snap to joint
        cmds.xform(world_up_crv_grp, translation=world_up_crv_dist[self.up_vector])  # translate up
        cmds.parent(world_up_crv_grp, world=True)  # unparent
        parent_constr(self.parent_ctrl, world_up_crv_grp, offset=True)

        # ----- aim constraint -----
        self.aim_const = aim_constr(
            targets=[self.aim_object, static_aim_crv],
            object=self.fk_ctrl_aux_grp,
            world_up_object=world_up_crv,
            aim_vector=self.aim_vector,
            up_vector=self.up_vector,
            offset=True,
        )

        # ----- lock and hide -----
        for crv in [static_aim_crv, world_up_crv]:
            for axis in "XYZ":
                cmds.setAttr(f"{crv}.translate{axis}", lock=True)
                cmds.setAttr(f"{crv}.rotate{axis}", lock=True)
                cmds.setAttr(f"{crv}.scale{axis}", lock=True)
            cmds.setAttr(f"{crv}.visibility", 0)

        # ----- organize -----
        for grp in [static_aim_crv_grp, world_up_crv_grp]:
            cmds.parent(grp, self.mod_top_grp)

    def setup_toggle_attr(self):
        """Add aim toggle attribute to parent ctrl.
        Useful when switching between ik/fk limb and want aim functionality toggled off.
        """
        # ----- aim toggle attr -----
        add_divider_attribue(control_name=self.parent_ctrl, divider_amount=10)
        cmds.addAttr(
            self.parent_ctrl,
            longName="aimToggle",
            minValue=0.0,
            maxValue=1.0,
            defaultValue=1.0,
            keyable=True,
        )

        # ----- connect parent ctrl to aim toggle -----
        swch_reverse_nd = cmds.createNode(
            "reverse",
            name=f"{self.mod_name}AimToggle{self.mirr_side}reverse",
        )

        cmds.connectAttr(
            f"{self.parent_ctrl}.aimToggle",
            f"{self.aim_const}.target[0].targetWeight",
            force=True,
        )

        cmds.connectAttr(f"{self.parent_ctrl}.aimToggle", f"{swch_reverse_nd}.inputX")
        cmds.connectAttr(
            f"{swch_reverse_nd}.outputX",
            f"{self.aim_const}.target[1].targetWeight",
            force=True,
        )
