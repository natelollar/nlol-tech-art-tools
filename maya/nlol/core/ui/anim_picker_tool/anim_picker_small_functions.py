"""Maya selection helpers for the anim picker UI."""

import re
from pathlib import Path

from maya import cmds


def get_maya_selection() -> list[str]:
    """Return currently selected Maya object names."""
    return cmds.ls(selection=True) or []


def _dag_parent(long_path: str) -> str:
    path = str(long_path or "")
    if "|" not in path:
        return ""
    parent = path.rsplit("|", 1)[0]
    return parent if parent else ""


def _path_tokens(long_path: str) -> list[str]:
    return [p for p in str(long_path or "").split("|") if p]


def _transform_children(parent: str) -> list[str]:
    """Direct transform children in Outliner order (shapes excluded)."""
    if parent:
        kids = cmds.listRelatives(parent, children=True, type="transform", fullPath=True)
        return kids or []
    return cmds.ls(assemblies=True, long=True) or []


def _sibling_index(long_path: str) -> int:
    """Child index under the parent (Outliner / listRelatives order)."""
    path = str(long_path or "")
    siblings = _transform_children(_dag_parent(path))
    try:
        return siblings.index(path)
    except ValueError:
        return 0


def _hierarchy_sort_key(long_path: str) -> tuple:
    """Outliner order key: sibling index at every level of the DAG path."""
    tokens = _path_tokens(long_path)
    key: list[int] = []
    for i in range(len(tokens)):
        partial = "|" + "|".join(tokens[: i + 1])
        key.append(_sibling_index(partial))
    return tuple(key)


def _natural_leaf_key(long_path: str) -> list:
    """Natural-sort key for the leaf name (fk_2 before fk_10)."""
    leaf = _path_tokens(long_path)[-1] if _path_tokens(long_path) else long_path
    leaf = leaf.rsplit(":", 1)[-1]
    parts = re.split(r"(\d+)", leaf)
    key = []
    for part in parts:
        if not part:
            continue
        if part.isdigit():
            key.append((0, int(part)))
        else:
            key.append((1, part.lower()))
    return key


def has_obvious_hierarchy(nodes: list[str]) -> bool:
    """True when selection shares one top-level assembly / branch.

    Covers siblings, FK chains, and per-segment groups under one tentacle/rig.
    """
    long_names = cmds.ls(nodes, long=True) or []
    if len(long_names) < 2:
        return False
    roots = set()
    for path in long_names:
        tokens = _path_tokens(path)
        if tokens:
            roots.add(tokens[0])
    # Same top assembly (e.g. all under the character/rig root).
    return len(roots) == 1


def order_by_hierarchy(nodes: list[str]) -> list[str]:
    """Return nodes in Outliner / DAG order (then natural leaf name).

    Works when each ctrl lives under its own segment group — not only when they
    share the same immediate parent. Preserves original names from ``nodes``.
    """
    if not nodes:
        return []
    if len(nodes) == 1:
        return list(nodes)

    long_names = cmds.ls(nodes, long=True) or []
    if not long_names:
        return list(nodes)

    long_to_orig: dict[str, str] = {}
    for name in nodes:
        longs = cmds.ls(name, long=True) or []
        if longs and longs[0] not in long_to_orig:
            long_to_orig[longs[0]] = name

    ordered_long = sorted(
        long_names,
        key=lambda p: (_hierarchy_sort_key(p), _natural_leaf_key(p)),
    )
    return [long_to_orig.get(n, n) for n in ordered_long]


def selection_for_add_buttons(nodes: list[str] | None = None) -> list[str]:
    """Selection for Add Selection when Hierarchy Order is on (Outliner order)."""
    sel = list(nodes if nodes is not None else get_maya_selection())
    if len(sel) > 1:
        return order_by_hierarchy(sel)
    return sel


def strip_all_namespaces(node_name: str) -> str:
    """Return the short node name with every namespace prefix removed."""
    name = str(node_name or "")
    if "|" in name:
        # Keep DAG path structure, strip ns from each path token
        parts = []
        for token in name.split("|"):
            parts.append(token.rsplit(":", 1)[-1] if token else token)
        return "|".join(parts)
    return name.rsplit(":", 1)[-1]


# Back-compat alias
strip_namespace = strip_all_namespaces


def short_node_name(node_name: str) -> str:
    """Leaf node name without namespace or DAG parents (for button rename labels)."""
    name = strip_all_namespaces(node_name)
    if "|" in name:
        name = name.rsplit("|", 1)[-1]
    return name


def strip_rig_namespace(node_name: str, namespace: str = "") -> str:
    """Remove only the Rig Context namespace prefix; keep nested import namespaces.

    Example with namespace ``cultist``:
    ``cultist:tubeClaw_left_rig:claw_ctrl`` → ``tubeClaw_left_rig:claw_ctrl``
    """
    name = str(node_name or "")
    ns = str(namespace or "").strip().rstrip(":")
    if not name or not ns:
        return name

    prefix = f"{ns}:"

    def strip_token(token: str) -> str:
        if token and token.startswith(prefix):
            return token[len(prefix) :]
        return token

    if "|" in name:
        return "|".join(strip_token(token) for token in name.split("|"))
    return strip_token(name)


def apply_rig_namespace(node_name: str, namespace: str = "") -> str:
    """Prefix the Rig Context namespace; preserve nested import namespaces.

    Example with namespace ``cultist``:
    ``tubeClaw_left_rig:claw_ctrl`` → ``cultist:tubeClaw_left_rig:claw_ctrl``
    """
    name = str(node_name or "")
    ns = str(namespace or "").strip().rstrip(":")
    if not name or not ns:
        return name

    prefix = f"{ns}:"

    def apply_token(token: str) -> str:
        if not token or token.startswith(prefix):
            return token
        return f"{prefix}{token}"

    if "|" in name:
        return "|".join(apply_token(token) for token in name.split("|"))
    return apply_token(name)


def strip_namespaces(names: list[str] | None, namespace: str = "") -> list[str]:
    """Strip only the Rig Context ``namespace`` from names (deduped, order preserved).

    Nested namespaces (imported sub-rigs) are kept. When ``namespace`` is empty,
    names are stored unchanged.
    """
    return combine_targets([strip_rig_namespace(n, namespace) for n in (names or [])])


def apply_namespaces(names: list[str] | None, namespace: str = "") -> list[str]:
    """Apply the Rig Context namespace to stored target names at select time."""
    return [apply_rig_namespace(n, namespace) for n in (names or [])]


def list_scene_namespaces() -> list[str]:
    """Return non-UI Maya namespaces currently in the scene (no leading colon)."""
    try:
        namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True) or []
    except RuntimeError:
        return []
    skip = {"UI", "shared"}
    cleaned = []
    for ns in namespaces:
        name = str(ns).lstrip(":")
        if not name or name in skip:
            continue
        cleaned.append(name)
    return sorted(set(cleaned), key=str.lower)


def guess_namespace_for_rig(rig_name: str, namespaces: list[str] | None = None) -> str:
    """Pick a scene namespace that best matches the rig context name."""
    namespaces = list(namespaces if namespaces is not None else list_scene_namespaces())
    if not namespaces:
        return ""
    rig = str(rig_name or "").strip().lower()
    if not rig:
        return ""
    for ns in namespaces:
        if ns.lower() == rig:
            return ns
    for ns in namespaces:
        if ns.lower().startswith(rig) or rig.startswith(ns.lower()):
            return ns
    for ns in namespaces:
        if rig in ns.lower() or ns.lower() in rig:
            return ns
    return ""


def combine_targets(*target_lists: list[str]) -> list[str]:
    """Merge target lists, preserving order and removing duplicates."""
    combined: list[str] = []
    seen: set[str] = set()
    for targets in target_lists:
        for name in targets or []:
            if name in seen:
                continue
            seen.add(name)
            combined.append(name)
    return combined


def select_picker_targets(
    targets: list[str] | None,
    label: str = "",
    *,
    namespace: str = "",
) -> None:
    """Select Maya nodes assigned to picker button(s).

    Targets keep nested import namespaces; only the Rig Context ``namespace``
    is stripped on assign and re-applied here at select time.
    """
    targets = apply_namespaces(list(targets or []), namespace)
    if not targets:
        cmds.select(clear=True)
        name = label or "button"
        print(f"[AnimPicker] '{name}' — no targets to select")
        return

    existing = [t for t in targets if cmds.objExists(t)]
    missing = [t for t in targets if t not in existing]
    if missing:
        print(f"[AnimPicker] missing targets: {missing}")
    if not existing:
        cmds.select(clear=True)
        print(f"[AnimPicker] '{label}' has no valid targets in the scene")
        return

    cmds.select(existing, replace=True)
    print(f"[AnimPicker] selected ({len(existing)}): {existing}")


def clear_selection() -> None:
    """Clear the current Maya selection."""
    cmds.select(clear=True)
    print("[AnimPicker] clear_selection()")


def open_maya_file(filepath: Path | str | None) -> bool:
    """Confirm and open a Maya file, replacing the current scene.

    Returns True if the file was opened.
    """
    if filepath is None:
        print("[AnimPicker] No rig file path — select a Rig Context")
        return False
    path = Path(filepath)
    if not path.is_file():
        print(f"[AnimPicker] File not found: {path}")
        return False

    yes_string = "Yes"
    no_string = "No"
    dialog_result = cmds.confirmDialog(
        title="Confirm",
        message=f"Open file? This will replace the current scene.\n\n{path.name}",
        button=[yes_string, no_string],
        defaultButton=yes_string,
        cancelButton=no_string,
        dismissString=no_string,
        bgc=(0.2, 0.2, 0.2),
    )
    if dialog_result == no_string:
        print("[AnimPicker] Open file cancelled.")
        return False

    cmds.file(
        path.as_posix(),
        open=True,
        force=True,
        ignoreVersion=True,
        options="v=0;",
    )
    print(f"[AnimPicker] Opened: {path}")
    return True


def print_selection() -> None:
    """Print currently selected objects to the Maya console."""
    selected = get_maya_selection()
    print(f"[AnimPicker] selection ({len(selected)}): {selected}")


def format_targets_summary(targets: list[str] | None, max_names: int = 3) -> str:
    """Short status string for assigned targets."""
    targets = list(targets or [])
    if not targets:
        return "Targets: (none)"
    if len(targets) <= max_names:
        return f"Targets ({len(targets)}): {', '.join(targets)}"
    shown = ", ".join(targets[:max_names])
    return f"Targets ({len(targets)}): {shown}, ..."


def replace_in_targets(
    targets: list[str] | None,
    find: str,
    replace: str,
) -> tuple[list[str], int]:
    """Replace substring in each target name. Returns (new_targets, changed_count)."""
    find_text = str(find or "")
    replace_text = str(replace or "")
    if not find_text:
        return list(targets or []), 0
    updated: list[str] = []
    changed = 0
    for name in targets or []:
        new_name = str(name).replace(find_text, replace_text)
        if new_name != name:
            changed += 1
        updated.append(new_name)
    return updated, changed
