from importlib import reload

from maya import cmds
from nlol.core.general_utils import add_divider_attribue, cap
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_nurbs_curves,
    create_ruler,
    follicle_at_surface,
)
from nlol.core.rig_modules import fk_chain_mod
from nlol.utilities.nlol_maya_logger import get_logger

reload(create_joint)

create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
point_constr = clean_constraints.point_constr
scale_constr = clean_constraints.scale_constr
create_attached_ruler = create_ruler.create_attached_ruler


class FlexiSurfaceIkChainSimpleModule:
    """Flexi surface that uses ik chain instead of separated fk ctrls.
    Attaches joint chain to flexiSurface geo.
    Requires "x" or "-x" down the chain.
    Attached via follicles and ik single-chain solvers.
    Also, has an fk ctrl chain offset.
    Has stretch and uv slide.  Slide works when stretch on.
    Currently, acts as a rig sub-module, needing ctrls for flexiSurface skinned joints.

    Entry Points:
        - scale constrain the parent ctrl
        - parent & scale constrain the top flexiSurface skin joint

    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list[str],
        flexi_surface: str = "flexiSurface_geo",
        hide_end_ctrl: bool = False,
        hide_all_ctrls: bool = False,
    ):
        """Initialize rig module.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: String describing mirror side. Ex. "left", "right".
            main_joints: The main skinned joints.
            flexi_surface: Polygonal or nurbs mesh object to attach Maya (hair) follicles to.
                This mesh object would be skinned to some joints for base movement.
                Should contain the string "flexiSurface".
            hide_end_ctrl: Hide last of the created fk controls.
            hide_all_ctrls: Hide all the fk offset ctrls.

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints
        self.flexi_surface = flexi_surface
        self.hide_end_ctrl = hide_end_ctrl
        self.hide_all_ctrls = hide_all_ctrls

        self.logger = get_logger()

    def build(self) -> str:
        """Main build method for flexi surface rig module.
        --------------------------------------------------
        Create and attach follicles on flexi surface closest to each joint position.
        Create and attach an fk chain to these follicles via ik single chain solvers.
        Add stretch attribute to allow joint length to optionally stretch with follicles.
        Add uv slide attribute for extra follicle movement.
        Add parent ctrl for attributes and global scale.

        Returns:
            Rig module top group.

        """
        # ----- create top groups -----
        self.create_top_grps()
        self.create_follices()
        self.create_ikjoints_ikhandles()
        self.create_offset_fkctrls()
        self.create_parent_ctrl()
        self.create_jnt_connection_offsets()
        self.create_uv_slide()
        self.create_ik_stretch()
        self.hide_lock_items()
        self.top_grouping()

        return self.mod_top_grp

    def create_top_grps(self):
        """Create top groups for rig module organization."""
        self.mod_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}Main{self.mirr_side}grp",
        )
        self.follicle_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}follicleGrp",
        )
        self.ikhandle_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}ikHandleGrp",
        )
        self.ik_stretch_top_grp = cmds.group(
            empty=True,
            name=f"ik{cap(self.mod_name)}Stretch{self.mirr_side}grp",
        )
        self.fk_ctrl_top_grp = cmds.group(
            empty=True,
            name=f"fk{cap(self.mod_name)}{self.mirr_side}ctrlGrp",
        )

        # parent groups
        cmds.parent(self.follicle_top_grp, self.mod_top_grp)
        cmds.parent(self.ikhandle_top_grp, self.mod_top_grp)
        cmds.parent(self.ik_stretch_top_grp, self.mod_top_grp)
        cmds.parent(self.fk_ctrl_top_grp, self.mod_top_grp)

    def create_follices(self):
        """Create Maya follicles along flexi surface at nearest main joint position."""
        # follicles to flexi surface
        self.follicles = []
        self.follicle_shapes = []
        for i, jnt in enumerate(self.main_joints):
            follicle, follicle_shape, _ = follicle_at_surface.create_joint_follicle(
                flexi_surface=self.flexi_surface,
                joint=jnt,
                name=f"{self.mod_name}{self.mirr_side}{i + 1:02d}",
            )
            self.follicles.append(follicle)
            self.follicle_shapes.append(follicle_shape)

    def create_ikjoints_ikhandles(self):
        """Setup ik joints and ik handles."""
        self.setup_iksinglesolver_chain(
            joint_chain=self.main_joints,
            follicle_chain=self.follicles,
        )

    def setup_iksinglesolver_chain(
        self,
        joint_chain: list[str],
        follicle_chain: list[str],
    ) -> list[str]:
        """Create ik joint chain along main skinned joint chain
        and setup ik single-chain solvers along this ik joint chain.
        Constrain top ik joint and ik handles to flexi surface follicles.

        Args:
            joint_chain: List of joints in main skinned joint chain.
            follicle_chain: List of follicles used for setting up flexi ik chain.

        Returns:
            List of ik joints.

        """
        # ----- create ik joints -----
        # create parent joint for direct connections offset
        ik_parent_jnt = create_joint.single_joint(
            name=f"ik{cap(self.mod_name)}Parent{self.mirr_side}jnt",
            radius=10,
            color_index=1,
            scale_compensate=False,
            parent_snap=joint_chain[0],
        )

        # create main ik joint chain
        ik_jnts = []
        for i, (jnt, foll) in enumerate(zip(joint_chain, follicle_chain, strict=False)):
            ik_jnt = create_joint.single_joint(
                name=f"ik{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_jnt",
                radius=1,
                color_index=1,
                scale_compensate=False,
                parent_snap=jnt,
            )
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)
            ik_jnts.append(ik_jnt)

        # parent ik joints into chain
        # add offset joint to front of list
        ik_joint_chain = [ik_parent_jnt] + ik_jnts
        for i in range(1, len(ik_joint_chain)):
            cmds.parent(ik_joint_chain[i], ik_joint_chain[i - 1])

        # ----- setup point constraint and ik handles -----
        # skip ik parent offset joint
        ik_handles = []
        for i, (ik_jnt, foll) in enumerate(zip(ik_jnts, follicle_chain, strict=False)):
            if i == 0:  # point constrain first ik joint
                point_constr(foll, ik_jnt)
            else:
                # ----- ik handle with single-chain solver -----
                # ik handle between current joint and previous joint
                ik_handle, ik_handle_effector = cmds.ikHandle(
                    name=f"{self.mod_name}{self.mirr_side}{i:02d}_ikHandle",
                    startJoint=ik_jnts[i - 1],
                    endEffector=ik_jnt,
                    solver="ikSCsolver",
                )
                cmds.rename(ik_handle_effector, f"{ik_handle}Effector")  # rename effector

                parent_constr(foll, ik_handle, offset=True)

                ik_handles.append(ik_handle)

        # ----- assign instance variables -----
        self.ik_jnts = ik_jnts
        self.ik_parent_jnt = ik_parent_jnt
        self.ik_handles = ik_handles

    def create_offset_fkctrls(self):
        """Creat offset fk ctrls.
        May be used to offset from flexi ctrls attached to flexiSurface geo.
        """
        self.fk_ctrl_grps, _, self.fk_ctrl_swch_grps, _, self.fk_ctrl_aux_grps, self.fk_ctrls = (
            fk_chain_mod.FkChainModule(
                rig_module_name=f"fk{cap(self.mod_name)}",
                mirror_direction=self.mirr_side,
                main_joints=self.main_joints,
                aux_offset_grp=True,
                return_all_grps=True,
            ).build()
        )

    def create_jnt_connection_offsets(self):
        """Create plusMinusAverage offsets for joint direct connections."""
        for i, (ik_jnt, aux_grp) in enumerate(
            zip(self.ik_jnts, self.fk_ctrl_aux_grps, strict=False),
        ):
            offset_translate_nd = cmds.createNode(
                "plusMinusAverage",
                name=(f"{self.mod_name}Translate{self.mirr_side}{i + 1:02d}_plusMinusAverage"),
            )

            # query and apply plusMinusAverage offset values
            ik_jnt_translate = cmds.getAttr(f"{ik_jnt}.translate")[0]
            ik_jnt_translate = [-1 * val for val in ik_jnt_translate]
            cmds.setAttr(f"{offset_translate_nd}.input3D[1]", *ik_jnt_translate)

            # keep aux_grp zeroed out with plusMinusAverage offset values
            # ik_jnt > plusMinusAverage > aux_grp
            cmds.connectAttr(f"{ik_jnt}.translate", f"{offset_translate_nd}.input3D[0]")
            cmds.connectAttr(f"{offset_translate_nd}.output3D", f"{aux_grp}.translate")

            # direct connection for rotate. already zeroed out.
            cmds.connectAttr(f"{ik_jnt}.rotate", f"{aux_grp}.rotate")

        # # parent ctrl scale to first fk ctrl aux grp
        # scale_constr(self.parent_fk_ctrl, self.fk_ctrl_aux_grps[0])
        # # parent ctrl scale to first ik joint, after parent ik joint
        # scale_constr(self.parent_fk_ctrl, self.ik_jnts[0])
        cmds.parent(self.fk_ctrl_grps[0], self.parent_fk_ctrl)
        cmds.parent(self.ik_parent_jnt, self.parent_fk_ctrl)

    def create_parent_ctrl(self):
        """The parent control for scaling, uv sliding, and stretching."""
        # ----- control curve -----
        self.parent_fk_ctrl = create_nurbs_curves.CreateCurves(
            name=f"fk{cap(self.mod_name)}Parent{self.mirr_side}ctrl",
            size=0.5,
            color_rgb=(0.2, 0, 1),
        ).box_curve()

        # ----- control group -----
        self.parent_fk_ctrl_grp, _, _, _, self.parent_fk_ctrl_aux_grp = create_ctrl_grps(
            self.parent_fk_ctrl,
            aux_offset_grp=True,
        )

        # ----- snap control group to joint -----
        cmds.matchTransform(self.parent_fk_ctrl_grp, self.main_joints[0])

        # ----- attach to first follicle -----
        parent_constr(self.follicles[0], self.parent_fk_ctrl_aux_grp, offset=True)

    def create_uv_slide(self):
        """Setup UV slide attribute to stretch and compress follicles
        along the U parameter of the flexi surface.
        """
        add_divider_attribue(control_name=self.parent_fk_ctrl, divider_amount=10)
        cmds.addAttr(
            self.parent_fk_ctrl,
            longName="uvSlide",
            defaultValue=1.0,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )

        for i, follicle_shape in enumerate(self.follicle_shapes):
            multipydivide_nd = cmds.createNode(
                "multiplyDivide",
                name=f"{self.mod_name}UvSlide{self.mirr_side}{i + 1:02d}_multiplyDivide",
            )
            parameter_u = cmds.getAttr(f"{follicle_shape}.parameterU")
            cmds.setAttr(f"{multipydivide_nd}.input2X", parameter_u)
            cmds.connectAttr(f"{self.parent_fk_ctrl}.uvSlide", f"{multipydivide_nd}.input1X")
            cmds.connectAttr(f"{multipydivide_nd}.outputX", f"{follicle_shape}.parameterU")

    def create_ik_stretch(self):
        """Setup ik joint stretch."""
        self.setup_stretch_attr(
            joints=self.ik_jnts,
            follicles=self.follicles,
            global_scale_offs_obj=self.fk_ctrl_swch_grps[0],
        )

    def setup_stretch_attr(
        self,
        joints: list[str],
        follicles: list[str],
        global_scale_offs_obj: list[str],
    ) -> None:
        """Set up ik stretch functionality and add attribute to parent ctrl.

        Args:
            joints: List of joints for to apply stretch to.
            follicles: List of follicles used for setting up flexi ik chain.
            global_scale_offs_obj: Object or group to get ".scaleX" from
                for global scale stretch offset.

        """
        # create stretch attribute
        add_divider_attribue(control_name=self.parent_fk_ctrl, divider_amount=5)
        cmds.addAttr(
            self.parent_fk_ctrl,
            longName="ikStretch",
            minValue=0.0,
            maxValue=1.0,
            defaultValue=1.0,
            keyable=True,
        )

        # ----------
        for i, (jnt, foll) in enumerate(
            zip(joints, follicles, strict=False),
        ):
            if i == 0:  # skip first joint
                continue
            # ----- create joint length ruler -----
            # length of joint translate X
            ruler_shape, ruler_transform, ruler_loc_01, ruler_loc_02, *_ = create_attached_ruler(
                name=f"{self.mod_name}Ruler{self.mirr_side}{i:02d}",
                ruler_start_object=follicles[i - 1],
                ruler_end_object=foll,
            )
            # ----- global scale stretch offset -----
            scale_offs_decompmatrix = cmds.createNode(
                "decomposeMatrix",
                name=f"{self.mod_name}IkStretchGlobalScale{self.mirr_side}{i:02d}_decomposeMatrix",
            )
            scale_offs_multdivide = cmds.createNode(
                "multiplyDivide",
                name=f"{self.mod_name}IkStretchGlobalScale{self.mirr_side}{i:02d}_multiplyDivide",
            )
            cmds.setAttr(f"{scale_offs_multdivide}.operation", 2)  # divide operation
            cmds.connectAttr(
                f"{global_scale_offs_obj}.worldMatrix[0]",
                f"{scale_offs_decompmatrix}.inputMatrix",
            )
            cmds.connectAttr(
                f"{scale_offs_decompmatrix}.outputScaleX",
                f"{scale_offs_multdivide}.input2X",
            )
            # ----- setup stretch blendColors node -----
            trans_stretch_nd = cmds.createNode(
                "blendColors",
                name=f"{self.mod_name}IkStretchTranslate{self.mirr_side}{i:02d}_blendColors",
            )
            cmds.connectAttr(
                f"{self.parent_fk_ctrl}.ikStretch",
                f"{trans_stretch_nd}.blender",
                force=True,
            )
            # query joint length
            jnt_trans_x = cmds.getAttr(f"{jnt}.translateX")
            # add negative multiplier if "x" chain facing negative direction
            if jnt_trans_x < 0:
                inverse_nd = cmds.createNode(
                    "multiplyDivide",
                    name=f"{self.mod_name}IkStretchInverse{self.mirr_side}{i:02d}_multiplyDivide",
                )
                cmds.setAttr(f"{inverse_nd}.input2X", -1)
                cmds.connectAttr(f"{ruler_shape}.distance", f"{scale_offs_multdivide}.input1X")
                cmds.connectAttr(f"{scale_offs_multdivide}.outputX", f"{inverse_nd}.input1X")
                cmds.connectAttr(f"{inverse_nd}.outputX", f"{trans_stretch_nd}.color1R")
            else:
                # set blendColors 1R to dynamic length distance
                cmds.connectAttr(f"{ruler_shape}.distance", f"{scale_offs_multdivide}.input1X")
                cmds.connectAttr(f"{scale_offs_multdivide}.outputX", f"{trans_stretch_nd}.color1R")

            # set blendColors 2R to static joint length
            cmds.setAttr(f"{trans_stretch_nd}.color2R", jnt_trans_x)
            # connect blendColors to joint
            cmds.connectAttr(f"{trans_stretch_nd}.outputR", f"{jnt}.translateX")

            # ----- parent and hide -----
            for obj in [ruler_transform, ruler_loc_01, ruler_loc_02]:
                cmds.parent(obj, self.ik_stretch_top_grp)

    def hide_lock_items(self):
        """Hide and lock objects and attributes."""
        # ---------- hide and lock ----------
        # last fk ctrl
        if self.hide_end_ctrl:
            for axis in "XYZ":
                cmds.setAttr(f"{self.fk_ctrls[-1]}.translate{axis}", lock=True)
                cmds.setAttr(f"{self.fk_ctrls[-1]}.rotate{axis}", lock=True)
                cmds.setAttr(f"{self.fk_ctrls[-1]}.scale{axis}", lock=True)
            # hide last fk top ctrl group
            cmds.setAttr(f"{self.fk_ctrl_grps[-1]}.visibility", 0)

        # all fk ctrls
        if self.hide_all_ctrls:
            for ctrl, grp in zip(self.fk_ctrls, self.fk_ctrl_grps, strict=False):
                for axis in "XYZ":
                    cmds.setAttr(f"{ctrl}.translate{axis}", lock=True)
                    cmds.setAttr(f"{ctrl}.rotate{axis}", lock=True)
                    cmds.setAttr(f"{ctrl}.scale{axis}", lock=True)
                cmds.setAttr(f"{grp}.visibility", 0)

        # parent ctrl
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{self.parent_fk_ctrl}.translate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{self.parent_fk_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{self.parent_fk_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{self.parent_fk_ctrl}.visibility", **lock_hide_kwargs)

        # ----- hide objects -----
        cmds.setAttr(f"{self.flexi_surface}.visibility", 0)
        cmds.setAttr(f"{self.follicle_top_grp}.visibility", 0)
        cmds.setAttr(f"{self.ikhandle_top_grp}.visibility", 0)
        cmds.setAttr(f"{self.ik_stretch_top_grp}.visibility", 0)

    def top_grouping(self):
        """Parent objects under top groups."""
        cmds.parent(self.ik_handles, self.ikhandle_top_grp)
        cmds.parent(self.follicles, self.follicle_top_grp)
        cmds.parent(self.parent_fk_ctrl_grp, self.fk_ctrl_top_grp)
