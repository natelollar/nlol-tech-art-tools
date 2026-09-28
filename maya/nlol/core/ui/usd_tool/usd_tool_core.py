"""USD tool actions: save MaterialX, refresh viewports, and duplicate onto Maya objects."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from pxr import Sdf, Usd, UsdShade

from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()

_VALUE_EPSILON = 1e-5

_TUPLE_TYPES = {
    "color3": "Color3",
    "color4": "Color4",
    "vector2": "Vector2",
    "vector3": "Vector3",
    "vector4": "Vector4",
    "float2": "Vector2",
    "float3": "Vector3",
    "float4": "Vector4",
}


def save_selected_mtlx() -> list[str]:
    """Save MaterialX input edits for each selected USD material.

    Returns:
        Change-log lines. Empty when nothing was written.
    """
    materials = _selected_materials()
    if not materials:
        logger.warning("Select a referenced MaterialX material.")
        return []

    changelog = []
    for material in materials:
        changelog.extend(save_material_prim(material))
    return changelog


def refresh_usd_scenes() -> None:
    """Redraw every Maya USD proxy, including materials and textures."""
    import maya.cmds as cmds

    proxies = cmds.ls(type="mayaUsdProxyShape", long=True) or []
    for proxy in proxies:
        complexity = proxy + ".complexity"
        if cmds.attributeQuery("complexity", node=proxy, exists=True):
            value = cmds.getAttr(complexity)
            cmds.setAttr(complexity, 0.0 if value > 0.0 else 1.0)
            cmds.setAttr(complexity, value)

        for flag in ("visibility", "castsShadows", "receiveShadows"):
            plug = proxy + "." + flag
            if cmds.attributeQuery(flag, node=proxy, exists=True):
                current = cmds.getAttr(plug)
                cmds.setAttr(plug, current)

    cmds.ogs(reset=True)
    cmds.refresh(force=True)
    scene_word = "scene" if len(proxies) == 1 else "scenes"
    logger.info(f"Refreshed {len(proxies)} USD {scene_word}.")


def duplicate_usd_to_maya_objects() -> None:
    """Duplicate one selected USD Xform onto each selected Maya transform.

    Copies translate, rotate, and scale. Maya objects stay in the scene.
    """
    import maya.cmds as cmds

    usd_path, maya_targets = _usd_source_and_maya_targets()
    if not usd_path:
        return

    created = 0
    cmds.undoInfo(openChunk=True)
    try:
        for target in maya_targets:
            duplicated = cmds.duplicate(usd_path, returnRootsOnly=True) or []
            if not duplicated:
                logger.warning(f"Could not duplicate USD object for {target}.")
                continue
            _match_usd_to_maya(duplicated[0], target)
            created += 1
    finally:
        cmds.undoInfo(closeChunk=True)

    object_word = "object" if created == 1 else "objects"
    logger.info(f"Duplicated USD object onto {created} Maya {object_word}.")


def save_material_prim(material_prim, dry_run: bool = False) -> list[str]:
    """Diff one material prim against its source ``.mtlx`` and write value changes.

    Args:
        material_prim: ``Usd.Prim`` for the material, or a prim under it.
        dry_run: Log the diff and skip the file write.

    Returns:
        Change-log lines.
    """
    material = _enclosing_material(material_prim)
    if material is None:
        logger.warning("Select a referenced MaterialX material.")
        return []

    mtlx_path = _mtlx_path_for_prim(material)
    if not mtlx_path:
        logger.warning(f"No MaterialX source layer on {material.GetPath()}.")
        return []

    loaded = _read_mtlx(mtlx_path)
    if loaded is None:
        return []
    mx, document, stdlib = loaded

    changes = _collect_changes(mx, document, stdlib, material)
    if not changes:
        logger.info(f"No MaterialX input changes to save for {material.GetPath()}.")
        return []

    changelog = [_format_change(change) for change in changes]
    for line in changelog:
        logger.info(line)

    if dry_run:
        logger.info(f"Dry run. {mtlx_path} was not modified.")
        return changelog

    if not os.access(mtlx_path, os.W_OK):
        logger.error(f"MaterialX file is read-only: {mtlx_path}")
        return changelog

    backup_path = _backup_mtlx(mtlx_path)
    logger.info(f"MaterialX backup: {backup_path}")
    _apply_changes(changes)
    mx.writeToXmlFile(document, mtlx_path)
    logger.info(f"Saved MaterialX source: {mtlx_path}")
    return changelog


def _read_mtlx(mtlx_path):
    """Read the source file. Nodedefs stay in a second document so they are not saved."""
    try:
        import MaterialX as mx
    except ImportError:
        logger.error("MaterialX Python module is not available.")
        return None

    document = mx.createDocument()
    mx.readFromXmlFile(document, mtlx_path)
    stdlib = mx.createDocument()
    mx.loadLibraries(mx.getDefaultDataLibraryFolders(), mx.getDefaultDataSearchPath(), stdlib)
    return mx, document, stdlib


def _match_usd_to_maya(usd_path, maya_target) -> None:
    """Copy a Maya object's world translate, rotate, and scale onto a USD prim.

    ``matchTransform`` does not accept USD paths, so the world matrix is written
    through UFE in the prim's parent space.
    """
    import maya.api.OpenMaya as om
    import maya.cmds as cmds
    import maya.internal.ufeSupport.ufeCmdWrapper as ufe_cmd
    import ufe

    scene_item = ufe.Hierarchy.createItem(ufe.PathString.path(usd_path))
    transform = ufe.Transform3d.transform3d(scene_item)
    maya_world = om.MMatrix(cmds.xform(maya_target, query=True, matrix=True, worldSpace=True))
    parent_world = _mmatrix_from_ufe(transform.exclusiveMatrix())
    local = _ufe_matrix(parent_world.inverse() * maya_world)
    ufe_cmd.execute(transform.setMatrixCmd(local))


def _mmatrix_from_ufe(matrix):
    """Convert a UFE matrix to a Maya matrix."""
    import maya.api.OpenMaya as om

    flat = [value for row in matrix.matrix for value in row]
    return om.MMatrix(flat)


def _ufe_matrix(matrix):
    """Convert a Maya matrix to a UFE matrix."""
    import ufe

    rows = [[matrix.getElement(row, column) for column in range(4)] for row in range(4)]
    return ufe.Matrix4d(rows)


def _usd_source_and_maya_targets():
    """Split the selection into one USD Xform path and Maya transform targets."""
    import maya.cmds as cmds

    try:
        import mayaUsd.ufe as maya_usd_ufe
    except ImportError:
        logger.error("mayaUsd is not available.")
        return None, []

    usd_items = []
    maya_targets = []
    for item in _selection_paths():
        prim = _prim_from_selection(maya_usd_ufe, item)
        if prim is not None:
            usd_items.append((item, prim))
            continue
        if cmds.objExists(item) and cmds.nodeType(item) == "transform":
            maya_targets.append(item)

    if len(usd_items) != 1 or not maya_targets:
        logger.warning("Select one USD Xform and one or more Maya objects.")
        return None, []

    usd_path, prim = usd_items[0]
    if prim.GetTypeName() != "Xform":
        logger.warning(f"USD selection must be an Xform: {prim.GetPath()}")
        return None, []
    return usd_path, maya_targets


def _selection_paths():
    """Return the current selection, including USD prims."""
    import maya.cmds as cmds

    try:
        return cmds.ls(selection=True, long=True, ufeObjects=True) or []
    except TypeError:
        return cmds.ls(selection=True, long=True) or []


def _prim_from_selection(maya_usd_ufe, item):
    """Return a valid USD prim for a selection path, or None for a Maya node."""
    try:
        prim = maya_usd_ufe.ufePathToPrim(item)
    except Exception:
        return None
    if prim and prim.IsValid():
        return prim
    return None


def _selected_materials():
    """Return unique material prims from the Maya USD selection."""
    import maya.cmds as cmds

    try:
        import mayaUsd.ufe as maya_usd_ufe
    except ImportError:
        logger.error("mayaUsd is not available.")
        return []

    try:
        selection = cmds.ls(selection=True, long=True, ufeObjects=True) or []
    except TypeError:
        selection = cmds.ls(selection=True, long=True) or []

    materials = []
    seen = set()
    for item in selection:
        try:
            prim = maya_usd_ufe.ufePathToPrim(item)
        except Exception:
            logger.warning(f"Could not resolve USD prim from selection: {item}")
            continue
        if not prim or not prim.IsValid():
            continue
        material = _enclosing_material(prim)
        if material is None:
            logger.warning(f"Selection is not a MaterialX material: {prim.GetPath()}")
            continue
        path = material.GetPath()
        if path in seen:
            continue
        seen.add(path)
        materials.append(material)
    return materials


def _enclosing_material(prim):
    """Walk up to the ``UsdShade.Material`` that contains ``prim``."""
    current = prim
    while current and current.IsValid():
        if current.IsA(UsdShade.Material):
            return current
        current = current.GetParent()
    return None


def _mtlx_path_for_prim(prim) -> str | None:
    """Return the filesystem path of the ``.mtlx`` layer on this prim's stack."""
    for spec in prim.GetPrimStack():
        layer = spec.layer
        if layer is None or not _is_mtlx_layer(layer):
            continue
        path = layer.realPath or layer.identifier
        path = path.split(":SDF_FORMAT_ARGS:")[0]
        if path:
            return path
    return None


def _is_mtlx_layer(layer) -> bool:
    """True when ``layer`` is a MaterialX file."""
    identifier = (layer.identifier or "").replace("\\", "/").lower()
    if identifier.endswith(".mtlx"):
        return True
    file_format = layer.GetFileFormat()
    format_id = getattr(file_format, "formatId", None) if file_format else None
    return format_id == "mtlx"


def _iter_document_nodes(document):
    """Yield document-level nodes and nodes inside nodegraphs."""
    yield from document.getNodes()
    for node_graph in document.getNodeGraphs():
        yield from node_graph.getNodes()


def _collect_changes(mx, document, stdlib, material) -> list[dict]:
    """Return value edits on ``material`` that differ from the source document."""
    shader_prims = _descendants_by_name(material)
    changes = []
    for node in _iter_document_nodes(document):
        nodedef = _nodedef_for_node(node, stdlib)
        if nodedef is None:
            logger.warning(f"No nodedef for MaterialX node {node.getName()}.")
            continue
        prims = shader_prims.get(node.getName(), [])
        shader_prim = _prim_with_local_values(prims, nodedef)
        if shader_prim is None:
            continue
        for nd_input in nodedef.getInputs():
            change = _input_change(mx, node, nd_input, shader_prim)
            if change is not None:
                changes.append(change)
    return changes


def _nodedef_for_node(node, stdlib):
    """Look up a nodedef without merging the standard library into the file."""
    nodedef_name = node.getNodeDefString()
    if nodedef_name:
        nodedef = stdlib.getNodeDef(nodedef_name)
        if nodedef:
            return nodedef
    return node.getNodeDef()


def _descendants_by_name(material) -> dict:
    """Map each descendant prim name to the prims that use it."""
    found = {}
    for prim in Usd.PrimRange(material):
        if prim == material:
            continue
        found.setdefault(prim.GetName(), []).append(prim)
    return found


def _prim_with_local_values(prims, nodedef):
    """Prefer the prim that has a non-MaterialX value opinion."""
    if not prims:
        return None
    if len(prims) == 1:
        return prims[0]

    def score(prim):
        count = 0
        for nd_input in nodedef.getInputs():
            attr = _input_attr(prim, nd_input.getName())
            if attr is None or _connected(prim, nd_input.getName()):
                continue
            if _strongest_is_local(attr):
                count += 1
        return count

    return max(prims, key=score)


def _input_change(mx, node, nd_input, shader_prim):
    """Build one change record, or None when the input should stay as it is."""
    name = nd_input.getName()
    mx_type = nd_input.getType()
    mx_input = node.getInput(name)
    if _mtlx_input_is_connection(mx_input):
        return None

    if _connected(shader_prim, name):
        return None

    attr = _input_attr(shader_prim, name)
    if attr is None or not _strongest_is_local(attr):
        return None

    usd_value = attr.Get(Usd.TimeCode.Default())
    if usd_value is None:
        return None

    converted = _usd_to_mx(mx, usd_value, mx_type)
    if converted is None:
        logger.warning(f"Skipped {node.getName()}.{name}: unsupported MaterialX type {mx_type}.")
        return None

    default = nd_input.getValue()
    has_file_value = mx_input is not None and mx_input.getValue() is not None
    file_value = mx_input.getValue() if has_file_value else default

    if _values_equal(converted, file_value):
        return None

    remove = has_file_value and _values_equal(converted, default)
    return {
        "node": node,
        "name": name,
        "mx_type": mx_type,
        "old": file_value if has_file_value else default,
        "new": None if remove else converted,
        "remove": remove,
    }


def _mtlx_input_is_connection(mx_input) -> bool:
    """True when the source input is wired instead of storing a value."""
    if mx_input is None:
        return False
    return bool(mx_input.getNodeName() or mx_input.getInterfaceName() or mx_input.getOutputString())


def _input_attr(prim, name):
    """Return the ``inputs:<name>`` attribute when it exists."""
    attr = prim.GetAttribute(f"inputs:{name}")
    if attr and attr.IsValid():
        return attr
    return None


def _connected(prim, name) -> bool:
    """True when the shader input is connected on the USD prim."""
    shader_input = UsdShade.Shader(prim).GetInput(name)
    if shader_input and shader_input.HasConnectedSource():
        return True
    attr = _input_attr(prim, name)
    return bool(attr and attr.HasAuthoredConnections())


def _strongest_is_local(attr) -> bool:
    """True when the winning opinion is authored outside the ``.mtlx`` layer."""
    stack = attr.GetPropertyStack(Usd.TimeCode.Default())
    if not stack:
        return False
    layer = stack[0].layer
    return layer is not None and not _is_mtlx_layer(layer)


def _usd_to_mx(mx, value, mx_type):
    """Convert a USD value to the MaterialX value ``setInputValue`` expects."""
    if isinstance(value, Sdf.AssetPath):
        value = value.path

    if mx_type == "float":
        return float(value)
    if mx_type == "integer":
        return int(value)
    if mx_type == "boolean":
        return bool(value)
    if mx_type in ("string", "filename", "token"):
        return "" if value is None else str(value)

    ctor_name = _TUPLE_TYPES.get(mx_type)
    if ctor_name is None:
        return None
    components = [float(component) for component in value]
    return getattr(mx, ctor_name)(*components)


def _values_equal(left, right) -> bool:
    """Compare MaterialX and USD values, with a small tolerance for floats."""
    left_n = _normalize_value(left)
    right_n = _normalize_value(right)
    if isinstance(left_n, float) and isinstance(right_n, float):
        return abs(left_n - right_n) <= _VALUE_EPSILON
    if isinstance(left_n, tuple) and isinstance(right_n, tuple):
        if len(left_n) != len(right_n):
            return False
        return all(abs(a - b) <= _VALUE_EPSILON for a, b in zip(left_n, right_n))
    return left_n == right_n


def _normalize_value(value):
    """Flatten MaterialX and USD values to floats, tuples, or strings."""
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return tuple(float(component) for component in value)
    except (TypeError, ValueError):
        return value


def _apply_changes(changes) -> None:
    """Add, update, or remove inputs on the in-memory MaterialX document."""
    for change in changes:
        node = change["node"]
        name = change["name"]
        if change["remove"]:
            node.removeInput(name)
            continue
        node.setInputValue(name, change["new"], change["mx_type"])


def _format_change(change) -> str:
    """One log line for a saved or removed input."""
    old = _format_value(change["old"])
    new = "default" if change["remove"] else _format_value(change["new"])
    node_name = change["node"].getName()
    return f"{node_name}.{change['name']} ({change['mx_type']}): {old} -> {new}"


def _format_value(value) -> str:
    """Short text for a MaterialX value."""
    normalized = _normalize_value(value)
    if normalized is None:
        return "none"
    if isinstance(normalized, float):
        return f"{normalized:g}"
    if isinstance(normalized, tuple):
        return "(" + ", ".join(f"{component:g}" for component in normalized) + ")"
    return str(normalized)


def _backup_mtlx(mtlx_path: str) -> str:
    """Copy the source file to the temp directory before overwriting it."""
    source = Path(mtlx_path)
    backup = Path(tempfile.gettempdir()) / f"{source.stem}_mtlx_backup{source.suffix}"
    shutil.copy2(source, backup)
    return str(backup)
