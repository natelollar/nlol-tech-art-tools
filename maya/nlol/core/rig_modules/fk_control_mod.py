from importlib import reload

from maya import cmds
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_nurbs_curves,
)
from nlol.utilities import utils_maya
from nlol.utilities.nlol_maya_logger import get_logger

reload(create_nurbs_curves)
reload(create_control_groups)
reload(clean_constraints)

CreateCurves = create_nurbs_curves.CreateCurves
create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
scale_constr = clean_constraints.scale_constr
add_divider_attribue = utils_maya.add_divider_attribue


class FkControlModule:
    """For building a basic fk control setup as a rig module.
    May include multiple main_joints for creating multiple standalone fk controls.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str | None = None,
        main_joints: list | None = None,
        constraint: bool = True,
        use_joint_names: bool = False,
        blend_joints: list | None = None,
        hide_and_lock: bool = False,
        hide_translate: bool = False,
        hide_rotate: bool = False,
        hide_scale: bool = False,
    ):
        """Args:
        rig_module_name: Custom name for the rig module.
        mirror_direction: Name for mirror side.
        main_joints: Joint/s (or object/s). Where control is positioned.
            And what the control constrains, unless "constraint=False".
        constraint: Whether to connect the control and joint
            with a parent and scale constraint. Useful if parenting another control
            to this control instead of a joint.
        use_joint_names: Use joint names for control names if joint using nLol naming convention.
            "<name>_<direction>_<id>_<type>". Replaces the end type with "ctrl".
        blend_joints: Two joints (or objects) to blend control between.
            For example, blend mouth corner control between head and jaw joints.
        hide_and_lock: Whether to hide the control and lock the attributes.
            Used by world_control_mod to hide and lock at world origin.
        hide_translate, hide_rotate, hide scale: Lock and hide control attribute.
        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_joints = main_joints

        self.constraint = constraint
        self.use_joint_names = use_joint_names
        self.hide_and_lock = hide_and_lock
        self.blend_joints = blend_joints

        self.hide_translate = hide_translate
        self.hide_rotate = hide_rotate
        self.hide_scale = hide_scale

        self.logger = get_logger()

    def build(self) -> str | list[str]:
        """Create simple fk control for each joint or object in main_joints.
        --------------------------------------------------
        Locators may be used instead of joints for control placement.
        Create a single standalone fk control, or multiple.

        Returns:
            Top control group.

        """
        if self.main_joints is None:
            self.main_joints = [None]  # still iterate once if no joints

        fkctrl_grps = []
        for i, obj in enumerate(self.main_joints):
            # ----- create control curve -----
            if self.use_joint_names:  # use joint name just change the <type> string
                obj_type = obj.split("_")[-1]
                ctrl_name = obj.replace(obj_type, "ctrl")
            elif len(self.main_joints) > 1:  # use index id for multiple
                ctrl_name = f"{self.mod_name}{self.mirr_side}{i + 1:02d}_ctrl"
            else:
                ctrl_name = f"{self.mod_name}{self.mirr_side}ctrl"
            self.fkctrl = CreateCurves(
                name=ctrl_name,
                size=1,
                curve_type="box_curve",
            ).nurbs_curve
            # ----- create control groups -----
            self.fkctrl_aux_grp = None
            if self.blend_joints:
                self.fkctrl_grp, _, _, _, self.fkctrl_aux_grp = create_ctrl_grps(
                    self.fkctrl,
                    aux_offset_grp=True,
                )
            else:
                self.fkctrl_grp = create_ctrl_grps(self.fkctrl)[0]

            # ----- match control transforms to object -----
            if obj:  # obj might be None
                cmds.matchTransform(self.fkctrl_grp, obj)
                # if locator used from rig_helpers.ma, delete it
                if cmds.objectType(obj) != "joint":
                    obj_shp = cmds.listRelatives(obj, shapes=True)
                    if cmds.objectType(obj_shp) == "locator":
                        cmds.delete(obj)

            # ----- constrain object to control -----
            if self.constraint:  # parent constrain joint to control
                if not obj:
                    error_msg = f'{self.fkctrl}: Missing "joints" key. Need "joints" to constrain.'
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)
                parent_constr(self.fkctrl, obj)
                scale_constr(self.fkctrl, obj)

            # ----- optional blend between two parents -----
            if self.blend_joints:
                self.index = i
                self.setup_control_blend()

            # ----- hide and lock attrs -----
            if self.hide_and_lock:  # lock attributes and hide control
                cmds.setAttr(f"{self.fkctrl}.translate", lock=True)
                cmds.setAttr(f"{self.fkctrl}.rotate", lock=True)
                cmds.setAttr(f"{self.fkctrl}.scale", lock=True)
                cmds.setAttr(f"{self.fkctrl}.visibility", 0)

            lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}
            if self.hide_translate or self.hide_rotate or self.hide_scale:
                for axis in "XYZ":
                    if self.hide_translate:
                        cmds.setAttr(f"{self.fkctrl}.translate{axis}", **lock_hide_kwargs)
                    if self.hide_rotate:
                        cmds.setAttr(f"{self.fkctrl}.rotate{axis}", **lock_hide_kwargs)
                    if self.hide_scale:
                        cmds.setAttr(f"{self.fkctrl}.scale{axis}", **lock_hide_kwargs)
            # hide visibility attribute
            cmds.setAttr(f"{self.fkctrl}.visibility", **lock_hide_kwargs)

            # ----- return single control top group -----
            # if only one object
            if len(self.main_joints) == 1:
                return self.fkctrl_grp

            # ----- add top group to list
            fkctrl_grps.append(self.fkctrl_grp)

        # ----- control groups to top group -----
        fkctrls_top_grp = cmds.group(
            empty=True,
            name=f"{self.mod_name}Main{self.mirr_side}ctrlGrp",
        )
        cmds.parent(fkctrl_grps, fkctrls_top_grp)

        # return top group that contains multiple control groups
        return fkctrls_top_grp

    def setup_control_blend(self):
        """Blend auxiliary offset group between two objects, usually joints.
        Also, create a blend attribute to control the parent constraint weight
        between those two objects.
        """
        if len(self.blend_joints) != 2:
            msg = (
                f"({self.mod_name}, {self.mirr_side}) Must be exactly 2 blend joints.\n"
                f"Blend joints: {self.blend_joints}"
            )
            self.logger.error(msg)
            raise ValueError(msg)
        # create constraints
        prnt_const = parent_constr(self.blend_joints, self.fkctrl_aux_grp, offset=True)
        scl_const = scale_constr(self.blend_joints, self.fkctrl_aux_grp, offset=True)
        # add blend attribute to control
        add_divider_attribue(control_name=self.fkctrl, divider_amount=5)
        cmds.addAttr(
            self.fkctrl,
            longName="parentBlend",
            defaultValue=0.5,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        # reverse node for second weight connection to blend attribute
        reverse_nd_name = f"{self.mod_name}Blend{self.mirr_side}{self.index + 1:02d}_reverse"
        reverse_nd = cmds.createNode("reverse", name=reverse_nd_name)
        cmds.connectAttr(
            f"{self.fkctrl}.parentBlend",
            f"{reverse_nd}.inputX",
        )
        # parent constraint connections
        cmds.connectAttr(
            f"{self.fkctrl}.parentBlend",
            f"{prnt_const}.target[0].targetWeight",
            force=True,
        )
        cmds.connectAttr(
            f"{reverse_nd}.outputX",
            f"{prnt_const}.target[1].targetWeight",
            force=True,
        )
        # scale constraint connections
        cmds.connectAttr(
            f"{self.fkctrl}.parentBlend",
            f"{scl_const}.target[0].targetWeight",
            force=True,
        )
        cmds.connectAttr(
            f"{reverse_nd}.outputX",
            f"{scl_const}.target[1].targetWeight",
            force=True,
        )
