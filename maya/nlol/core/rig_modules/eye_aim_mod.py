from importlib import reload

from maya import cmds
from nlol.core.rig_components import (
    clean_constraints,
    create_control_groups,
    create_nurbs_curves,
)
from nlol.core.rig_tools import get_aligned_axis
from nlol.utilities.nlol_maya_logger import get_logger
from nlol.utilities.utils_maya import cap, invert_axis_string

reload(create_nurbs_curves)
reload(clean_constraints)

CreateCurves = create_nurbs_curves.CreateCurves
create_ctrl_grps = create_control_groups.create_ctrl_grps
parent_constr = clean_constraints.parent_constr
scale_constr = clean_constraints.scale_constr
aim_constr = clean_constraints.aim_constr


class EyeAimModule:
    """Standard left and right eyes for a human style character.
    Creates "aim at" controls out in front of the face.
    Also, creates fk offset controls directly on the eyes.
    """

    def __init__(
        self,
        rig_module_name: str,
        main_joints: list | None = None,
        aim_vector: str | None = None,
        up_vector: str | None = None,
        reverse_right_vectors: bool | None = None,
    ):
        """Args:
        rig_module_name: Custom name for the rig module.
        main_joints: Left and right eye joints aimed at controls, with left listed first.
            Exactly two joints.
        aim_vector: Forword axis of the eye joints.
        up_vector: Up axis of the eye joints.
        reverse_right_axis:  Reverse the right eye vector axis'.
            Useful if right joint mirrored with standard Maya "Mirror Joints" behavior.
        """
        self.mod_name = rig_module_name
        self.main_joints = main_joints
        self.aim_vector = aim_vector
        self.up_vector = up_vector
        self.reverse_right_vectors = reverse_right_vectors

        self.lock_hide_kwargs = {"lock": True, "keyable": False, "channelBox": False}

        self.logger = get_logger()

    def build(self) -> str:
        """Build the eye aim module.
        --------------------------------------------------
        Uses a left and right eye joint. Or a single eye joint.
        """
        mod_top_grp = cmds.group(empty=True, name=f"{self.mod_name}_grp")

        # check how many eye joints
        if len(self.main_joints) == 1:
            mirr_side = ["_"]
        if len(self.main_joints) == 2:
            mirr_side = ["_left_", "_right_"]
        elif len(self.main_joints) > 2:
            error_msg = (
                "Eye aim module requires a left and right eye joint, or a single joint. "
                f"Cannot have more than 2 joints. Current joints: {self.main_joints}"
            )
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # create default axis vector values if missing. mainly for aim constraint.
        # finds joint axis based on world up and world forward
        if not self.aim_vector:
            self.aim_vector = get_aligned_axis.axis_facing_direction(
                object=self.main_joints[0],
                world_space_direction="z",
            )
        if not self.up_vector:
            self.up_vector = get_aligned_axis.axis_facing_direction(
                object=self.main_joints[0],
                world_space_direction="y",
            )

        # eye joint parent
        jnt_parent = cmds.listRelatives(self.main_joints[0], parent=True)[0]
        if not jnt_parent:
            self.logger.warning(
                f'"{self.main_joints[0]}" is missing its parent joint: "{jnt_parent}"',
            )

        # iterate through eye joints
        aimctrl_top_grps = []
        for i, jnt in enumerate(self.main_joints):
            # base fk eye control
            fkctrl = CreateCurves(
                name=f"fk{cap(self.mod_name)}{mirr_side[i]}ctrl",
                size=0.4,
                color_rgb=(0.9, 0.9, 0.0),
            ).box_curve()
            fkctrl_top_grp, fkctrl_prnt_grp, _, _, fkctrl_aux_grp = create_ctrl_grps(
                fkctrl,
                aux_offset_grp=True,
            )
            cmds.matchTransform(fkctrl_top_grp, jnt)  # snap control to joint
            # constrain joint to control
            parent_constr(fkctrl, jnt)
            scale_constr(fkctrl, jnt)
            # parent control to joint parent
            if jnt_parent:
                parent_constr(jnt_parent, fkctrl_prnt_grp, offset=True)
                scale_constr(jnt_parent, fkctrl_prnt_grp)

            # reverse aim axis' vector for right side. example: "x" to "-x".
            if (
                self.reverse_right_vectors
                and len(self.main_joints) > 1
                and jnt == self.main_joints[1]
            ):
                self.aim_vector = invert_axis_string(self.aim_vector)
                self.up_vector = invert_axis_string(self.up_vector)

            # up vector locator curve. is aim constraints up object
            upvector_curve = CreateCurves(
                name=f"{self.mod_name}UpVector{mirr_side[i]}crv",
                size=0.5,
            ).locator_curve()
            cmds.setAttr(f"{upvector_curve}.visibility", 0)  # hide curve
            upobj_dist = 50  # up object distance
            axis_vectors = {
                "x": (upobj_dist, 0, 0),
                "y": (0, upobj_dist, 0),
                "z": (0, 0, upobj_dist),
                "-x": (-upobj_dist, 0, 0),
                "-y": (0, -upobj_dist, 0),
                "-z": (0, 0, -upobj_dist),
            }
            # transform upvector_curve
            cmds.parent(upvector_curve, jnt, relative=True)
            cmds.xform(
                upvector_curve,
                translation=(axis_vectors[self.up_vector.lower()]),
                relative=True,
            )
            cmds.parent(upvector_curve, world=True)  # unparent
            if jnt_parent:  # constrain upvector_curve to eye joint's parent
                parent_constr(jnt_parent, upvector_curve, offset=True)
                scale_constr(jnt_parent, upvector_curve)

            # aim control
            aimctrl = CreateCurves(
                name=f"{self.mod_name}Aim{mirr_side[i]}ctrl",
                size=0.25,
                color_rgb=(0.0, 0.4, 1.0),
            ).box_curve()
            aimctrl_top_grp, *_ = create_ctrl_grps(aimctrl)
            # transform aimctrl
            cmds.parent(aimctrl_top_grp, jnt, relative=True)
            cmds.xform(
                aimctrl_top_grp,
                translation=(axis_vectors[self.aim_vector.lower()]),
                relative=True,
            )
            cmds.parent(aimctrl_top_grp, world=True)

            # aim the fkctrl at aimctrl
            aim_constr(
                targets=aimctrl,
                object=fkctrl_aux_grp,
                world_up_object=upvector_curve,
                aim_vector=self.aim_vector,
                up_vector=self.up_vector,
            )

            # parent objects to rig mod top group
            if len(self.main_joints) == 1:
                cmds.parent(aimctrl_top_grp, mod_top_grp)
            cmds.parent(fkctrl_top_grp, mod_top_grp)
            cmds.parent(upvector_curve, mod_top_grp)

            # control attribute visibility
            for axis in "XYZ":
                cmds.setAttr(f"{aimctrl}.rotate{axis}", **self.lock_hide_kwargs)
                cmds.setAttr(f"{aimctrl}.scale{axis}", **self.lock_hide_kwargs)
            cmds.setAttr(f"{aimctrl}.visibility", **self.lock_hide_kwargs)
            cmds.setAttr(f"{fkctrl}.visibility", **self.lock_hide_kwargs)

            # -----
            aimctrl_top_grps.append(aimctrl_top_grp)

        # aim control parent. create single parent control to control both eye aim controls
        if len(self.main_joints) == 2:
            aimprnt_ctrl = CreateCurves(
                name=f"{self.mod_name}AimParent_ctrl",
                size=0.75,
                color_rgb=(0.9, 0.9, 0.0),
            ).box_curve()
            aimprnt_ctrl_top_grp, *_ = create_ctrl_grps(aimprnt_ctrl)
            placement_const = parent_constr(aimctrl_top_grps, aimprnt_ctrl_top_grp)
            cmds.delete(placement_const)

            # parent oganize
            cmds.parent(aimctrl_top_grps, aimprnt_ctrl)
            cmds.parent(aimprnt_ctrl_top_grp, mod_top_grp)

            # control attribute visibility
            for axis in "XYZ":
                cmds.setAttr(f"{aimprnt_ctrl}.scale{axis}", **self.lock_hide_kwargs)
            cmds.setAttr(f"{aimprnt_ctrl}.visibility", **self.lock_hide_kwargs)

        return mod_top_grp
