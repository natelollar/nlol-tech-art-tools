from maya import cmds
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_nurbs_curves,
)
from nlol.utilities.nlol_maya_logger import get_logger

parent_constr = clean_constraints.parent_constr
point_constr = clean_constraints.point_constr
orient_constr = clean_constraints.orient_constr
aim_constr = clean_constraints.aim_constr
scale_constr = clean_constraints.scale_constr
create_ctrl_grps = create_control_groups.create_ctrl_grps
CreateCurves = create_nurbs_curves.CreateCurves

logger = get_logger()


class PistonMod:
    """Create hydraulic style piston rig module with three-axis gimbal connection on both ends.
    Should be built at origin. Orient the piston joints to world space scene Y-up.
    Joints should be planar aligned on YZ plane. Piston center should be straight up and down.
    Should be one mid joint and three top and bottom joints.
    First two top and bottom joints should have the same position. And third joint extends towards
    where the piston would connect to another object.
    The top and bottom joints should be listed in order.
    See example setup in "defaults/piston_mod" folder.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        origin_joint: list[str],
        mid_joints: list[str],
        top_joints: list[str],
        bot_joints: list[str],
    ):
        """Args:
        rig_module_name: Rig module base name. Example: "hydraulicPiston".
        mirror_direction: Optional. The mirror side. Example: "left" or "right".
        origin_joint: Optional. Root joint for the rig module.
            Allows easier scaling and positioning.
        mid_joints: The single mid joint skinned to the bulk of the piston middle.
        top_joints: The three skinned top joints controlling the top "three-axis gimbal".
            Also, first two joints used for placements and gimbal aiming.
            End joint used for end aim curve placement and top ik end joint placement.
        bot_joints: Same as top_joints except for the bottom.
        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.origin_joint = origin_joint
        self.mid_joints = mid_joints
        self.top_joints = top_joints
        self.bot_joints = bot_joints

        self.input_checks()

    def build(self):
        """Entry point. Run method to build rig module.
        --------------------------------------------------

        Returns:
            Top group for rig module.

        """
        self.setup_top_grps()
        self.setup_single_ikchains()
        self.setup_ctrls()
        self.setup_aim_crvs()
        self.parenting_connections()
        self.setup_distance_node()

        return self.mod_top_grp

    def setup_top_grps(self):
        """Create top rig module groups for organization."""
        self.mod_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}grp",
        )

    def setup_single_ikchains(self):
        """Set up "Single-Chain Solver" ik chains and joints."""
        # main ik chain
        self.ikmain_start_jnt, self.ikmain_end_jnt, self.ikmain_handle, _ = (
            self.create_single_ikchain(
                start_jnt=self.bot_joints[0],
                end_jnt=self.top_joints[0],
                jnt_radius=3,
                jnt_color=(1.0, 0.2, 0.2),
                base_name=f"{self.mod_name}ikChainMain",
                parent_grp=self.mod_top_grp,
            )
        )
        # top ik chain
        self.iktop_start_jnt, self.iktop_end_jnt, self.iktop_handle, _ = self.create_single_ikchain(
            start_jnt=self.top_joints[1],
            end_jnt=self.top_joints[2],
            jnt_radius=1.5,
            jnt_color=(0.2, 0.8, 0.2),
            base_name=f"{self.mod_name}ikChainTop",
            parent_grp=self.mod_top_grp,
        )
        cmds.parent(self.iktop_start_jnt, self.ikmain_end_jnt)
        # bot ik chain
        self.ikbot_start_jnt, self.ikbot_end_jnt, self.ikbot_handle, _ = self.create_single_ikchain(
            start_jnt=self.bot_joints[1],
            end_jnt=self.bot_joints[2],
            jnt_radius=1.5,
            jnt_color=(0.2, 0.8, 0.2),
            base_name=f"{self.mod_name}ikChainBot",
            parent_grp=self.mod_top_grp,
        )
        cmds.parent(self.ikbot_start_jnt, self.ikmain_start_jnt)

    def create_single_ikchain(
        self,
        start_jnt: str,
        end_jnt: str,
        base_name: str,
        jnt_radius: float = 1,
        jnt_color: tuple = (1.0, 0.4, 0.0),
        parent_grp: str | None = None,
    ) -> tuple[str]:
        """Create "Single-Chain Solver" for 2 input joints.

        Args:
            start_jnt: Parent joint in chain.
            end_jnt: Child joint in chain.
            base_name: camelCase name component, as in, nLol naming convention.
                Basic name string prefix.
            jnt_radius: Created joints viewport size.
            jnt_color: Created joints viewport color.
            parent_grp: Organization group to parent joint and ikHandle under.

        Returns:
            Joints, ik handle, and ik effector.

        """
        ik_start_jnt = create_joint.single_joint(
            name=f"{base_name}Start{self.mirr_side}jnt",
            radius=jnt_radius,
            color_rgb=jnt_color,
            parent_snap=start_jnt,
        )
        ik_end_jnt = create_joint.single_joint(
            name=f"{base_name}End{self.mirr_side}jnt",
            radius=jnt_radius,
            color_rgb=jnt_color,
            parent_snap=end_jnt,
        )
        cmds.parent(ik_end_jnt, ik_start_jnt)

        ik_handle, ik_handle_effector = cmds.ikHandle(
            name=f"{base_name}_ikHandle",
            startJoint=ik_start_jnt,
            endEffector=ik_end_jnt,
            solver="ikSCsolver",
        )
        ik_handle_effector = cmds.rename(ik_handle_effector, f"{ik_handle}Effector")

        if parent_grp:
            cmds.parent(ik_start_jnt, ik_handle, self.mod_top_grp)

        # hide
        cmds.setAttr(f"{ik_start_jnt}.visibility", 0)
        cmds.setAttr(f"{ik_handle}.visibility", 0)

        return ik_start_jnt, ik_end_jnt, ik_handle, ik_handle_effector

    def setup_ctrls(self):
        """Create usable control curves.
        Also used for general setup and aiming.
        """
        # create base ctrl if origin joint
        base_ctrl = None
        if self.origin_joint:
            base_ctrl = create_nurbs_curves.CreateCurves(
                name=f"{self.mod_name}Base{self.mirr_side}ctrl",
                size=0.75,
                color_rgb=(0.8, 0.8, 0.0),
            ).hexadecagon_curve()
            base_ctrl_grp, *_ = create_ctrl_grps(base_ctrl)
            cmds.matchTransform(base_ctrl_grp, self.origin_joint)
            parent_constr(base_ctrl, self.origin_joint)
            scale_constr(base_ctrl, self.origin_joint)

        # create main top and bottom ctrls
        jnt_region = {
            "Top": (self.ikmain_end_jnt, self.top_joints[-1]),
            "Bot": (self.ikmain_start_jnt, self.bot_joints[-1]),
        }
        self.ikmain_ctrls = []
        self.ikparent_ctrls = []
        for region, (ikmain_jnt, topbot_end_jnt) in jnt_region.items():
            ikmain_ctrl = create_nurbs_curves.CreateCurves(
                name=f"{self.mod_name}ikMain{region}{self.mirr_side}ctrl",
                size=0.75,
                color_rgb=(0.8, 0.8, 0.0),
            ).square_curve()
            ikmain_ctrl_grp, *_ = create_ctrl_grps(ikmain_ctrl)
            cmds.matchTransform(ikmain_ctrl_grp, ikmain_jnt)

            ikparent_ctrl = create_nurbs_curves.CreateCurves(
                name=f"{self.mod_name}ikParent{region}{self.mirr_side}ctrl",
                size=1.0,
                color_rgb=(0.5, 0.25, 1.0),
            ).square_curve()
            ikparent_ctrl_grp, *_ = create_ctrl_grps(ikparent_ctrl)
            cmds.matchTransform(ikparent_ctrl_grp, topbot_end_jnt)

            # parenting
            cmds.parent(ikmain_ctrl_grp, ikparent_ctrl)
            if base_ctrl:
                cmds.parent(ikparent_ctrl_grp, base_ctrl)
                cmds.parent(base_ctrl_grp, self.mod_top_grp)
            else:
                cmds.parent(ikparent_ctrl_grp, self.mod_top_grp)

            # hide
            cmds.setAttr(f"{ikmain_ctrl_grp}.visibility", 0)
            # lock
            lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
            for axis in "XYZ":
                cmds.setAttr(f"{ikmain_ctrl}.scale{axis}", **lock_hide_kwargs)
                cmds.setAttr(f"{ikparent_ctrl}.scale{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{ikmain_ctrl}.visibility", **lock_hide_kwargs)
            cmds.setAttr(f"{ikparent_ctrl}.visibility", **lock_hide_kwargs)

            # append
            self.ikmain_ctrls.append(ikmain_ctrl)
            self.ikparent_ctrls.append(ikparent_ctrl)

    def setup_aim_crvs(self):
        """Create locator shaped curves for gimbal axis aiming.
        Curves centered at the top and bottom joints, straight up and down from 
        the top and bot joints, and at the ends of the top and bot joint chains 
        for the gimbal axis to aim at.
        """
        jnt_region = {
            "Top": (self.ikmain_end_jnt, self.top_joints[-1], 65, self.ikparent_ctrls[0]),
            "Bot": (self.ikmain_start_jnt, self.bot_joints[-1], -65, self.ikparent_ctrls[1]),
        }
        self.aim_02_crvs = []
        self.aim_crv_grps = []
        self.aim_up_crvs = []
        self.end_aim_crvs = []
        self.end_aim_crv_grps = []
        for region, (ikmain_jnt, topbot_end_jnt, y_offset, ikparent_ctrl) in jnt_region.items():
            # ----- centered at top and bottom joints -----
            aim_01_crv = CreateCurves(
                name=f"{self.mod_name}Aim{region}_01{self.mirr_side}crv",
                size=1.0,
                color_rgb=(0.8, 0.2, 0.4),
            ).locator_curve()
            aim_02_crv = CreateCurves(
                name=f"{self.mod_name}Aim{region}_02{self.mirr_side}crv",
                size=0.7,
                color_rgb=(0.2, 0.4, 0.8),
                line_width=3.0,
            ).locator_curve()
            cmds.parent(aim_02_crv, aim_01_crv)

            aim_crv_grp = cmds.group(
                aim_01_crv,
                name=f"{self.mod_name}Aim{region}{self.mirr_side}crvGrp",
            )
            cmds.matchTransform(aim_crv_grp, ikmain_jnt)
            parent_constr(ikmain_jnt, aim_crv_grp, offset=True)
            scale_constr(ikmain_jnt, aim_crv_grp)

            # ----- straight up and down from top and bot joints -----
            aim_up_crv = CreateCurves(
                name=f"{self.mod_name}AimUp{region}{self.mirr_side}crv",
                size=0.5,
                color_rgb=(0.2, 0.8, 0.8),
            ).locator_curve()
            aim_up_crv_grp = cmds.group(
                aim_up_crv,
                name=f"{aim_up_crv}Grp",
            )
            cmds.matchTransform(aim_up_crv_grp, ikmain_jnt)

            cmds.xform(aim_up_crv_grp, translation=(0, y_offset, 0))

            parent_constr(ikmain_jnt, aim_up_crv_grp, offset=True)

            # ----- end aim point for gimbal axis mechanism -----
            end_aim_crv = CreateCurves(
                name=f"{self.mod_name}EndAim{region}{self.mirr_side}crv",
                size=1.0,
                color_rgb=(0.8, 0.2, 0.4),
            ).locator_curve()

            end_aim_crv_grp = cmds.group(
                end_aim_crv,
                name=f"{end_aim_crv}Grp",
            )
            cmds.matchTransform(end_aim_crv_grp, topbot_end_jnt)
            cmds.parent(end_aim_crv_grp, ikparent_ctrl)

            # ----- top grp parenting -----
            cmds.parent(aim_crv_grp, self.mod_top_grp)
            cmds.parent(aim_up_crv_grp, self.mod_top_grp)

            # ----- hide -----
            cmds.setAttr(f"{aim_crv_grp}.visibility", 0)
            cmds.setAttr(f"{aim_up_crv_grp}.visibility", 0)
            cmds.setAttr(f"{end_aim_crv_grp}.visibility", 0)

            # ----- append -----
            self.aim_02_crvs.append(aim_02_crv)
            self.aim_crv_grps.append(aim_crv_grp)
            self.aim_up_crvs.append(aim_up_crv)
            self.end_aim_crvs.append(end_aim_crv)
            self.end_aim_crv_grps.append(end_aim_crv_grp)

    def parenting_connections(self):
        """Create additional object parenting relationships and connections."""
        # parent main ik handle
        cmds.parent(self.ikmain_handle, self.ikmain_ctrls[0])
        # constrain ikmain start jnt
        point_constr(self.ikmain_ctrls[1], self.ikmain_start_jnt)
        scale_constr(self.ikmain_ctrls[1], self.ikmain_start_jnt)
        # constrain mid joint
        parent_constr(self.aim_02_crvs[1], self.mid_joints[0], offset=True)

        # top and bot parenting and connections
        jnt_region = {
            "Top": (
                self.end_aim_crvs[0],
                self.iktop_handle,
                self.top_joints[0],
                self.aim_02_crvs[0],
                self.top_joints[1],
                self.iktop_start_jnt,
                "y",
                self.aim_up_crvs[0],
                self.end_aim_crv_grps[0],
            ),
            "Bot": (
                self.end_aim_crvs[1],
                self.ikbot_handle,
                self.bot_joints[0],
                self.aim_02_crvs[1],
                self.bot_joints[1],
                self.ikbot_start_jnt,
                "-y",
                self.aim_up_crvs[1],
                self.end_aim_crv_grps[1],
            ),
        }
        for region, (
            end_aim_crv,
            topbot_ik_handle,
            topbot_start_jnt,
            aim_02_crv,
            topbot_second_jnt,
            topbot_ik_start_jnt,
            up_vector,
            aim_up_crv,
            end_aim_crv_grp,
        ) in jnt_region.items():
            # parent top and bot ik handles
            cmds.parent(topbot_ik_handle, end_aim_crv)
            # constrain first topbot jnts
            parent_constr(aim_02_crv, topbot_start_jnt)

            # constrain top and bot gimbal aiming
            orient_constr(topbot_ik_start_jnt, aim_02_crv, skip_x=True, skip_z=True)
            orient_constr(topbot_ik_start_jnt, topbot_second_jnt, skip_y=True)
            aim_constr(
                targets=aim_up_crv,
                object=end_aim_crv_grp,
                world_up_object=aim_up_crv,
                aim_vector=up_vector,
                up_vector=up_vector,
                offset=True,
                skip_x=True,
                skip_y=True,
            )

    def setup_distance_node(self):
        """Set up distance stretch node for main vertical axis
        allowing the piston to move in and out.
        The distance node controls the length of the main ik end joint.
        Assumes Y down the chain, for the sake of keeping all joints world oriented.
        Add decomposeMatrix and multiplyDivide nodes to account for global scale.
        """
        # ----------
        distancebetween_nd = cmds.createNode(
            "distanceBetween",
            name=f"{self.mod_name}ikMainStretch{self.mirr_side}distanceBetween",
        )
        decomposematrix_nd = cmds.createNode(  # for scale offset
            "decomposeMatrix",
            name=f"{self.mod_name}ikMainStretch{self.mirr_side}decomposeMatrix",
        )
        multiplydivide_nd = cmds.createNode(  # for scale offset
            "multiplyDivide",
            name=f"{self.mod_name}ikMainStretch{self.mirr_side}multiplyDivide",
        )
        cmds.setAttr(f"{multiplydivide_nd}.operation", 2)  # divide
        # ----------
        cmds.connectAttr(
            f"{self.ikmain_ctrls[0]}.worldMatrix[0]",
            f"{distancebetween_nd}.inMatrix1",
        )
        cmds.connectAttr(
            f"{self.ikmain_ctrls[1]}.worldMatrix[0]",
            f"{distancebetween_nd}.inMatrix2",
        )
        cmds.connectAttr(
            f"{self.ikmain_ctrls[1]}.worldMatrix[0]",
            f"{decomposematrix_nd}.inputMatrix",
        )
        # ----------
        cmds.connectAttr(
            f"{distancebetween_nd}.distance",
            f"{multiplydivide_nd}.input1X",
        )
        cmds.connectAttr(
            f"{decomposematrix_nd}.outputScaleX",
            f"{multiplydivide_nd}.input2X",
        )
        # ----------
        cmds.connectAttr(
            f"{multiplydivide_nd}.outputX",
            f"{self.ikmain_end_jnt}.translateY",
        )

    def input_checks(self):
        """Validate class args. Check input data."""
        required_joints = {
            "mid_joints": 1,
            "top_joints": 3,
            "bot_joints": 3,
        }
        if self.origin_joint:
            required_joints["origin_joint"] = 1

        errors = []
        for jnt_var, required_count in required_joints.items():
            jnt_list = getattr(self, jnt_var)

            if len(jnt_list) != required_count:
                errors.append(
                    f"{self.mod_name}, {jnt_list}: Include exactly {required_count} {jnt_var}. ",
                )

            for jnt in jnt_list:
                if not cmds.objExists(jnt):
                    errors.append(f'{self.mod_name}: Joint "{jnt}" does not exist.')

        if errors:
            errors.append('See example rig module in "defaults/piston_mod".')
            error_msg = "\n".join(errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
