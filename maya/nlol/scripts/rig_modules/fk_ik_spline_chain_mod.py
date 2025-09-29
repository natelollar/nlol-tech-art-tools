import math
from importlib import reload

from maya import cmds
from nlol.scripts.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_locators,
    create_nurbs_curves,
    create_ruler,
)
from nlol.scripts.rig_tools import get_aligned_axis
from nlol.utilities.nlol_maya_logger import get_logger
from nlol.utilities.utils_maya import add_divider_attribue, cap

reload(create_ruler)
reload(get_aligned_axis)

scale_constr = clean_constraints.scale_constr
parent_constr = clean_constraints.parent_constr
create_ctrl_grps = create_control_groups.create_ctrl_grps
create_attached_ruler = create_ruler.create_attached_ruler
query_main_axis = get_aligned_axis.query_main_axis


class FkIkSplineChainModule:
    def __init__(self, rig_module_name: str, mirror_direction: str, main_joints: list[str]):
        """Create fk ik blended ctrl chain. The ik chain uses "Ik Spline Handle" curve.
        Useful for a spline spine.
        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints

        self.logger = get_logger()

    def build(self):
        """Entry point. Run method to build rig module.
        --------------------------------------------------

        Returns:
            Top group for rig module.

        """
        self.build_top_grps()
        self.build_fk_ik_jnts()
        self.build_switch_ctrl()
        self.build_fk_ctrls()
        self.build_ik_ctrls()

        return self.mod_top_grp

    def build_top_grps(self):
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
        cmds.parent(self.fk_top_grp, self.mod_top_grp)
        cmds.parent(self.ik_top_grp, self.mod_top_grp)

    def build_fk_ik_jnts(self):
        """An fk ik blended joint chain.
        Create fk ik joint chains and blend with main joint chain.
        """
        fk_jnts = []
        ik_jnts = []
        fk_ik_scale_consts = []
        for i, jnt in enumerate(self.main_joints):
            # -------------------------------------------------------------
            # -------------------- create fk ik chains --------------------
            fk_jnt = create_joint.single_joint(
                name=f"fk{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_jnt",
                radius=5,
                color_rgb=(1.0, 0.0, 0.1),
                scale_compensate=False,
                parent_snap=jnt,
            )
            ik_jnt = create_joint.single_joint(
                name=f"ik{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_jnt",
                radius=4,
                color_rgb=(1.0, 0.9, 0.1),
                scale_compensate=False,
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
        for i, (fk_jnt, ik_jnt, jnt) in enumerate(
            zip(
                fk_jnts,
                ik_jnts,
                self.main_joints,
                strict=False,
            ),
        ):
            # create blend color nodes
            tran_blend_node = cmds.createNode(
                "blendColors",
                name=f"{self.mod_name}Tran{self.mirr_side}{i + 1:02d}_blendColors",
            )
            rot_blend_node = cmds.createNode(
                "blendColors",
                name=f"{self.mod_name}Rot{self.mirr_side}{i + 1:02d}_blendColors",
            )
            # translate blend
            cmds.connectAttr(f"{fk_jnt}.translate", f"{tran_blend_node}.color1")
            cmds.connectAttr(f"{ik_jnt}.translate", f"{tran_blend_node}.color2")
            cmds.connectAttr(f"{tran_blend_node}.output", f"{jnt}.translate")
            # rotate blend
            cmds.connectAttr(f"{fk_jnt}.rotate", f"{rot_blend_node}.color1")
            cmds.connectAttr(f"{ik_jnt}.rotate", f"{rot_blend_node}.color2")
            cmds.connectAttr(f"{rot_blend_node}.output", f"{jnt}.rotate")

            translate_blend_nodes.append(tran_blend_node)
            rotate_blend_nodes.append(rot_blend_node)

        # parent top fk ik joints to locator constrained to main_joints parent
        # accounts for needed blendColor node transform offset
        self.main_joints_parent = cmds.listRelatives(self.main_joints[0], parent=True)
        if self.main_joints_parent:
            parent_loc = create_locators.locator_snap_parent(
                objects=self.main_joints_parent,
                locator_name=f"{self.mod_name}Offset{self.mirr_side}loc",
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

    def build_fk_ctrls(self):
        """Create fk ctrl chain. Constrain fk joints to follow fk ctrls."""
        fk_ctrl_grps = []
        fk_ctrls = []
        for i, jnt in enumerate(self.fk_jnts):
            # control curve and group
            fk_ctrl = create_nurbs_curves.CreateCurves(
                name=f"fk{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_ctrl",
                size=1.0,
                color_rgb=(1, 0, 0),
            ).box_curve()
            fk_ctrl_grp = create_ctrl_grps(fk_ctrl)[0]

            # snap ctrl group to joint
            cmds.matchTransform(fk_ctrl_grp, jnt)

            # constrain fk joints to follow ctrls
            parent_constr(fk_ctrl, jnt)
            scale_constr(fk_ctrl, jnt)

            # lock and hide attributes
            cmds.setAttr(f"{fk_ctrl}.visibility", lock=True, keyable=False, channelBox=False)

            # create group list for parenting
            fk_ctrl_grps.append(fk_ctrl_grp)
            fk_ctrls.append(fk_ctrl)

        # parent controls and groups together
        for grp, ctrl in zip(fk_ctrl_grps[1:], fk_ctrls, strict=False):
            cmds.parent(grp, ctrl)

        # parent under main fk group
        cmds.parent(fk_ctrl_grps[0], self.fk_top_grp)

        # assign instance variable
        self.fk_ctrls = fk_ctrls

    def build_ik_ctrls(self):
        """Create ik controls. Create ik spline handle and curve.
        Drive ik joints with spline curve. Create ik spline stretch 
        and twist setup.
        """
        # -------------------------------------------------------
        # --------------- create ik spline handle ---------------
        ik_spline_handle, ik_spline_handle_eff, ik_spline_crv = cmds.ikHandle(
            name=f"{self.mod_name}{self.mirr_side}ikHandkle",
            startJoint=self.ik_jnts[0],
            endEffector=self.ik_jnts[-1],
            solver="ikSplineSolver",
            simplifyCurve=False,
            parentCurve=False,
        )
        # rename ikHandle effector
        cmds.rename(ik_spline_handle_eff, f"{ik_spline_handle}Effector")
        ik_spline_crv = cmds.rename(ik_spline_crv, f"{ik_spline_handle}Crv")

        # ---------- start end spline joints ----------
        # for skinning spline curve to
        start_spline_jnt = create_joint.single_joint(
            name=f"{self.mod_name}SplineCrvStart{self.mirr_side}jnt",
            radius=7,
            color_rgb=(0.0, 0.0, 0.0),
            scale_compensate=False,
            parent_snap=self.ik_jnts[0],
        )
        end_spline_jnt = create_joint.single_joint(
            name=f"{self.mod_name}SplineCrvEnd{self.mirr_side}jnt",
            radius=7,
            color_rgb=(0.0, 0.0, 0.0),
            scale_compensate=False,
            parent_snap=self.ik_jnts[-1],
        )
        # parent end to start joint
        cmds.parent(end_spline_jnt, start_spline_jnt)

        # ---------- skin spline curve to start end joints ----------
        cmds.skinCluster(
            start_spline_jnt,
            end_spline_jnt,
            ik_spline_crv,
            n=f"{ik_spline_crv}SkinCluster",
        )
        # ---------- smooth curve skin weights ----------
        self.smooth_crv_weights(
            ik_spline_crv,
            start_spline_jnt,
            end_spline_jnt,
            # smoothstep=True,
            # smootherstep=True,
            # smooth_sine=True,
            smooth_cubic=True,
        )

        # ------------------------------------------------------
        # --------------- create ik spline ctrls ---------------
        # ---------- start ctrl ----------
        ik_start_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.mod_name)}Start{self.mirr_side}ctrl",
            size=1,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()
        ik_start_ctrl_grp = create_ctrl_grps(ik_start_ctrl)[0]  # grp ctrl
        cmds.matchTransform(ik_start_ctrl_grp, self.ik_jnts[0])  # snap ctrl group to joint
        # constrain start joint to follow start ctrl
        parent_constr(ik_start_ctrl, start_spline_jnt)
        scale_constr(ik_start_ctrl, start_spline_jnt)

        # ---------- mid ctrl ----------
        ik_mid_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.mod_name)}Mid{self.mirr_side}ctrl",
            size=1,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()
        ik_mid_ctrl_grp = create_ctrl_grps(ik_mid_ctrl)[0]  # grp ctrl
        # transform ik mid control between first and last ik joints
        mid_transform_const = parent_constr((self.ik_jnts[0], self.ik_jnts[-1]), ik_mid_ctrl_grp)
        cmds.delete(mid_transform_const)
        # parent mid under start ctrl
        cmds.parent(ik_mid_ctrl_grp, ik_start_ctrl)

        # ---------- end ctrl ----------
        ik_end_ctrl = create_nurbs_curves.CreateCurves(
            name=f"ik{cap(self.mod_name)}End{self.mirr_side}ctrl",
            size=1,
            color_rgb=(0.1, 1.0, 0.0),
        ).box_curve()
        ik_end_ctrl_grp = create_ctrl_grps(ik_end_ctrl)[0]  # grp ctrl
        cmds.matchTransform(ik_end_ctrl_grp, self.ik_jnts[-1])  # snap ctrl grp to joint
        # parent end under mid ctrl
        cmds.parent(ik_end_ctrl_grp, ik_mid_ctrl)
        # constrain end joint to follow end ctrl
        parent_constr(ik_end_ctrl, end_spline_jnt)
        scale_constr(ik_end_ctrl, end_spline_jnt)

        # -----------------------------------------------------
        # --------------- ik handle twist setup ---------------
        # get down the chain axis
        down_chain_axis = query_main_axis(
            parent_jnt=self.main_joints[0],
            child_jnt=self.main_joints[1],
            mod_name=self.mod_name,
            mirr_side=self.mirr_side,
        )
        forward_axis = 0  # Positive X
        if down_chain_axis == "-x":
            forward_axis = 1  # Negative X
        # create locator up objects for spline twist control
        ik_start_loc = create_locators.axis_locator(
            objects=ik_start_ctrl,
            locator_name=f"ik{cap(self.mod_name)}UpObjStart{self.mirr_side}loc",
            local_scale=(5, 5, 5),
        )[0][0]
        ik_end_loc = create_locators.axis_locator(
            objects=ik_end_ctrl,
            locator_name=f"ik{cap(self.mod_name)}UpObjEnd{self.mirr_side}loc",
            local_scale=(5, 5, 5),
        )[0][0]
        # enable advanced twist controls
        cmds.setAttr(f"{ik_spline_handle}.dTwistControlEnable", 1)
        # World Up Type: Object Rotation Up (Start/End)
        cmds.setAttr(f"{ik_spline_handle}.dWorldUpType", 4)
        # Forward Axis: Positive or Negative X. Down the chain axis.
        cmds.setAttr(f"{ik_spline_handle}.dForwardAxis", forward_axis)
        # Up Axis: Positive Y
        cmds.setAttr(f"{ik_spline_handle}.dWorldUpAxis", 0)
        # Up Vector: 1.0 Y. Match jnt and locator axis.
        cmds.setAttr(f"{ik_spline_handle}.dWorldUpVectorY", 1.0)
        cmds.setAttr(f"{ik_spline_handle}.dWorldUpVectorEndY", 1.0)
        # World Up Object
        cmds.connectAttr(f"{ik_start_loc}.worldMatrix[0]", f"{ik_spline_handle}.dWorldUpMatrix")
        # World Up Object 2
        cmds.connectAttr(f"{ik_end_loc}.worldMatrix[0]", f"{ik_spline_handle}.dWorldUpMatrixEnd")

        # ---------- start parent twist blend ----------
        # determines whether start twist is controlled by parent joint or start ctrl
        if self.main_joints_parent:
            start_parent_twist_const = parent_constr(
                self.main_joints_parent,
                ik_start_loc,
                skip_tran=True,
                offset=True,
            )
            add_divider_attribue(control_name=ik_start_ctrl, divider_amount=10)
            cmds.addAttr(
                ik_start_ctrl,
                longName="startTwistBlend",
                minValue=0.0,
                maxValue=1.0,
                defaultValue=0.0,
                keyable=True,
            )
            cmds.connectAttr(
                f"{ik_start_ctrl}.startTwistBlend",
                f"{start_parent_twist_const}.target[0].targetWeight",
                force=True,
            )
            start_twist_blend_reverse_nd = cmds.createNode(
                "reverse",
                name=f"{self.mod_name}StartTwistBlend{self.mirr_side}reverse",
            )
            # attach start ctrl again, for smooth blending
            cmds.connectAttr(
                f"{ik_start_ctrl}.startTwistBlend",
                f"{start_twist_blend_reverse_nd}.inputX",
            )
            cmds.connectAttr(
                f"{start_twist_blend_reverse_nd}.outputX",
                f"{start_parent_twist_const}.target[1].targetWeight",
                force=True,
            )

        # -------------------------------------------------
        # --------------- create ik stretch ---------------
        # stretch attr
        add_divider_attribue(control_name=ik_start_ctrl, divider_amount=9)
        cmds.addAttr(
            ik_start_ctrl,
            longName="stretch",
            minValue=0.0,
            maxValue=1.0,
            defaultValue=1.0,
            keyable=True,
        )
        # create and attach ruler to controls
        *_, blendcolors_nd, global_scale_nd = create_attached_ruler(
            name=f"ik{cap(self.mod_name)}Ruler{self.mirr_side}",
            ruler_start_object=ik_start_ctrl,
            ruler_end_object=ik_end_ctrl,
            parent_hide_grp=self.ik_top_grp,
            include_stretch_nodes=True,
        )
        # stretch attr to blendColors stretch on/off toggle
        cmds.connectAttr(f"{ik_start_ctrl}.stretch", f"{blendcolors_nd}.blender")
        # connect ruler distance ratio to ik joints translateX
        for i, ik_jnt in enumerate(self.ik_jnts[1:]):
            multiplydivide_nd = cmds.createNode(
                "multiplyDivide",
                name=f"ik{cap(self.mod_name)}Stretch{self.mirr_side}{i + 1:02d}_multiplyDivide",
            )
            jnt_trans_x = cmds.getAttr(f"{ik_jnt}.translateX")
            cmds.connectAttr(f"{blendcolors_nd}.outputR", f"{multiplydivide_nd}.input1X")
            cmds.setAttr(f"{multiplydivide_nd}.input2X", jnt_trans_x)
            cmds.connectAttr(f"{multiplydivide_nd}.outputX", f"{ik_jnt}.translateX")

        # ----- ik stretch global scale -----
        # start ctrl world space scaleX to stretch distance scale offset
        decomposematrix_nd = cmds.createNode(
            "decomposeMatrix",
            name=f"{self.mod_name}StretchGlobalScale{self.mirr_side}decomposeMatrix",
        )
        cmds.connectAttr(f"{ik_start_ctrl}.worldMatrix[0]", f"{decomposematrix_nd}.inputMatrix")
        cmds.connectAttr(f"{decomposematrix_nd}.outputScaleX", f"{global_scale_nd}.input1X")

        # ---------------------------------------------------
        # ---------- lock/ hide attrs. visibility. ----------
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for ctrl in (ik_start_ctrl, ik_mid_ctrl, ik_end_ctrl):
            for axis in "XYZ":
                cmds.setAttr(f"{ctrl}.scale{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{ctrl}.visibility", **lock_hide_kwargs)

        for obj in (ik_start_loc, ik_end_loc):
            for axis in "XYZ":
                if obj == ik_end_loc:
                    cmds.setAttr(f"{obj}.rotate{axis}", lock=True)
                cmds.setAttr(f"{obj}.translate{axis}", lock=True)
                cmds.setAttr(f"{obj}.scale{axis}", lock=True)
            cmds.setAttr(f"{obj}.visibility", 0)
            cmds.setAttr(f"{obj}.visibility", lock=True)

        # ----- top group parenting -----
        for obj in (ik_spline_handle, ik_spline_crv, start_spline_jnt):
            cmds.parent(obj, self.ik_top_grp)
            cmds.setAttr(f"{obj}.visibility", 0)
        cmds.parent(ik_start_ctrl_grp, self.ik_top_grp)

    def build_switch_ctrl(self):
        """Create fk ik switch ctrl."""
        # ---------- create control crv and grp ----------
        switch_ctrl = create_nurbs_curves.CreateCurves(
            name=f"{self.mod_name}Swch{self.mirr_side}ctrl",
            size=1,
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

        # ----- connect switch control to visibility -----
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

    def smooth_crv_weights(
        self,
        spline_crv: str,
        start_jnt: str,
        end_jnt: str,
        smoothstep: bool = False,
        smootherstep: bool = False,
        smooth_sine: bool = False,
        smooth_cubic: bool = False,
    ) -> None:
        """Smooth vertex skin weights for ik spline curve.
        Set smoothing per cv from start to end joint.
        Linear smoothing is default. Enable a smooth arg if needed.
        Skin cluster between two joints should already be created for curve.

        Args:
            spline_crv: Spline curve used by the ik spline handle,
                or any curve skinned between two joints.
            start_jnt: The first joint for the spline curve skinning.
            end_jnt: The second and last joint for the spline curve skinning.
            smoothstep: Smooth ease in/out for curve weights instead of linear.
            smootherstep: An even smoother ease in/out for curve weights.
            smooth_sine: Curve smoothness inbetween smoothstep and smootherstep.
            smooth_cubic: Sharp acceleration/deceleration smooth.
                More dramatic. Slow start/end, rapid change in middle.

        """
        if sum([smoothstep, smootherstep, smooth_sine, smooth_cubic]) > 1:
            msg = "Should only have one smoothing option for smooth_crv_weights()."
            self.logger.error(msg)
            raise ValueError(msg)

        crv_verts = cmds.getAttr(f"{spline_crv}.cv[*]")
        crv_skin_cluster = cmds.ls(cmds.listHistory(spline_crv), type="skinCluster")[0]

        num_vrts = len(crv_verts)
        weights = []
        if smoothstep:  # smoothstep ease in out curve weights
            for i in range(num_vrts):
                weight = i / (num_vrts - 1)  # normalize to 0-1 range
                weight = 3 * weight**2 - 2 * weight**3
                weights.append(weight)
        elif smootherstep:  # even smoother
            for i in range(num_vrts):
                weight = i / (num_vrts - 1)
                weight = 6 * weight**5 - 15 * weight**4 + 10 * weight**3
                weights.append(weight)
        elif smooth_sine:  # inbetween smoothstep and smootherstep
            for i in range(num_vrts):
                weight = i / (num_vrts - 1)
                weight = (1 - math.cos(weight * math.pi)) / 2
                weights.append(weight)
        elif smooth_cubic:  # sharper acceleration/deceleration
            for i in range(num_vrts):
                weight = i / (num_vrts - 1)
                if weight < 0.5:
                    weight = 4 * weight**3
                else:
                    weight = 1 - (-2 * weight + 2) ** 3 / 2
                weights.append(weight)
        else:  # equally distributed linear curve weights
            weight_increase = 1.0 / (num_vrts - 1)  # x verts means x-1 sections
            weight = 0
            for i in range(num_vrts):
                weights.append(weight)
                weight += weight_increase
        weights = [round(weight, 6) for weight in weights]

        # apply vertex weights to spline curve
        for i, weight in enumerate(weights):
            cmds.skinPercent(
                crv_skin_cluster,
                f"{spline_crv}.cv[{i}]",
                transformValue=((start_jnt, 1.0 - weight), (end_jnt, weight)),
            )
