from importlib import reload

from maya import cmds
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_locators,
    create_nurbs_curves,
)
from nlol.core.rig_modules.biped_limb_mod import BipedLimbModule
from nlol.core import general_utils
from nlol.utilities.nlol_maya_logger import get_logger

reload(general_utils)
reload(create_control_groups)
reload(create_joint)
reload(create_locators)
reload(create_nurbs_curves)
reload(clean_constraints)

CreateCurves = create_nurbs_curves.CreateCurves
create_ctrl_grps = create_control_groups.create_ctrl_grps
cap = general_utils.cap
parent_constr = clean_constraints.parent_constr
point_constr = clean_constraints.point_constr
orient_constr = clean_constraints.orient_constr
scale_constr = clean_constraints.scale_constr


class BipedFootModule:
    """Create reverse foot rig module."""

    def __init__(
        self,
        limb_module: BipedLimbModule,
        foot_locators: list[str] | None = None,
        invert_toe_wiggle: bool = False,
        invert_toe_spin: bool = False,
        invert_foot_lean: bool = False,
        invert_foot_tilt: bool = False,
        invert_foot_roll: bool = False,
    ) -> None:
        """Initialize foot module.

        Args:
            limb_module: The "BipedLimbModule" instance this foot belongs to.
            foot_locators: Locators determining position rotation of reverse foot ctrls.
                4 locators; toe end, heel, lateral foot side and medial foot side,
                listed in that order. Foot locator names do not matter,
                just that they are listed in the correct order.
                Or use the pre-determined locator names and skip the arg,
                if character just has the bipedal left and right leg.

        """
        self.limb_mod = limb_module
        self.mod_name = f"{limb_module.mod_name}Foot"
        self.mirr_side = self.limb_mod.mirr_side
        self.foot_locators = foot_locators
        self.invert_toe_wiggle = invert_toe_wiggle
        self.invert_toe_spin = invert_toe_spin
        self.invert_foot_lean = invert_foot_lean
        self.invert_foot_tilt = invert_foot_tilt
        self.invert_foot_roll = invert_foot_roll
        self.logger = get_logger()

    def build(self, base_foot_aim: bool = True, reverse_foot_attrs: bool = True):
        """Create foot rig module.
        --------------------------------------------------
        Based on locators establishing reverse foot rotation points.
        Position locators in "rig_helpers.ma" file.

        Args:
            base_foot_point: Wether to make the foot always
                aim towards the base foot control.
            reverse_foot_attrs: Add reverse foot attributes to main limb ik control.

        """
        # ----- check if toe joint exists -----
        if len(self.limb_mod.ik_jnts) != 4:
            msg = (
                f'Rig submodule "{self.limb_mod.mod_name}, {self.mirr_side}" failed to build. '
                f"Needs 4 joints. Likely, toe joint missing in rig object data toml."
            )
            self.logger.error(msg)
            raise ValueError(msg)
        if self.foot_locators and len(self.foot_locators) != 4:
            msg = (
                'Must be 4 "foot_locators" listed: '
                "toe end, heel, lateral foot side and medial foot side. "
                f'"{self.mod_name}, {self.mirr_side}"'
            )
            self.logger.error(msg)
            raise ValueError(msg)

        # ----- delete simple ik to control -----
        if self.limb_mod.ik_toe_ctrl_grp:
            cmds.delete(self.limb_mod.ik_toe_ctrl_grp)

        # ---------------------------------------------------------
        # --------------- create and find locators ---------------
        foot_ankle_loc = create_locators.locator_snap(
            objects=self.limb_mod.main_joints[2],
            locator_name=f"ankle{self.mirr_side}loc",
            local_scale=(5, 5, 5),
        )[0]
        toe_loc = create_locators.locator_snap(
            objects=self.limb_mod.main_joints[3],
            locator_name=f"toe{self.mirr_side}loc",
            local_scale=(5, 5, 5),
        )[0]
        # additionally, match toe locator rotation to ankle
        cmds.matchTransform(toe_loc, self.limb_mod.main_joints[2], rotation=True)

        if self.foot_locators:
            foot_locators = self.foot_locators
        else:
            foot_locators = [  # reverse foot locator list
                f"toeEnd{self.mirr_side}loc",
                f"heel{self.mirr_side}loc",
                f"lateral{self.mirr_side}loc",
                f"medial{self.mirr_side}loc",
            ]
        foot_locators.insert(0, foot_ankle_loc)
        foot_locators.insert(1, toe_loc)

        missing_loc = [loc for loc in foot_locators if not cmds.objExists(loc)]
        if missing_loc:
            msg = f"Missing reverse foot locators: {missing_loc}. Foot module failed to build."
            self.logger.error(msg)
            raise ValueError(msg)

        # ---------------------------------------------------------
        # ---------- create controls to replace locators ----------
        foot_ctrls = []
        foot_ctrl_grps = []
        foot_aux_ctrl_grps = []
        loc_base_names = ["ankle", "toe", "toeEnd", "heel", "lateral", "medial"]
        for loc, loc_nm in zip(foot_locators, loc_base_names, strict=False):
            # ----- create control -----
            foot_ctrl = CreateCurves(
                name=f"{self.mod_name}{cap(loc_nm)}{self.mirr_side}ctrl",
                size=0.25,
                color_rgb=(0.2, 1.0, 0.0),
            ).sphere_curve()

            # ----- control group -----
            foot_ctrl_grp, *_, foot_aux_ctrl_grp = create_ctrl_grps(
                foot_ctrl,
                aux_offset_grp=True,
            )

            # ----- snap control group to locator -----
            cmds.matchTransform(foot_ctrl_grp, loc)

            foot_ctrls.append(foot_ctrl)
            foot_ctrl_grps.append(foot_ctrl_grp)
            foot_aux_ctrl_grps.append(foot_aux_ctrl_grp)

        # parent controls and groups together
        for grp, ctrl in zip(
            reversed(foot_ctrl_grps[:-1]),
            reversed(foot_ctrls),
            strict=False,
        ):
            cmds.parent(grp, ctrl)

        # -----------------------------------------------------
        # ---------- create extra toe offset control ----------
        toe_wiggle_ctrl = CreateCurves(
            name=f"{self.mod_name}ToeWiggle{self.mirr_side}ctrl",
            size=1,
            color_rgb=(1, 0, 1),
        ).box_curve()
        # ----- control group -----
        toe_wiggle_ctrl_grp, *_, toe_wiggle_aux_ctrl_grp = create_ctrl_grps(
            toe_wiggle_ctrl,
            aux_offset_grp=True,
        )
        # ----- snap control to locator -----
        cmds.matchTransform(toe_wiggle_ctrl_grp, foot_locators[1])

        # -------------------------------------------------------
        # -------------------- parent groups --------------------
        foot_top_grp = cmds.group(name=f"{self.mod_name}{self.mirr_side}grp", empty=True)
        foot_pivot_grp = cmds.group(name=f"{self.mod_name}Pivot{self.mirr_side}grp", empty=True)
        cmds.matchTransform(foot_pivot_grp, self.limb_mod.ik_jnts[2])
        cmds.parent(foot_pivot_grp, foot_top_grp)
        cmds.parent(foot_top_grp, self.limb_mod.ik_limb_top_grp)
        # parent foot controls under pivot group
        cmds.parent(foot_ctrl_grps[-1], foot_pivot_grp)

        # --------------- parent toe wiggle control ---------------
        cmds.parent(toe_wiggle_ctrl_grp, foot_top_grp)

        # ------------------------------------------------------
        # --------------- reverse foot parenting ---------------
        # break default limb constraints
        cmds.delete(self.limb_mod.limb_ik_handle_const)
        cmds.delete(self.limb_mod.limb_ik_end_rot_const)
        cmds.delete(self.limb_mod.limb_ik_end_scale_const)
        cmds.delete(self.limb_mod.soft_ik_handle_const)
        cmds.delete(self.limb_mod.soft_ik_ruler_end_const)

        # ----- translate constrain -----
        # attach limb length ruler end to foot ankle control
        point_constr(foot_ctrls[0], self.limb_mod.soft_ik_ruler_end)
        # ----- translate constrain -----
        # limb ik control > foot pivot grp, ankle foot control > soft ik handle
        # ik soft end joint > limb ik handle
        point_constr(self.limb_mod.ik_ctrl, foot_pivot_grp, offset=True)
        point_constr(foot_ctrls[0], self.limb_mod.soft_ik_handle, offset=True)
        point_constr(self.limb_mod.soft_ik_jnts[1], self.limb_mod.limb_ik_handle, offset=True)
        # ----- rotate constrain -----
        # limb ik control > foot pivot grp, ankle foot control > ik ankle joint
        orient_constr(self.limb_mod.ik_ctrl, foot_pivot_grp, offset=True)
        self.foot_ankle_orient_const = orient_constr(
            foot_ctrls[0],
            self.limb_mod.ik_jnts[2],
            offset=True,
        )
        # toe wiggle constrain
        orient_constr(toe_wiggle_ctrl, self.limb_mod.ik_jnts[3], offset=True)
        # ----- scale constrain -----
        # limb ik control > foot pivot grp, ankle foot control > ik ankle joint
        scale_constr(self.limb_mod.ik_ctrl, foot_pivot_grp)
        scale_constr(foot_ctrls[0], self.limb_mod.ik_jnts[2])
        # toe wiggle to joint
        scale_constr(toe_wiggle_ctrl, self.limb_mod.ik_jnts[3])

        # ---------- lock and hide attributes ----------
        # hide reverse foot ankle control
        cmds.setAttr(f"{foot_ctrl_grps[0]}.visibility", 0)
        # hide foot control attributes
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for ctrl in foot_ctrls:
            for axis in "XYZ":
                cmds.setAttr(f"{ctrl}.translate{axis}", **lock_hide_kwargs)
                cmds.setAttr(f"{ctrl}.scale{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{ctrl}.visibility", **lock_hide_kwargs)
        # hide toe wiggle control attributes
        for axis in "XYZ":
            cmds.setAttr(f"{toe_wiggle_ctrl}.translate{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{toe_wiggle_ctrl}.visibility", **lock_hide_kwargs)

        # ---------- assign instance variables ----------
        self.foot_top_grp = foot_top_grp
        self.foot_ctrls = foot_ctrls
        self.foot_aux_ctrl_grps = foot_aux_ctrl_grps
        self.toe_wiggle_ctrl_grp = toe_wiggle_ctrl_grp
        self.toe_wiggle_aux_ctrl_grp = toe_wiggle_aux_ctrl_grp

        # ---------- point foot at base control ----------
        # use two single ik chains to angle foot
        # towards base ik control when foot moving away
        if base_foot_aim:
            self.aim_foot_at_base()

        # ---------- add reverse foot attributes ----------
        # add attrs to main limb ik control
        if reverse_foot_attrs:
            self.reverse_foot_attributes()

        # ----- delete foot locators -----
        for loc in foot_locators:
            if cmds.objExists(loc):
                cmds.delete(loc)

    def aim_foot_at_base(self):
        """Add two single-chain solver ik joint chains
        to make the foot always aim towards the base foot control.
        """
        # ---------- create foot aim joints ----------
        foot_aim_jnts = []
        for i, ctrl in enumerate(self.foot_ctrls[:3], 1):
            foot_aim_jnt = create_joint.single_joint(
                name=f"{self.mod_name}Aim{self.mirr_side}{i:02d}_jnt",
                radius=5,
                color_rgb=(1.0, 0.4, 0.0),
                scale_compensate=False,
                parent_snap=ctrl,
            )
            foot_aim_jnts.append(foot_aim_jnt)

        # parent joints together
        for i, jnt in enumerate(foot_aim_jnts):
            if jnt != foot_aim_jnts[0]:
                cmds.parent(jnt, foot_aim_jnts[i - 1])

        # ----- ik handles with single-chain solver -----
        aim_ik_handle_01 = cmds.ikHandle(
            name=f"{self.mod_name}Aim{self.mirr_side}01_ikHandle",
            startJoint=foot_aim_jnts[0],
            endEffector=foot_aim_jnts[1],
            solver="ikSCsolver",
        )
        cmds.rename(aim_ik_handle_01[1], f"{aim_ik_handle_01[0]}Effector")

        aim_ik_handle_02 = cmds.ikHandle(
            name=f"{self.mod_name}Aim{self.mirr_side}02_ikHandle",
            startJoint=foot_aim_jnts[1],
            endEffector=foot_aim_jnts[2],
            solver="ikSCsolver",
        )
        cmds.rename(aim_ik_handle_02[1], f"{aim_ik_handle_02[0]}Effector")

        # ----- constrain ik handles to foot controls  -----
        parent_constr(self.foot_ctrls[1], aim_ik_handle_01[0])
        parent_constr(self.foot_ctrls[2], aim_ik_handle_02[0])
        # ----- point and scale constrain top foot joint  -----
        point_constr(self.limb_mod.ik_jnts[2], foot_aim_jnts[0])
        scale_constr(self.foot_ctrls[0], foot_aim_jnts[0])
        # ----- constrain foot joints -----
        cmds.delete(self.foot_ankle_orient_const)  # remove default foot constraint
        orient_constr(foot_aim_jnts[0], self.limb_mod.ik_jnts[2], offset=True)
        # constraint wiggle ctrl to follow second foot aim joint
        parent_constr(foot_aim_jnts[1], self.toe_wiggle_ctrl_grp, offset=True)
        scale_constr(foot_aim_jnts[1], self.toe_wiggle_ctrl_grp)

        # ---------- top parent group ----------
        cmds.parent(foot_aim_jnts[0], self.foot_top_grp)
        cmds.parent(aim_ik_handle_01[0], self.foot_top_grp)
        cmds.parent(aim_ik_handle_02[0], self.foot_top_grp)
        # ---------- hide objects ----------
        cmds.setAttr(f"{foot_aim_jnts[0]}.visibility", 0)
        cmds.setAttr(f"{aim_ik_handle_01[0]}.visibility", 0)
        cmds.setAttr(f"{aim_ik_handle_02[0]}.visibility", 0)

    def reverse_foot_attributes(self):
        """Add reverse foot attributes to main ik control.
        Also, add nodes and setup attributes.
        """
        # ---------- add foot attributes ----------
        soft_ik_divider_name = "____Foot____"
        cmds.addAttr(
            self.limb_mod.ik_ctrl,
            longName=soft_ik_divider_name,
            niceName=soft_ik_divider_name,
            attributeType="enum",
            enumName="----------",
        )
        cmds.setAttr(f"{self.limb_mod.ik_ctrl}.{soft_ik_divider_name}", channelBox=True)
        # ----------
        cmds.addAttr(self.limb_mod.ik_ctrl, longName="toeWiggle", keyable=True)
        cmds.addAttr(self.limb_mod.ik_ctrl, longName="toeSpin", keyable=True)
        cmds.addAttr(self.limb_mod.ik_ctrl, longName="lean", keyable=True)
        cmds.addAttr(self.limb_mod.ik_ctrl, longName="tilt", keyable=True)

        cmds.addAttr(self.limb_mod.ik_ctrl, longName="roll", keyable=True)
        # NOTE: Mirroing leg does not change forward rotation axis.
        # Though may need to adjust for certain scenarios.
        # default_toe_bend_angle = -35 if self.limb_mod.down_chain_axis == "-x" else 35
        default_toe_bend_angle = -35
        cmds.addAttr(
            self.limb_mod.ik_ctrl,
            longName="rollToeBendAngle",
            defaultValue=default_toe_bend_angle,
            keyable=True,
        )
        cmds.addAttr(
            self.limb_mod.ik_ctrl,
            longName="rollToeEndRangeMult",
            defaultValue=2,
            keyable=True,
        )
        cmds.setAttr(f"{self.limb_mod.ik_ctrl}.rollToeBendAngle", lock=True)
        cmds.setAttr(f"{self.limb_mod.ik_ctrl}.rollToeEndRangeMult", lock=True)

        # -------------------------------------------------------
        # ---------- connect and setup foot attributes ----------
        # --------------- toe wiggle ---------------
        if self.invert_toe_wiggle:
            toewiggle_multiply_nd = cmds.createNode(
                "multiply",
                name=f"{self.mod_name}ToeWiggle{self.mirr_side}multiply",
            )
            cmds.setAttr(f"{toewiggle_multiply_nd}.input[0]", -1)
            cmds.connectAttr(
                f"{self.limb_mod.ik_ctrl}.toeWiggle",
                f"{toewiggle_multiply_nd}.input[1]",
            )
            cmds.connectAttr(
                f"{toewiggle_multiply_nd}.output",
                f"{self.toe_wiggle_aux_ctrl_grp}.rotateZ",
            )
        else:
            cmds.connectAttr(
                f"{self.limb_mod.ik_ctrl}.toeWiggle",
                f"{self.toe_wiggle_aux_ctrl_grp}.rotateZ",
            )
        # --------------- top spin ---------------
        if self.invert_toe_spin:
            toespin_multiply_nd = cmds.createNode(
                "multiply",
                name=f"{self.mod_name}ToeSpin{self.mirr_side}multiply",
            )
            cmds.setAttr(f"{toespin_multiply_nd}.input[0]", -1)
            cmds.connectAttr(
                f"{self.limb_mod.ik_ctrl}.toeSpin",
                f"{toespin_multiply_nd}.input[1]",
            )
            cmds.connectAttr(
                f"{toespin_multiply_nd}.output",
                f"{self.foot_aux_ctrl_grps[2]}.rotateX",
            )
        else:
            cmds.connectAttr(
                f"{self.limb_mod.ik_ctrl}.toeSpin",
                f"{self.foot_aux_ctrl_grps[2]}.rotateX",
            )
        # --------------- lean ---------------
        if self.invert_foot_lean:
            lean_multiply_nd = cmds.createNode(
                "multiply",
                name=f"{self.mod_name}Lean{self.mirr_side}multiply",
            )
            cmds.setAttr(f"{lean_multiply_nd}.input[0]", -1)
            cmds.connectAttr(
                f"{self.limb_mod.ik_ctrl}.lean",
                f"{lean_multiply_nd}.input[1]",
            )
            cmds.connectAttr(
                f"{lean_multiply_nd}.output",
                f"{self.foot_aux_ctrl_grps[1]}.rotateY",
            )
        else:
            cmds.connectAttr(
                f"{self.limb_mod.ik_ctrl}.lean",
                f"{self.foot_aux_ctrl_grps[1]}.rotateY",
            )
        # ----------------------------------------------
        # -------------------- tilt --------------------
        tilt_clamp_nd = cmds.createNode(
            "clamp",
            name=f"{self.mod_name}Tilt{self.mirr_side}clamp",
        )
        cmds.setAttr(f"{tilt_clamp_nd}.minG", -180)
        cmds.setAttr(f"{tilt_clamp_nd}.maxR", 180)
        cmds.connectAttr(f"{self.limb_mod.ik_ctrl}.tilt", f"{tilt_clamp_nd}.inputR")
        cmds.connectAttr(f"{self.limb_mod.ik_ctrl}.tilt", f"{tilt_clamp_nd}.inputG")
        if self.invert_foot_tilt:
            tilt_multiplydivid_nd = cmds.createNode(
                "multiplyDivide",
                name=f"{self.mod_name}Tilt{self.mirr_side}multiplyDivide",
            )
            cmds.setAttr(f"{tilt_multiplydivid_nd}.input2X", -1)
            cmds.setAttr(f"{tilt_multiplydivid_nd}.input2Y", -1)
            cmds.connectAttr(
                f"{tilt_clamp_nd}.outputR",
                f"{tilt_multiplydivid_nd}.input1X",
            )
            cmds.connectAttr(
                f"{tilt_multiplydivid_nd}.outputX",
                f"{self.foot_aux_ctrl_grps[4]}.rotateY",
            )
            cmds.connectAttr(
                f"{tilt_clamp_nd}.outputG",
                f"{tilt_multiplydivid_nd}.input1Y",
            )
            cmds.connectAttr(
                f"{tilt_multiplydivid_nd}.outputY",
                f"{self.foot_aux_ctrl_grps[5]}.rotateY",
            )
        else:
            cmds.connectAttr(
                f"{tilt_clamp_nd}.outputR",
                f"{self.foot_aux_ctrl_grps[4]}.rotateY",
            )
            cmds.connectAttr(
                f"{tilt_clamp_nd}.outputG",
                f"{self.foot_aux_ctrl_grps[5]}.rotateY",
            )
        # ----------------------------------------------
        # -------------------- roll --------------------
        # ----------
        if self.invert_foot_roll:
            roll_multiplydivide_nd = cmds.createNode(
                "multiplyDivide",
                name=f"{self.mod_name}Roll{self.mirr_side}multiplyDivide",
            )
            for axis in "XYZ":
                cmds.setAttr(f"{roll_multiplydivide_nd}.input2{axis}", -1)
        # ----------
        toe_remapevalue_double_nd = cmds.createNode(
            "multiplyDivide",
            name=f"{self.mod_name}ToeRemapValueDouble{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.rollToeBendAngle",
            f"{toe_remapevalue_double_nd}.input1X",
        )
        cmds.setAttr(f"{toe_remapevalue_double_nd}.input2X", 2)
        # ----------
        toe_roll_remap_nd = cmds.createNode(
            "remapValue",
            name=f"{self.mod_name}ToeRoll{self.mirr_side}remapValue",
        )
        cmds.setAttr(f"{toe_roll_remap_nd}.value[0].value_Position", 0.0)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[0].value_FloatValue", 0.0)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[1].value_Position", 0.5)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[1].value_FloatValue", 1.0)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[2].value_Position", 1.0)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[2].value_FloatValue", 0.0)
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.roll",
            f"{toe_roll_remap_nd}.inputValue",
        )
        cmds.connectAttr(
            f"{toe_remapevalue_double_nd}.outputX",
            f"{toe_roll_remap_nd}.inputMax",
        )
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.rollToeBendAngle",
            f"{toe_roll_remap_nd}.outputMax",
        )
        if self.invert_foot_roll:
            cmds.connectAttr(
                f"{toe_roll_remap_nd}.outValue",
                f"{roll_multiplydivide_nd}.input1X",
            )
            cmds.connectAttr(
                f"{roll_multiplydivide_nd}.outputX",
                f"{self.foot_aux_ctrl_grps[1]}.rotateZ",
            )
        else:
            cmds.connectAttr(
                f"{toe_roll_remap_nd}.outValue",
                f"{self.foot_aux_ctrl_grps[1]}.rotateZ",
            )
        # ----------
        condition_180_switch_nd = cmds.createNode(
            "condition",
            name=f"{self.mod_name}180Switch{self.mirr_side}condition",
        )
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.rollToeBendAngle",
            f"{condition_180_switch_nd}.firstTerm",
        )
        cmds.setAttr(f"{condition_180_switch_nd}.operation", 4)  # less than
        cmds.setAttr(f"{condition_180_switch_nd}.colorIfTrueR", 180)
        cmds.setAttr(f"{condition_180_switch_nd}.colorIfFalseR", -180)
        # ----------
        invet_180_nd = cmds.createNode(
            "multiplyDivide",
            name=f"{self.mod_name}180Invert{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(f"{condition_180_switch_nd}.outColorR", f"{invet_180_nd}.input1X")
        cmds.setAttr(f"{invet_180_nd}.input2X", -1)
        # ----------
        toe_end_range_mult_nd = cmds.createNode(
            "multiplyDivide",
            name=f"{self.mod_name}ToeEndRange{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(f"{invet_180_nd}.outputX", f"{toe_end_range_mult_nd}.input1X")
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.rollToeEndRangeMult",
            f"{toe_end_range_mult_nd}.input2X",
        )
        # ----------
        difference_180_nd = cmds.createNode(
            "plusMinusAverage",
            name=f"{self.mod_name}180Difference{self.mirr_side}plusMinusAverage",
        )
        cmds.connectAttr(
            f"{invet_180_nd}.outputX",
            f"{difference_180_nd}.input1D[0]",
        )
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.rollToeBendAngle",
            f"{difference_180_nd}.input1D[1]",
        )
        # ----------
        toe_end_roll_remap_nd = cmds.createNode(
            "remapValue",
            name=f"{self.mod_name}ToeEndRoll{self.mirr_side}remapValue",
        )
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.roll",
            f"{toe_end_roll_remap_nd}.inputValue",
        )
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.rollToeBendAngle",
            f"{toe_end_roll_remap_nd}.inputMin",
        )
        cmds.connectAttr(
            f"{difference_180_nd}.output1D",
            f"{toe_end_roll_remap_nd}.inputMax",
        )
        cmds.connectAttr(
            f"{toe_end_range_mult_nd}.outputX",
            f"{toe_end_roll_remap_nd}.outputMax",
        )
        if self.invert_foot_roll:
            cmds.connectAttr(
                f"{toe_end_roll_remap_nd}.outValue",
                f"{roll_multiplydivide_nd}.input1Y",
            )
            cmds.connectAttr(
                f"{roll_multiplydivide_nd}.outputY",
                f"{self.foot_aux_ctrl_grps[2]}.rotateZ",
            )
        else:
            cmds.connectAttr(
                f"{toe_end_roll_remap_nd}.outValue",
                f"{self.foot_aux_ctrl_grps[2]}.rotateZ",
            )
        # ----------
        heel_roll_remap_nd = cmds.createNode(
            "remapValue",
            name=f"{self.mod_name}HeelRoll{self.mirr_side}remapValue",
        )
        cmds.connectAttr(
            f"{self.limb_mod.ik_ctrl}.roll",
            f"{heel_roll_remap_nd}.inputValue",
        )
        cmds.connectAttr(
            f"{condition_180_switch_nd}.outColorR",
            f"{heel_roll_remap_nd}.inputMax",
        )
        cmds.connectAttr(
            f"{condition_180_switch_nd}.outColorR",
            f"{heel_roll_remap_nd}.outputMax",
        )
        if self.invert_foot_roll:
            cmds.connectAttr(
                f"{heel_roll_remap_nd}.outValue",
                f"{roll_multiplydivide_nd}.input1Z",
            )
            cmds.connectAttr(
                f"{roll_multiplydivide_nd}.outputZ",
                f"{self.foot_aux_ctrl_grps[3]}.rotateZ",
            )
        else:
            cmds.connectAttr(
                f"{heel_roll_remap_nd}.outValue",
                f"{self.foot_aux_ctrl_grps[3]}.rotateZ",
            )
