import os  # noqa: F401
from pathlib import Path

from nlol import defaults # noqa: F401

rig_folderpath = Path(defaults.__file__).parent / "rig_unreal"
# rig_folderpath = Path(os.environ.get("NLOL_RIG_FOLDERPATH"))

rig_standalone_folderpath = Path(defaults.__file__).parent / "standalone_modules"
# rig_folderpath = rig_standalone_folderpath / "eye_aim_mod"
# rig_folderpath = rig_standalone_folderpath / "fk_control_blend_mod"
# rig_folderpath = rig_standalone_folderpath / "flexi_surface_fk_ctrl_mod"
# rig_folderpath = rig_standalone_folderpath / "fk_ik_spline_chain_mod"
# rig_folderpath = rig_standalone_folderpath / "flexi_to_cloth_v1"
# rig_folderpath = rig_standalone_folderpath / "flexi_to_cloth_v2"
# rig_folderpath = rig_standalone_folderpath / "digitigrade_leg_mod"
# rig_folderpath = rig_standalone_folderpath / "wyvern_wing"
# rig_folderpath = rig_standalone_folderpath / "tentacle_mod"
# rig_folderpath = rig_standalone_folderpath / "piston_mod"
