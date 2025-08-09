"""Utilites for installing and uninstalling nlol Maya tools."""

import os
from pathlib import Path

from maya import cmds


def update_project_env_path(project_path: str | Path, install: bool) -> None:
    """Add nlol maya project directory path to MAYA_MODULE_PATH variable in Maya.env.
    Maya.env path example:  "C:/Users/<user>/Documents/maya/<maya_version>/Maya.env"

    Args:
        project_path: Python project path to append to Maya environment file "Maya.env".
        install: Whether to add or remove Python project path from "Maya.env".
            True will add. False will remove.

    """
    maya_home_folder = os.getenv("MAYA_APP_DIR", Path.home() / "maya")
    maya_version = cmds.about(version=True)
    maya_env_filepath = Path(maya_home_folder) / maya_version / "Maya.env"
    nlol_path = project_path
    nlol_path_str = str(nlol_path)
    seperator = ";"

    file_lines = []
    module_path_index = None
    if maya_env_filepath.exists():
        with open(maya_env_filepath, encoding="utf-8") as file:
            file_lines = file.readlines()
        file_lines = [line.strip() for line in file_lines]

    for i, line in enumerate(file_lines):
        if line.startswith("MAYA_MODULE_PATH"):
            module_path_index = i

    if module_path_index is not None:
        current_paths = file_lines[module_path_index].split("=", 1)[1].split(seperator)

        # standardize path style then convert to string for comparison
        # remove spaces and semicolons at start and end of paths
        # remove empty paths
        refined_paths = [
            str(Path(py_path)).strip(f" {seperator}")
            for py_path in current_paths
            if py_path and py_path.strip()
        ]

        if (nlol_path_str not in refined_paths) if install else (nlol_path_str in refined_paths):
            if install:  # add project folder path
                refined_paths.append(nlol_path_str)
            else:  # remove project folder path
                refined_paths = [py_path for py_path in refined_paths if py_path != nlol_path_str]
            joined_paths = seperator.join(str(py_path) for py_path in refined_paths)
            file_lines[module_path_index] = f"MAYA_MODULE_PATH = {joined_paths}"
        elif install:
            print(f"Project path already in Maya.env MAYA_MODULE_PATH: {nlol_path_str}")
        else:
            print(f"Project path not in Maya.env MAYA_MODULE_PATH: {nlol_path_str}")
    elif install:
        file_lines.append(f"MAYA_MODULE_PATH = {nlol_path_str}")
    else:
        pass

    try:
        with open(maya_env_filepath, "w", encoding="utf-8") as file:
            file.write("\n".join(file_lines) + "\n")
        if install:
            print(f'Updated MAYA_MODULE_PATH: "{nlol_path_str}" in "{maya_env_filepath}"')
        else:
            print(f'Removed MAYA_MODULE_PATH: "{nlol_path_str}" in "{maya_env_filepath}"')
    except Exception:
        print(f"Error writing to: {maya_env_filepath}")
        raise
