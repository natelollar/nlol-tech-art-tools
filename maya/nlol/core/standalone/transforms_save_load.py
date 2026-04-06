"""transforms_save_load.py

Save/load current transforms for selected objects.
"""

import json
from pathlib import Path

from maya import cmds
from nlol import defaults
from nlol.utilities.nlol_maya_logger import get_logger

default_folderpath = Path(defaults.__file__).parent
save_filepath = default_folderpath / "other_control_transforms.json"

logger = get_logger()


def save_transforms():
    """Save transforms of selected objects to json file."""
    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning("Nothing selected! Select controls first.")
        return

    data = {}
    for obj in selected:
        data[obj] = {
            "translateX": cmds.getAttr(f"{obj}.translateX"),
            "translateY": cmds.getAttr(f"{obj}.translateY"),
            "translateZ": cmds.getAttr(f"{obj}.translateZ"),
            "rotateX": cmds.getAttr(f"{obj}.rotateX"),
            "rotateY": cmds.getAttr(f"{obj}.rotateY"),
            "rotateZ": cmds.getAttr(f"{obj}.rotateZ"),
            "scaleX": cmds.getAttr(f"{obj}.scaleX"),
            "scaleY": cmds.getAttr(f"{obj}.scaleY"),
            "scaleZ": cmds.getAttr(f"{obj}.scaleZ"),
        }

    with open(save_filepath, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"File saved to...  {save_filepath}")


def load_transforms():
    """Load transforms to selected objects (in save order)."""
    if not save_filepath.exists():
        cmds.warning(f"File not found: {save_filepath}")
        return

    with open(save_filepath, encoding="utf-8") as f:
        data = json.load(f)

    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning("Nothing selected! Select same number/order of controls.")
        return

    # apply to selected objects in order they were saved
    saved_objs = list(data.keys())
    for i, obj in enumerate(selected):
        if i >= len(saved_objs):
            break  # more selected than saved, stop

        saved_name = saved_objs[i]  # original name doesn't matter
        d = data[saved_name]

        try:
            cmds.setAttr(f"{obj}.translateX", d["translateX"])
            cmds.setAttr(f"{obj}.translateY", d["translateY"])
            cmds.setAttr(f"{obj}.translateZ", d["translateZ"])

            cmds.setAttr(f"{obj}.rotateX", d["rotateX"])
            cmds.setAttr(f"{obj}.rotateY", d["rotateY"])
            cmds.setAttr(f"{obj}.rotateZ", d["rotateZ"])

            cmds.setAttr(f"{obj}.scaleX", d["scaleX"])
            cmds.setAttr(f"{obj}.scaleY", d["scaleY"])
            cmds.setAttr(f"{obj}.scaleZ", d["scaleZ"])

        except Exception as e:
            print(f"Failed to set {obj}: {e}")

    logger.debug(f"Transforms loaded from: {save_filepath}")
