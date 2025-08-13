"""Set up parent space switching for rig modules.
Uses parent space data from "rig_parent_spaces.toml".
"""

import tomllib
from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.scripts.rig_components import clean_constraints, multi_point_constraint
from nlol.utilities.nlol_maya_logger import get_logger

reload(multi_point_constraint)
reload(clean_constraints)

multi_point_const = multi_point_constraint.multi_point_const
parent_constr = clean_constraints.parent_constr
scale_constr = clean_constraints.scale_constr


def setup_parent_spaces(rig_ps_filepath: str | Path):
    """Set up parent spaces for the rig. Also, used
    for main parenting of rig modules to eachother
    even if they don't have multiple parent spaces.

    Args:
        The "rig_parent_spaces.toml" file to import.
            Contains names of child parent relationships
            for rig control.

    """
    logger = get_logger()

    # query parent space data
    with open(rig_ps_filepath, "rb") as f:
        rig_ps_data = tomllib.load(f)["control"]

    # ----- add right controls -----
    right_controls = []
    for ps_dict in rig_ps_data:
        mirror_right = ps_dict.get("mirror_right")
        if mirror_right and "_left" in ps_dict["control"]:
            control = ps_dict["control"].replace("_left", "_right")
            parents = ps_dict.get("parents")
            if parents:
                parents = ps_dict["parents"].replace("_left", "_right")
            right_dict = {
                "control": control,
                "parents": parents,
                "separate_transforms": ps_dict.get("separate_transforms"),
                "skip_translate": ps_dict.get("skip_translate"),
                "skip_rotate": ps_dict.get("skip_rotate"),
                "skip_scale": ps_dict.get("skip_scale"),
                "use_point_constraint": ps_dict.get("use_point_constraint"),
                "default_parent": ps_dict.get("default_parent"),
            }
            right_controls.append(right_dict)
    rig_ps_data.extend(right_controls)

    # ----------
    for ps_dict in rig_ps_data:
        # ----- get variables for child control -----
        control = ps_dict["control"]
        parents = ps_dict.get("parents")
        if parents:
            parents = parents.split(",")
            parents = [str.strip() for str in parents]
        separate_transforms = ps_dict.get("separate_transforms")
        skip_translate = ps_dict.get("skip_translate")
        skip_rotate = ps_dict.get("skip_rotate")
        skip_scale = ps_dict.get("skip_scale")
        use_point_constraint = ps_dict.get("use_point_constraint")
        default_parent = ps_dict.get("default_parent")

        # ----- check if control and parent objects exist in scene -----
        if not cmds.objExists(control):
            logger.warning(f"{control}: Skipping, control does not exist in Maya scene.")
            continue
        for obj in parents:
            if not cmds.objExists(obj):
                error_msg = f"{obj}: Parent object does not exist in Maya scene."
                logger.warning(error_msg)
                raise ValueError(error_msg)

        # ----- get parent switch group -----
        cmds.select(control)
        for _ in range(2):
            cmds.pickWalk(direction="up")
        ps_grp = cmds.ls(selection=True)[0]
        if "PrntSwchGrp" not in ps_grp:
            error_msg = f'Failed to find "PrntSwchGrp" for: "{control}"\n'
            f'Instead found:"{ps_grp}"'
            logger.error(error_msg)
            raise ValueError(error_msg)
        # ----- get default parent group -----
        cmds.select(control)
        for _ in range(3):
            cmds.pickWalk(direction="up")
        dp_grp = cmds.ls(selection=True)[0]  # child controls default parent group
        if "PrntGrp" not in dp_grp:
            error_msg = f'Failed to find "PrntGrp" for: "{control}"\n'
            f'Instead found:"{dp_grp}"'
            logger.error(error_msg)
            raise ValueError(error_msg)

        # ---------- check values ----------
        # check "parents" values
        errors = []
        if not parents and not default_parent:
            errors.append(f'{control}: Must have "default_parent" if no "parents" object/s.')
        if separate_transforms and not parents:
            errors.append(f'{control}: "separate_transforms" requires "parents".')
        # require "default_parent" for "use_point_constraint"
        if use_point_constraint and not default_parent:
            errors.append(f'{control}: "default_parent" value required for "use_point_constraint"')
        # do not allow separate_transforms with only one object in parents
        if len(parents) < 2 and separate_transforms:
            errors.append(
                f'{control}: "separate_transforms" not needed if only one object in "parents"',
            )
        if errors:
            error_msg = "\n".join(errors)
            logger.error(error_msg)
            raise ValueError(error_msg)

        if not separate_transforms and use_point_constraint:
            logger.warning(f'{control}: "separate_transforms" needed for "use_point_constraint"')

        # ----- default_parent setup -----
        if default_parent:
            parent_constr(default_parent, dp_grp, offset=True)
            scale_constr(default_parent, dp_grp)

        # ----- stop loop here if no "parents" key -----
        if not parents:
            continue

        # ----- check skip values -----
        # check that default_parent exists if skip values exist
        if (skip_translate or skip_rotate or skip_scale) and not default_parent:
            error_msg = (
                f'{control}: Must have "default_parent" to skip transforms for parent switching.'
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # ----- divider attribute for organization -----
        if len(parents) > 1:  # add if more than one "parents" value
            ps_divider_name = "____Parent_Spaces____"
            cmds.addAttr(
                control,
                longName=ps_divider_name,
                niceName=ps_divider_name,
                attributeType="enum",
                enumName="----------",
            )
            cmds.setAttr(f"{control}.{ps_divider_name}", channelBox=True)

        # hide "parent space/s" attr if only one parent
        ps_attr_visible = not (len(parents) < 2)

        # --------------- main parent switch setup ---------------
        if not separate_transforms:
            # ----- parent space attribute -----
            # enum attr with parent object names
            cmds.addAttr(
                control,
                longName="parentSpaces",
                attributeType="enum",
                keyable=ps_attr_visible,
            )
            enum_name_str = ""
            for i, obj in enumerate(parents):
                enum_name_str = obj if i == 0 else f"{enum_name_str}:{obj}"
                cmds.addAttr(f"{control}.parentSpaces", edit=True, enumName=enum_name_str)

            # ----- set up parent constraint -----
            for i, prnt_obj in enumerate(parents):
                prnt_const = parent_constr(prnt_obj, ps_grp, offset=True)
                # only skip if skip_scale and default_parent
                if not (skip_scale and default_parent):  # skip for skip_scale
                    scl_const = scale_constr(prnt_obj, ps_grp, offset=True)

                ps_condition_nd_name = ps_grp.replace(
                    "_ctrlPrntSwchGrp",
                    f"_{i:02d}_ctrlPrntSwchGrpCondition",
                )
                ps_condition_nd = cmds.shadingNode(
                    "condition",
                    asUtility=True,
                    name=ps_condition_nd_name,
                )
                cmds.setAttr(f"{ps_condition_nd}.operation", 0)  # equal
                cmds.setAttr(f"{ps_condition_nd}.colorIfTrueR", 1)
                cmds.setAttr(f"{ps_condition_nd}.colorIfFalseR", 0)
                cmds.setAttr(f"{ps_condition_nd}.secondTerm", i)  # if equal to ps index
                cmds.connectAttr(f"{control}.parentSpaces", f"{ps_condition_nd}.firstTerm")
                # connect to constraint weight
                cmds.connectAttr(
                    f"{ps_condition_nd}.outColorR",
                    f"{prnt_const}.target[{i}].targetWeight",
                    force=True,
                )
                if not (skip_scale and default_parent):
                    cmds.connectAttr(
                        f"{ps_condition_nd}.outColorR",
                        f"{scl_const}.target[{i}].targetWeight",
                        force=True,
                    )
        elif separate_transforms:
            # ----- check skip transform and use_point_constraint values -----
            translate_str = "point" if use_point_constraint else "translate"
            transform_attrs = [
                translate_str if not skip_translate else None,
                "rotate" if not skip_rotate else None,
                "scale" if not skip_scale else None,
            ]
            # check that not all transforms are skipped and default_parent is being used if skipping
            if transform_attrs == [None, None, None]:
                error_msg = f"{control}: No attributes available for parent switching."
                " All attributes skipped."
                logger.error(error_msg)
                raise ValueError(error_msg)

            # parent space enum attribute with parent object names
            for attr in transform_attrs:
                if attr is None:
                    continue
                cmds.addAttr(
                    control,
                    longName=f"{attr}Space",
                    attributeType="enum",
                    keyable=ps_attr_visible,
                )
                enum_name_str = ""
                for i, obj in enumerate(parents):
                    enum_name_str = obj if i == 0 else f"{enum_name_str}:{obj}"
                    cmds.addAttr(f"{control}.{attr}Space", edit=True, enumName=enum_name_str)

            # --------------- set up constraints ---------------
            if not skip_translate:
                if use_point_constraint:
                    # custom point constraint with proper target parent offsets
                    tran_const = multi_point_const(
                        parent_objects=parents,
                        child_object=ps_grp,
                        index_attribute=f"{control}.pointSpace",
                    )
                else:
                    tran_const = parent_constr(parents, ps_grp, skip_rot=True, offset=True)
            else:
                tran_const = None
            if not skip_rotate:
                rot_const = parent_constr(parents, ps_grp, skip_tran=True, offset=True)
            else:
                rot_const = None
            if not skip_scale:
                scl_const = scale_constr(parents, ps_grp)
            else:
                scl_const = None

            constraints = [tran_const, rot_const, scl_const]

            # ---------- connect constraint condition nodes ----------
            for i, prnt_obj in enumerate(parents):
                for const, attr in zip(constraints, transform_attrs, strict=False):
                    if const is None:  # if constraint is None, go to the next one
                        continue

                    # ----- constraint weight index condition node -----
                    ps_condition_nd_name = ps_grp.replace(
                        "_ctrlPrntSwchGrp",
                        f"_{i:02d}_ctrlPrntSwchGrp{attr.capitalize()}Condition",
                    )
                    ps_condition_nd = cmds.shadingNode(
                        "condition",
                        asUtility=True,
                        name=ps_condition_nd_name,
                    )
                    cmds.setAttr(f"{ps_condition_nd}.operation", 0)  # equal
                    cmds.setAttr(f"{ps_condition_nd}.colorIfTrueR", 1)
                    cmds.setAttr(f"{ps_condition_nd}.colorIfFalseR", 0)
                    cmds.setAttr(f"{ps_condition_nd}.secondTerm", i)  # if equal to ps index
                    cmds.connectAttr(f"{control}.{attr}Space", f"{ps_condition_nd}.firstTerm")
                    # connect to constraint weight
                    cmds.connectAttr(
                        f"{ps_condition_nd}.outColorR",
                        f"{const}.target[{i}].targetWeight",
                        force=True,
                    )

    # ----------
    cmds.select(clear=True)
    cmds.flushUndo()
