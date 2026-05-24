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

AUX_ATTRS = (
    "fkIkBlend",
    "parentSpaces",
    "pointSpace",
    "baseParent",
    "translateSpace",
    "rotateSpace",
    "scaleSpace",
)


def save_transforms() -> None:
    """Save transforms of selected objects to json file."""
    selected = cmds.ls(selection=True)
    if not selected:
        cmds.warning("Nothing selected! Select controls first.")
        return

    data = {}
    for obj in selected:
        data[obj] = {}
        for attr in AUX_ATTRS:
            if cmds.objExists(f"{obj}.{attr}"):
                data[obj][attr] = cmds.getAttr(f"{obj}.{attr}")
        for attr in ("translate", "rotate", "scale"):
            for axis in "XYZ":
                if cmds.objExists(f"{obj}.{attr}{axis}"):
                    data[obj][f"{attr}{axis}"] = cmds.getAttr(f"{obj}.{attr}{axis}")

    with open(save_filepath, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"File saved to...  {save_filepath}")


def load_transforms() -> None:
    """Load transforms to selected objects. No selection required."""
    if not save_filepath.exists():
        cmds.warning(f"File not found: {save_filepath}")
        return

    with open(save_filepath, encoding="utf-8") as f:
        data = json.load(f)

    for obj, obj_transforms in data.items():
        if not cmds.objExists(obj):
            logger.info(f"Object not found in scene: {obj}")
            continue
        for attr in AUX_ATTRS:
            if attr in obj_transforms:
                cmds.setAttr(f"{obj}.{attr}", obj_transforms[attr])
        for attr in ("translate", "rotate", "scale"):
            for axis in "XYZ":
                if f"{attr}{axis}" in obj_transforms:
                    try:
                        cmds.setAttr(f"{obj}.{attr}{axis}", obj_transforms[f"{attr}{axis}"])
                    except Exception as e:
                        logger.debug(f"Failed to set {obj}.{attr}{axis}: {e}")

    logger.info(f"Transforms loaded from: {save_filepath}")


def load_selected_transforms_same_order() -> None:
    """Load transforms to selected objects (in save order).
    Save order selection required.
    Useful for copying transforms from one object to another,
    as a copy and paste transforms function.
    """
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

        saved_name = saved_objs[i]  # used as dict key only, not applied to scene
        d = data[saved_name]

        for attr in AUX_ATTRS:
            if attr in d:
                if cmds.objExists(f"{obj}.{attr}"):
                    cmds.setAttr(f"{obj}.{attr}", d[attr])

        for attr in ("translate", "rotate", "scale"):
            for axis in "XYZ":
                key = f"{attr}{axis}"
                if key in d:
                    try:
                        cmds.setAttr(f"{obj}.{attr}{axis}", d[key])
                    except Exception as e:
                        logger.debug(f"Failed to set {obj}.{attr}{axis}: {e}")

    logger.info(f"Transforms loaded from: {save_filepath}")
