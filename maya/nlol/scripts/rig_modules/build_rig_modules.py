"""Run through rig modules in rig selection json file.
Take in module args. Run the modules to build the different rig parts.
"""

import json
from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger
from nlol.scripts.rig_modules import biped_leg_mod, fk_control_mod

reload(biped_leg_mod)
reload(fk_control_mod)


def build_modules(rig_data_filepath: str | Path):
    """Cycle through rig module list and build them.
    Also, create top rig group and tag controllers for parallel evalution.

    Args:
        rig_data_filepath: Json filepath with name and joint data for rig.

    """
    logger = get_logger()

    # ----- query json file list -----
    with open(rig_data_filepath, encoding="utf-8") as f:
        rig_object_data = json.load(f)

    # ----------
    top_groups = []
    for mod_dict in rig_object_data:
        try:
            rig_module = mod_dict["rig_module"]
            rig_module_name = mod_dict["rig_module_name"]
            mirror_direction = mod_dict.get("mirror_direction")

            main_joints = mod_dict["joints"].split(",")
            main_joints = [str.strip() for str in main_joints]
            upper_twist_joints = mod_dict.get("upper_twist_joints", "").split(",")
            upper_twist_joints = [str.strip() for str in upper_twist_joints]
            lower_twist_joints = mod_dict.get("lower_twist_joints", "").split(",")
            lower_twist_joints = [str.strip() for str in lower_twist_joints]

            match rig_module:
                case "biped_leg_mod":
                    module_instance = biped_leg_mod.BipedLegModule(
                        rig_data_filepath=rig_data_filepath,
                        rig_module="biped_leg_mod",
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                        upper_twist_joints=upper_twist_joints,
                        lower_twist_joints=lower_twist_joints,
                    )
                    module_top_group = module_instance.build_leg_module()
                    top_groups.append(module_top_group)
                case "fk_control_mod":
                    module_instance = fk_control_mod.FkControlModule(
                        rig_data_filepath=rig_data_filepath,
                        rig_module="fk_control_mod",
                        rig_module_name=rig_module_name,
                        mirror_direction=mirror_direction,
                        main_joints=main_joints,
                    )
                    module_top_group = module_instance.create_fk_ctrl()
                    top_groups.append(module_top_group)
                case _:
                    logger.warning(f"Unknown rig module: {rig_module}")
        except Exception:
            mirr_side = f"_{mirror_direction}" if mirror_direction else ""
            error_msg = f"Error building rig module: {rig_module}{mirr_side}"
            logger.exception(error_msg)
            raise

    # ----------
    main_rig_group = cmds.group(empty=True, name="rig_allGrp")
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

    # ----------
    cmds.select(clear=True)
    cmds.flushUndo()  # file import restricts undo. use delete rig script to undo.
