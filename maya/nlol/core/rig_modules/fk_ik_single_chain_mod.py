from maya import cmds
from nlol.core import general_utils
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_locators,
    create_nurbs_curves,
    create_ruler,
)
from nlol.core.rig_tools import get_aligned_axis
from nlol.core.standalone import small_functions
from nlol.utilities.nlol_maya_logger import get_logger

create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
point_constr = clean_constraints.point_constr
orient_constr = clean_constraints.orient_constr
scale_constr = clean_constraints.scale_constr
add_divider_attribue = general_utils.add_divider_attribue
cap = general_utils.cap
create_attached_ruler = create_ruler.create_attached_ruler
swap_side_str = general_utils.swap_side_str


class FkIkSingleChainModule:
    """A two joint fk ik blend with an ik single chain solver. In other words, a
    single chain solver for ik between two joints blended with a simple two joint fk chain.
    Useful for clavicle/shoulder control.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list,
        end_jnt_connect: bool = False,
        switch_ctrl_size: float = 0.12,
        switch_ctrl_distance: float = 14,
        switch_ctrl_constraint: bool = False,
        enable_auto_clav: bool = False,
        ik_wrist_ctrl: str = "",
        ik_arm_switch_ctrl: str = "",
    ):
        """Initialize rig module.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: String describing mirror side. Ex. "left", "right".
            main_joints: The main skinned joints.
            switch_ctrl_size: Size of the switch ctrl.
            switch_ctrl_distance: Distance of switch ctrl from constraint object,
                if constraint object used.
            switch_ctrl_constraint: Whether to constrain the switch ctrl to parent object or leave
                for later parent spaceing.
            end_jnt_connect: Connects the main end joint to the fk ik blend (end offset joint).
                Disconnected by default, allowing another module to connect to the end joint
                instead, like an arm module.
            enable_auto_clav: Add auto clavicle option to ik joint chain.
                Controls ik shoulder rotation with wrist/hand ctrl translation.
            ik_wrist_ctrl: Name of the wrist/hand control. Used for auto clav endpoint.
                Required when using "enable_auto_clav".
            ik_wrist_switch_ctrl: Switch ctrl for fk ik arm. Not required for auto clav.

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints

        self.end_jnt_connect = end_jnt_connect
        self.switch_ctrl_size = switch_ctrl_size
        self.switch_ctrl_distance = switch_ctrl_distance
        self.switch_ctrl_constraint = switch_ctrl_constraint

        self.enable_auto_clav = enable_auto_clav
        self.ik_wrist_ctrl = ik_wrist_ctrl
        if self.enable_auto_clav:
            if not ik_arm_switch_ctrl:
                ik_arm_switch_ctrl = self.find_ik_arm_switch()
        self.ik_arm_switch_ctrl = ik_arm_switch_ctrl

        self.logger = get_logger()

    def build(self) -> str:
        """Build the rig module.
        --------------------------------------------------

        Returns:
            Top group for all the rig module objects.

        """
        failed_build_string = (
            f'Rig module "{self.mod_name}{self.mirr_side.rstrip("_")}" failed to build.'
        )

        # ---------- build rig module ----------
        try:
            if all(cmds.objExists(jnt) for jnt in self.main_joints):
                if len(self.main_joints) == 2:
                    self.query_main_axis()
                    self.build_top_groups()
                    self.build_fk_ik_joints()
                    self.build_fk_controls()
                    self.build_ik_controls()
                    self.build_ik_stretch()
                    self.build_fk_ik_switch()
                    if self.enable_auto_clav:
                        self.build_autoclav_chain()
                        self.setup_autoclav_connections()
                else:
                    error_msg = (
                        'The "single_chain_fk_ik_mod" requires exactly 2 joints.\n'
                        f"{failed_build_string}"
                    )
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)
            else:
                missing_jnts = [jnt for jnt in self.main_joints if not cmds.objExists(jnt)]
                error_msg = f"Missing main joints: {missing_jnts}\n{failed_build_string}"
                self.logger.error(error_msg)
                raise ValueError(error_msg)
        except Exception:
            self.logger.exception(failed_build_string)
            raise
        else:
            return self.mod_top_grp

    def build_top_groups(self):
        """Create top rig module groups to parent controls and joints under."""
        # groups for organization
        self.mod_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}grp",
        )
        self.fk_mod_top_grp = cmds.group(
            empty=True,
            name=f"fk{cap(self.mod_name)}{self.mirr_side}grp",
        )
        self.ik_mod_top_grp = cmds.group(
            empty=True,
            name=f"ik{cap(self.mod_name)}{self.mirr_side}grp",
        )

        cmds.parent(self.fk_mod_top_grp, self.mod_top_grp)
        cmds.parent(self.ik_mod_top_grp, self.mod_top_grp)

    def build_fk_ik_joints(self):
        """An fk ik blended joint chain.
        Create fk ik joint chains and blend with an offset joint chain
        which is then constrained to the main joint chain for a single
        parent space end point (the offset end joint).
        """
        fk_jnts = []
        ik_jnts = []
        offset_jnts = []
        for i, jnt in enumerate(self.main_joints):
            # -------------------------------------------------------------
            # -------------------- create fk ik chains --------------------
            fk_jnt = create_joint.single_joint(
                name=f"fk{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_jnt",
                radius=4,
                color_rgb=(1.0, 0.0, 0.1),
                scale_compensate=False,
                parent_snap=jnt,
            )
            ik_jnt = create_joint.single_joint(
                name=f"ik{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_jnt",
                radius=3,
                color_rgb=(1.0, 0.9, 0.1),
                scale_compensate=False,
                parent_snap=jnt,
            )
            offset_jnt = create_joint.single_joint(
                name=f"offset{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_jnt",
                radius=2,
                color_rgb=(0.7, 0.7, 1.0),
                scale_compensate=False,
                parent_snap=jnt,
            )
            # scale compensate off to avoid double scaling when global scaling
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)

            fk_jnts.append(fk_jnt)
            ik_jnts.append(ik_jnt)
            offset_jnts.append(offset_jnt)

            # scale constraint instead of blendColors scale
            # for proper control and global scale
            scale_constr(fk_jnt, offset_jnt)
            scale_constr(ik_jnt, offset_jnt)

            if not self.end_jnt_connect and i != 0:  # only contrain first main jnt
                break

            # constrain offset joints to main joints
            # offset joints allow a single point for child rig mods to parent switch to
            parent_constr(offset_jnt, jnt)
            scale_constr(offset_jnt, jnt)

        # parent fk, ik and offset joints into chains
        cmds.parent(fk_jnts[1], fk_jnts[0])
        cmds.parent(ik_jnts[1], ik_jnts[0])
        cmds.parent(offset_jnts[1], offset_jnts[0])

        # ---------------------------------------------------------------------
        # -------------------- blend joint chains together --------------------
        translate_blend_nds = []
        rotate_blend_nds = []
        for i, (fk_jnt, ik_jnt, jnt) in enumerate(zip(fk_jnts, ik_jnts, offset_jnts, strict=False)):
            # create blend color nodes
            tran_blend_nd = cmds.createNode(
                "blendColors",
                name=f"{self.mod_name}Tran{self.mirr_side}{i + 1:02d}_blendColors",
            )
            rot_blend_nd = cmds.createNode(
                "blendColors",
                name=f"{self.mod_name}Rot{self.mirr_side}{i + 1:02d}_blendColors",
            )
            # translate blend
            cmds.connectAttr(f"{fk_jnt}.translate", f"{tran_blend_nd}.color1", force=True)
            cmds.connectAttr(f"{ik_jnt}.translate", f"{tran_blend_nd}.color2", force=True)
            cmds.connectAttr(f"{tran_blend_nd}.output", f"{jnt}.translate", force=True)
            # rotate blend
            cmds.connectAttr(f"{fk_jnt}.rotate", f"{rot_blend_nd}.color1", force=True)
            cmds.connectAttr(f"{ik_jnt}.rotate", f"{rot_blend_nd}.color2", force=True)
            cmds.connectAttr(f"{rot_blend_nd}.output", f"{jnt}.rotate", force=True)

            translate_blend_nds.append(tran_blend_nd)
            rotate_blend_nds.append(rot_blend_nd)

        # parent top fk ik joints to locator constrained to main_joints parent
        # avoids parenting under main skeleton
        # accounts for needed blendColor node transformation offset
        main_joints_parent = cmds.listRelatives(self.main_joints[0], parent=True)
        if main_joints_parent:
            parent_loc = create_locators.locator_snap_parent(
                objects=main_joints_parent,
                locator_name=f"{self.mod_name}Offset{self.mirr_side}loc",
                local_scale=(5, 5, 5),
            )[0]
            cmds.parent(fk_jnts[0], parent_loc)
            cmds.parent(ik_jnts[0], parent_loc)
            cmds.parent(offset_jnts[0], parent_loc)

            # parent and hide joint locator and joints
            cmds.parent(parent_loc, self.mod_top_grp)
            cmds.setAttr(f"{parent_loc}.visibility", 0)
        else:
            for attr in [fk_jnts[0], ik_jnts[0]]:
                cmds.parent(attr, self.mod_top_grp)
                cmds.setAttr(f"{attr}.visibility", 0)

        # assign instance variables
        self.fk_jnts = fk_jnts
        self.ik_jnts = ik_jnts
        self.offset_jnts = offset_jnts
        self.translate_blend_nds = translate_blend_nds
        self.rotate_blend_nds = rotate_blend_nds
        self.main_joints_parent = main_joints_parent
        self.parent_loc = parent_loc

    def build_fk_controls(self):
        """Create fk controls. Constrain fk controls to fk joints."""
        fk_ctrl_grps = []
        fk_ctrls = []
        # create control curves
        for i, jnt in enumerate(self.fk_jnts):
            # ----- control curve -----
            fk_ctrl = create_nurbs_curves.CreateCurves(
                name=f"fk{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_ctrl",
                size=1,
                color_rgb=(1, 0, 0),
            ).box_curve()

            # ----- control group -----
            fk_ctrl_grp = create_ctrl_grps(fk_ctrl)[0]

            # ----- snap control group to joint -----
            cmds.matchTransform(fk_ctrl_grp, jnt)

            # parent and scale constrain controls to fk joints
            parent_constr(fk_ctrl, jnt)
            scale_constr(fk_ctrl, jnt)

            # create a list of groups for parenting
            fk_ctrl_grps.append(fk_ctrl_grp)
            fk_ctrls.append(fk_ctrl)

        # parent controls and groups together
        # parent 2nd group to 1st control, 3rd group to 2nd control, etc.
        for grp, ctrl in zip(fk_ctrl_grps[1:], fk_ctrls, strict=False):
            cmds.parent(grp, ctrl)

        # parent under main fk group
        cmds.parent(fk_ctrl_grps[0], self.fk_mod_top_grp)

        # ----------- hide and lock -----------
        # lock and hide attributes for start fk control
        cmds.setAttr(f"{fk_ctrls[0]}.visibility", lock=True, keyable=False, channelBox=False)

        # hide control and lock transforms for end fk control
        # could be unlocked for future rig module adjustments
        cmds.setAttr(f"{fk_ctrls[1]}.translate", lock=True)
        cmds.setAttr(f"{fk_ctrls[1]}.rotate", lock=True)
        cmds.setAttr(f"{fk_ctrls[1]}.scale", lock=True)
        cmds.setAttr(f"{fk_ctrls[1]}.visibility", 0)
        cmds.setAttr(f"{fk_ctrls[1]}.visibility", lock=True)

    def build_ik_controls(self):
        """Create ik controls. Create ik handle."""
        # ----- ik handles with single-chain solver -----
        ik_handle = cmds.ikHandle(
            name=f"{self.mod_name}{self.mirr_side}ikHandle",
            startJoint=self.ik_jnts[0],
            endEffector=self.ik_jnts[1],
            solver="ikSCsolver",
        )
        cmds.rename(ik_handle[1], f"{ik_handle[0]}Effector")

        # parent grp to top grp
        cmds.parent(ik_handle[0], self.ik_mod_top_grp)

        # -------------------- create ik handle control --------------------
        ik_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.mod_name)}{self.mirr_side}ctrl",
            size=1,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()

        ik_ctrl_grp = create_ctrl_grps(ik_ctrl)[0]

        cmds.matchTransform(ik_ctrl_grp, self.ik_jnts[1])

        point_constr(ik_ctrl, ik_handle[0])
        orient_constr(ik_ctrl, self.ik_jnts[1])
        scale_constr(ik_ctrl, self.ik_jnts[1])

        # -------------------- create ik start control --------------------
        ik_start_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.mod_name)}Start{self.mirr_side}ctrl",
            size=1,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()

        ik_start_ctrl_grp, _, ik_start_prntswtch_ctrl_grp, _ = create_ctrl_grps(ik_start_ctrl)

        cmds.matchTransform(ik_start_ctrl_grp, self.ik_jnts[0])  # snap to position

        point_constr(ik_start_ctrl, self.ik_jnts[0])
        scale_constr(ik_start_ctrl, self.ik_jnts[0])

        orient_constr(ik_start_ctrl, ik_handle[0], offset=True)  # prevent ik handle flipping

        # parent grp to top grp to organize
        cmds.parent(ik_start_ctrl_grp, self.ik_mod_top_grp)

        # ---------- parent ik controls together ----------
        cmds.parent(ik_ctrl_grp, ik_start_ctrl)

        # -------------------- lock and hide attributes --------------------
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            # cmds.setAttr(f"{ik_start_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{ik_start_ctrl}.scale{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{ik_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{ik_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{ik_ctrl}.visibility", **lock_hide_kwargs)
        cmds.setAttr(f"{ik_start_ctrl}.visibility", **lock_hide_kwargs)
        cmds.setAttr(f"{ik_handle[0]}.visibility", 0)

        # ---------- instance variables ----------
        self.ik_ctrl = ik_ctrl
        self.ik_ctrl_grp = ik_ctrl_grp
        self.ik_start_ctrl = ik_start_ctrl
        self.ik_start_ctrl_grp = ik_start_ctrl_grp
        self.ik_start_prntswtch_ctrl_grp = ik_start_prntswtch_ctrl_grp

    def build_ik_stretch(self):
        """Create ik stretch with the help of a distanceDimension ruler.
        Create stretch attribute on ik ctrl.
        """
        add_divider_attribue(control_name=self.ik_ctrl, divider_amount=10)
        stretch_attr = "stretch"
        cmds.addAttr(
            self.ik_ctrl,
            longName=stretch_attr,
            defaultValue=1.0,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        ruler_shape, ruler_transform, ruler_loc_01, ruler_loc_02, *_ = create_attached_ruler(
            name=f"{self.mod_name}{cap(stretch_attr)}Ruler{self.mirr_side}",
            ruler_start_object=self.ik_start_ctrl,
            ruler_end_object=self.ik_ctrl,
        )
        makenegative_nd = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}MakeNegativeToggle{self.mirr_side}multiplyDivide",
        )
        blendcolors_nd = cmds.shadingNode(
            "blendColors",
            asUtility=True,
            name=f"{self.mod_name}{cap(stretch_attr)}{self.mirr_side}blendColors",
        )
        scaleoffset_nd = cmds.shadingNode(
            "multiplyDivide",
            asUtility=True,
            name=f"{self.mod_name}ScaleOffset{self.mirr_side}multiplyDivide",
        )
        cmds.setAttr(f"{scaleoffset_nd}.operation", 2)  # divide

        negative_toggle_val = 1
        if self.down_chain_axis == "-x":
            negative_toggle_val = -1

        ik_end_jnt_length = cmds.getAttr(f"{self.ik_jnts[1]}.translateX")

        cmds.connectAttr(f"{ruler_shape}.distance", f"{makenegative_nd}.input1X")
        cmds.setAttr(f"{makenegative_nd}.input2X", negative_toggle_val)
        cmds.connectAttr(f"{makenegative_nd}.outputX", f"{scaleoffset_nd}.input1X")
        cmds.connectAttr(f"{self.ik_start_prntswtch_ctrl_grp}.scaleX", f"{scaleoffset_nd}.input2X")

        cmds.connectAttr(f"{self.ik_ctrl}.{stretch_attr}", f"{blendcolors_nd}.blender")
        cmds.connectAttr(f"{scaleoffset_nd}.outputX", f"{blendcolors_nd}.color1R")
        cmds.setAttr(f"{blendcolors_nd}.color2R", ik_end_jnt_length)
        cmds.connectAttr(f"{blendcolors_nd}.outputR", f"{self.ik_jnts[1]}.translateX")

        # ---------- top grp parenting, visibility ----------
        cmds.parent(ruler_transform, self.mod_top_grp)
        cmds.parent(ruler_loc_01, self.mod_top_grp)
        cmds.parent(ruler_loc_02, self.mod_top_grp)
        cmds.setAttr(f"{ruler_transform}.visibility", 0)
        cmds.setAttr(f"{ruler_loc_01}.visibility", 0)
        cmds.setAttr(f"{ruler_loc_02}.visibility", 0)

        # ----- assign instance variables -----
        self.stretch_attr = stretch_attr
        self.stretch_blendcolors = blendcolors_nd

    def build_fk_ik_switch(self):
        """Create fk ik switch control."""
        # ---------- create control curve object ----------
        switch_ctrl = create_nurbs_curves.CreateCurves(
            name=f"{self.mod_name}Swch{self.mirr_side}ctrl",
            size=self.switch_ctrl_size,
            color_rgb=(0.0, 0.0, 0.0),
        ).sphere_curve()

        switch_ctrl_grp = create_ctrl_grps(switch_ctrl)[0]

        # ---------- setup twist ctrl position and constraint ----------
        if self.switch_ctrl_constraint:
            # move control in rear joint axis direction
            rear_facing_axis_jnt = (
                self.main_joints_parent[0] if self.main_joints_parent else self.main_joints[0]
            )
            rear_facing_axis = get_aligned_axis.axis_facing_direction(
                object=rear_facing_axis_jnt,
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

            # snap to start joint
            cmds.matchTransform(switch_ctrl_grp, self.main_joints[0])

            # parent and scale constrain switch ctrl
            if self.main_joints_parent:
                parent_constr(self.main_joints_parent[0], switch_ctrl_grp)
                scale_constr(self.main_joints_parent[0], switch_ctrl_grp)
            else:
                parent_constr(self.main_joints[0], switch_ctrl_grp)
                scale_constr(self.main_joints[0], switch_ctrl_grp)

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
        for nd_translate, nd_rotate in zip(
            self.translate_blend_nds,
            self.rotate_blend_nds,
            strict=False,
        ):
            cmds.connectAttr(
                f"{switch_ctrl}.fkIkBlend",
                f"{nd_translate}.blender",
                force=True,
            )
            cmds.connectAttr(
                f"{switch_ctrl}.fkIkBlend",
                f"{nd_rotate}.blender",
                force=True,
            )

        # ----- connect switch control to visibility -----
        # 1 is fk, 0 is ik
        # use set driven keys
        cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 0)
        cmds.setAttr(f"{self.ik_mod_top_grp}.visibility", 1)
        cmds.setAttr(f"{self.fk_mod_top_grp}.visibility", 0)
        cmds.setDrivenKeyframe(
            f"{self.ik_mod_top_grp}.visibility",
            currentDriver=f"{switch_ctrl}.fkIkBlend",
        )
        cmds.setDrivenKeyframe(
            f"{self.fk_mod_top_grp}.visibility",
            currentDriver=f"{switch_ctrl}.fkIkBlend",
        )

        cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 1)
        cmds.setAttr(f"{self.ik_mod_top_grp}.visibility", 0)
        cmds.setAttr(f"{self.fk_mod_top_grp}.visibility", 1)
        cmds.setDrivenKeyframe(
            f"{self.ik_mod_top_grp}.visibility",
            currentDriver=f"{switch_ctrl}.fkIkBlend",
        )
        cmds.setDrivenKeyframe(
            f"{self.fk_mod_top_grp}.visibility",
            currentDriver=f"{switch_ctrl}.fkIkBlend",
        )

        # ----- connect switch control scale constraints -----
        for i, (fk_jnt, ik_jnt, offset_jnt) in enumerate(
            zip(self.fk_jnts, self.ik_jnts, self.offset_jnts, strict=False),
        ):
            cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 1)
            cmds.setAttr(f"{offset_jnt}ScaleConstraint.{fk_jnt}W0", 1)
            cmds.setAttr(f"{offset_jnt}ScaleConstraint.{ik_jnt}W1", 0)
            cmds.setDrivenKeyframe(
                f"{offset_jnt}ScaleConstraint.{fk_jnt}W0",
                currentDriver=f"{switch_ctrl}.fkIkBlend",
            )
            cmds.setDrivenKeyframe(
                f"{offset_jnt}ScaleConstraint.{ik_jnt}W1",
                currentDriver=f"{switch_ctrl}.fkIkBlend",
            )

            cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 0)
            cmds.setAttr(f"{offset_jnt}ScaleConstraint.{fk_jnt}W0", 0)
            cmds.setAttr(f"{offset_jnt}ScaleConstraint.{ik_jnt}W1", 1)
            cmds.setDrivenKeyframe(
                f"{offset_jnt}ScaleConstraint.{fk_jnt}W0",
                currentDriver=f"{switch_ctrl}.fkIkBlend",
            )
            cmds.setDrivenKeyframe(
                f"{offset_jnt}ScaleConstraint.{ik_jnt}W1",
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
        # cmds.setAttr(f"{switch_ctrl}.fkIkBlend", 1) # set default fk

        # parent to top grp
        cmds.parent(switch_ctrl_grp, self.mod_top_grp)

        # assign instance variables
        self.switch_ctrl = switch_ctrl

    def query_main_axis(self) -> str | None:
        """Get down the joint chain main axis.
        Query the main axis facing down the joint chain.
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

    def build_autoclav_chain(self):
        """Set up auto clavicle start and end joint with single chain solver ik handle.
        Place the joint chain into position, starting at the shoulder and ending at the wrist.
        Auto clavicle is used to control shoulder rotation based on wrist/hand translation alone.
        """
        # get distance between
        jnt_length = small_functions.distance_between(
            object_1=self.ik_jnts[0],
            object_2=self.ik_wrist_ctrl,
        )

        # create auto clav joints
        autoclav_jnts = []
        x_pos = [0, jnt_length]
        for i in range(2):
            jnt = create_joint.single_joint(
                name=f"{self.mod_name}AutoClavIkArm{self.mirr_side}{i + 1:02d}_jnt",
                radius=10,
                color_rgb=(1.0, 0.0, 1.0),
                position=(x_pos[i], 0, 0),
            )
            autoclav_jnts.append(jnt)
        cmds.parent(autoclav_jnts[1], autoclav_jnts[0])

        # ik handle with single-chain solver
        autoclav_ikhandle = cmds.ikHandle(
            name=f"{self.mod_name}AutoClavIkArm{self.mirr_side}ikHandle",
            startJoint=autoclav_jnts[0],
            endEffector=autoclav_jnts[1],
            solver="ikSCsolver",
        )
        cmds.rename(autoclav_ikhandle[1], f"{autoclav_ikhandle[0]}Effector")

        # position auto clav jnt chain and ik handle
        start_jnt_pos = cmds.xform(  # example: shoulder start jnt
            self.ik_jnts[0],
            query=True,
            worldSpace=True,
            translation=True,
        )
        cmds.xform(autoclav_jnts[0], worldSpace=True, translation=start_jnt_pos)
        end_jnt_pos = cmds.xform(
            self.ik_wrist_ctrl,
            query=True,
            worldSpace=True,
            translation=True,
        )
        cmds.xform(autoclav_ikhandle[0], worldSpace=True, translation=end_jnt_pos)

        # parent auto clav under parent locator
        if self.parent_loc:
            cmds.parent(autoclav_ikhandle[0], self.parent_loc)
            cmds.parent(autoclav_jnts[0], self.parent_loc)
        # constrain ik handle under wrist/hand ctrl
        point_constr(self.ik_wrist_ctrl, autoclav_ikhandle[0])
        # constrain auto clav jnt under ik start ctrl
        point_constr(self.ik_start_ctrl, autoclav_jnts[0])
        scale_constr(self.ik_start_ctrl, autoclav_jnts[0])

        # create auto clav attribute
        self.autoclav_attr = "AutoClavIkArm"
        cmds.addAttr(
            self.switch_ctrl,
            longName=self.autoclav_attr,
            defaultValue=0,
            minValue=0,
            maxValue=1,
            keyable=True,
        )

        # create base ik joints to blend regular ik and auto clav between
        base_ik_jnts = []
        for i, jnt in enumerate(self.main_joints):
            base_ik_jnt = create_joint.single_joint(
                name=f"ik{cap(self.mod_name)}Base{self.mirr_side}{i + 1:02d}_jnt",
                radius=3,
                color_rgb=(1.0, 0.9, 0.1),
                parent_snap=jnt,
            )
            base_ik_jnts.append(base_ik_jnt)

        cmds.parent(base_ik_jnts[1], base_ik_jnts[0])
        cmds.parent(base_ik_jnts[0], self.parent_loc)

        # assign instance variables
        self.autoclav_jnts = autoclav_jnts
        self.base_ik_jnts = base_ik_jnts

    def setup_autoclav_connections(self):
        """Create nodes and set up connections for the auto clavicle."""
        # ----------------------------------------
        # reverse and multiplyDivide node auto clav toggle connections
        ik_arm_switch_name = self.ik_arm_switch_ctrl.split("_")[0]
        wrist_fkikblend_reverse = cmds.createNode(
            "reverse",
            name=f"{self.mod_name}{cap(ik_arm_switch_name)}FkIkBlend{self.mirr_side}reverse",
        )
        autoclav_toggle_multdivide = cmds.createNode(
            "multiplyDivide",
            name=f"{self.mod_name}{self.autoclav_attr}{self.mirr_side}multiplyDivide",
        )
        autoclav_toggle_reverse = cmds.createNode(
            "reverse",
            name=f"{self.mod_name}{self.autoclav_attr}{self.mirr_side}reverse",
        )
        cmds.connectAttr(
            f"{self.ik_arm_switch_ctrl}.fkIkBlend",
            f"{wrist_fkikblend_reverse}.inputX",
        )
        cmds.connectAttr(
            f"{wrist_fkikblend_reverse}.outputX",
            f"{autoclav_toggle_multdivide}.input1X",
        )
        cmds.connectAttr(
            f"{self.switch_ctrl}.{self.autoclav_attr}",
            f"{autoclav_toggle_multdivide}.input2X",
        )
        cmds.connectAttr(
            f"{autoclav_toggle_multdivide}.outputX",
            f"{autoclav_toggle_reverse}.inputX",
        )
        # hide regular ik ctrl if auto clav enabled
        # cmds.connectAttr(f"{autoclav_toggle_reverse}.outputX", f"{self.ik_ctrl_grp}.visibility")

        # ----------------------------------------
        # ik stretch toggle connections
        stretch_toggle_blendColors = cmds.createNode(
            "blendColors",
            name=f"{self.mod_name}{self.autoclav_attr}StretchToggle{self.mirr_side}blendColors",
        )

        cmds.connectAttr(
            f"{autoclav_toggle_reverse}.outputX",
            f"{stretch_toggle_blendColors}.blender",
        )
        cmds.connectAttr(
            f"{self.ik_ctrl}.{self.stretch_attr}",
            f"{stretch_toggle_blendColors}.color1R",
        )
        cmds.connectAttr(
            f"{stretch_toggle_blendColors}.outputR",
            f"{self.stretch_blendcolors}.blender",
            force=True,
        )

        # ----------------------------------------
        # ik base joint blendColor connections
        for base_ik_jnt, tran_blend_nd, rot_blend_nd in zip(
            self.base_ik_jnts,
            self.translate_blend_nds,
            self.rotate_blend_nds,
            strict=False,
        ):
            cmds.connectAttr(f"{base_ik_jnt}.translate", f"{tran_blend_nd}.color2", force=True)
            cmds.connectAttr(f"{base_ik_jnt}.rotate", f"{rot_blend_nd}.color2", force=True)

        # ----------------------------------------
        # ik base joint constraints
        base_ik_jnt_consts = []
        for base_ik_jnt, ik_jnt, autoclav_jnt in zip(
            self.base_ik_jnts,
            self.ik_jnts,
            self.autoclav_jnts,
            strict=False,
        ):
            prnt_const = parent_constr(
                targets=[autoclav_jnt, ik_jnt],
                object=base_ik_jnt,
                offset=True,
                interp_type=2,
            )
            scale_constr(ik_jnt, base_ik_jnt)

            base_ik_jnt_consts.append(prnt_const)

        for prnt_const in base_ik_jnt_consts:
            cmds.connectAttr(
                f"{autoclav_toggle_multdivide}.outputX",
                f"{prnt_const}.target[0].targetWeight",
                force=True,
            )
            cmds.connectAttr(
                f"{autoclav_toggle_reverse}.outputX",
                f"{prnt_const}.target[1].targetWeight",
                force=True,
            )

    def find_ik_arm_switch(self) -> str:
        """Find arm switch ctrl for the ik wrist/hand ctrl used for auto clav."""
        try:
            cmds.select(self.ik_wrist_ctrl)
        except ValueError as e:
            error_msg = (
                'Missing "ik_wrist_ctrl" varible with "enable_auto_clav" for '
                '"fk_ik_single_chain_mod".'
            )
            self.logger.error(f"{error_msg}\n{e}")

        for i in range(5):
            cmds.pickWalk(direction="up")
        ik_arm_grp = cmds.ls(selection=True)[0]

        setdriven_anim_crv = cmds.listConnections(
            f"{ik_arm_grp}.visibility",
            source=True,
            destination=False,
        )
        ik_arm_switch_ctrl = cmds.listConnections(
            setdriven_anim_crv,
            source=True,
            destination=False,
        )[0]

        return ik_arm_switch_ctrl
