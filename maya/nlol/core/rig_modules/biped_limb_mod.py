"""Biped limb rig module.
Works with human arms and legs, and other bipedal creatures.
"""

from importlib import reload

from maya import cmds
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_locators,
    create_nurbs_curves,
    create_ruler,
)
from nlol.core.rig_tools import get_aligned_axis, limb_hinge_vector
from nlol.utilities import utils_maya
from nlol.utilities.nlol_maya_logger import get_logger

reload(get_aligned_axis)
reload(limb_hinge_vector)
reload(utils_maya)
reload(create_control_groups)
reload(create_joint)
reload(create_locators)
reload(create_nurbs_curves)
reload(clean_constraints)
reload(create_ruler)

create_ctrl_grps = create_control_groups.create_ctrl_grps
cap = utils_maya.cap
snake_to_camel = utils_maya.snake_to_camel
add_divider_attribue = utils_maya.add_divider_attribue
parent_constr = clean_constraints.parent_constr
point_constr = clean_constraints.point_constr
orient_constr = clean_constraints.orient_constr
scale_constr = clean_constraints.scale_constr
create_attached_ruler = create_ruler.create_attached_ruler


class BipedLimbModule:
    """Create biped style limb rig based on joint selection in rig data toml file.
    Supports four main joints and twist joints.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list[str],
        upper_twist_joints: list[str],
        lower_twist_joints: list[str],
        main_object_names: list[str] = [],
        upper_twist_name: str = "",
        lower_twist_name: str = "",
        fk_ctrl_size: float = 1,
        ik_ctrl_size: float = 1,
        ik_hip_ctrl_size: float = 1.5,
        polevector_ctrl_size: float = 0.5,
        polevector_ctrl_distance: float = 75,
        switch_ctrl_size: float = 0.13,
        switch_ctrl_distance: float = 17,
        switch_ctrl_constraint: bool = False,
    ):
        """Initialize limb rig module.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: Extra string describing mirror side. Ex. "left", "right".
            main_joints: The main skinned joints.
            upper_twist_joints: Main skinned twist joints for upper limb segment.
            lower_twist_joints: Main skinned twist joints for lower limb segment.

            main_object_names: Main object names to be used instead of raw joint names.
            upper_twist_name: Main upper twist object name instead of raw joint names.
            lower_twist_name: Main lower twist object name instead of raw joint names.

            fk_ctrl_size: Size of fk controls.
            ik_ctrl_size: Size of main end limb ik control.
            polevector_ctrl_size: Size of ik hinge control (knee, elbow).
            polevector_ctrl_distance: Default distance hinge control placed from hinge joint.
            switch_ctrl_size: Fk ik blend control size.
            switch_ctrl_distance: Fk ik blend control distance from end limb joint.
            switch_ctrl_constraint: Whether to constrain switch control to limb by default.
        """
        self.logger = get_logger()

        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints
        self.upper_twist_joints = upper_twist_joints
        self.lower_twist_joints = lower_twist_joints

        self.main_object_names = main_object_names
        self.upper_twist_name = upper_twist_name
        self.lower_twist_name = lower_twist_name

        if self.main_object_names:
            if len(self.main_object_names) != len(self.main_joints):
                msg = "Should be same number of main_object_names as main_joints: "
                f'"{self.mod_name}, {self.mirr_side}"'
                self.logger.warning(msg)
        if not self.main_object_names:
            self.main_object_names = [
                f"upper{cap(self.mod_name)}",
                f"lower{cap(self.mod_name)}",
                f"end{cap(self.mod_name)}",
                f"extremity{cap(self.mod_name)}",
            ]
        if not self.upper_twist_name:
            self.upper_twist_name = f"upper{cap(self.mod_name)}Twist"
        if not self.lower_twist_name:
            self.lower_twist_name = f"lower{cap(self.mod_name)}Twist"

        self.fk_ctrl_size = fk_ctrl_size
        self.ik_ctrl_size = ik_ctrl_size
        self.ik_hip_ctrl_size = ik_hip_ctrl_size
        self.polevector_ctrl_size = polevector_ctrl_size
        self.polevector_ctrl_distance = polevector_ctrl_distance
        self.switch_ctrl_size = switch_ctrl_size
        self.switch_ctrl_distance = switch_ctrl_distance
        self.switch_ctrl_constraint = switch_ctrl_constraint

    def build(self) -> str:
        """Build the limb rig module.
        --------------------------------------------------

        Returns:
            Top group for all the limb objects.

        """
        failed_build_string = (
            f'Rig module "{self.mod_name}{self.mirr_side.rstrip("_")}" failed to build.'
        )

        # ---------- build rig module ----------
        try:
            if all(cmds.objExists(jnt) for jnt in self.main_joints):
                if self.query_main_axis() is None:
                    return None
                self.build_top_groups()
                self.build_fk_ik_joints()
                self.build_fk_controls()
                self.build_ik_controls()
                self.build_fk_ik_switch()
                self.build_twist_setup()
                self.build_soft_ik_setup()
            else:
                missing_jnts = [jnt for jnt in self.main_joints if not cmds.objExists(jnt)]
                error_msg = f"Missing main joints: {missing_jnts}\n{failed_build_string}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
        except Exception:
            self.logger.exception(failed_build_string)
            raise
        else:
            cmds.select(clear=True)  # clear remaining selection
            return self.limb_top_grp

    def query_main_axis(self) -> str | None:
        """Get down the chain limb axis.
        Query the main axis facing down the limb joint chain.
        """
        self.down_chain_axis = get_aligned_axis.axis_facing_child(
            object_parent=self.main_joints[0],
            object_child=self.main_joints[1],
        )
        if self.down_chain_axis not in ["x", "-x"]:
            error_msg = (
                f'Main axis pointing down the "{self.mod_name}{self.mirr_side}"'
                f' chain is "{self.down_chain_axis}".\n'
                'Main axis should be "x" or "-x".\n  '
                f'Rig module "{self.mod_name}{self.mirr_side}" did not build.',
            )
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        return self.down_chain_axis

    def build_top_groups(self):
        """Create top limb groups to parent controls and joints to."""
        # groups for organization
        self.limb_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}grp",
        )
        self.fk_limb_top_grp = cmds.group(
            empty=True,
            name=f"fk{cap(self.mod_name)}{self.mirr_side}grp",
        )
        self.ik_limb_top_grp = cmds.group(
            empty=True,
            name=f"ik{cap(self.mod_name)}{self.mirr_side}grp",
        )
        self.twist_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}Twist{self.mirr_side}grp",
        )
        self.twist_stretch_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}TwistStretch{self.mirr_side}grp",
        )
        self.soft_ik_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}SoftIk{self.mirr_side}grp",
        )
        cmds.parent(self.fk_limb_top_grp, self.limb_top_grp)
        cmds.parent(self.ik_limb_top_grp, self.limb_top_grp)
        cmds.parent(self.twist_top_grp, self.limb_top_grp)
        cmds.parent(self.twist_stretch_top_grp, self.limb_top_grp)
        cmds.parent(self.soft_ik_top_grp, self.limb_top_grp)

    def build_fk_ik_joints(self):
        """An fk ik blended joint chain.
        Create fk ik joint chains and blend with main joint chain.
        """
        fk_jnts = []
        ik_jnts = []
        for i, jnt in enumerate(self.main_joints):
            # -------------------------------------------------------------
            # -------------------- create fk ik chains --------------------
            fk_jnt = create_joint.single_joint(
                name=f"fk{cap(self.main_object_names[i])}{self.mirr_side}jnt",
                radius=5,
                color_rgb=(1.0, 0.0, 0.1),
                scale_compensate=False,
                parent_snap=jnt,
            )
            ik_jnt = create_joint.single_joint(
                name=f"ik{cap(self.main_object_names[i])}{self.mirr_side}jnt",
                radius=4,
                color_rgb=(1.0, 0.9, 0.1),
                scale_compensate=False,
                parent_snap=jnt,
            )
            # scale compensate off to avoid double scaling when global scaling
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)

            # scale constraint instead of blendColors scale
            # for proper control and global scale
            scale_constr(fk_jnt, jnt)
            scale_constr(ik_jnt, jnt)

            fk_jnts.append(fk_jnt)
            ik_jnts.append(ik_jnt)

        # parent fk ik joints into chains
        for i, jnt in enumerate(fk_jnts):
            if jnt != fk_jnts[0]:
                cmds.parent(jnt, fk_jnts[i - 1])
        for i, jnt in enumerate(ik_jnts):
            if jnt != ik_jnts[0]:
                cmds.parent(jnt, ik_jnts[i - 1])

        # ---------------------------------------------------------------------
        # -------------------- blend joint chains together --------------------
        translate_blend_nodes = []
        rotate_blend_nodes = []
        for fk_jnt, ik_jnt, jnt, obj_name in zip(
            fk_jnts,
            ik_jnts,
            self.main_joints,
            self.main_object_names,
            strict=False,
        ):
            # create blend color nodes
            tran_blend_node = cmds.createNode(
                "blendColors",
                name=f"{obj_name}Tran{self.mirr_side}blendColors",
            )
            rot_blend_node = cmds.createNode(
                "blendColors",
                name=f"{obj_name}Rot{self.mirr_side}blendColors",
            )
            # translate blend
            cmds.connectAttr(f"{fk_jnt}.translate", f"{tran_blend_node}.color1", force=True)
            cmds.connectAttr(f"{ik_jnt}.translate", f"{tran_blend_node}.color2", force=True)
            cmds.connectAttr(f"{tran_blend_node}.output", f"{jnt}.translate", force=True)
            # rotate blend
            cmds.connectAttr(f"{fk_jnt}.rotate", f"{rot_blend_node}.color1", force=True)
            cmds.connectAttr(f"{ik_jnt}.rotate", f"{rot_blend_node}.color2", force=True)
            cmds.connectAttr(f"{rot_blend_node}.output", f"{jnt}.rotate", force=True)

            translate_blend_nodes.append(tran_blend_node)
            rotate_blend_nodes.append(rot_blend_node)

        # parent top fk ik joints to locator constrained to main_joints parent
        # avoids parenting under main skeleton
        # accounts for needed blendColor node transformation offset
        main_joints_parent = cmds.listRelatives(self.main_joints[0], parent=True)
        if main_joints_parent:
            parent_loc = create_locators.locator_snap_parent(
                objects=main_joints_parent,
                locator_name=f"{self.main_object_names[0]}Offset{self.mirr_side}loc",
                local_scale=(5, 5, 5),
            )[0]
            cmds.parent(fk_jnts[0], parent_loc)
            cmds.parent(ik_jnts[0], parent_loc)

            # parent and hide joint locator and joints
            cmds.parent(parent_loc, self.limb_top_grp)
            cmds.setAttr(f"{parent_loc}.visibility", 0)
        else:
            for jnt in [fk_jnts[0], ik_jnts[0]]:
                cmds.parent(jnt, self.limb_top_grp)
                cmds.setAttr(f"{jnt}.visibility", 0)

        # assign instance variables
        self.fk_jnts = fk_jnts
        self.ik_jnts = ik_jnts
        self.translate_blend_nodes = translate_blend_nodes
        self.rotate_blend_nodes = rotate_blend_nodes

    def build_fk_controls(self):
        """Create fk limb controls. Constrain fk controls to fk joints."""
        fk_ctrl_grps = []
        fk_ctrls = []
        # create control curves
        for i, jnt in enumerate(self.fk_jnts):
            # ----- control curve -----
            fk_ctrl = create_nurbs_curves.CreateCurves(
                name=f"fk{cap(self.main_object_names[i])}{self.mirr_side}ctrl",
                size=self.fk_ctrl_size,
                color_rgb=(1, 0, 0),
            ).box_curve()

            # ----- control group -----
            fk_ctrl_grp = create_ctrl_grps(fk_ctrl)[0]

            # ----- snap control group to joint -----
            cmds.matchTransform(fk_ctrl_grp, jnt)

            # parent and scale constrain controls to fk joints
            parent_constr(fk_ctrl, jnt)
            scale_constr(fk_ctrl, jnt)

            # lock and hide attributes
            cmds.setAttr(f"{fk_ctrl}.visibility", lock=True, keyable=False, channelBox=False)

            # create a list of groups for parenting
            fk_ctrl_grps.append(fk_ctrl_grp)
            fk_ctrls.append(fk_ctrl)

        # parent controls and groups together
        # parent 2nd group to 1st control, 3rd group to 2nd control, etc.
        for grp, ctrl in zip(fk_ctrl_grps[1:], fk_ctrls, strict=False):
            cmds.parent(grp, ctrl)

        # parent under main fk group
        cmds.parent(fk_ctrl_grps[0], self.fk_limb_top_grp)

        # assign instance variables
        self.fk_ctrls = fk_ctrls

    def build_ik_controls(self):
        """Create ik limb controls. Create ik handle. Create pole vector constraint."""
        # ----------------------------------------------------------
        # -------------------- create ik handle --------------------
        limb_ik_handle = cmds.ikHandle(
            name=f"{self.mod_name}{self.mirr_side}ikHandkle",
            startJoint=self.ik_jnts[0],
            endEffector=self.ik_jnts[2],
        )
        cmds.setAttr(f"{limb_ik_handle[0]}.visibility", 0)
        cmds.setAttr(f"{limb_ik_handle[0]}.poleVector", 0, 0, 0)

        # rename ikHandle effector
        cmds.rename(limb_ik_handle[1], f"{limb_ik_handle[0]}Effector")

        # parent ik handle to module top grp
        cmds.parent(limb_ik_handle[0], self.ik_limb_top_grp)

        # ------------------------------------------------------------------
        # -------------------- create ik handle control --------------------
        # create curve box
        ik_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.main_object_names[2])}{self.mirr_side}ctrl",
            size=self.ik_ctrl_size,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()

        # ----- control group -----
        ik_ctrl_grp = create_ctrl_grps(ik_ctrl)[0]

        # ----- snap control group to joint -----
        cmds.matchTransform(ik_ctrl_grp, self.ik_jnts[2])

        # constrain to ikHandle and ik end joint
        limb_ik_handle_const = point_constr(ik_ctrl, limb_ik_handle[0])
        limb_ik_end_rot_const = orient_constr(ik_ctrl, self.ik_jnts[2])
        limb_ik_end_scale_const = scale_constr(ik_ctrl, self.ik_jnts[2])

        # parent to top group to organize
        cmds.parent(ik_ctrl_grp, self.ik_limb_top_grp)

        # ---------------------------------------------------------------
        # -------------------- create ik hip control --------------------
        # create box curve
        ik_hip_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.main_object_names[0])}{self.mirr_side}ctrl",
            size=self.ik_hip_ctrl_size,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()

        # ----- control group -----
        ik_hip_ctrl_grp, _, ik_hip_ctrl_prntswtch_grp, _ = create_ctrl_grps(ik_hip_ctrl)

        # ----- snap control group to joint -----
        cmds.matchTransform(ik_hip_ctrl_grp, self.ik_jnts[0])

        # parent grp to global grp to organize
        cmds.parent(ik_hip_ctrl_grp, self.ik_limb_top_grp)

        # constrain hip joint to control
        point_constr(ik_hip_ctrl, self.ik_jnts[0])
        scale_constr(ik_hip_ctrl, self.ik_jnts[0])

        # ----------------------------------------------------------------------
        # -------------------- create simple ik toe control --------------------
        ik_toe_ctrl = None
        ik_toe_ctrl_grp = None
        if len(self.ik_jnts) > 3:
            ik_toe_ctrl = create_nurbs_curves.CreateCurves(
                name=f"ik{cap(self.main_object_names[3])}{self.mirr_side}ctrl",
                size=1,
                color_rgb=(0.1, 1.0, 0.0),
            ).box_curve()

            # ----- control group -----
            ik_toe_ctrl_grp = create_ctrl_grps(ik_toe_ctrl)[0]

            # ----- snap control group to joint -----
            cmds.matchTransform(ik_toe_ctrl_grp, self.ik_jnts[3])

            cmds.parent(ik_toe_ctrl_grp, ik_ctrl)

            orient_constr(ik_toe_ctrl, self.ik_jnts[3])
            scale_constr(ik_toe_ctrl, self.ik_jnts[3])

        # -----------------------------------------------------------------------
        # -------------------- create ik pole vector control --------------------
        # create pyramid curve
        polevector_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.mod_name)}PoleVector{self.mirr_side}ctrl",
            size=self.polevector_ctrl_size,
            color_rgb=(1.0, 1.0, 0.0),
        ).pyramid_curve()

        # ----- control group -----
        polevector_ctrl_grp = create_ctrl_grps(polevector_ctrl)[0]

        # ---------- pole vector control transformation ----------
        limb_hinge_vector.apply_hinge_vector(
            limb_joints=self.ik_jnts[0:4],
            control_object=polevector_ctrl_grp,
            control_object_distance=self.polevector_ctrl_distance,
        )

        # connect pole vector constraint
        cmds.poleVectorConstraint(polevector_ctrl, limb_ik_handle[0])

        # parent to top grp
        cmds.parent(polevector_ctrl_grp, self.ik_limb_top_grp)

        # ------------------------------------------------------------------
        # -------------------- lock and hide attributes --------------------
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{ik_hip_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{ik_hip_ctrl}.scale{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{polevector_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{polevector_ctrl}.scale{axis}", **lock_hide_kwargs)
            if ik_toe_ctrl:
                cmds.setAttr(f"{ik_toe_ctrl}.translate{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{ik_ctrl}.visibility", **lock_hide_kwargs)
        cmds.setAttr(f"{ik_hip_ctrl}.visibility", **lock_hide_kwargs)
        cmds.setAttr(f"{polevector_ctrl}.visibility", **lock_hide_kwargs)
        if ik_toe_ctrl:
            cmds.setAttr(f"{ik_toe_ctrl}.visibility", **lock_hide_kwargs)

        # assign instance variables
        self.limb_ik_handle = limb_ik_handle[0]
        self.limb_ik_handle_const = limb_ik_handle_const
        self.limb_ik_end_rot_const = limb_ik_end_rot_const
        self.limb_ik_end_scale_const = limb_ik_end_scale_const
        self.ik_ctrl = ik_ctrl
        self.ik_hip_ctrl = ik_hip_ctrl
        self.ik_hip_ctrl_prntswtch_grp = ik_hip_ctrl_prntswtch_grp
        self.polevector_ctrl = polevector_ctrl
        self.ik_toe_ctrl_grp = ik_toe_ctrl_grp

    def build_fk_ik_switch(self):
        """Create fk ik switch control."""
        # ---------- create control curve object ----------
        # create sphere curve
        switch_ctrl = create_nurbs_curves.CreateCurves(
            name=f"{self.mod_name}Swch{self.mirr_side}ctrl",
            size=self.switch_ctrl_size,
            color_rgb=(0.0, 0.0, 0.0),
        ).sphere_curve()

        # ----- control group -----
        switch_ctrl_grp = create_ctrl_grps(switch_ctrl)[0]

        # ---------- setup twist ctrl position and constraint ----------
        if self.switch_ctrl_constraint:
            # move control in rear joint axis direction
            rear_facing_axis = get_aligned_axis.axis_facing_direction(
                object=self.main_joints[2],
                world_space_direction="-z",
            )
            direction_multiplier = -1 if rear_facing_axis[0] == "-" else 1
            rear_facing_axis = rear_facing_axis.lstrip("-").upper()
            cmds.setAttr(
                f"{switch_ctrl}.translate{rear_facing_axis}",
                direction_multiplier * self.switch_ctrl_distance,
            )
            # pivot to origin
            cmds.xform(switch_ctrl, worldSpace=True, pivots=(0, 0, 0))
            cmds.makeIdentity(switch_ctrl, apply=True)

            # snap to end limb joint
            cmds.matchTransform(switch_ctrl_grp, self.main_joints[2])

            # parent and scale constrain switch ctrl to end limb joint
            parent_constr(self.main_joints[2], switch_ctrl_grp)
            scale_constr(self.main_joints[2], switch_ctrl_grp)

        # ---------- add fk ik blend attribute ----------
        add_divider_attribue(control_name=switch_ctrl, divider_amount=5)
        cmds.addAttr(
            switch_ctrl,
            longName="fkIkBlend",
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )

        # ----- connect switch control to blend nodes -----
        for node_translate, node_rotate in zip(
            self.translate_blend_nodes,
            self.rotate_blend_nodes,
            strict=False,
        ):
            cmds.connectAttr(
                f"{switch_ctrl}.fkIkBlend",
                f"{node_translate}.blender",
                force=True,
            )
            cmds.connectAttr(
                f"{switch_ctrl}.fkIkBlend",
                f"{node_rotate}.blender",
                force=True,
            )

        # ----- connect switch control to visibility -----
        # 1 is fk, 0 is ik
        # use set driven keys
        cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 0)
        cmds.setAttr(f"{self.ik_limb_top_grp}.visibility", 1)
        cmds.setAttr(f"{self.fk_limb_top_grp}.visibility", 0)
        cmds.setDrivenKeyframe(
            f"{self.ik_limb_top_grp}.visibility",
            currentDriver=f"{switch_ctrl}.fkIkBlend",
        )
        cmds.setDrivenKeyframe(
            f"{self.fk_limb_top_grp}.visibility",
            currentDriver=f"{switch_ctrl}.fkIkBlend",
        )

        cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 1)
        cmds.setAttr(f"{self.ik_limb_top_grp}.visibility", 0)
        cmds.setAttr(f"{self.fk_limb_top_grp}.visibility", 1)
        cmds.setDrivenKeyframe(
            f"{self.ik_limb_top_grp}.visibility",
            currentDriver=f"{switch_ctrl}.fkIkBlend",
        )
        cmds.setDrivenKeyframe(
            f"{self.fk_limb_top_grp}.visibility",
            currentDriver=f"{switch_ctrl}.fkIkBlend",
        )

        # ----- connect switch control scale constraints -----
        for fk_jnt, ik_jnt, jnt in zip(self.fk_jnts, self.ik_jnts, self.main_joints, strict=False):
            cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 1)
            cmds.setAttr(f"{jnt}ScaleConstraint.{fk_jnt}W0", 1)
            cmds.setAttr(f"{jnt}ScaleConstraint.{ik_jnt}W1", 0)
            cmds.setDrivenKeyframe(
                f"{jnt}ScaleConstraint.{fk_jnt}W0",
                currentDriver=f"{switch_ctrl}.fkIkBlend",
            )
            cmds.setDrivenKeyframe(
                f"{jnt}ScaleConstraint.{ik_jnt}W1",
                currentDriver=f"{switch_ctrl}.fkIkBlend",
            )

            cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 0)
            cmds.setAttr(f"{jnt}ScaleConstraint.{fk_jnt}W0", 0)
            cmds.setAttr(f"{jnt}ScaleConstraint.{ik_jnt}W1", 1)
            cmds.setDrivenKeyframe(
                f"{jnt}ScaleConstraint.{fk_jnt}W0",
                currentDriver=f"{switch_ctrl}.fkIkBlend",
            )
            cmds.setDrivenKeyframe(
                f"{jnt}ScaleConstraint.{ik_jnt}W1",
                currentDriver=f"{switch_ctrl}.fkIkBlend",
            )

        # ---------- visibility, parenting, other ----------
        # lock and hide unused attributes for switch control
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{switch_ctrl}.translate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{switch_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{switch_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{switch_ctrl}.visibility", **lock_hide_kwargs)

        # parent to top grp
        cmds.parent(switch_ctrl_grp, self.limb_top_grp)

        # assign instance variables
        self.switch_ctrl = switch_ctrl

    def build_twist_setup(self):
        """Verify twist joints exist then execute main twist setup."""
        # ----- build twist joint setup -----
        twist_setup_objects = [
            (
                self.upper_twist_joints,
                self.upper_twist_name,
                self.main_joints[0],
                self.main_joints[1],
            ),
            (
                self.lower_twist_joints,
                self.lower_twist_name,
                self.main_joints[1],
                self.main_joints[2],
            ),
        ]
        for twist_jnts, twist_name, strt_jnt, end_jnt in twist_setup_objects:
            if [jnt for jnt in twist_jnts if jnt]:  # check for empty string
                if all(cmds.objExists(jnt) for jnt in twist_jnts):  # check if in scene
                    self.build_main_twist_setup(twist_jnts, twist_name, strt_jnt, end_jnt)
                else:
                    missing_jnts = [jnt for jnt in twist_jnts if not cmds.objExists(jnt)]
                    warning_msg = (
                        f"Missing twist joints: {missing_jnts}\nTwist joint setup failed to run."
                    )
                    self.logger.warning(warning_msg)

                    cmds.delete(self.twist_top_grp)
                    cmds.delete(self.twist_stretch_top_grp)
                    return

    def build_main_twist_setup(
        self,
        twist_jnts: list[str],
        twist_name: str,
        start_segment_jnt: str,
        end_segment_jnt: str,
    ) -> None:
        """Create twist joint setup for a limb segment.
        Example of twist limb segment: shoulder to elbow, knee to ankle, etc.
        The limb segment refers to joints from the original skeleton.

        Args:
            twist_jnts: The limbs twist joints for the segment.
            twist_name: The name to add for each new twist joint created.
            start_segment_jnt: The first joint in the limb segment.
            end_segment_jnt: The last joint in the limb segment.

        """
        # -------------------- twist joints --------------------
        # list of main limb joints that make up the segment being twisted
        limb_segment_jnts = [start_segment_jnt, *twist_jnts, end_segment_jnt]

        # ---------- start twist joint ----------
        # for skinning spline curve to
        start_twist_jnt = create_joint.single_joint(
            name=f"{twist_name}Start{self.mirr_side}jnt",
            radius=7,
            color_rgb=(0.0, 0.0, 0.0),
            scale_compensate=False,
            parent_snap=start_segment_jnt,
        )
        # constrain to first joint of the limb segment
        parent_constr(start_segment_jnt, start_twist_jnt)

        # ---------- end twist joint ----------
        end_twist_jnt = create_joint.single_joint(
            name=f"{twist_name}End{self.mirr_side}jnt",
            radius=7,
            color_rgb=(0.0, 0.0, 0.0),
            scale_compensate=False,
            parent_snap=end_segment_jnt,
            axis_parent_snap=start_segment_jnt,
        )
        # parent end to start twist joint
        # cleaner rotate values for end_twist_jnt rotate blending
        cmds.parent(end_twist_jnt, start_twist_jnt)

        # point constraint to last joint of the limb segment
        point_constr(end_segment_jnt, end_twist_jnt)
        # rotate parent constraint blend for controlling twist weight
        end_twist_jnt_rot_const = parent_constr(
            start_segment_jnt,  # default static rotation
            end_twist_jnt,
            skip_tran=True,
            offset=True,
        )
        parent_constr(
            end_segment_jnt,  # end limb rotation
            end_twist_jnt,
            skip_tran=True,
            offset=True,
        )
        cmds.setAttr(f"{end_twist_jnt_rot_const}.interpType", 2)  # shortest

        # ---------- joints for spline twist ----------
        spline_jnts = []
        for i, jnt in enumerate(limb_segment_jnts, 1):
            spline_joint = create_joint.single_joint(
                name=f"{twist_name}Spline{self.mirr_side}{i:02d}_jnt",
                radius=3,
                color_rgb=(1.0, 1.0, 1.0),
                scale_compensate=False,
                parent_snap=jnt,
                axis_parent_snap=start_segment_jnt,
            )
            spline_jnts.append(spline_joint)
            # turn off scale compensate for limb segmant twist joints
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)

        # parent spline joints together
        for i, jnt in enumerate(spline_jnts):
            if jnt != spline_jnts[0]:
                cmds.parent(jnt, spline_jnts[i - 1])

        # constrain spline joints to limb segment twist joints
        for spline_jnt, limb_jnt in zip(spline_jnts, limb_segment_jnts, strict=False):
            # first and last limb segment joint are already constrained
            if spline_jnt not in (spline_jnts[0], spline_jnts[-1]):
                # point and orient constraint work better than parent constraint for global scaling
                point_constr(spline_jnt, limb_jnt, offset=True)
                orient_constr(spline_jnt, limb_jnt, offset=True)

        # -------------------- create ik spline for arm twist --------------------
        twist_crv_start = cmds.xform(
            start_twist_jnt,
            query=True,
            worldSpace=True,
            rotatePivot=True,
        )
        twist_crv_end = cmds.xform(end_twist_jnt, query=True, worldSpace=True, rotatePivot=True)
        twist_crv = cmds.curve(
            name=f"{twist_name}{self.mirr_side}ikHandleCrv",
            degree=1,
            point=[twist_crv_start, twist_crv_end],
        )
        # create ik spline handle
        limb_twist_ikHandle = cmds.ikHandle(
            name=f"{twist_name}{self.mirr_side}ikHandle",
            startJoint=spline_jnts[0],
            endEffector=spline_jnts[-1],
            solver="ikSplineSolver",
            createCurve=False,
            curve=twist_crv,
        )
        cmds.setAttr(f"{limb_twist_ikHandle[0]}.poleVector", 0, 0, 0)
        cmds.rename(limb_twist_ikHandle[1], f"{limb_twist_ikHandle[0]}Effector")

        # ---------- ik spline handle advanced twist controls ----------
        cmds.setAttr(limb_twist_ikHandle[0] + ".dTwistControlEnable", 1)
        cmds.setAttr(limb_twist_ikHandle[0] + ".dWorldUpType", 4)
        cmds.setAttr(limb_twist_ikHandle[0] + ".dWorldUpAxis", 4)

        # switch forward axis "x" to negative if needed, default is positive "x"
        if self.down_chain_axis == "-x":
            cmds.setAttr(f"{limb_twist_ikHandle[0]}.dForwardAxis", 1)

        cmds.setAttr(f"{limb_twist_ikHandle[0]}.dWorldUpVector", 0, 0, -1)
        cmds.setAttr(f"{limb_twist_ikHandle[0]}.dWorldUpVectorEnd", 0, 0, -1)
        cmds.connectAttr(
            f"{start_twist_jnt}.worldMatrix[0]",
            f"{limb_twist_ikHandle[0]}.dWorldUpMatrix",
        )
        cmds.connectAttr(
            f"{end_twist_jnt}.worldMatrix[0]",
            f"{limb_twist_ikHandle[0]}.dWorldUpMatrixEnd",
        )

        # ---------- skin spline curve to start end joints ----------
        twist_skin_cluster = cmds.skinCluster(
            start_twist_jnt,
            end_twist_jnt,
            twist_crv,
            n=f"{twist_name}{self.mirr_side}skinCluster",
        )[0]
        # reskin curve to avoid maya skinning anomalies
        cmds.skinPercent(
            twist_skin_cluster,
            f"{twist_crv}.cv[0]",
            transformValue=[(start_twist_jnt, 1.0), (end_twist_jnt, 0.0)],
        )
        cmds.skinPercent(
            twist_skin_cluster,
            f"{twist_crv}.cv[1]",
            transformValue=[(start_twist_jnt, 0.0), (end_twist_jnt, 1.0)],
        )

        # ---------- setup rotate blend for twist weight control ----------
        # add twist weights attributes to switch control
        # add divider attribute
        if not cmds.objExists(f"{self.switch_ctrl}.{10 * '_'}"):
            add_divider_attribue(control_name=self.switch_ctrl, divider_amount=10)
        # add weight blend attribute
        twist_weight_attr = snake_to_camel(f"{twist_name}{self.mirr_side}weight")
        cmds.addAttr(
            self.switch_ctrl,
            longName=twist_weight_attr,
            defaultValue=0.5,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        reverse_node = cmds.shadingNode(
            "reverse",
            asUtility=True,
            n=f"{twist_name}{self.mirr_side}reverse",
        )
        cmds.connectAttr(
            f"{self.switch_ctrl}.{twist_weight_attr}",
            f"{reverse_node}.inputX",
            force=True,
        )
        cmds.connectAttr(
            f"{reverse_node}.outputX",
            f"{end_twist_jnt_rot_const}.{start_segment_jnt}W0",
            force=True,
        )
        cmds.connectAttr(
            f"{self.switch_ctrl}.{twist_weight_attr}",
            f"{end_twist_jnt_rot_const}.{end_segment_jnt}W1",
            force=True,
        )

        # ---------- parent and hide under main group ----------
        cmds.parent(start_twist_jnt, self.twist_top_grp)
        cmds.parent(spline_jnts[0], self.twist_top_grp)
        cmds.parent(twist_crv, self.twist_top_grp)
        cmds.parent(limb_twist_ikHandle[0], self.twist_top_grp)

        cmds.setAttr(f"{self.twist_top_grp}.visibility", 0)

        # ---------- add stretch ----------
        # main axis twist joint stretch
        self.build_twist_stretch(
            twist_name,
            start_segment_jnt,
            end_segment_jnt,
            spline_jnts,
        )

    def build_twist_stretch(
        self,
        twist_name: str,
        start_segment_jnt: str,
        end_segment_jnt: str,
        stretch_jnts: str,
    ) -> None:
        """Add stretch to the twist joints along the main axis.

        Args:
            twist_name: Same as _build_twist_setup().
            start_segment_jnt: Same as _build_twist_setup().
            end_segment_jnt: Same as _build_twist_setup().
            stretch_jnts: Joints to be stretched.
                Stretched meaning moved along main axis.

        """
        # ----- create upper limb ruler -----
        ruler_shape, ruler_transform, ruler_loc_01, ruler_loc_02, *_ = create_attached_ruler(
            name=f"{twist_name}Ruler{self.mirr_side}",
            ruler_start_object=start_segment_jnt,
            ruler_end_object=end_segment_jnt,
        )
        # ----- create limb segment distance ratio node -----
        limb_distance_ratio = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{twist_name}DistanceRatio{self.mirr_side}multiplyDivide",
        )
        cmds.setAttr(f"{limb_distance_ratio}.operation", 2)  # divide operation
        cmds.connectAttr(
            f"{ruler_shape}.distance",
            f"{limb_distance_ratio}.input1X",
            force=True,
        )
        ruler_length = cmds.getAttr(f"{ruler_shape}.distance")
        cmds.setAttr(f"{limb_distance_ratio}.input2X", ruler_length)
        # ----- create stretch multiply node for each strech jnt -----
        # multiply joint length by limb distance ratio
        for jnt in stretch_jnts[1:]:
            jnt_length_multiply = cmds.shadingNode(
                "multiplyDivide",
                asUtility=True,
                name=f"{jnt}_multiplyDivide",
            )
            cmds.connectAttr(
                f"{limb_distance_ratio}.outputX",
                f"{jnt_length_multiply}.input1X",
                force=True,
            )
            jnt_length = cmds.getAttr(f"{jnt}.translateX")
            cmds.setAttr(f"{jnt_length_multiply}.input2X", jnt_length)
            # connect jnt_length_multiply to jnt
            cmds.connectAttr(
                f"{jnt_length_multiply}.outputX",
                f"{jnt}.translateX",
                force=True,
            )

        # ----- group for organization -----
        cmds.parent(ruler_transform, self.twist_stretch_top_grp)
        cmds.parent(ruler_loc_01, self.twist_stretch_top_grp)
        cmds.parent(ruler_loc_02, self.twist_stretch_top_grp)
        cmds.setAttr(f"{self.twist_stretch_top_grp}.visibility", 0)

    def build_soft_ik_setup(self, use_expression: bool = False) -> None:
        """Create soft ik setup.

        Args:
            use_expression: Use expression instead of nodes for exponential curve setup.
                Expression useful for testing.

        """
        # ----- distance between start joint and ik control -----
        ruler_shape, ruler_transform, ruler_loc_01, ruler_loc_02, _, ruler_loc_02_const, *_ = (
            create_attached_ruler(
                name=f"{self.mod_name}SoftIkRuler{self.mirr_side}",
                ruler_start_object=self.ik_hip_ctrl,
                ruler_end_object=self.ik_ctrl,
            )
        )

        # ----- create soft ik joints -----
        soft_ik_jnts = []
        for i in range(2):
            x_pos = [0, 50]
            x_rad = [5, 2.5]
            jnt = create_joint.single_joint(
                name=f"{self.mod_name}SoftIk{self.mirr_side}{i + 1:02d}_jnt",
                radius=x_rad[i],
                color_rgb=(1.0, 0.4, 0.0),
                scale_compensate=False,
                position=(x_pos[i], 0, 0),
            )
            soft_ik_jnts.append(jnt)
        cmds.parent(soft_ik_jnts[1], soft_ik_jnts[0])

        # ----- ik handle with single-chain solver -----
        soft_ik_handle = cmds.ikHandle(
            name=f"{self.mod_name}SoftIk{self.mirr_side}ikHandle",
            startJoint=soft_ik_jnts[0],
            endEffector=soft_ik_jnts[1],
            solver="ikSCsolver",
        )
        cmds.rename(soft_ik_handle[1], f"{soft_ik_handle[0]}Effector")
        cmds.setAttr(f"{soft_ik_handle[0]}.snapEnable", 0)

        # ----- position soft ik joint chain and ik handle -----
        top_limb_position = cmds.xform(
            self.ik_jnts[0],
            worldSpace=True,
            query=True,
            translation=True,
        )
        cmds.xform(soft_ik_jnts[0], worldSpace=True, translation=top_limb_position)
        ik_ctrl_position = cmds.xform(
            self.ik_ctrl,
            worldSpace=True,
            query=True,
            translation=True,
        )
        cmds.xform(soft_ik_handle[0], worldSpace=True, translation=ik_ctrl_position)
        soft_ik_handle_const = point_constr(
            self.ik_ctrl,
            soft_ik_handle[0],
            offset=True,
        )

        # ----- position soft ik end joint -----
        # straight distance from start to end limb joint
        ik_limb_span = cmds.getAttr(f"{ruler_shape}.distance")
        cmds.setAttr(f"{soft_ik_jnts[1]}.translateX", ik_limb_span)
        # ----- constrain limb ik handle to soft ik end joint -----
        cmds.delete(self.limb_ik_handle_const)
        ik_handle_constraint = point_constr(
            soft_ik_jnts[1],
            self.limb_ik_handle,
            offset=True,
        )
        # ----- constrain soft ik start joint to ik hip control -----
        point_constr(self.ik_hip_ctrl, soft_ik_jnts[0], offset=True)

        # ---------- create soft ik attributes ----------
        soft_ik_divider_name = "____Soft_Ik____"
        cmds.addAttr(
            self.ik_ctrl,
            longName=soft_ik_divider_name,
            niceName=soft_ik_divider_name,
            attributeType="enum",
            enumName="----------",
        )
        cmds.setAttr(f"{self.ik_ctrl}.{soft_ik_divider_name}", channelBox=True)
        # depending on rig, animators adjust values to achieve desired result
        # example values: 0.035 soft, 3 falloff. 0.02, 2. 0.01, 1.
        # higher falloffs such as 5 or 10 may also work well
        cmds.addAttr(
            self.ik_ctrl,
            longName="soft",
            defaultValue=0,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        cmds.addAttr(
            self.ik_ctrl,
            longName="softFalloff",
            defaultValue=3,
            minValue=0.01,
            maxValue=20,
            keyable=True,
        )

        # ----- group for organization -----
        cmds.parent(ruler_transform, self.soft_ik_top_grp)
        cmds.parent(ruler_loc_01, self.soft_ik_top_grp)
        cmds.parent(ruler_loc_02, self.soft_ik_top_grp)
        cmds.parent(soft_ik_jnts[0], self.soft_ik_top_grp)
        cmds.parent(soft_ik_handle[0], self.soft_ik_top_grp)
        cmds.setAttr(f"{self.soft_ik_top_grp}.visibility", 0)

        # ----- assign instance variables -----
        self.soft_ik_ruler = ruler_shape
        self.soft_ik_jnts = soft_ik_jnts
        self.limb_ik_handle_const = ik_handle_constraint  # reassign
        self.soft_ik_handle = soft_ik_handle[0]
        self.soft_ik_handle_const = soft_ik_handle_const
        self.soft_ik_ruler_end = ruler_loc_02
        self.soft_ik_ruler_end_const = ruler_loc_02_const

        # ----- create soft ik exponential curve -----
        ik_jnt_mid_pos_x = cmds.getAttr(f"{self.ik_jnts[1]}.translateX")
        ik_jnt_end_pos_x = cmds.getAttr(f"{self.ik_jnts[2]}.translateX")
        self.limb_chain_length = abs(ik_jnt_mid_pos_x + ik_jnt_end_pos_x)
        if use_expression:
            self.soft_ik_expression()
        else:
            self.soft_ik_nodes()

    def soft_ik_expression(self):
        """Create soft ik exponential curve logic with expression."""
        cmds.expression(
            s=f"float $limb_dist = {self.limb_chain_length};\n"
            f"float $soft_dist_excess = {self.ik_ctrl}.soft;\n"
            "float $soft_dist = $limb_dist * (1-$soft_dist_excess);\n"
            f"float $ik_ctrl_dist = {self.soft_ik_ruler}.distance;\n"
            f"float $soft_falloff = {self.ik_ctrl}.softFalloff;\n"
            "\n"
            "if ($ik_ctrl_dist > $soft_dist)\n"
            f"    {self.soft_ik_jnts[1]}.translateX = $limb_dist * "
            "(1-($soft_dist_excess * exp(-(($ik_ctrl_dist-$soft_dist)/$soft_falloff))));\n"
            "else\n"
            f"    {self.soft_ik_jnts[1]}.translateX = $ik_ctrl_dist;\n",
            n=f"{self.mod_name}SoftIk{self.mirr_side}expression",
        )

    def soft_ik_nodes(self):
        """Create soft ik exponential curve logic with nodes.
        Also, added global scale ratio nodes not in expression.
        """
        # ----------
        distglobalscale_node = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}DistGlobalScale{self.mirr_side}multiplyDivide",
        )
        cmds.setAttr(f"{distglobalscale_node}.input1X", self.limb_chain_length)
        cmds.connectAttr(
            f"{self.ik_hip_ctrl_prntswtch_grp}.scaleX",
            f"{distglobalscale_node}.input2X",
        )
        # ----------
        oneminus_softdistexcess_node = cmds.shadingNode(
            "plusMinusAverage",
            asUtility=True,
            name=f"{self.mod_name}OneMinusSoftDistExcess{self.mirr_side}plusMinusAverage",
        )
        cmds.setAttr(f"{oneminus_softdistexcess_node}.operation", 2)  # subtract
        cmds.setAttr(f"{oneminus_softdistexcess_node}.input1D[0]", 1)
        cmds.connectAttr(f"{self.ik_ctrl}.soft", f"{oneminus_softdistexcess_node}.input1D[1]")
        # ----------
        softdist_node = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}SoftDist{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(f"{distglobalscale_node}.outputX", f"{softdist_node}.input1X")
        cmds.connectAttr(f"{oneminus_softdistexcess_node}.output1D", f"{softdist_node}.input2X")
        # ----------
        ikctrldist_minus_softdist_node = cmds.shadingNode(
            "plusMinusAverage",
            asUtility=True,
            name=f"{self.mod_name}IkCtrlDistMinusSoftDist{self.mirr_side}plusMinusAverage",
        )
        cmds.setAttr(f"{ikctrldist_minus_softdist_node}.operation", 2)  # subtract
        cmds.connectAttr(
            f"{self.soft_ik_ruler}.distance",
            f"{ikctrldist_minus_softdist_node}.input1D[0]",
        )
        cmds.connectAttr(
            f"{softdist_node}.outputX",
            f"{ikctrldist_minus_softdist_node}.input1D[1]",
        )
        # ----------
        falloff_globalscale_node = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}FalloffGlobalScale{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(
            f"{self.ik_hip_ctrl_prntswtch_grp}.scaleX",
            f"{falloff_globalscale_node}.input1X",
        )
        cmds.connectAttr(
            f"{self.ik_ctrl}.softFalloff",
            f"{falloff_globalscale_node}.input2X",
        )
        # ----------
        softfalloff_divide_node = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}SoftFalloffDivide{self.mirr_side}multiplyDivide",
        )
        cmds.setAttr(f"{softfalloff_divide_node}.operation", 2)  # divide
        cmds.connectAttr(
            f"{ikctrldist_minus_softdist_node}.output1D",
            f"{softfalloff_divide_node}.input1X",
        )
        cmds.connectAttr(
            f"{falloff_globalscale_node}.outputX",
            f"{softfalloff_divide_node}.input2X",
        )
        # ----------
        make_negative_node = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}MakeNegative{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(f"{softfalloff_divide_node}.outputX", f"{make_negative_node}.input1X")
        cmds.setAttr(f"{make_negative_node}.input2X", -1)
        # ----------
        exponential_curve_node = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}ExponentialCurve{self.mirr_side}multiplyDivide",
        )
        cmds.setAttr(f"{exponential_curve_node}.operation", 3)  # power
        cmds.setAttr(f"{exponential_curve_node}.input1X", 2.718281828)  # eulers number
        cmds.connectAttr(f"{make_negative_node}.outputX", f"{exponential_curve_node}.input2X")
        # ----------
        softexcess_mult_expcurve_node = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}SoftExcessMultExpCurve{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(f"{self.ik_ctrl}.soft", f"{softexcess_mult_expcurve_node}.input1X")
        cmds.connectAttr(
            f"{exponential_curve_node}.outputX",
            f"{softexcess_mult_expcurve_node}.input2X",
        )
        # ----------
        main_equation_mid_node = cmds.shadingNode(
            "plusMinusAverage",
            asUtility=True,
            name=f"{self.mod_name}MainEquationMid{self.mirr_side}plusMinusAverage",
        )
        cmds.setAttr(f"{main_equation_mid_node}.operation", 2)  # subtract
        cmds.setAttr(f"{main_equation_mid_node}.input1D[0]", 1)
        cmds.connectAttr(
            f"{softexcess_mult_expcurve_node}.outputX",
            f"{main_equation_mid_node}.input1D[1]",
        )
        # ----------
        main_equation_end_node = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}MainEquationEnd{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(f"{distglobalscale_node}.outputX", f"{main_equation_end_node}.input1X")
        cmds.connectAttr(
            f"{main_equation_mid_node}.output1D",
            f"{main_equation_end_node}.input2X",
        )
        # ----------
        ifgreaterthan_node = cmds.shadingNode(
            "condition",
            asUtility=True,
            name=f"{self.mod_name}IfGreaterThan{self.mirr_side}condition",
        )
        cmds.setAttr(f"{ifgreaterthan_node}.operation", 2)  # greater than
        cmds.connectAttr(f"{self.soft_ik_ruler}.distance", f"{ifgreaterthan_node}.firstTerm")
        cmds.connectAttr(f"{self.soft_ik_ruler}.distance", f"{ifgreaterthan_node}.colorIfFalseR")
        cmds.connectAttr(f"{softdist_node}.outputX", f"{ifgreaterthan_node}.secondTerm")
        cmds.connectAttr(f"{main_equation_end_node}.outputX", f"{ifgreaterthan_node}.colorIfTrueR")
        cmds.connectAttr(f"{ifgreaterthan_node}.outColorR", f"{self.soft_ik_jnts[1]}.translateX")
