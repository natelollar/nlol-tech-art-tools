from importlib import util
from pathlib import Path

from nlol.defaults.rig_folder_path import rig_folderpath
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def run_finalize_script(finalize_script_filepath: str | Path | None = None) -> None:
    """Run "finalize_script.py" from rig folder at the end of the rig build.
    For cleanup and adding final touches to rig.
    """
    finalize_script_filepath = finalize_script_filepath or (rig_folderpath() / "finalize_script.py")

    if Path(finalize_script_filepath).is_file():
        spec = util.spec_from_file_location("finalize_script", finalize_script_filepath)
        finalize_script_module = util.module_from_spec(spec)
        spec.loader.exec_module(finalize_script_module)

        if hasattr(finalize_script_module, "main"):
            finalize_script_module.main()
        else:
            logger.warning(f"Missing main() function: {finalize_script_filepath}")
    else:
        msg = '"finalize_script.py" not in rig folder. Skipping finalize script...\n'
        logger.info(msg)
        msg = f'File not found: "{finalize_script_filepath}".'
        logger.debug(msg)
