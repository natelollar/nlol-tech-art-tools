"""Run through rig modules in rig object data toml file.
Take in module args. Run the modules to build the different rig parts.
"""

import tomllib
from importlib import reload
from pathlib import Path

from nlol.scripts.rig_modules import (
    biped_leg_mod,
    biped_limb_mod,
    fk_chain_mod,
    fk_control_mod,
    fk_ik_single_chain_mod,
    world_control_mod,
)
from nlol.utilities import utils_maya
from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

reload(biped_leg_mod)
reload(fk_control_mod)
reload(fk_chain_mod)
reload(fk_ik_single_chain_mod)
reload(world_control_mod)
reload(biped_limb_mod)
reload(biped_limb_mod)
reload(utils_maya)

left_to_right_str = utils_maya.left_to_right_str


def build_modules(rig_data_filepath: str | Path):
    """Cycle through rig module list and build them.
    Also, create top rig group and tag controllers for parallel evalution.

    Args:
        rig_data_filepath: Toml filepath with name and joint data for rig.

    """
    logger = get_logger()

    # ----- query rig module data -----
    with open(rig_data_filepath, "rb") as f:
        rig_object_data_file = tomllib.load(f)
        rig_name = rig_object_data_file.get("rig_name")
        rig_object_data = rig_object_data_file["rig_module"]

    # ----- add right modules -----
    right_modules = []
    for mod_dict in rig_object_data:
        rig_module = mod_dict["rig_module"]
        rig_module_name = mod_dict["rig_module_name"]
        mirror_right = mod_dict.get("mirror_right")
        mirror_direction = mod_dict.get("mirror_direction")
        if mirror_right and "left" in mirror_direction:
            joints = left_to_right_str(mod_dict.get("joints"))
            upper_twist_joints = left_to_right_str(mod_dict.get("upper_twist_joints", ""))
            lower_twist_joints = left_to_right_str(mod_dict.get("lower_twist_joints", ""))
            if mirror_direction:
                mirror_direction = mirror_direction.replace("left", "right")
            right_dict = {
                "rig_module": rig_module,
                "rig_module_name": rig_module_name,
                "joints": joints,
                "upper_twist_joints": upper_twist_joints,
                "lower_twist_joints": lower_twist_joints,
                "mirror_direction": mirror_direction,
                "constraint": mod_dict.get("constraint"),
            }
            right_modules.append(right_dict)
        elif mirror_right and "left" not in mirror_direction:
            error_msg = '"mirror_right" failed for: '
            f'{rig_module}, {rig_module_name}, {mirror_direction}\n"left" not in "mirror_direction"'
            logger.error(error_msg)
            raise ValueError(error_msg)
    rig_object_data.extend(right_modules)

    # ----------
    top_groups = []
    for mod_dict in rig_object_data:
        try:
            rig_module = mod_dict["rig_module"]
            rig_module_name = mod_dict["rig_module_name"]
            mirror_direction = mod_dict.get("mirror_direction")

            main_joints = mod_dict.get("joints")
            if main_joints:
                main_joints = mod_dict["joints"].split(",")
                main_joints = [str.strip() for str in main_joints]
            upper_twist_joints = mod_dict.get("upper_twist_joints", "").split(",")
            upper_twist_joints = [str.strip() for str in upper_twist_joints]
            lower_twist_joints = mod_dict.get("lower_twist_joints", "").split(",")
            lower_twist_joints = [str.strip() for str in lower_twist_joints]

            constraint = mod_dict.get("constraint")

            match rig_module:
                case "biped_limb_mod":
                    module_instance = biped_limb_mod.BipedLimbModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                        upper_twist_joints=upper_twist_joints,
                        lower_twist_joints=lower_twist_joints,
                    )
                    module_top_group = module_instance.build_limb_module()
                    top_groups.append(module_top_group)
                case "biped_leg_mod":
                    module_instance = biped_leg_mod.BipedLegModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                        upper_twist_joints=upper_twist_joints,
                        lower_twist_joints=lower_twist_joints,
                    )
                    module_top_group = module_instance.build_leg_module()
                    top_groups.append(module_top_group)
                case "fk_control_mod":
                    kwargs = {
                        "rig_module_name": rig_module_name,
                        "mirror_direction": mirror_direction,
                        "main_joints": main_joints,
                    }
                    kwargs_optional = [("constraint", constraint)]
                    for key, value in kwargs_optional:
                        if value is not None:
                            kwargs[key] = value

                    module_instance = fk_control_mod.FkControlModule(**kwargs)
                    module_top_group = module_instance.create_fk_ctrl()
                    top_groups.append(module_top_group)
                case "world_control_mod":
                    module_instance = world_control_mod.WorldControlModule(
                        rig_module_name=rig_module_name,
                    )
                    module_top_group = module_instance.create_world_ctrl()
                    top_groups.append(module_top_group)
                case "fk_chain_mod":
                    module_instance = fk_chain_mod.FkChainModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                    )
                    module_top_group = module_instance.build_fk_ctrl_chain()
                    top_groups.append(module_top_group)
                case "fk_ik_single_chain_mod":
                    module_instance = fk_ik_single_chain_mod.FkIkSingleChainModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                    )
                    module_top_group = module_instance.build_module()
                    top_groups.append(module_top_group)
                case _:
                    logger.warning(f"Unknown rig module: {rig_module}")
        except Exception:
            mirr_side = mirror_direction if mirror_direction else ""
            error_msg = f"Error building rig module: {rig_module}, {rig_module_name}, {mirr_side}"
            logger.exception(error_msg)
            raise RuntimeError(error_msg)

    # ---------- create top rig group ----------
    if rig_name:
        rig_name = f"{rig_name}_rigGrp"
    else:
        rig_name = "main_rigGrp"
    main_rig_group = cmds.group(empty=True, name=rig_name)
    for grp in top_groups:
        cmds.parent(grp, main_rig_group)

    # ----- tag controls for parallel evaluation -----
    rig_ctrls = cmds.listRelatives(main_rig_group, allDescendents=True)
    rig_ctrls = [
        ctrl
        for ctrl in rig_ctrls
        if cmds.listRelatives(ctrl, shapes=True, type="nurbsCurve")
        and "ctrl" in ctrl.lower()
        and not any(word in ctrl.lower() for word in ("switch", "swch"))
    ]
    cmds.controller(rig_ctrls)
