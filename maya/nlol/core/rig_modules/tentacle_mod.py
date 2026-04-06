from importlib import reload

from maya import cmds
from nlol.core.general_utils import add_divider_attribue, cap
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_locators,
    create_nurbs_curves,
)
from nlol.core.rig_modules import flexi_surface_fk_ctrl_mod, flexi_surface_ik_chain_simple_mod
from nlol.utilities.nlol_maya_logger import get_logger

reload(flexi_surface_fk_ctrl_mod)
reload(flexi_surface_ik_chain_simple_mod)

logger = get_logger()

scale_constr = clean_constraints.scale_constr
parent_constr = clean_constraints.parent_constr
create_ctrl_grps = create_control_groups.create_ctrl_grps


class TentacleModule:
    """Rig module good for tentacle, tail, stretchy spine, etc.
    Has a main base layer of flexi joints. This base layer of flexi joints blends
    between fk ctrls and offset flexi ctrls.
    See example in "defaults/standalone_modules/tentacle_mod".
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        main_joints: list[str],
        flexi_joints_main: list[str],
        flexi_joints_offset: list[str],
        flexi_surface_main: str,
        flexi_surface_offset: str,
        separate_flexi_ctrls: bool = False,
        use_flexi_ik_chain: bool = False,
    ):
        """Initialize rig module class.

        Args:
            rig_module_name: Custom rig module name.
            mirror_direction: Mirror side as in "left" or "right".
            main_joints: Skinned joints driving the tentacle character geo. Will be attached to
                flexi_surface_main via follices.
            flexi_joints_main: Base layer of joints that will be parent to base flexi setup.
                Will blend between fk and offset flexi ctrls.
            flexi_joints_offset: Outer joints that will be the opposite of the fk joints.
                One of the chains to blend between.  Usually contains just a few joints, like three.
            flexi_surface_main: Main base layer of flexi geo that will be skinned
                to flexi_joints_main. If using cloth sim, apply to this geo.
            flexi_surface_offset: Flexi geo skinned to flexi_joints_offset. A joint chain
                will be created in this class called flexi_jnts that will be attached
                to this geo via follicles.
            separate_flexi_ctrls: Whether to leave ctrls grouped to eachother in a hierarchy,
                or separate them as individual ctrls. Useful for complex parent spacing.
            use_flexi_ik_chain: Enable chain of single solver ikHandles for flexi ctrls
                instead of regular fk attachments.  Allows adding stretch attribute toggle,
                to maintain chain length.

        """
        self.mod_name = rig_module_name
        self.mirror_direction = mirror_direction
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints
        self.flexi_joints_main = flexi_joints_main
        self.flexi_joints_offset = flexi_joints_offset
        self.flexi_surface_main = flexi_surface_main
        self.flexi_surface_offset = flexi_surface_offset
        self.separate_flexi_ctrls = separate_flexi_ctrls
        self.use_flexi_ik_chain = use_flexi_ik_chain

    def build(self):
        """Entry point. Run method to build rig module.
        --------------------------------------------------

        Returns:
            Top Maya group for rig module.

        """
        self.setup_top_grps()
        self.setup_fk_flexi_jnts()
        self.build_flexi_base()
        self.build_flexi_offset()
        self.setup_fk_ctrls()
        self.setup_flexi_ctrls()
        self.setup_switch_ctrl()
        self.setup_switch_hide_flexi()
        self.setup_global_scale()
        self.setup_slide_stretch_attrs()
        self.hide_lock_items()

        return self.mod_top_grp

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
        self.flexi_top_grp = cmds.group(
            empty=True,
            name=f"flexi{cap(self.mod_name)}{self.mirr_side}grp",
        )
        cmds.parent(self.fk_top_grp, self.mod_top_grp)
        cmds.parent(self.flexi_top_grp, self.mod_top_grp)

    def build_flexi_base(self):
        """Create base flexi surface that will blend between the two joint chains.
        This surface attaches to the main skinned joints.
        """
        self.flexi_base_mod = flexi_surface_fk_ctrl_mod.FlexiSurfaceFkCtrlModule(
            rig_module_name=f"{self.mod_name}Base",
            mirror_direction=self.mirror_direction,
            main_joints=self.main_joints,
            flexi_surface=self.flexi_surface_main,
        )
        flexi_base_top_grp = self.flexi_base_mod.build()
        cmds.parent(flexi_base_top_grp, self.mod_top_grp)

    def build_flexi_offset(self):
        """This flexi surface is one of the blended chains.
        Attaches to the flexi joint chain that is opposite to the fk chain.
        """
        if self.use_flexi_ik_chain:
            self.flexi_offset_mod = (
                flexi_surface_ik_chain_simple_mod.FlexiSurfaceIkChainSimpleModule(
                    rig_module_name=f"{self.mod_name}Offset",
                    mirror_direction=self.mirror_direction,
                    main_joints=self.flexi_jnts,
                    flexi_surface=self.flexi_surface_offset,
                )
            )
            flexi_offset_top_grp = self.flexi_offset_mod.build()
            cmds.parent(flexi_offset_top_grp, self.mod_top_grp)
        else:
            self.flexi_offset_mod = flexi_surface_fk_ctrl_mod.FlexiSurfaceFkCtrlModule(
                rig_module_name=f"{self.mod_name}Offset",
                mirror_direction=self.mirror_direction,
                main_joints=self.flexi_jnts,
                flexi_surface=self.flexi_surface_offset,
                hide_all_ctrls=True,
            )
            flexi_offset_top_grp = self.flexi_offset_mod.build()
            cmds.parent(flexi_offset_top_grp, self.mod_top_grp)

    def setup_fk_flexi_jnts(self):
        """Fk and offset flexi blended joint chains.
        Creates fk and flexi surface joint chains to blend main joint chain between.
        """
        fk_jnts = []
        flexi_jnts = []
        fk_flexi_scale_consts = []
        for i, jnt in enumerate(self.flexi_joints_main):
            # -------------------------------------------------------------
            # -------------------- create fk flexi chains --------------------
            fk_jnt = create_joint.single_joint(
                name=f"fk{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_jnt",
                radius=5,
                color_rgb=(1.0, 0.0, 0.1),
                parent_snap=jnt,
            )
            flexi_jnt = create_joint.single_joint(
                name=f"flexi{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_jnt",
                radius=4,
                color_rgb=(0.0, 0.9, 0.1),
                parent_snap=jnt,
            )
            # scale compensate off to avoid double scaling when global scaling
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", 0)

            # better scaling with constraint instead of blendColors scale
            fk_flexi_scale_const = scale_constr((fk_jnt, flexi_jnt), jnt)

            fk_jnts.append(fk_jnt)
            flexi_jnts.append(flexi_jnt)
            fk_flexi_scale_consts.append(fk_flexi_scale_const)

        # parent fk flexi joints into chains
        for i, jnt in enumerate(fk_jnts):
            if jnt != fk_jnts[0]:
                cmds.parent(jnt, fk_jnts[i - 1])
        for i, jnt in enumerate(flexi_jnts):
            if jnt != flexi_jnts[0]:
                cmds.parent(jnt, flexi_jnts[i - 1])

        # ---------------------------------------------------------------------
        # -------------------- blend joint chains together --------------------
        translate_blend_nodes = []
        rotate_blend_nodes = []
        for i, (fk_jnt, flexi_jnt, jnt) in enumerate(
            zip(
                fk_jnts,
                flexi_jnts,
                self.flexi_joints_main,
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
            cmds.connectAttr(f"{flexi_jnt}.translate", f"{tran_blend_node}.color2")
            cmds.connectAttr(f"{tran_blend_node}.output", f"{jnt}.translate")
            # rotate blend
            cmds.connectAttr(f"{fk_jnt}.rotate", f"{rot_blend_node}.color1")
            cmds.connectAttr(f"{flexi_jnt}.rotate", f"{rot_blend_node}.color2")
            cmds.connectAttr(f"{rot_blend_node}.output", f"{jnt}.rotate")

            translate_blend_nodes.append(tran_blend_node)
            rotate_blend_nodes.append(rot_blend_node)

        # parent top fk flexi joints to locator constrained to main_joints parent
        # accounts for needed blendColor node transform offset
        self.main_joints_parent = cmds.listRelatives(self.main_joints[0], parent=True)
        parent_loc = None
        if self.main_joints_parent:
            parent_loc = create_locators.locator_snap_parent(
                objects=self.main_joints_parent,
                locator_name=f"{self.mod_name}Offset{self.mirr_side}loc",
                local_scale=(5, 5, 5),
            )[0]
            cmds.parent(fk_jnts[0], parent_loc)
            cmds.parent(flexi_jnts[0], parent_loc)
            cmds.parent(self.flexi_joints_main[0], parent_loc)

            # parent and hide joint locator and joints
            cmds.parent(parent_loc, self.mod_top_grp)
            cmds.setAttr(f"{parent_loc}.visibility", 0)
        else:
            for jnt in [fk_jnts[0], flexi_jnts[0], self.flexi_joints_main[0]]:
                cmds.parent(jnt, self.mod_top_grp)
                cmds.setAttr(f"{jnt}.visibility", 0)

        # assign instance variables
        self.fk_jnts = fk_jnts
        self.flexi_jnts = flexi_jnts
        self.fk_flexi_scale_consts = fk_flexi_scale_consts
        self.translate_blend_nodes = translate_blend_nodes
        self.rotate_blend_nodes = rotate_blend_nodes
        self.parent_loc = parent_loc

    def setup_switch_ctrl(self):
        """Create fk flexi switch ctrl."""
        # ---------- create control crv and grp ----------
        switch_ctrl = create_nurbs_curves.CreateCurves(
            name=f"{self.mod_name}Swch{self.mirr_side}ctrl",
            size=1,
            color_rgb=(0.0, 0.0, 0.0),
        ).sphere_curve()
        switch_ctrl_grp = create_ctrl_grps(switch_ctrl)[0]

        # ---------- add attributes ----------
        # fk flexi blend attr
        add_divider_attribue(control_name=switch_ctrl, divider_amount=10)
        cmds.addAttr(
            switch_ctrl,
            longName="fkFlexiBlend",
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
                f"{switch_ctrl}.fkFlexiBlend",
                f"{node_translate}.blender",
                force=True,
            )
            cmds.connectAttr(
                f"{switch_ctrl}.fkFlexiBlend",
                f"{node_rotate}.blender",
                force=True,
            )

        # ----- connect switch control to visibility -----
        swch_reverse_nd = cmds.createNode(
            "reverse",
            name=f"{self.mod_name}Swch{self.mirr_side}reverse",
        )
        cmds.connectAttr(f"{switch_ctrl}.fkFlexiBlend", f"{self.fk_top_grp}.visibility")
        cmds.connectAttr(f"{switch_ctrl}.fkFlexiBlend", f"{swch_reverse_nd}.inputX")
        cmds.connectAttr(f"{swch_reverse_nd}.outputX", f"{self.flexi_top_grp}.visibility")
        if self.use_flexi_ik_chain:
            cmds.connectAttr(
                f"{swch_reverse_nd}.outputX",
                f"{self.flexi_offset_mod.fk_ctrl_top_grp}.visibility",
            )

        # ----- connect switch control scale constraints -----
        for fk_jnt, flexi_jnt, scale_const in zip(
            self.fk_jnts,
            self.flexi_jnts,
            self.fk_flexi_scale_consts,
            strict=False,
        ):
            cmds.connectAttr(
                f"{switch_ctrl}.fkFlexiBlend",
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

    def setup_switch_hide_flexi(self):
        """Set up show/hide attribute for base flexi ctrls.
        Helpful to avoid interfering with fk ctrl selection.
        """
        add_divider_attribue(control_name=self.switch_ctrl, divider_amount=8)
        cmds.addAttr(
            self.switch_ctrl,
            longName="flexiBaseVis",
            defaultValue=1.0,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        cmds.connectAttr(
            f"{self.switch_ctrl}.flexiBaseVis",
            f"{self.flexi_base_mod.fk_ctrl_top_grp}.visibility",
        )

        if self.use_flexi_ik_chain:
            cmds.addAttr(
                self.switch_ctrl,
                longName="flexiOffsetVis",
                defaultValue=1.0,
                minValue=0.0,
                maxValue=1.0,
                keyable=True,
            )
            cmds.connectAttr(
                f"{self.switch_ctrl}.flexiOffsetVis",
                f"{self.flexi_offset_mod.fk_ctrl_grps[0]}.visibility",
            )

    def setup_fk_ctrls(self):
        """Create fk ctrl chain. Constrain fk joints to follow fk ctrls."""
        fk_ctrl_grps = []
        fk_ctrls = []
        for i, jnt in enumerate(self.fk_jnts):
            # control curve and group
            fk_ctrl = create_nurbs_curves.CreateCurves(
                name=f"fk{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_ctrl",
                size=1.0,
                color_rgb=(0.0, 0.3, 1),
            ).box_curve()
            fk_ctrl_grp = create_ctrl_grps(fk_ctrl)[0]

            # snap ctrl group to joint
            cmds.matchTransform(fk_ctrl_grp, jnt)

            # constrain fk joints to follow ctrls
            parent_constr(fk_ctrl, jnt)
            scale_constr(fk_ctrl, jnt)

            # lock and hide attributes
            lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
            for axis in "XYZ":
                cmds.setAttr(f"{fk_ctrl}.scale{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{fk_ctrl}.visibility", **lock_hide_kwargs)

            # create group list for parenting
            fk_ctrl_grps.append(fk_ctrl_grp)
            fk_ctrls.append(fk_ctrl)

        # parent controls and groups together
        for grp, ctrl in zip(fk_ctrl_grps[1:], fk_ctrls, strict=False):
            cmds.parent(grp, ctrl)

        # parent under main fk group
        cmds.parent(fk_ctrl_grps[0], self.fk_top_grp)

    def setup_flexi_ctrls(self):
        """Create main flexi offset ctrls, opposite to fk ctrl chain.
        Constrain flexi offset joints to main flexi offset ctrls.
        """
        flexi_ctrl_grps = []
        flexi_ctrls = []
        for i, jnt in enumerate(self.flexi_joints_offset):
            # control curve and group
            flexi_ctrl = create_nurbs_curves.CreateCurves(
                name=f"flexi{cap(self.mod_name)}{self.mirr_side}{i + 1:02d}_ctrl",
                size=1.0,
                color_rgb=(0.4, 0.0, 1.0),
            ).sphere_curve()
            flexi_ctrl_grp = create_ctrl_grps(flexi_ctrl)[0]

            # snap ctrl group to joint
            cmds.matchTransform(flexi_ctrl_grp, jnt)

            # constrain flexi joints to follow ctrls
            parent_constr(flexi_ctrl, jnt)
            scale_constr(flexi_ctrl, jnt)

            # lock and hide attributes
            lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
            for axis in "XYZ":
                cmds.setAttr(f"{flexi_ctrl}.scale{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{flexi_ctrl}.visibility", **lock_hide_kwargs)

            # create group list for parenting
            flexi_ctrl_grps.append(flexi_ctrl_grp)
            flexi_ctrls.append(flexi_ctrl)

        if self.separate_flexi_ctrls:  # avoid parenting ctrls in hierarchy
            for grp in flexi_ctrl_grps:
                cmds.parent(grp, self.flexi_top_grp)
        else:
            # parent controls and groups together
            for grp, ctrl in zip(flexi_ctrl_grps[1:], flexi_ctrls, strict=False):
                cmds.parent(grp, ctrl)
            # parent under main flexi group
            cmds.parent(flexi_ctrl_grps[0], self.flexi_top_grp)

        # assign instance variable
        self.flexi_ctrls = flexi_ctrls

    def setup_global_scale(self):
        """Setup global scale for flexi surfaces."""
        scale_constr(self.parent_loc, self.flexi_base_mod.parent_fk_ctrl_aux_grp)
        scale_constr(self.parent_loc, self.flexi_offset_mod.parent_fk_ctrl_aux_grp)

    def setup_slide_stretch_attrs(self):
        """Setup uv slide attribute on first ctrls. Also, set up ik stretch
        if using flexi ik chain.
        """
        # ----- base fk ctrl attrs -----
        add_divider_attribue(control_name=self.flexi_base_mod.fk_ctrls[0], divider_amount=10)
        cmds.addAttr(
            self.flexi_base_mod.fk_ctrls[0],
            longName="uvSlide",
            defaultValue=1.0,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        cmds.connectAttr(
            f"{self.flexi_base_mod.fk_ctrls[0]}.uvSlide",
            f"{self.flexi_base_mod.parent_fk_ctrl}.uvSlide",
        )

        # ----- flexi ctrl attrs -----
        add_divider_attribue(control_name=self.flexi_ctrls[0], divider_amount=10)
        cmds.addAttr(
            self.flexi_ctrls[0],
            longName="uvSlide",
            defaultValue=1.0,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        cmds.connectAttr(
            f"{self.flexi_ctrls[0]}.uvSlide",
            f"{self.flexi_offset_mod.parent_fk_ctrl}.uvSlide",
        )
        # add ik stretch attribute
        if self.use_flexi_ik_chain:
            add_divider_attribue(control_name=self.flexi_ctrls[0], divider_amount=11)
            cmds.addAttr(
                self.flexi_ctrls[0],
                longName="ikStretch",
                defaultValue=1.0,
                minValue=0.0,
                maxValue=1.0,
                keyable=True,
            )
            cmds.connectAttr(
                f"{self.flexi_ctrls[0]}.ikStretch",
                f"{self.flexi_offset_mod.parent_fk_ctrl}.ikStretch",
            )

    def hide_lock_items(self):
        """Hide and lock objects and attrs."""
        cmds.setAttr(f"{self.flexi_base_mod.parent_fk_ctrl_grp}.visibility", 0)

        if self.use_flexi_ik_chain:
            cmds.setAttr(f"{self.flexi_offset_mod.ik_parent_jnt}.visibility", 0)

            parent_ctrl_shp = cmds.listRelatives(self.flexi_offset_mod.parent_fk_ctrl, shapes=True)
            # shape vis needs to be saved with crv shape json
            cmds.setAttr(f"{parent_ctrl_shp[0]}.visibility", 0)

            for fk_ctrl in self.flexi_offset_mod.fk_ctrls:
                lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
                for axis in "XYZ":
                    cmds.setAttr(f"{fk_ctrl}.scale{axis}", **lock_hide_kwargs)
        else:
            cmds.setAttr(f"{self.flexi_offset_mod.parent_fk_ctrl_grp}.visibility", 0)
