"""Set up parent space switching for rig modules.
Uses parent space data from "rig_parent_spaces.toml".
"""

import tomllib
from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.scripts.rig_components import clean_constraints, multi_point_constraint
from nlol.utilities import utils_maya
from nlol.utilities.nlol_maya_logger import get_logger

reload(multi_point_constraint)
reload(clean_constraints)

multi_point_const = multi_point_constraint.multi_point_const
parent_constr = clean_constraints.parent_constr
scale_constr = clean_constraints.scale_constr
left_to_right_str = utils_maya.left_to_right_str


class ParentSpacing:
    """Set up parent spaces for the rig. Also, used
    for main parenting of rig modules to eachother
    even if they don't have multiple parent spaces.
    """

    def __init__(self, rig_ps_filepath: str | Path):
        """Args:
        The "rig_parent_spaces.toml" file to import.
        Contains names of child parent relationships
        for rig control.
        """
        self.rig_ps_filepath = rig_ps_filepath

        self.logger = get_logger()

    def build(self):
        """Build process entry point for ParentSpacing class.
        --------------------------------------------------
        Get data from "rig_parent_spaces.toml" first.  Then setup parent spaces.
        """
        if not Path(self.rig_ps_filepath).is_file():
            msg = (
                '"rig_parent_spaces.toml" not in rig folder. Skipping parent space setup.\n'
                f'File not found: "{self.rig_ps_filepath}".'
            )
            self.logger.info(msg)
            return

        # query parent space data
        with open(self.rig_ps_filepath, "rb") as f:
            rig_ps_data = tomllib.load(f)["control"]

        # ----- add right controls -----
        right_controls = []
        for ps_dict in rig_ps_data:
            mirror_right = ps_dict.get("mirror_right")
            if mirror_right and "left" in ps_dict["control"].lower():
                control = left_to_right_str(ps_dict["control"])

                parents = ps_dict.get("parents")
                if parents:  # may be only base_parent exists
                    parents = left_to_right_str(parents)

                base_parent = ps_dict.get("base_parent")
                if base_parent:
                    base_parent = left_to_right_str(base_parent)

                right_dict = {
                    "control": control,
                    "parents": parents,
                    "separate_transforms": ps_dict.get("separate_transforms"),
                    "skip_translate": ps_dict.get("skip_translate"),
                    "skip_rotate": ps_dict.get("skip_rotate"),
                    "skip_scale": ps_dict.get("skip_scale"),
                    "use_point_constraint": ps_dict.get("use_point_constraint"),
                    "base_parent": base_parent,
                    "base_parent_enable": ps_dict.get("base_parent_enable"),
                }
                right_controls.append(right_dict)
        rig_ps_data.extend(right_controls)

        # ---------- iterate through parent space dictionaries ----------
        for ps_dict in rig_ps_data:
            # ----- get variables for child control/s -----
            control = ps_dict["control"]
            control = control.split(",")
            control = [txt.strip() for txt in control if txt.strip()]

            parents = ps_dict.get("parents")
            if parents:  # may be only base_parent exists
                parents = parents.split(",")
                parents = [txt.strip() for txt in parents if txt.strip()]

            separate_transforms = ps_dict.get("separate_transforms")
            skip_translate = ps_dict.get("skip_translate")
            skip_rotate = ps_dict.get("skip_rotate")
            skip_scale = ps_dict.get("skip_scale")

            use_point_constraint = ps_dict.get("use_point_constraint")

            base_parent = ps_dict.get("base_parent")
            if base_parent:
                base_parent = base_parent.split(",")
                base_parent = [txt.strip() for txt in base_parent if txt.strip()]
            
            base_parent_enable = ps_dict.get("base_parent_enable")
            if base_parent and base_parent_enable: # redundant if both keys used
                msg = (
                    f'Do not need both "base_parent" and "base_parent_enable": {control}\n'
                    '"base_parent_enable" copies and uses "parents" for "base_parent" values.'
                )
                self.logger.error(msg)
                raise ValueError(msg)
            if base_parent_enable: # used instead of base_parent
                base_parent = parents

            # check if parent objects exist in scene
            for obj in parents or []:
                if not cmds.objExists(obj):
                    error_msg = f"{obj}: Parent object does not exist in Maya scene."
                    self.logger.warning(error_msg)
                    raise ValueError(error_msg)

            # ----- assign instance variables -----
            self.parents = parents
            self.separate_transforms = separate_transforms
            self.skip_translate = skip_translate
            self.skip_rotate = skip_rotate
            self.skip_scale = skip_scale
            self.use_point_constraint = use_point_constraint
            self.base_parent = base_parent

            # ---------- apply parent spaces ----------
            for ctrl in control:  # check if multiple controls listed
                if not cmds.objExists(ctrl):  # check if control object exist in scene
                    self.logger.warning(f'Skipping, control does not exist in Maya scene: "{ctrl}"')
                    continue

                self.control = ctrl
                self.build_parent_spaces()

    def build_parent_spaces(self):
        """Check parent space parameters first.
        Then, build parent space switching for rig controls.
        """
        # ----- get parent switch group -----
        # used for main parent space connections
        cmds.select(self.control)
        ps_grp_search = []  # search groups incase hierarchy moves
        for _ in range(3):
            cmds.pickWalk(direction="up")
            grp = cmds.ls(selection=True)[0]
            ps_grp_search.append(grp)
        ps_grp_matches = [grp for grp in ps_grp_search if "PrntSwchGrp" in grp]
        if not ps_grp_matches:
            error_msg = f'Failed to find "PrntSwchGrp" for: "{self.control}"\n'
            f'Instead found:"{ps_grp_search}"'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        ps_grp = ps_grp_matches[0]

        # ----- get base parent group -----
        # sits right above parent switch group
        cmds.select(self.control)
        bp_grp_search = []
        for _ in range(4):
            cmds.pickWalk(direction="up")
            grp = cmds.ls(selection=True)[0]
            bp_grp_search.append(grp)
        bp_grp_matches = [grp for grp in bp_grp_search if "PrntGrp" in grp]
        if not bp_grp_matches:
            error_msg = f'Failed to find "PrntGrp" for: "{self.control}"\n'
            f'Instead found:"{bp_grp_search}"'
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        bp_grp = bp_grp_matches[0]

        # ---------- check values ----------
        # check "parents" values
        errors = []
        if not self.parents and not self.base_parent:
            errors.append(f'{self.control}: Must have "base_parent" if no "parents" object/s.')
        if self.separate_transforms and not self.parents:
            errors.append(f'{self.control}: "separate_transforms" requires "parents".')
        # require "base_parent" for "use_point_constraint"
        if self.use_point_constraint and not self.base_parent:
            errors.append(
                f'{self.control}: "base_parent" value required for "use_point_constraint"',
            )
        # do not allow separate_transforms with only one object in parents
        if self.parents and len(self.parents) == 1 and self.separate_transforms:
            errors.append(
                f'{self.control}: "separate_transforms" not needed if only one object in "parents"',
            )
        # ----------
        if not self.separate_transforms and self.use_point_constraint:
            errors.append(
                f'{self.control}: "separate_transforms" needed for "use_point_constraint"',
            )
        # ---------- check skip values ----------
        # check that base_parent exists if skip values exist
        if (
            self.parents
            and (self.skip_translate or self.skip_rotate or self.skip_scale)
            and not self.base_parent
        ):
            errors.append(
                f'{self.control}: Must have "base_parent" to skip transforms for parent switching.',
            )
        # ---------- log errors ----------
        if errors:
            error_msg = "\n".join(errors)
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        # ---------- assign instance variables ----------
        self.ps_grp = ps_grp
        self.bp_grp = bp_grp

        # ---------- main parent space setup ----------
        if self.parents:
            self.setup_main_parents()

        # --------------- base_parent setup ---------------
        if self.base_parent and len(self.base_parent) == 1:
            parent_constr(self.base_parent[0], self.bp_grp, offset=True)
            scale_constr(self.base_parent[0], self.bp_grp)
        # ----- multiple base_parent setup -----
        elif self.base_parent and len(self.base_parent) > 1:
            self.setup_multiple_base_parents()

    def setup_main_parents(self):
        """Setup parent space switching for main parents."""
        # ----- divider attribute for organization -----
        # add if more than one "parents" value
        ps_divider_name = "____Parent_Spaces____"
        if len(self.parents) > 1:
            cmds.addAttr(
                self.control,
                longName=ps_divider_name,
                niceName=ps_divider_name,
                attributeType="enum",
                enumName="----------",
            )
            cmds.setAttr(f"{self.control}.{ps_divider_name}", channelBox=True)

        # ----- hide "parent space/s" attr if only one parent -----
        ps_attr_visible = not (len(self.parents) < 2)

        # --------------- main parent switch setup ---------------
        if not self.separate_transforms:
            # ----- parent space attribute -----
            # enum attr with parent object names
            cmds.addAttr(
                self.control,
                longName="parentSpaces",
                attributeType="enum",
                keyable=ps_attr_visible,
            )
            enum_name_str = ""
            for i, obj in enumerate(self.parents):
                enum_name_str = obj if i == 0 else f"{enum_name_str}:{obj}"
                cmds.addAttr(f"{self.control}.parentSpaces", edit=True, enumName=enum_name_str)

            # ----- set up parent and scale constraint -----
            for i, prnt_obj in enumerate(self.parents):
                prnt_const = parent_constr(prnt_obj, self.ps_grp, offset=True)
                # only skip if skip_scale and base_parent
                if not (self.skip_scale and self.base_parent):  # skip for skip_scale
                    scl_const = scale_constr(prnt_obj, self.ps_grp, offset=True)

                ps_condition_nd_name = self.ps_grp.replace(
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
                cmds.connectAttr(f"{self.control}.parentSpaces", f"{ps_condition_nd}.firstTerm")
                # connect to constraint weight
                cmds.connectAttr(
                    f"{ps_condition_nd}.outColorR",
                    f"{prnt_const}.target[{i}].targetWeight",
                    force=True,
                )
                if not (self.skip_scale and self.base_parent):
                    cmds.connectAttr(
                        f"{ps_condition_nd}.outColorR",
                        f"{scl_const}.target[{i}].targetWeight",
                        force=True,
                    )
        elif self.separate_transforms:
            # ----- check skip transform and use_point_constraint values -----
            translate_str = "point" if self.use_point_constraint else "translate"
            transform_attrs = [
                translate_str if not self.skip_translate else None,
                "rotate" if not self.skip_rotate else None,
                "scale" if not self.skip_scale else None,
            ]
            # check that not all transforms are skipped and base_parent is being used if skipping
            if transform_attrs == [None, None, None]:
                error_msg = (
                    f"{self.control}: No attributes available for parent switching."
                    " All attributes skipped."
                )
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            # parent space enum attribute with parent object names
            for attr in transform_attrs:
                if attr is None:
                    continue
                cmds.addAttr(
                    self.control,
                    longName=f"{attr}Space",
                    attributeType="enum",
                    keyable=ps_attr_visible,
                )
                enum_name_str = ""
                for i, obj in enumerate(self.parents):
                    enum_name_str = obj if i == 0 else f"{enum_name_str}:{obj}"
                    cmds.addAttr(f"{self.control}.{attr}Space", edit=True, enumName=enum_name_str)

            # --------------- set up constraints ---------------
            if not self.skip_translate:
                if self.use_point_constraint:
                    # custom point constraint with proper target parent offsets
                    tran_const = multi_point_const(
                        parent_objects=self.parents,
                        child_object=self.ps_grp,
                        index_attribute=f"{self.control}.pointSpace",
                    )
                else:
                    tran_const = parent_constr(
                        self.parents,
                        self.ps_grp,
                        skip_rot=True,
                        offset=True,
                    )
            else:
                tran_const = None
            if not self.skip_rotate:
                rot_const = parent_constr(self.parents, self.ps_grp, skip_tran=True, offset=True)
            else:
                rot_const = None
            if not self.skip_scale:
                scl_const = scale_constr(self.parents, self.ps_grp)
            else:
                scl_const = None

            constraints = [tran_const, rot_const, scl_const]

            # ---------- connect constraint condition nodes ----------
            for i, prnt_obj in enumerate(self.parents):
                for const, attr in zip(constraints, transform_attrs, strict=False):
                    if const is None:  # if constraint is None, go to the next one
                        continue

                    # ----- constraint weight index condition node -----
                    ps_condition_nd_name = self.ps_grp.replace(
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
                    cmds.connectAttr(f"{self.control}.{attr}Space", f"{ps_condition_nd}.firstTerm")
                    # connect to constraint weight
                    cmds.connectAttr(
                        f"{ps_condition_nd}.outColorR",
                        f"{const}.target[{i}].targetWeight",
                        force=True,
                    )

    def setup_multiple_base_parents(self):
        """Create a secondary space switching for the base parent group.
        This is the group right above the parent switch group.
        Multiple base parents useful to maintain a master parent if skipping
        certain constraints in parent switching or using a point constraint
        which needs an additional parent to hold master rotation values.
        """
        # ----- divider attribute for organization -----
        ps_divider_name = "____Parent_Spaces____"
        if not cmds.objExists(f"{self.control}.{ps_divider_name}"):
            cmds.addAttr(
                self.control,
                longName=ps_divider_name,
                niceName=ps_divider_name,
                attributeType="enum",
                enumName="----------",
            )
            cmds.setAttr(f"{self.control}.{ps_divider_name}", channelBox=True)
        # ----- parent space attribute -----
        cmds.addAttr(
            self.control,
            longName="baseParent",
            attributeType="enum",
            keyable=True,
        )
        enum_name_str = ""
        for i, obj in enumerate(self.base_parent):
            enum_name_str = obj if i == 0 else f"{enum_name_str}:{obj}"
            cmds.addAttr(f"{self.control}.baseParent", edit=True, enumName=enum_name_str)

        # ----- set up parent and scale constraint -----
        for i, prnt_obj in enumerate(self.base_parent):
            prnt_const = parent_constr(prnt_obj, self.bp_grp, offset=True)
            scl_const = scale_constr(prnt_obj, self.bp_grp, offset=True)

            ps_condition_nd_name = self.bp_grp.replace(
                "_ctrlPrntGrp",
                f"_{i:02d}_ctrlPrntGrpCondition",
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
            cmds.connectAttr(f"{self.control}.baseParent", f"{ps_condition_nd}.firstTerm")
            # connect to constraint weight
            cmds.connectAttr(
                f"{ps_condition_nd}.outColorR",
                f"{prnt_const}.target[{i}].targetWeight",
                force=True,
            )
            cmds.connectAttr(
                f"{ps_condition_nd}.outColorR",
                f"{scl_const}.target[{i}].targetWeight",
                force=True,
            )
