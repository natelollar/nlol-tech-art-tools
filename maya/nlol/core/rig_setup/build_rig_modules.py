"""Run through rig modules in rig object data toml file.
Take in module args. Run the modules to build the different rig parts.
"""

import tomllib
from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.core import general_utils
from nlol.core.rig_components import create_display_layers
from nlol.core.rig_modules import (
    biped_leg_mod,
    biped_limb_mod,
    eye_aim_mod,
    fk_chain_mod,
    fk_control_mod,
    fk_ik_single_chain_mod,
    fk_ik_spline_chain_mod,
    flexi_surface_fk_ctrl_mod,
    flexi_surface_ik_chain_mod,
    piston_mod,
    digitigrade_leg_mod,
    world_control_mod,
)
from nlol.core.rig_tools import select_multiple_joints
from nlol.utilities.nlol_maya_logger import get_logger

reload(biped_leg_mod)
reload(biped_limb_mod)
reload(fk_chain_mod)
reload(fk_control_mod)
reload(fk_ik_single_chain_mod)
reload(fk_ik_spline_chain_mod)
reload(flexi_surface_ik_chain_mod)
reload(flexi_surface_fk_ctrl_mod)
reload(piston_mod)
reload(world_control_mod)
reload(general_utils)
reload(eye_aim_mod)
reload(digitigrade_leg_mod)
reload(create_display_layers)

swap_side_str = general_utils.swap_side_str
objects_display_lyr = create_display_layers.objects_display_lyr


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
        if mirror_right and mirror_direction and "left" in mirror_direction:
            main_joints = swap_side_str(mod_dict.get("joints"))
            mirror_direction = (
                mirror_direction.replace("left", "right") if mirror_direction else None
            )
            upper_twist_joints = swap_side_str(mod_dict.get("upper_twist_joints", ""))
            lower_twist_joints = swap_side_str(mod_dict.get("lower_twist_joints", ""))
            foot_locators = (
                swap_side_str(ft_locs) if (ft_locs := mod_dict.get("foot_locators")) else ""
            )

            joint_chains_str_list = mod_dict.get("joint_chains", [])
            joint_chains = [swap_side_str(string_list) for string_list in joint_chains_str_list]

            origin_joint = swap_side_str(mod_dict.get("origin_joint", ""))
            mid_joints = swap_side_str(mod_dict.get("mid_joints", ""))
            top_joints = swap_side_str(mod_dict.get("top_joints", ""))
            bot_joints = swap_side_str(mod_dict.get("bot_joints", ""))

            right_dict = {
                "rig_module": rig_module,
                "rig_module_name": rig_module_name,
                "joints": main_joints,
                "mirror_direction": mirror_direction,
                "joint_chains": joint_chains,
                "constraint": mod_dict.get("constraint"),
                "use_joint_names": mod_dict.get("use_joint_names"),
                "blend_joints": mod_dict.get("blend_joints"),
                "get_joint_chain": mod_dict.get("get_joint_chain"),
                "flexi_surface": mod_dict.get("flexi_surface"),
                "hide_end_ctrl": mod_dict.get("hide_end_ctrl"),
                "hide_translate": mod_dict.get("hide_translate"),
                "hide_rotate": mod_dict.get("hide_rotate"),
                "hide_scale": mod_dict.get("hide_scale"),
                "display_layer": mod_dict.get("display_layer"),
                "upper_twist_joints": upper_twist_joints,
                "lower_twist_joints": lower_twist_joints,
                "main_object_names": mod_dict.get("main_object_names", ""),
                "upper_twist_name": mod_dict.get("upper_twist_name"),
                "lower_twist_name": mod_dict.get("lower_twist_name"),
                "foot_locators": foot_locators,
                "invert_toe_wiggle": mod_dict.get("invert_toe_wiggle"),
                "invert_toe_spin": mod_dict.get("invert_toe_spin"),
                "invert_foot_lean": mod_dict.get("invert_foot_lean"),
                "invert_foot_tilt": mod_dict.get("invert_foot_tilt"),
                "invert_foot_roll": mod_dict.get("invert_foot_roll"),
                "origin_joint": origin_joint,
                "mid_joints": mid_joints,
                "top_joints": top_joints,
                "bot_joints": bot_joints,
            }
            right_modules.append(right_dict)
        elif mirror_right and (mirror_direction is None or "left" not in mirror_direction):
            error_msg = (
                '"mirror_right" failed for: '
                f"{rig_module}, {rig_module_name}, {mirror_direction}\n"
                '"left" not in "mirror_direction" or missing "mirror_direction" key.'
            )
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
                main_joints = [txt.strip() for txt in main_joints if txt.strip()]
            if mod_dict.get("get_joint_chain"):
                main_joints = select_multiple_joints.select_joint_chain(main_joints)

            blend_joints = mod_dict.get("blend_joints")
            if blend_joints:
                blend_joints = [txt.strip() for txt in blend_joints.split(",") if txt.strip()]

            joint_chains_str_list = mod_dict.get("joint_chains", [])
            joint_chains = []
            for string_list in joint_chains_str_list:
                joint_list = string_list.split(",")
                joint_list = [txt.strip() for txt in joint_list if txt.strip()]
                joint_chains.append(joint_list)

            constraint = mod_dict.get("constraint")
            use_joint_names = mod_dict.get("use_joint_names")
            flexi_surface = mod_dict.get("flexi_surface")
            hide_end_ctrl = mod_dict.get("hide_end_ctrl")
            hide_translate = mod_dict.get("hide_translate")
            hide_rotate = mod_dict.get("hide_rotate")
            hide_scale = mod_dict.get("hide_scale")
            display_layer = mod_dict.get("display_layer")

            upper_twist_joints = mod_dict.get("upper_twist_joints", "").split(",")
            upper_twist_joints = [txt.strip() for txt in upper_twist_joints if txt.strip()]
            lower_twist_joints = mod_dict.get("lower_twist_joints", "").split(",")
            lower_twist_joints = [txt.strip() for txt in lower_twist_joints if txt.strip()]
            main_object_names = mod_dict.get("main_object_names", "").split(",")
            main_object_names = [txt.strip() for txt in main_object_names if txt.strip()]
            upper_twist_name = mod_dict.get("upper_twist_name")
            lower_twist_name = mod_dict.get("lower_twist_name")
            foot_locators = mod_dict.get("foot_locators", "").split(",")
            foot_locators = [txt.strip() for txt in foot_locators if txt.strip()]
            invert_toe_wiggle = mod_dict.get("invert_toe_wiggle")
            invert_toe_spin = mod_dict.get("invert_toe_spin")
            invert_foot_lean = mod_dict.get("invert_foot_lean")
            invert_foot_tilt = mod_dict.get("invert_foot_tilt")
            invert_foot_roll = mod_dict.get("invert_foot_roll")
            origin_joint = mod_dict.get("origin_joint", "").split(",")
            origin_joint = [txt.strip() for txt in origin_joint if txt.strip()]
            mid_joints = mod_dict.get("mid_joints", "").split(",")
            mid_joints = [txt.strip() for txt in mid_joints if txt.strip()]
            top_joints = mod_dict.get("top_joints", "").split(",")
            top_joints = [txt.strip() for txt in top_joints if txt.strip()]
            bot_joints = mod_dict.get("bot_joints", "").split(",")
            bot_joints = [txt.strip() for txt in bot_joints if txt.strip()]

            aim_vector = mod_dict.get("aim_vector")
            up_vector = mod_dict.get("up_vector")
            reverse_right_vectors = mod_dict.get("reverse_right_vectors")

            match rig_module:
                case "biped_limb_mod":
                    module_instance = biped_limb_mod.BipedLimbModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                        upper_twist_joints=upper_twist_joints,
                        lower_twist_joints=lower_twist_joints,
                        main_object_names=main_object_names,
                        upper_twist_name=upper_twist_name,
                        lower_twist_name=lower_twist_name,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "biped_leg_mod":
                    module_instance = biped_leg_mod.BipedLegModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                        upper_twist_joints=upper_twist_joints,
                        lower_twist_joints=lower_twist_joints,
                        main_object_names=main_object_names,
                        upper_twist_name=upper_twist_name,
                        lower_twist_name=lower_twist_name,
                        foot_locators=foot_locators,
                        invert_toe_wiggle=invert_toe_wiggle,
                        invert_toe_spin=invert_toe_spin,
                        invert_foot_lean=invert_foot_lean,
                        invert_foot_tilt=invert_foot_tilt,
                        invert_foot_roll=invert_foot_roll,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "fk_control_mod" | "fk_control_blend_mod":
                    kwargs = {
                        "rig_module_name": rig_module_name,
                        "mirror_direction": mirror_direction,
                        "main_joints": main_joints,
                    }
                    kwargs_optional = [
                        ("constraint", constraint),
                        ("use_joint_names", use_joint_names),
                        ("blend_joints", blend_joints),
                        ("hide_translate", hide_translate),
                        ("hide_rotate", hide_rotate),
                        ("hide_scale", hide_scale),
                    ]
                    for key, value in kwargs_optional:
                        if value is not None:
                            kwargs[key] = value

                    module_instance = fk_control_mod.FkControlModule(**kwargs)
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "world_control_mod":
                    module_instance = world_control_mod.WorldControlModule(
                        rig_module_name=rig_module_name,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "fk_chain_mod":
                    module_instance = fk_chain_mod.FkChainModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "fk_ik_single_chain_mod":
                    module_instance = fk_ik_single_chain_mod.FkIkSingleChainModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "fk_ik_spline_chain_mod":
                    module_instance = fk_ik_spline_chain_mod.FkIkSplineChainModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "flexi_surface_ik_chain_mod":
                    module_instance = flexi_surface_ik_chain_mod.FlexiSurfaceIkChainModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        joint_chains=joint_chains,
                        flexi_surface=flexi_surface,
                        hide_end_ctrl=hide_end_ctrl,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "flexi_surface_fk_ctrl_mod":
                    module_instance = flexi_surface_fk_ctrl_mod.FlexiSurfaceFkCtrlModule(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                        flexi_surface=flexi_surface,
                        hide_end_ctrl=hide_end_ctrl,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "eye_aim_mod":
                    module_instance = eye_aim_mod.EyeAimModule(
                        rig_module_name=rig_module_name,
                        main_joints=main_joints,
                        aim_vector=aim_vector,
                        up_vector=up_vector,
                        reverse_right_vectors=reverse_right_vectors,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "piston_mod":
                    module_instance = piston_mod.PistonMod(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        origin_joint=origin_joint,
                        mid_joints=mid_joints,
                        top_joints=top_joints,
                        bot_joints=bot_joints,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case "digitigrade_leg_mod":
                    module_instance = digitigrade_leg_mod.DigitigradeLegMod(
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                        main_object_names=main_object_names,
                        foot_locators=foot_locators,
                        invert_toe_wiggle=invert_toe_wiggle,
                        invert_toe_spin=invert_toe_spin,
                        invert_foot_lean=invert_foot_lean,
                        invert_foot_tilt=invert_foot_tilt,
                        invert_foot_roll=invert_foot_roll,
                    )
                    module_top_group = module_instance.build()
                    top_groups.append(module_top_group)
                    display_layer and objects_display_lyr(module_top_group)

                case _:
                    logger.warning(f"Unknown rig module: {rig_module}")

        except Exception:
            mirr_side = mirror_direction if mirror_direction else ""
            error_msg = f"Error building rig module: {rig_module}, {rig_module_name}, {mirr_side}"
            logger.exception(error_msg)
            raise RuntimeError(error_msg)

    # ---------- create top rig group ----------
    if rig_name:
        main_rig_group = f"{rig_name}_rigGrp"
    else:
        main_rig_group = "main_rigGrp"
    if not cmds.objExists(main_rig_group):
        main_rig_group = cmds.group(empty=True, name=main_rig_group)
    for grp in top_groups:
        if grp and cmds.objExists(grp):
            cmds.parent(grp, main_rig_group)

    # ----- tag controls for parallel evaluation -----
    rig_ctrls = cmds.listRelatives(main_rig_group, allDescendents=True) or []
    rig_ctrls = [
        ctrl
        for ctrl in rig_ctrls
        if cmds.listRelatives(ctrl, shapes=True, type="nurbsCurve")
        and "ctrl" in ctrl.lower()
        and not any(word in ctrl.lower() for word in ("switch", "swch"))
    ]
    cmds.controller(rig_ctrls)
