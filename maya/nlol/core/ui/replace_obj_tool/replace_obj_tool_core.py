"""Replace selected objects with another Arnold .ass version."""

import os
from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.core.modeling_tools import basic_layout, export_import_multiple
from nlol.utilities.nlol_maya_logger import get_logger

reload(export_import_multiple)
ExportImportMultiple = export_import_multiple.ExportImportMultiple

logger = get_logger()


def query_first_selection() -> dict:
    """Read the first selected standin and list matching .ass versions.

    Returns:
        status: Short message for the UI.
        versions: Matching .ass paths, sorted by filename.
        current: The standin's .ass path, or None.

    """
    selected = cmds.ls(selection=True) or []
    if not selected:
        return {"status": "Nothing selected.", "versions": [], "current": None}

    shape = _standin_shape(selected[0])
    if not shape:
        return {"status": "Select an Arnold standin.", "versions": [], "current": None}

    raw_path = cmds.getAttr(f"{shape}.dso") or ""
    if not raw_path:
        return {"status": "No .ass path on this standin.", "versions": [], "current": None}

    current = Path(raw_path)
    if not current.parent.is_dir():
        return {"status": f"Folder not found: {current.parent}", "versions": [], "current": current}

    versions = _version_files(current)
    count = len(versions)
    version_word = "version" if count == 1 else "versions"
    status = f"{current.stem}: {count} {version_word}."
    return {"status": status, "versions": versions, "current": current}


def paths_match(left: Path, right: Path) -> bool:
    """True when two paths point at the same file."""
    left_path = os.path.normcase(os.path.normpath(str(left)))
    right_path = os.path.normcase(os.path.normpath(str(right)))
    return left_path == right_path


def replace_selected(ass_path: Path | str) -> None:
    """Import ass_path as a new standin and instance-replace the current selection."""
    if not ass_path:
        logger.warning("Choose a version to load.")
        return

    targets = cmds.ls(selection=True) or []
    if not targets:
        logger.warning("Select objects to replace.")
        return

    cmds.undoInfo(openChunk=True)
    try:
        created = ExportImportMultiple().import_multiple([ass_path], replace_existing=False)
        if not created:
            logger.warning("Could not import the Arnold standin.")
            return

        standin = created[0]
        targets = [obj for obj in targets if obj != standin]
        if not targets:
            logger.warning("Select objects to replace.")
            cmds.delete(standin)
            return

        cmds.select(standin, *targets)
        basic_layout.duplicate_replace(source_as_first_new_target=True)
        object_word = "object" if len(targets) == 1 else "objects"
        logger.info(f"Replaced {len(targets)} {object_word} with {Path(ass_path).stem}.")
    finally:
        cmds.undoInfo(closeChunk=True)


def _standin_shape(node: str) -> str | None:
    """Return the aiStandIn shape for a transform or shape."""
    if cmds.nodeType(node) == "aiStandIn":
        return node
    shapes = cmds.listRelatives(node, shapes=True, type="aiStandIn") or []
    if shapes:
        return shapes[0]
    return None


def _name_token(stem: str) -> str:
    """First underscore piece of a filename. This is the nLol <name> component."""
    return stem.split("_")[0]


def _version_files(ass_path: Path) -> list[Path]:
    """Return .ass files in the same folder that share the first name token."""
    token = _name_token(ass_path.stem)
    matches = []
    for path in ass_path.parent.iterdir():
        if not path.is_file() or path.suffix.lower() != ".ass":
            continue
        if _name_token(path.stem) == token:
            matches.append(path)
    matches.sort(key=lambda path: path.stem.lower())
    return matches
