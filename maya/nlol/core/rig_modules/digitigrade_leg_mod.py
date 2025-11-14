from maya import cmds, mel
from nlol.core import general_utils
from nlol.core.general_utils import cap
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_locators,
    create_nurbs_curves,
    create_ruler,
)
from nlol.core.rig_tools import limb_hinge_vector
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()

add_divider_attribue = general_utils.add_divider_attribue
create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
point_constr = clean_constraints.point_constr
orient_constr = clean_constraints.orient_constr
scale_constr = clean_constraints.scale_constr
create_attached_ruler = create_ruler.create_attached_ruler


class DigitigradeLegMod:
    """Quadruped style leg rig module, specifically, a digitigrade leg,
    where the creature walks on its toes.  For example a dog, cat, or bird.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list[str],
        main_object_names: list[str] = [],
        polevector_ctrl_distance: float = 75,
        foot_locators: list[str] | None = None,
        invert_toe_wiggle: bool = False,
        invert_toe_spin: bool = False,
        invert_foot_lean: bool = False,
        invert_foot_tilt: bool = False,
        invert_foot_roll: bool = False,
    ):
        """Initialize rig module.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: Extra string describing mirror side. Ex. "left", "right".
            main_joints: The main skinned joints.
            main_object_names: Main object names to be used instead of raw joint names.
            polevector_ctrl_distance: Default distance hinge control placed from hinge joint.
            foot_locators: Locators determining position rotation of reverse foot ctrls.
                4 locators; toe end, heel, lateral foot side and medial foot side,
                listed in that order. Foot locator names do not matter,
                just that they are listed in the correct order.
                Or use the pre-determined locator names and skip the arg.
            invert_toe_wiggle, invert_toe_spin, invert_foot_lean, invert_foot_tilt,
                invert_foot_roll: Invert direction of specific reverse foot ctrl.

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints
        self.main_object_names = main_object_names

        if self.main_object_names:
            if len(self.main_object_names) != len(self.main_joints):
                msg = "Should be same number of main_object_names as main_joints: "
                f'"{self.mod_name}, {self.mirr_side}"'
                logger.warning(msg)
        else:
            self.main_object_names = [
                f"upper{cap(self.mod_name)}",
                f"middle{cap(self.mod_name)}",
                f"lower{cap(self.mod_name)}",
                f"ankle{cap(self.mod_name)}",
                f"toe{cap(self.mod_name)}",
            ]

        self.polevector_ctrl_distance = polevector_ctrl_distance

        self.foot_locators = foot_locators
        self.invert_toe_wiggle = invert_toe_wiggle
        self.invert_toe_spin = invert_toe_spin
        self.invert_foot_lean = invert_foot_lean
        self.invert_foot_tilt = invert_foot_tilt
        self.invert_foot_roll = invert_foot_roll

    def build(self):
        """Entry point. Run method to build rig module.
        --------------------------------------------------

        Returns:
            Top Maya group for rig module.

        """
        self.input_checks()
        self.setup_top_grps()
        self.setup_fk_ik_jnts()
        self.setup_fk_ctrls()
        self.setup_switch_ctrl()
        self.setup_ik_driver_jnts()
        self.setup_ik_ctrls()
        self.setup_soft_ik()
        self.setup_foot_ctrls()

        return self.mod_top_grp

    def input_checks(self):
        """Validate class args. Check input data."""
        # ----------
        required_joints = {
            "main_joints": 5,
        }
        errors = []
        for obj_var, required_count in required_joints.items():
            obj_list = getattr(self, obj_var)
            if len(obj_list) != required_count:
                errors.append(
                    f"{self.mod_name}, {obj_list}: Include exactly {required_count} {obj_var}. ",
                )
            for obj in obj_list:
                if not cmds.objExists(obj):
                    errors.append(f'{self.mod_name}: Object "{obj}" does not exist.')
        # ----------
        if self.foot_locators and len(self.foot_locators) != 4:
            msg = (
                'Must be 4 "foot_locators" listed: '
                "toe end, heel, lateral foot side and medial foot side. "
                f'"{self.mod_name}, {self.mirr_side}"'
            )
            errors.append(msg)
        # ----------
        if errors:
            errors.append('See example rig module in "defaults/digitigrade_leg_mod".')
            error_msg = "\n".join(errors)
            logger.error(error_msg)
            raise ValueError(error_msg)

    def setup_top_grps(self):
        """Create top rig module groups for organization."""
        self.mod_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}grp",
        )
        self.fk_top_grp = cmds.group(
            empty=True,
            name=f"fk{cap(self.mod_name)}{self.mirr_side}grp",
        )
        self.ik_top_grp = cmds.group(
            empty=True,
            name=f"ik{cap(self.mod_name)}{self.mirr_side}grp",
        )
        self.soft_ik_top_grp = cmds.group(
            empty=True,
            name=f"softIk{cap(self.mod_name)}{self.mirr_side}grp",
        )
        cmds.parent(self.fk_top_grp, self.mod_top_grp)
        cmds.parent(self.ik_top_grp, self.mod_top_grp)
        cmds.parent(self.soft_ik_top_grp, self.ik_top_grp)

    def setup_fk_ik_jnts(self):
        """Create fk ik joint chains and blend with main joint chain."""
        fk_jnts = []
        ik_jnts = []
        fk_ik_scale_consts = []
        for i, jnt in enumerate(self.main_joints):
            # -------------------------------------------------------------
            # -------------------- create fk ik chains --------------------
            fk_jnt = create_joint.single_joint(
                name=f"fk{cap(self.main_object_names[i])}{self.mirr_side}jnt",
                radius=5,
                color_rgb=(1.0, 0.0, 0.1),
                parent_snap=jnt,
            )
            ik_jnt = create_joint.single_joint(
                name=f"ik{cap(self.main_object_names[i])}{self.mirr_side}jnt",
                radius=4,
                color_rgb=(0.1, 0.9, 0.0),
                parent_snap=jnt,
            )
            # scale compensate off to avoid double scaling when global scaling
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)

            # better scaling with constraint instead of blendColors scale
            fk_ik_scale_const = scale_constr((fk_jnt, ik_jnt), jnt)

            fk_jnts.append(fk_jnt)
            ik_jnts.append(ik_jnt)
            fk_ik_scale_consts.append(fk_ik_scale_const)

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
        # accounts for needed blendColor node transform offset
        parent_loc = None
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
            cmds.parent(parent_loc, self.mod_top_grp)
            cmds.setAttr(f"{parent_loc}.visibility", 0)
        else:
            for jnt in [fk_jnts[0], ik_jnts[0]]:
                cmds.parent(jnt, self.mod_top_grp)
                cmds.setAttr(f"{jnt}.visibility", 0)

        # assign instance variables
        self.fk_jnts = fk_jnts
        self.ik_jnts = ik_jnts
        self.fk_ik_scale_consts = fk_ik_scale_consts
        self.translate_blend_nodes = translate_blend_nodes
        self.rotate_blend_nodes = rotate_blend_nodes
        self.parent_loc = parent_loc

    def setup_fk_ctrls(self):
        """Create fk ctrls. Constrain fk ctrls to fk joints."""
        fk_ctrl_grps = []
        fk_ctrls = []
        # create ctrl curves
        for i, jnt in enumerate(self.fk_jnts):
            # ctrl curve
            fk_ctrl = create_nurbs_curves.CreateCurves(
                name=f"fk{cap(self.main_object_names[i])}{self.mirr_side}ctrl",
                size=2.0,
                color_rgb=(1, 0, 0),
            ).circle_curve()
            fk_ctrl_grp = create_ctrl_grps(fk_ctrl)[0]
            # snap ctrl group to joint
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
        for grp, ctrl in zip(fk_ctrl_grps[1:], fk_ctrls, strict=False):
            cmds.parent(grp, ctrl)

        # parent under main fk group
        cmds.parent(fk_ctrl_grps[0], self.fk_top_grp)

        # assign instance variables
        self.fk_ctrls = fk_ctrls

    def setup_switch_ctrl(self):
        """Create fk ik switch ctrl."""
        # ---------- create control crv and grp ----------
        switch_ctrl = create_nurbs_curves.CreateCurves(
            name=f"{self.mod_name}Swch{self.mirr_side}ctrl",
            size=1.0,
            color_rgb=(0.0, 0.0, 0.0),
        ).sphere_curve()
        switch_ctrl_grp = create_ctrl_grps(switch_ctrl)[0]

        # ---------- add attributes ----------
        # fk ik blend attr
        add_divider_attribue(control_name=switch_ctrl, divider_amount=10)
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

        # ----- connect switch ctrl to visibility -----
        swch_reverse_nd = cmds.createNode(
            "reverse",
            name=f"{self.mod_name}Swch{self.mirr_side}reverse",
        )
        cmds.connectAttr(f"{switch_ctrl}.fkIkBlend", f"{self.fk_top_grp}.visibility")
        cmds.connectAttr(f"{switch_ctrl}.fkIkBlend", f"{swch_reverse_nd}.inputX")
        cmds.connectAttr(f"{swch_reverse_nd}.outputX", f"{self.ik_top_grp}.visibility")

        # ----- connect switch control scale constraints -----
        for fk_jnt, ik_jnt, scale_const in zip(
            self.fk_jnts,
            self.ik_jnts,
            self.fk_ik_scale_consts,
            strict=False,
        ):
            cmds.connectAttr(
                f"{switch_ctrl}.fkIkBlend",
                f"{scale_const}.target[0].targetWeight",
                force=True,
            )
            cmds.connectAttr(
                f"{swch_reverse_nd}.outputX",
                f"{scale_const}.target[1].targetWeight",
                force=True,
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
        cmds.parent(switch_ctrl_grp, self.mod_top_grp)

        # assign instance variables
        self.switch_ctrl = switch_ctrl

    def setup_ik_driver_jnts(self):
        """Create a driver ik joint chain that drives the two underlying ik solvers
        on the main ik joint chain for the upper and lower leg.
        """
        # ----- create jnts -----
        ik_drvr_jnts = []
        for i, jnt in enumerate(self.main_joints[:4]):
            ik_drvr_jnt = create_joint.single_joint(
                name=f"ikDrvr{cap(self.main_object_names[i])}{self.mirr_side}jnt",
                radius=6,
                color_rgb=(0.0, 0.0, 1.0),
                parent_snap=jnt,
            )
            ik_drvr_jnts.append(ik_drvr_jnt)
        # parent joints into chain
        for i, jnt in enumerate(ik_drvr_jnts):
            if jnt != ik_drvr_jnts[0]:
                cmds.parent(jnt, ik_drvr_jnts[i - 1])

        # ----- ik handle w/ spring solver -----
        # load spring solver
        if not cmds.pluginInfo("ikSpringSolver.mll", query=True, loaded=True):
            cmds.loadPlugin("ikSpringSolver.mll")
        mel.eval("ikSpringSolver;")
        # create ik handle
        ik_drvr_ikhandle = cmds.ikHandle(
            name=f"{self.mod_name}ikDrvrSpring{self.mirr_side}ikHandle",
            startJoint=ik_drvr_jnts[0],
            endEffector=ik_drvr_jnts[3],
            solver="ikSpringSolver",
        )
        cmds.rename(ik_drvr_ikhandle[1], f"{ik_drvr_ikhandle[0]}Effector")

        # ----- place driver chain under main jnts parent -----
        if self.parent_loc:
            cmds.parent(ik_drvr_jnts[0], self.parent_loc)

        # ----------
        # organize parent
        cmds.parent(ik_drvr_ikhandle[0], self.ik_top_grp)
        # hide
        cmds.setAttr(f"{ik_drvr_ikhandle[0]}.visibility", 0)

        # assign instance variables
        self.ik_drvr_jnts = ik_drvr_jnts
        self.ik_drvr_ikhandle = ik_drvr_ikhandle[0]

    def setup_ik_ctrls(self):
        """Setup main ik ctrls and their connections."""
        # -------------------------------------
        # ---------- upper ik handle ----------
        upper_ik_handle = cmds.ikHandle(
            name=f"{self.mod_name}{self.mirr_side}UpperIkHandkle",
            startJoint=self.ik_jnts[0],
            endEffector=self.ik_jnts[2],
        )
        cmds.rename(upper_ik_handle[1], f"{upper_ik_handle[0]}Effector")

        # ---------- lower ik handle ----------
        lower_ik_handle = cmds.ikHandle(
            name=f"{self.mod_name}{self.mirr_side}LowerIkHandkle",
            startJoint=self.ik_jnts[1],
            endEffector=self.ik_jnts[3],
        )
        cmds.rename(lower_ik_handle[1], f"{lower_ik_handle[0]}Effector")
        # parent ik handle to driver joint
        cmds.parent(lower_ik_handle[0], self.ik_drvr_jnts[3])

        # -----------------------------------
        # ---------- ik ankle ctrl ----------
        # create curve box
        ik_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.main_object_names[3])}{self.mirr_side}ctrl",
            size=2.0,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()
        ik_ctrl_grp = create_ctrl_grps(ik_ctrl)[0]
        # snap control group to joint
        cmds.matchTransform(ik_ctrl_grp, self.ik_jnts[3])

        # ---------------------------------
        # ---------- ik hip ctrl ----------
        # create box curve
        ik_hip_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.main_object_names[0])}{self.mirr_side}ctrl",
            size=2.0,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()
        ik_hip_ctrl_grp, _, ik_hip_ctrl_prntswtch_grp, _ = create_ctrl_grps(ik_hip_ctrl)
        # snap control group to joint
        cmds.matchTransform(ik_hip_ctrl_grp, self.ik_jnts[0])
        # constrain hip joint to control
        point_constr(ik_hip_ctrl, self.ik_jnts[0])
        # constrain driver joint to control
        point_constr(ik_hip_ctrl, self.ik_drvr_jnts[0])

        # --------------------------------------------
        # ---------- upper pole vector ctrl ----------
        # create pyramid curve
        upper_polevector_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.mod_name)}UpperPoleVector{self.mirr_side}ctrl",
            size=0.5,
            color_rgb=(1.0, 1.0, 0.0),
        ).pyramid_curve()
        upper_polevector_ctrl_grp = create_ctrl_grps(upper_polevector_ctrl)[0]
        # pole vector control transformation
        limb_hinge_vector.apply_hinge_vector(
            limb_joints=self.ik_jnts[:3],
            control_object=upper_polevector_ctrl_grp,
            control_object_distance=self.polevector_ctrl_distance,
        )
        # connect pole vector constraint
        cmds.poleVectorConstraint(
            upper_polevector_ctrl,
            upper_ik_handle[0],
            name=f"{upper_polevector_ctrl}PoleVectorConstraint",
        )

        # ---------- lower pole vector ctrl ----------
        # create pyramid curve
        lower_polevector_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.mod_name)}LowerPoleVector{self.mirr_side}ctrl",
            size=0.5,
            color_rgb=(1.0, 1.0, 0.0),
        ).pyramid_curve()
        lower_polevector_ctrl_grp = create_ctrl_grps(lower_polevector_ctrl)[0]
        # pole vector control transformation
        limb_hinge_vector.apply_hinge_vector(
            limb_joints=self.ik_jnts[1:4],
            control_object=lower_polevector_ctrl_grp,
            control_object_distance=self.polevector_ctrl_distance,
        )
        # connect pole vector constraint
        cmds.poleVectorConstraint(
            lower_polevector_ctrl,
            lower_ik_handle[0],
            name=f"{lower_polevector_ctrl}PoleVectorConstraint",
        )

        # ------------------------------------------
        # ---------- ik lower offset ctrl ----------
        # create box curve
        ik_lower_offs_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.main_object_names[2])}Offset{self.mirr_side}ctrl",
            size=1.5,
            color_rgb=(0.5, 1.0, 0.0),
        ).box_curve()
        ik_lower_offs_ctrl_grp, *_, ik_lower_offs_ctrl_grp_aux = create_ctrl_grps(
            ik_lower_offs_ctrl,
            aux_offset_grp=True,
        )
        # snap control group to joint
        cmds.matchTransform(ik_lower_offs_ctrl_grp, self.ik_jnts[3])
        # constrain to drvr rear facing knee
        parent_constr(self.ik_drvr_jnts[2], ik_lower_offs_ctrl_grp, offset=True)
        scale_constr(self.ik_drvr_jnts[2], ik_lower_offs_ctrl_grp)

        # ----- parent upper ik handle to lower offset ctrl -----
        cmds.parent(upper_ik_handle[0], ik_lower_offs_ctrl)

        # ----- top grp parenting -----
        cmds.parent(ik_ctrl_grp, self.ik_top_grp)
        cmds.parent(ik_hip_ctrl_grp, self.ik_top_grp)
        cmds.parent(upper_polevector_ctrl_grp, self.ik_top_grp)
        cmds.parent(lower_polevector_ctrl_grp, self.ik_top_grp)
        cmds.parent(ik_lower_offs_ctrl_grp, self.ik_top_grp)

        # ----- lock and hide -----
        # hide objects
        cmds.setAttr(f"{upper_ik_handle[0]}.visibility", 0)
        cmds.setAttr(f"{lower_ik_handle[0]}.visibility", 0)
        cmds.setAttr(f"{ik_lower_offs_ctrl_grp}.visibility", 0)
        # lock and hide unused attributes
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{ik_hip_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{ik_hip_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{ik_hip_ctrl}.visibility", **lock_hide_kwargs)

        # ----- assign instance variables -----
        self.ik_ctrl = ik_ctrl
        self.ik_hip_ctrl = ik_hip_ctrl
        self.ik_hip_ctrl_prntswtch_grp = ik_hip_ctrl_prntswtch_grp
        self.ik_lower_offs_ctrl_grp_aux = ik_lower_offs_ctrl_grp_aux

        # ----- add attr to control ik_lower_offs_ctrl rotate Z -----
        self.add_ik_offset_attr()

    def add_ik_offset_attr(self):
        """Add attribute to the ik lower offset ctrl for bending the lower knee forward."""
        add_divider_attribue(self.ik_ctrl, divider_amount=8)
        cmds.addAttr(
            self.ik_ctrl,
            longName="ankleOffset",
            defaultValue=0,
            minValue=50,
            maxValue=-50,
            keyable=True,
        )
        cmds.connectAttr(
            f"{self.ik_ctrl}.ankleOffset",
            f"{self.ik_lower_offs_ctrl_grp_aux}.rotateZ",
        )

    def setup_soft_ik(self, use_expression: bool = False) -> None:
        """Create soft ik joints, connections and general setup.

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

        # ----- position soft ik end joint -----
        # straight distance from start to end limb joint
        ik_limb_span = cmds.getAttr(f"{ruler_shape}.distance")
        cmds.setAttr(f"{soft_ik_jnts[1]}.translateX", ik_limb_span)
        # ----- constrain limb ik handle to soft ik end joint -----
        point_constr(soft_ik_jnts[1], self.ik_drvr_ikhandle, offset=True)

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
        self.soft_ik_handle = soft_ik_handle[0]
        self.soft_ik_ruler_end = ruler_loc_02
        self.soft_ik_ruler_end_const = ruler_loc_02_const

        # ----- create soft ik exponential curve -----
        ik_jnt_02_pos_x = cmds.getAttr(f"{self.ik_jnts[1]}.translateX")
        ik_jnt_03_pos_x = cmds.getAttr(f"{self.ik_jnts[2]}.translateX")
        ik_jnt_04_pos_x = cmds.getAttr(f"{self.ik_jnts[3]}.translateX")
        self.limb_chain_length = abs(ik_jnt_02_pos_x + ik_jnt_03_pos_x + ik_jnt_04_pos_x)
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

    def setup_foot_ctrls(self, base_foot_aim: bool = True, reverse_foot_attrs: bool = True):
        """Create reverse foot ctrls for rig module.
        Based on locators establishing reverse foot rotation points.
        Position locators in "rig_helpers.ma" file.
            Note: Ankle joint X should be pointing world down or up.
        Ideally, ankle joint should be flat with the world,
        and foot locators should be based on ankle joint rotation.

        Args:
            base_foot_point: Wether to make the foot always
                aim towards the base foot control.
            reverse_foot_attrs: Add reverse foot attributes to main limb ik control.

        """
        # ---------------------------------------------------------
        # --------------- create and find locators ---------------
        foot_ankle_loc = create_locators.locator_snap(
            objects=self.main_joints[3],
            locator_name=f"ankle{self.mirr_side}loc",
            local_scale=(5, 5, 5),
        )[0]
        toe_loc = create_locators.locator_snap(
            objects=self.main_joints[4],
            locator_name=f"toe{self.mirr_side}loc",
            local_scale=(5, 5, 5),
        )[0]
        # additionally, match toe locator rotation to ankle
        cmds.matchTransform(toe_loc, self.main_joints[3], rotation=True)

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
            logger.error(msg)
            raise ValueError(msg)

        # ---------------------------------------------------------
        # ---------- create controls to replace locators ----------
        foot_ctrls = []
        foot_ctrl_grps = []
        foot_aux_ctrl_grps = []
        loc_base_names = ["ankle", "toe", "toeEnd", "heel", "lateral", "medial"]
        for loc, loc_nm in zip(foot_locators, loc_base_names, strict=False):
            # ----- create control -----
            foot_ctrl = create_nurbs_curves.CreateCurves(
                name=f"{self.mod_name}Foot{cap(loc_nm)}{self.mirr_side}ctrl",
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
        toe_wiggle_ctrl = create_nurbs_curves.CreateCurves(
            name=f"{self.mod_name}FootToeWiggle{self.mirr_side}ctrl",
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
        foot_top_grp = cmds.group(name=f"{self.mod_name}Foot{self.mirr_side}grp", empty=True)
        foot_pivot_grp = cmds.group(name=f"{self.mod_name}FootPivot{self.mirr_side}grp", empty=True)
        cmds.matchTransform(foot_pivot_grp, self.ik_jnts[3])
        cmds.parent(foot_pivot_grp, foot_top_grp)
        cmds.parent(foot_top_grp, self.ik_top_grp)
        # parent foot controls under pivot group
        cmds.parent(foot_ctrl_grps[-1], foot_pivot_grp)

        # --------------- parent toe wiggle control ---------------
        cmds.parent(toe_wiggle_ctrl_grp, foot_top_grp)

        # ------------------------------------------------------
        # --------------- reverse foot parenting ---------------
        # break default limb constraints
        cmds.delete(self.soft_ik_ruler_end_const)
        # cmds.delete(self.ik_drvr_ikhandle_constr)
        # ----- translate constrain -----
        # attach limb length ruler end to foot ankle control
        point_constr(foot_ctrls[0], self.soft_ik_ruler_end)
        # ----- translate constrain -----
        # limb ik control > foot pivot grp, ankle foot control > soft ik handle
        # ik soft end joint > limb ik handle
        point_constr(self.ik_ctrl, foot_pivot_grp, offset=True)
        point_constr(foot_ctrls[0], self.soft_ik_handle, offset=True)

        # ----- rotate constrain -----
        # limb ik control > foot pivot grp, ankle foot control > ik ankle joint
        orient_constr(self.ik_ctrl, foot_pivot_grp, offset=True)
        self.foot_ankle_orient_const = orient_constr(
            foot_ctrls[0],
            self.ik_jnts[3],
            offset=True,
        )
        # toe wiggle constrain
        orient_constr(toe_wiggle_ctrl, self.ik_jnts[4], offset=True)
        # ----- scale constrain -----
        # limb ik control > foot pivot grp, ankle foot control > ik ankle joint
        scale_constr(self.ik_ctrl, foot_pivot_grp)
        scale_constr(foot_ctrls[0], self.ik_jnts[3])
        # toe wiggle to joint
        scale_constr(toe_wiggle_ctrl, self.ik_jnts[4])

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
                name=f"{self.mod_name}FootAim{self.mirr_side}{i:02d}_jnt",
                radius=7,
                color_rgb=(1.0, 0.4, 0.0),
                parent_snap=ctrl,
            )
            foot_aim_jnts.append(foot_aim_jnt)

        # parent joints together
        for i, jnt in enumerate(foot_aim_jnts):
            if jnt != foot_aim_jnts[0]:
                cmds.parent(jnt, foot_aim_jnts[i - 1])

        # ----- ik handles with single-chain solver -----
        aim_ik_handle_01 = cmds.ikHandle(
            name=f"{self.mod_name}FootAim{self.mirr_side}01_ikHandle",
            startJoint=foot_aim_jnts[0],
            endEffector=foot_aim_jnts[1],
            solver="ikSCsolver",
        )
        cmds.rename(aim_ik_handle_01[1], f"{aim_ik_handle_01[0]}Effector")

        aim_ik_handle_02 = cmds.ikHandle(
            name=f"{self.mod_name}FootAim{self.mirr_side}02_ikHandle",
            startJoint=foot_aim_jnts[1],
            endEffector=foot_aim_jnts[2],
            solver="ikSCsolver",
        )
        cmds.rename(aim_ik_handle_02[1], f"{aim_ik_handle_02[0]}Effector")

        # ----- constrain ik handles to foot controls  -----
        parent_constr(self.foot_ctrls[1], aim_ik_handle_01[0])
        parent_constr(self.foot_ctrls[2], aim_ik_handle_02[0])
        # ----- point and scale constrain top foot joint  -----
        point_constr(self.ik_jnts[3], foot_aim_jnts[0])
        scale_constr(self.foot_ctrls[0], foot_aim_jnts[0])
        # ----- constrain foot joints -----
        cmds.delete(self.foot_ankle_orient_const)  # remove default foot constraint
        orient_constr(foot_aim_jnts[0], self.ik_jnts[3], offset=True)
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
            self.ik_ctrl,
            longName=soft_ik_divider_name,
            niceName=soft_ik_divider_name,
            attributeType="enum",
            enumName="----------",
        )
        cmds.setAttr(f"{self.ik_ctrl}.{soft_ik_divider_name}", channelBox=True)
        # ----------
        cmds.addAttr(self.ik_ctrl, longName="toeWiggle", keyable=True)
        cmds.addAttr(self.ik_ctrl, longName="toeSpin", keyable=True)
        cmds.addAttr(self.ik_ctrl, longName="lean", keyable=True)
        cmds.addAttr(self.ik_ctrl, longName="tilt", keyable=True)

        cmds.addAttr(self.ik_ctrl, longName="roll", keyable=True)
        # NOTE: Mirroing leg does not change forward rotation axis.
        # Though may need to adjust for certain scenarios.
        # default_toe_bend_angle = -35 if self.limb_mod.down_chain_axis == "-x" else 35
        default_toe_bend_angle = -35
        cmds.addAttr(
            self.ik_ctrl,
            longName="rollToeBendAngle",
            defaultValue=default_toe_bend_angle,
            keyable=True,
        )
        cmds.addAttr(
            self.ik_ctrl,
            longName="rollToeEndRangeMult",
            defaultValue=2,
            keyable=True,
        )
        cmds.setAttr(f"{self.ik_ctrl}.rollToeBendAngle", lock=True)
        cmds.setAttr(f"{self.ik_ctrl}.rollToeEndRangeMult", lock=True)

        # -------------------------------------------------------
        # ---------- connect and setup foot attributes ----------
        # --------------- toe wiggle ---------------
        if self.invert_toe_wiggle:
            toewiggle_multiply_nd = cmds.createNode(
                "multiply",
                name=f"{self.mod_name}FootToeWiggle{self.mirr_side}multiply",
            )
            cmds.setAttr(f"{toewiggle_multiply_nd}.input[0]", -1)
            cmds.connectAttr(
                f"{self.ik_ctrl}.toeWiggle",
                f"{toewiggle_multiply_nd}.input[1]",
            )
            cmds.connectAttr(
                f"{toewiggle_multiply_nd}.output",
                f"{self.toe_wiggle_aux_ctrl_grp}.rotateZ",
            )
        else:
            cmds.connectAttr(
                f"{self.ik_ctrl}.toeWiggle",
                f"{self.toe_wiggle_aux_ctrl_grp}.rotateZ",
            )
        # --------------- top spin ---------------
        if self.invert_toe_spin:
            toespin_multiply_nd = cmds.createNode(
                "multiply",
                name=f"{self.mod_name}FootToeSpin{self.mirr_side}multiply",
            )
            cmds.setAttr(f"{toespin_multiply_nd}.input[0]", -1)
            cmds.connectAttr(
                f"{self.ik_ctrl}.toeSpin",
                f"{toespin_multiply_nd}.input[1]",
            )
            cmds.connectAttr(
                f"{toespin_multiply_nd}.output",
                f"{self.foot_aux_ctrl_grps[2]}.rotateX",
            )
        else:
            cmds.connectAttr(
                f"{self.ik_ctrl}.toeSpin",
                f"{self.foot_aux_ctrl_grps[2]}.rotateX",
            )
        # --------------- lean ---------------
        if self.invert_foot_lean:
            lean_multiply_nd = cmds.createNode(
                "multiply",
                name=f"{self.mod_name}FootLean{self.mirr_side}multiply",
            )
            cmds.setAttr(f"{lean_multiply_nd}.input[0]", -1)
            cmds.connectAttr(
                f"{self.ik_ctrl}.lean",
                f"{lean_multiply_nd}.input[1]",
            )
            cmds.connectAttr(
                f"{lean_multiply_nd}.output",
                f"{self.foot_aux_ctrl_grps[1]}.rotateY",
            )
        else:
            cmds.connectAttr(
                f"{self.ik_ctrl}.lean",
                f"{self.foot_aux_ctrl_grps[1]}.rotateY",
            )
        # ----------------------------------------------
        # -------------------- tilt --------------------
        tilt_clamp_nd = cmds.createNode(
            "clamp",
            name=f"{self.mod_name}FootTilt{self.mirr_side}clamp",
        )
        cmds.setAttr(f"{tilt_clamp_nd}.minG", -180)
        cmds.setAttr(f"{tilt_clamp_nd}.maxR", 180)
        cmds.connectAttr(f"{self.ik_ctrl}.tilt", f"{tilt_clamp_nd}.inputR")
        cmds.connectAttr(f"{self.ik_ctrl}.tilt", f"{tilt_clamp_nd}.inputG")
        if self.invert_foot_tilt:
            tilt_multiplydivid_nd = cmds.createNode(
                "multiplyDivide",
                name=f"{self.mod_name}FootTilt{self.mirr_side}multiplyDivide",
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
                name=f"{self.mod_name}FootRoll{self.mirr_side}multiplyDivide",
            )
            for axis in "XYZ":
                cmds.setAttr(f"{roll_multiplydivide_nd}.input2{axis}", -1)
        # ----------
        toe_remapevalue_double_nd = cmds.createNode(
            "multiplyDivide",
            name=f"{self.mod_name}FootToeRemapValueDouble{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(
            f"{self.ik_ctrl}.rollToeBendAngle",
            f"{toe_remapevalue_double_nd}.input1X",
        )
        cmds.setAttr(f"{toe_remapevalue_double_nd}.input2X", 2)
        # ----------
        toe_roll_remap_nd = cmds.createNode(
            "remapValue",
            name=f"{self.mod_name}FootToeRoll{self.mirr_side}remapValue",
        )
        cmds.setAttr(f"{toe_roll_remap_nd}.value[0].value_Position", 0.0)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[0].value_FloatValue", 0.0)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[1].value_Position", 0.5)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[1].value_FloatValue", 1.0)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[2].value_Position", 1.0)
        cmds.setAttr(f"{toe_roll_remap_nd}.value[2].value_FloatValue", 0.0)
        cmds.connectAttr(
            f"{self.ik_ctrl}.roll",
            f"{toe_roll_remap_nd}.inputValue",
        )
        cmds.connectAttr(
            f"{toe_remapevalue_double_nd}.outputX",
            f"{toe_roll_remap_nd}.inputMax",
        )
        cmds.connectAttr(
            f"{self.ik_ctrl}.rollToeBendAngle",
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
            f"{self.ik_ctrl}.rollToeBendAngle",
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
            name=f"{self.mod_name}FootToeEndRange{self.mirr_side}multiplyDivide",
        )
        cmds.connectAttr(f"{invet_180_nd}.outputX", f"{toe_end_range_mult_nd}.input1X")
        cmds.connectAttr(
            f"{self.ik_ctrl}.rollToeEndRangeMult",
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
            f"{self.ik_ctrl}.rollToeBendAngle",
            f"{difference_180_nd}.input1D[1]",
        )
        # ----------
        toe_end_roll_remap_nd = cmds.createNode(
            "remapValue",
            name=f"{self.mod_name}FootToeEndRoll{self.mirr_side}remapValue",
        )
        cmds.connectAttr(
            f"{self.ik_ctrl}.roll",
            f"{toe_end_roll_remap_nd}.inputValue",
        )
        cmds.connectAttr(
            f"{self.ik_ctrl}.rollToeBendAngle",
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
            f"{self.ik_ctrl}.roll",
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
