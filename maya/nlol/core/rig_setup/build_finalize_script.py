from importlib import reload, util
from pathlib import Path

from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_folder_path)

rig_folderpath = rig_folder_path.rig_folderpath
default_finalize_script = rig_folderpath / "finalize_script.py"

logger = get_logger()


def run_finalize_script(finalize_script_filepath: str | Path = default_finalize_script) -> None:
    """Run "finalize_script.py" from rig folder at the end of the rig build.
    For cleanup and adding final touches to rig.
    """
    if Path(finalize_script_filepath).is_file():
        spec = util.spec_from_file_location("finalize_script", finalize_script_filepath)
        finalize_script_module = util.module_from_spec(spec)
        spec.loader.exec_module(finalize_script_module)

        if hasattr(finalize_script_module, "main"):
            finalize_script_module.main()
        else:
            logger.warning(f"Missing main() function: {finalize_script_filepath}")
    else:
        msg = (
            '"finalize_script.py" not in rig folder. Skipping finalize script.\n'
            f'File not found: "{finalize_script_filepath}".'
        )
        logger.info(msg)
