import os  # noqa: F401
from pathlib import Path

from nlol import defaults # noqa: F401

rig_folderpath = Path(defaults.__file__).parent / "rig_unreal"
# rig_folderpath = Path(os.environ.get("NLOL_RIG_FOLDERPATH"))

# rig_folderpath = Path(defaults.__file__).parent / "standalone_modules" / "eye_aim_mod"
# rig_folderpath = Path(defaults.__file__).parent / "standalone_modules" / "fk_control_blend_mod"
# rig_folderpath = Path(defaults.__file__).parent / "standalone_modules" / "flexi_surface_fk_ctrl_mod"
# rig_folderpath = Path(defaults.__file__).parent / "standalone_modules" / "fk_ik_spline_chain_mod"
# rig_folderpath = Path(defaults.__file__).parent / "standalone_modules" / "flexi_to_cloth_v1"
# rig_folderpath = Path(defaults.__file__).parent / "standalone_modules" / "flexi_to_cloth_v2"
