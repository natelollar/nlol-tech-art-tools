from importlib import reload

from maya import cmds
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_joint,
    create_locators,
    create_nurbs_curves,
    create_ruler,
    follicle_at_surface,
)
from nlol.core.rig_modules import fk_chain_mod
from nlol.core.rig_tools import select_multiple_joints
from nlol.utilities import utils_maya
from nlol.utilities.nlol_maya_logger import get_logger

reload(utils_maya)
reload(follicle_at_surface)
reload(select_multiple_joints)

cap = utils_maya.cap
parent_constr = clean_constraints.parent_constr
point_constr = clean_constraints.point_constr
create_ctrl_grps = create_control_groups.create_ctrl_grps
add_divider_attribue = utils_maya.add_divider_attribue
create_attached_ruler = create_ruler.create_attached_ruler


class FlexiSurfaceIkChainModule:
    """Attach one or more joint chains to flexi surface geo.
    Requires "x" or "-x" down the chain.
    These chains are attached via follicles and ik single-chain solvers.
    Also, there is an fk ctrl chain offset for these attach chains.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        joint_chains: list[list],
        flexi_surface: str,
        hide_end_ctrl: bool = False,
    ):
        """Initialize rig module.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: String describing mirror side. Ex. "left", "right".
            joint_chains: Joint chains being attached to flexi surface. Lists will
                either contain start joint or start and end joint of a joint chain.
                A function will later find the entire chain.
            flexi_surface: Polygonal or nurbs mesh object to attach Maya (hair) follicles to.
                This mesh object would be skinned to some joints for base movement.
                Should contain the string "flexiSurface".
            hide_end_ctrl: Hide last of the created fk controls.

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.joint_chains = joint_chains
        self.flexi_surface = flexi_surface if flexi_surface else "flexiSurface_geo"
        self.hide_end_ctrl = hide_end_ctrl

        self.logger = get_logger()

    def create_top_groups(self):
        """Create top groups for rig module organization.
        Also, parent these groups under main top group
        and hide certain groups.
        """
        self.mod_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}grp",
        )
        self.follicle_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}follicleGrp",
        )
        self.ikhandle_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}{self.mirr_side}ikHandleGrp",
        )
        self.ikjnts_top_grp = cmds.group(
            empty=True,
            name=f"ik{cap(self.mod_name)}{self.mirr_side}jntGrp",
        )
        self.ikstretch_top_grp = cmds.group(
            empty=True,
            name=f"ik{cap(self.mod_name)}Stretch{self.mirr_side}grp",
        )
        self.fkctrls_top_grp = cmds.group(
            empty=True,
            name=f"fk{cap(self.mod_name)}Main{self.mirr_side}ctrlGrp",
        )
        # parent groups
        cmds.parent(self.follicle_top_grp, self.mod_top_grp)
        cmds.parent(self.ikhandle_top_grp, self.mod_top_grp)
        cmds.parent(self.ikjnts_top_grp, self.mod_top_grp)
        cmds.parent(self.ikstretch_top_grp, self.mod_top_grp)
        cmds.parent(self.fkctrls_top_grp, self.mod_top_grp)
        # hide groups
        cmds.setAttr(f"{self.follicle_top_grp}.visibility", 0)
        cmds.setAttr(f"{self.ikhandle_top_grp}.visibility", 0)
        cmds.setAttr(f"{self.ikjnts_top_grp}.visibility", 0)
        cmds.setAttr(f"{self.ikstretch_top_grp}.visibility", 0)

    def build(self) -> str:
        """Main build method for flexi surface rig module.
        --------------------------------------------------
        Create and attach follicles on flexi surface closest to each joint position.
        Create and attach an fk chain to these follicles via ik single chain solvers.
        Add stretch attribute to allow joint length to optionally stretch with follicles.

        Returns:
            Rig module top group.

        """
        # ----- create top groups -----
        self.create_top_groups()

        # ----- create attribute control -----
        self.create_attribute_control()  # for ik stretch attribute

        # ---------- iterate through joint chains ----------
        follicles = []
        fkchain_top_grps = []
        ikparent_jnts = []
        for i, start_end_jnt in enumerate(self.joint_chains):
            letter_index = chr(ord("a") + i)  # use ascii to get letter index

            # ----- get main joint chain -----
            joint_chain = select_multiple_joints.select_joint_chain(start_end_jnt)

            # ----- follicles to flexi surface -----
            follicle_chain = []
            for i, jnt in enumerate(joint_chain):
                follicle, *_ = follicle_at_surface.create_joint_follicle(
                    flexi_surface=self.flexi_surface,
                    joint=jnt,
                    name=f"{self.mod_name}{self.mirr_side}{letter_index}{i + 1:02d}",
                )
                follicle_chain.append(follicle)

            # ----- setup ik joints and handles -----
            ik_jnts, ik_parent_jnt = self.setup_iksinglesolver_chain(
                joint_chain=joint_chain,
                follicle_chain=follicle_chain,
                iteration_id=letter_index,
            )

            # ----- create fk controls and joint chain -----
            fkctrl_top_grps, _, fkctrl_swch_grps, _, fkctrl_aux_grps, fkctrls = (
                fk_chain_mod.FkChainModule(
                    rig_module_name=f"fk{cap(self.mod_name)}",
                    mirror_direction=self.mirr_side,
                    main_joints=joint_chain,
                    iteration_id=letter_index,
                    aux_offset_grp=True,
                    return_all_grps=True,
                ).build()
            )

            # hide and lock last fk contrl
            if self.hide_end_ctrl: 
                for axis in "XYZ":  # lock last fk control attributes
                    cmds.setAttr(f"{fkctrls[-1]}.translate{axis}", lock=True)
                    cmds.setAttr(f"{fkctrls[-1]}.rotate{axis}", lock=True)
                    cmds.setAttr(f"{fkctrls[-1]}.scale{axis}", lock=True)
                # hide last fk top control group
                cmds.setAttr(f"{fkctrl_top_grps[-1]}.visibility", 0)  

            # ----- create plusMinus average offsets -----
            # for joint direct connections
            for ik_jnt, aux_grp in zip(ik_jnts, fkctrl_aux_grps, strict=False):
                offset_translate_nd = cmds.createNode(
                    "plusMinusAverage",
                    name=(
                        f"{self.mod_name}Translate{self.mirr_side}"
                        f"{letter_index}{i + 1:02d}_plusMinusAverage"
                    ),
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

            # ----- setup ik joint stretch -----
            self.setup_stretch_attr(
                joint_chain=ik_jnts,
                follicle_chain=follicle_chain,
                global_scale_offs_obj=fkctrl_swch_grps[0],
                iteration_id=letter_index,
            )

            # --------------------
            follicles.extend(follicle_chain)  # all follicles list
            fkchain_top_grps.append(fkctrl_top_grps[0])  # top fk ctrl chain grps
            ikparent_jnts.append(ik_parent_jnt)  # top ik joints

        # ----- ik joint offset locator -----
        # parent top ik joint to locator constrained to main joint chain parent
        joint_chain_parent = cmds.listRelatives(self.joint_chains[0][0], parent=True)
        if joint_chain_parent:
            ikparent_loc = create_locators.locator_snap_parent(
                objects=joint_chain_parent,
                locator_name=f"{self.mod_name}Offset{self.mirr_side}loc",
                local_scale=(5, 5, 5),
            )[0]
            # parent and hide joint locator and joints
            for prnt_jnt in ikparent_jnts:
                cmds.parent(prnt_jnt, ikparent_loc)
            cmds.parent(ikparent_loc, self.ikjnts_top_grp)
        else:
            for prnt_jnt in ikparent_jnts:
                cmds.parent(prnt_jnt, self.ikjnts_top_grp)

        # ----- top group parenting -----
        cmds.parent(follicles, self.follicle_top_grp)
        cmds.parent(fkchain_top_grps, self.fkctrls_top_grp)

        # ----- hide objects -----
        cmds.setAttr(f"{self.flexi_surface}.visibility", 0)

        return self.mod_top_grp

    def setup_iksinglesolver_chain(
        self,
        joint_chain: list[str],
        follicle_chain: list[str],
        iteration_id: str,
    ) -> list[str]:
        """Create ik joint chain along main skinned joint chain
        and setup ik single-chain solvers along this ik joint chain.
        Constrain top ik joint and ik handles to flexi surface follicles.

        Args:
            joint_chain: List of joints in main skinned joint chain.
            follicle_chain: List of follicles used for setting up flexi ik chain.
            iteration_id: Unique alphabetic id for each created joint chain.

        Returns:
            List of ik joints.

        """
        # ----- create ik joints -----
        # create parent joint for direct connections offset
        ik_parent_jnt = create_joint.single_joint(
            name=f"ik{cap(self.mod_name)}{self.mirr_side}{iteration_id}{'00'}_jnt",
            radius=3,
            color_rgb=(0.0, 0.7, 0.2),
            scale_compensate=False,
            parent_snap=joint_chain[0],
        )

        # create main ik joint chain
        ik_jnts = []
        for i, (jnt, foll) in enumerate(zip(joint_chain, follicle_chain, strict=False)):
            ik_jnt = create_joint.single_joint(
                name=f"ik{cap(self.mod_name)}{self.mirr_side}{iteration_id}{i + 1:02d}_jnt",
                radius=1,
                color_rgb=(0.0, 0.7, 0.2),
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
                    name=f"{self.mod_name}{self.mirr_side}{iteration_id}{i:02d}_ikHandle",
                    startJoint=ik_jnts[i - 1],
                    endEffector=ik_jnt,
                    solver="ikSCsolver",
                )
                cmds.rename(ik_handle_effector, f"{ik_handle}Effector")  # rename effector

                parent_constr(foll, ik_handle, offset=True)

                ik_handles.append(ik_handle)

        # ----- top group parenting -----
        cmds.parent(ik_handles, self.ikhandle_top_grp)

        return ik_jnts, ik_parent_jnt

    def create_attribute_control(self):
        """Create control for attributes including ik stretch."""
        # ----- create attribute control curve object -----
        attr_ctrl = create_nurbs_curves.CreateCurves(
            name=f"{self.mod_name}Attr{self.mirr_side}ctrl",
            size=0.25,
            color_rgb=(0.0, 0.0, 0.0),
        ).sphere_curve()

        attr_ctrl_grp = create_ctrl_grps(attr_ctrl)[0]

        # ----- add ik stretch blend attribute -----
        add_divider_attribue(control_name=attr_ctrl, divider_amount=5)
        cmds.addAttr(
            attr_ctrl,
            longName="ikStretch",
            minValue=0.0,
            maxValue=1.0,
            defaultValue=1.0,
            keyable=True,
        )

        # ----- visibility, parenting, other -----
        # hide unused attributes
        lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
        for axis in "XYZ":
            cmds.setAttr(f"{attr_ctrl}.translate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{attr_ctrl}.rotate{axis}", **lock_hide_kwargs)
            cmds.setAttr(f"{attr_ctrl}.scale{axis}", **lock_hide_kwargs)
        cmds.setAttr(f"{attr_ctrl}.visibility", **lock_hide_kwargs)

        # parent to top grp
        cmds.parent(attr_ctrl_grp, self.mod_top_grp)

        # assign instances variables
        self.attr_ctrl = attr_ctrl

    def setup_stretch_attr(
        self,
        joint_chain: list[str],
        follicle_chain: list[str],
        global_scale_offs_obj: list[str],
        iteration_id: str,
    ) -> None:
        """Setup ik stretch attribute for attribute control.

        Args:
            joint_chain: List of joints in main skinned joint chain.
            follicle_chain: List of follicles used for setting up flexi ik chain.
            global_scale_offs_obj: Object or group to get ".scaleX" from
                for global scale stretch offset.
            iteration_id: Unique alphabetic id for each created object.

        """
        for i, (jnt, foll) in enumerate(
            zip(joint_chain, follicle_chain, strict=False),
        ):
            if i == 0:  # skip first joint
                continue
            # ----- create joint length ruler -----
            # length of joint translate X
            ruler_shape, ruler_transform, ruler_loc_01, ruler_loc_02, *_ = create_attached_ruler(
                name=f"{self.mod_name}Ruler{self.mirr_side}{iteration_id}{i:02d}",
                ruler_start_object=follicle_chain[i - 1],
                ruler_end_object=foll,
            )
            # ----- global scale stretch offset -----
            globalscale_offs_nd = cmds.createNode(
                "multiplyDivide",
                name=f"{self.mod_name}IkStretchGlobalScale{self.mirr_side}{iteration_id}{i:02d}_multiplyDivide",
            )
            cmds.setAttr(f"{globalscale_offs_nd}.operation", 2)  # divide operation
            cmds.connectAttr(f"{global_scale_offs_obj}.scaleX", f"{globalscale_offs_nd}.input2X")
            # ----- setup stretch blendColors node -----
            trans_stretch_nd = cmds.createNode(
                "blendColors",
                name=f"{self.mod_name}IkStretchTranslate{self.mirr_side}{iteration_id}{i:02d}_blendColors",
            )
            cmds.connectAttr(
                f"{self.attr_ctrl}.ikStretch",
                f"{trans_stretch_nd}.blender",
                force=True,
            )
            # query joint length
            jnt_trans_x = cmds.getAttr(f"{jnt}.translateX")
            # add negative multiplier if "x" chain facing negative direction
            if jnt_trans_x < 0:
                inverse_nd = cmds.createNode(
                    "multiplyDivide",
                    name=f"{self.mod_name}IkStretchInverse{self.mirr_side}{iteration_id}{i:02d}_multiplyDivide",
                )
                cmds.setAttr(f"{inverse_nd}.input2X", -1)
                cmds.connectAttr(f"{ruler_shape}.distance", f"{globalscale_offs_nd}.input1X")
                cmds.connectAttr(f"{globalscale_offs_nd}.outputX", f"{inverse_nd}.input1X")
                cmds.connectAttr(f"{inverse_nd}.outputX", f"{trans_stretch_nd}.color1R")
            else:
                # set blendColors 1R to dynamic length distance
                cmds.connectAttr(f"{ruler_shape}.distance", f"{globalscale_offs_nd}.input1X")
                cmds.connectAttr(f"{globalscale_offs_nd}.outputX", f"{trans_stretch_nd}.color1R")

            # set blendColors 2R to static joint length
            cmds.setAttr(f"{trans_stretch_nd}.color2R", jnt_trans_x)
            # connect blendColors to joint
            cmds.connectAttr(f"{trans_stretch_nd}.outputR", f"{jnt}.translateX")

            # ----- parent and hide -----
            for obj in [ruler_transform, ruler_loc_01, ruler_loc_02]:
                cmds.parent(obj, self.ikstretch_top_grp)
