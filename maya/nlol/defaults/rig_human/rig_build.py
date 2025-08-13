from importlib import reload
from pathlib import Path

import nlol
from maya import cmds
from nlol.scripts.rig_tools import build_rig_modules, parent_space_switching

reload(build_rig_modules)
reload(parent_space_switching)

nlol_folderpath = Path(nlol.__file__).parent
rig_data_filepath = nlol_folderpath / "defaults" / "rig_human" / "rig_object_data.toml"
rig_ps_filepath = nlol_folderpath / "defaults" / "rig_human" / "rig_parent_spaces.toml"
rig_helpers_filepath = nlol_folderpath / "defaults" / "rig_human" / "rig_helpers.ma"


def run_rig_build():
    """Build entire rig."""
    # ----------
    cmds.file(rig_helpers_filepath, i=True)
    # ----------
    build_rig_modules.build_modules(rig_data_filepath)
    # ----------
    parent_space_switching.setup_parent_spaces(rig_ps_filepath)

