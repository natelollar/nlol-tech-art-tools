import json
import os
import shutil
import stat
from pathlib import Path

import nlol
from nlol import defaults
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()
# Main RIG folderpaths get added to this json
rig_context_json = Path(defaults.__file__).parent / "rig_context.json"


def check_rig_context_file() -> None:
    """Check if file exists, if not, create from example file."""
    if not rig_context_json.exists():
        src = Path(defaults.__file__).parent / "rig_context_example.json"
        shutil.copy2(src, rig_context_json)
        # remove read-only when copied
        mode = rig_context_json.stat().st_mode
        rig_context_json.chmod(mode | stat.S_IWUSR)

        logger.info(f'Created "rig_context.json": {rig_context_json}')


def set_single_env_var(var_name: str, var_folderpath: str | Path) -> None:
    """Add single environment variable (for Maya session). Skip if exists."""
    folderpath = os.environ.get(var_name, "")
    if not folderpath:
        folderpath = Path(var_folderpath).as_posix()
        os.environ[var_name] = folderpath

        logger.info(f'Set environment variable "{var_name}": {folderpath}')
        folderpath_exists = Path(folderpath).exists()
        logger.debug(f"Path exists? {folderpath_exists}")


def set_environment_variables(force: bool = False) -> None:
    """Add environment variables (for Maya session) from rig context json.

    Args:
        force: Force overwrite of existing environment variables (for Maya session).
            Useful if needing to update environment variables while Maya is open.

    """
    # ----- set env vars from json file
    with open(rig_context_json) as f:
        data = json.load(f)

    # ----- set default env vars
    nlol_folderpath = Path(nlol.__file__).parents[0]
    set_single_env_var("MAYA_NLOL_FOLDERPATH", nlol_folderpath)

    # ----- set custom env vars
    environment_variables = data.get("environment_variables", "")
    if environment_variables:
        for env_var in environment_variables:
            name = env_var["name"]
            if not name:
                continue

            folderpath = Path(
                os.path.expanduser(os.path.expandvars(env_var["folderpath"])),
            ).as_posix()
            env_var_exists = os.environ.get(name, "")

            if force or (not env_var_exists):
                os.environ[name] = folderpath
                logger.info(f'Set environment variable "{name}": {folderpath}')


def rig_folderpath() -> Path | str:
    """Get active RIG folder path from rig context json.
    Currently, expects "${VARIABLE_NAME}" style environment variables.

    Returns:
        Active rig folder path or empty string.

    """
    # -----
    with open(rig_context_json) as f:
        data = json.load(f)

    for rig in data["rigs"]:
        if rig["active"]:
            resolved = Path(os.path.expandvars(rig["folderpath"]))
            if "$" in str(resolved):
                msg = f"Unresolved environment variable in path: {resolved}"
                logger.error(msg)
                raise RuntimeError(msg)
            if not Path(resolved).exists():
                msg = f"RIG folder doesn't exist: {resolved}"
                logger.error(msg)
                raise FileNotFoundError(msg)
            return resolved

    # -----
    msg = '---------- No active rig folder. ----------\nSet one in "nlol/defaults/rig_context.json"'
    logger.info(msg)

    return ""


def rig_folderpath_log() -> Path | str:
    """Get active folder path. Show path in console with logger. Check if exists.

    Returns:
        Active rig folder path or empty string.

    """
    rig_fp = rig_folderpath()
    active_rig_folderpath = rig_fp.as_posix()
    logger.info(f"{active_rig_folderpath = }")
    folderpath_exists = Path(active_rig_folderpath).exists()
    logger.debug(f"Path exists? {folderpath_exists}")

    return rig_fp
