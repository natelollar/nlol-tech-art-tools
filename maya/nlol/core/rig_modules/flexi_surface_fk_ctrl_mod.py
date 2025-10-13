from maya import cmds
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_nurbs_curves,
    follicle_at_surface,
)
from nlol.utilities.nlol_maya_logger import get_logger
from nlol.utilities.utils_maya import add_divider_attribue, cap

create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
scale_constr = clean_constraints.scale_constr


class FlexiSurfaceFkCtrlModule:
    """Create fk controls for each joint in joint chain and attach to flexi surface via follicles.
    Controls will move along with flexi surface, but will otherwise be basic standalone fk controls.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list[str],
        flexi_surface: str = "flexiSurface_geo",
        hide_end_ctrl: bool = False,
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

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints
        self.flexi_surface = flexi_surface
        self.hide_end_ctrl = hide_end_ctrl

        self.logger = get_logger()

    def build(self) -> str:
        """Main build method for flexi surface fk control rig module.
        --------------------------------------------------

        Returns:
            Rig module top group.

        """
        # ----- create top groups -----
        self.create_top_grps()
        self.create_follices()
        self.create_fk_ctrls()
        self.create_parent_ctrl()
        self.attach_fk_ctrls()
        self.setup_uv_slide()

        # ----- hide objects -----
        cmds.setAttr(f"{self.flexi_surface}.visibility", 0)
        cmds.setAttr(f"{self.follicle_top_grp}.visibility", 0)
        # cmds.setAttr(f"{self.parent_fk_ctrl_grp}.visibility", 0)

        # ----- top group parenting -----
        cmds.parent(self.follicles, self.follicle_top_grp)
        cmds.parent(self.fk_ctrl_grps, self.fk_ctrl_top_grp)
        cmds.parent(self.parent_fk_ctrl_grp, self.fk_ctrl_top_grp)

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
        self.fk_ctrl_top_grp = cmds.group(
            empty=True,
            name=f"fk{cap(self.mod_name)}{self.mirr_side}ctrlGrp",
        )
        # parent groups
        cmds.parent(self.follicle_top_grp, self.mod_top_grp)
        cmds.parent(self.fk_ctrl_top_grp, self.mod_top_grp)

    def create_follices(self):
        """Create Maya follicles along flexi surface at nearest main joint position."""
        # ----- follicles to flexi surface -----
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

    def create_fk_ctrls(self):
        """Create fk controls and constrain main joints to them."""
        self.fk_ctrls = []
        self.fk_ctrl_grps = []
        self.fk_ctrl_aux_grps = []
        for i, jnt in enumerate(self.main_joints):
            # ----- control curve -----
            fk_ctrl = create_nurbs_curves.CreateCurves(
                name=f"fk{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_ctrl",
                size=0.25,
                color_rgb=(1, 0, 0.3),
            ).box_curve()

            # ----- control group -----
            fk_ctrl_grp, _, _, _, fk_ctrl_aux_grp = create_ctrl_grps(
                fk_ctrl,
                aux_offset_grp=True,
            )

            # ----- snap control group to joint -----
            cmds.matchTransform(fk_ctrl_grp, jnt)

            # ----- constrain main joints to controls -----
            parent_constr(fk_ctrl, jnt)
            scale_constr(fk_ctrl, jnt)

            # ----- lock and hide attributes -----
            cmds.setAttr(f"{fk_ctrl}.visibility", lock=True, keyable=False, channelBox=False)

            # ----- segment scale off for main joints -----
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)

            # -----
            self.fk_ctrls.append(fk_ctrl)
            self.fk_ctrl_grps.append(fk_ctrl_grp)
            self.fk_ctrl_aux_grps.append(fk_ctrl_aux_grp)

        # ----- lock and hide last control -----
        if self.hide_end_ctrl:
            for axis in "XYZ":
                cmds.setAttr(f"{self.fk_ctrls[-1]}.translate{axis}", lock=True)
                cmds.setAttr(f"{self.fk_ctrls[-1]}.rotate{axis}", lock=True)
                cmds.setAttr(f"{self.fk_ctrls[-1]}.scale{axis}", lock=True)
            cmds.setAttr(f"{self.fk_ctrl_grps[-1]}.visibility", 0)

    def attach_fk_ctrls(self):
        """Attach fk controls to follices via parent constraint."""
        for follicle, aux_grp in zip(self.follicles, self.fk_ctrl_aux_grps, strict=False):
            parent_constr(follicle, aux_grp, offset=True)
            scale_constr(self.parent_fk_ctrl, aux_grp)

    def create_parent_ctrl(self):
        """The parent control for scaling and uv sliding."""
        # ----- control curve -----
        self.parent_fk_ctrl = create_nurbs_curves.CreateCurves(
            name=f"fk{cap(self.mod_name)}Parent{self.mirr_side}ctrl",
            size=0.5,
            color_rgb=(0.2, 0, 1),
        ).box_curve()

        # ----- control group -----
        self.parent_fk_ctrl_grp, _, _, _, parent_fk_ctrl_aux_grp = create_ctrl_grps(
            self.parent_fk_ctrl,
            aux_offset_grp=True,
        )

        # ----- snap control group to joint -----
        cmds.matchTransform(self.parent_fk_ctrl_grp, self.main_joints[0])

        # ----- attach to first follicle -----
        parent_constr(self.follicles[0], parent_fk_ctrl_aux_grp, offset=True)

        # ----- hide and lock -----
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{self.parent_fk_ctrl}.translate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{self.parent_fk_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{self.parent_fk_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{self.parent_fk_ctrl}.visibility", **lock_hide_kwargs)

    def setup_uv_slide(self):
        """Setup UV slide attribute to stretch and compress follicles
        along the U parameter of the flexi surface.
        """
        for i, follicle_shape in enumerate(self.follicle_shapes):
            if i == 0:
                add_divider_attribue(control_name=self.parent_fk_ctrl, divider_amount=10)
                cmds.addAttr(
                    self.parent_fk_ctrl,
                    longName="uvSlide",
                    defaultValue=1.0,
                    minValue=0.0,
                    maxValue=1.0,
                    keyable=True,
                )
            multipydivide_nd = cmds.createNode(
                "multiplyDivide",
                name=f"{self.mod_name}UvSlide{self.mirr_side}{i + 1:02d}_multiplyDivide",
            )
            parameter_u = cmds.getAttr(f"{follicle_shape}.parameterU")
            cmds.setAttr(f"{multipydivide_nd}.input2X", parameter_u)
            cmds.connectAttr(f"{self.parent_fk_ctrl}.uvSlide", f"{multipydivide_nd}.input1X")
            cmds.connectAttr(f"{multipydivide_nd}.outputX", f"{follicle_shape}.parameterU")
