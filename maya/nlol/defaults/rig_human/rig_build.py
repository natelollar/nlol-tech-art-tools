from importlib import reload
from pathlib import Path

import nlol
from maya import cmds
from nlol.scripts.rig_modules import build_rig_modules

reload(build_rig_modules)

nlol_folderpath = Path(nlol.__file__).parent
rig_data_filepath = nlol_folderpath / "defaults" / "rig_human" / "rig_object_data.json"
rig_helpers_filepath = nlol_folderpath / "defaults" / "rig_human" / "rig_helpers.ma"


def run_rig_build():
    """Build entire rig."""
    # ----------
    cmds.file(rig_helpers_filepath, i=True)
    # ----------
    build_rig_modules.build_modules(rig_data_filepath)
    # ----------
    # apply parent spaces
    # ...

