"""Anim picker data model and JSON save/load."""

from __future__ import annotations

import json
import os
import uuid
from copy import deepcopy
from pathlib import Path

from nlol import defaults

PICKER_SUBFOLDER = "anim_picker"
DEFAULT_PICKER_FILENAME = "anim_picker.json"
RIG_CONTEXT_JSON = Path(defaults.__file__).parent / "rig_context.json"

DEFAULT_GRID_SIZE = 20
DEFAULT_BUTTON_W = 6
DEFAULT_BUTTON_H = 2
DEFAULT_BUTTON_COLOR = [80, 120, 170]
# Muted mid-tone presets for quick button coloring (readable with light labels).
MUTED_BUTTON_COLORS = [
    [80, 120, 170],   # slate blue (default)
    [90, 110, 130],   # steel
    [70, 125, 125],   # teal
    [75, 130, 100],   # sea green
    [140, 125, 65],   # mustard
    [155, 105, 70],   # soft orange
    [145, 85, 75],    # terra
    [140, 80, 100],   # rose
    [105, 90, 145],   # purple
    [85, 90, 95],     # charcoal
]
DEFAULT_CORNER_RADIUS = 0
# High enough for large square buttons to reach a full circle (paint clamps to half min side).
MAX_CORNER_RADIUS = 200
DEFAULT_FONT_SIZE = 11
MIN_FONT_SIZE = 6
MAX_FONT_SIZE = 48
DEFAULT_FONT_BOLD = False
DEFAULT_FONT_FAMILY = "Arial"
DEFAULT_TEXT_DARK = False
TEXT_COLOR_LIGHT = [230, 230, 230]
TEXT_COLOR_DARK = [20, 20, 20]
DEFAULT_BACKGROUND_WIDTH = 800.0
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def copy_muted_button_colors() -> list[list[int]]:
    """Return a fresh copy of the default muted preset palette."""
    return [list(rgb) for rgb in MUTED_BUTTON_COLORS]


def serialize_muted_colors(colors: list[list[int]] | None) -> str:
    """Encode muted preset RGB lists for QSettings (e.g. ``80,120,170;90,110,130``)."""
    parts = []
    for rgb in colors or []:
        if len(rgb) < 3:
            continue
        parts.append(f"{int(rgb[0])},{int(rgb[1])},{int(rgb[2])}")
    return ";".join(parts)


def parse_muted_colors(text: str | None) -> list[list[int]] | None:
    """Parse serialized muted colors. Returns None if invalid / wrong length."""
    raw = str(text or "").strip()
    if not raw:
        return None
    colors: list[list[int]] = []
    for part in raw.split(";"):
        part = part.strip()
        if not part:
            continue
        tokens = [t.strip() for t in part.split(",")]
        if len(tokens) != 3:
            return None
        try:
            rgb = [max(0, min(255, int(t))) for t in tokens]
        except ValueError:
            return None
        colors.append(rgb)
    if len(colors) != len(MUTED_BUTTON_COLORS):
        return None
    return colors


def default_view() -> dict:
    """Default canvas pan/zoom (centered on grid origin)."""
    return {
        "center_x": 0.0,
        "center_y": 0.0,
        "scale": 1.0,
    }


def normalize_view(view: dict | None) -> dict:
    """Sanitize view dict from JSON."""
    data = default_view()
    if not isinstance(view, dict):
        return data
    try:
        scale = float(view.get("scale", 1.0))
    except (TypeError, ValueError):
        scale = 1.0
    if scale <= 0.0:
        scale = 1.0
    try:
        data["center_x"] = float(view.get("center_x", 0.0))
        data["center_y"] = float(view.get("center_y", 0.0))
    except (TypeError, ValueError):
        pass
    data["scale"] = scale
    return data


def default_background() -> dict:
    """Default background image transform (empty path = none)."""
    return {
        "path": "",
        "x": 0.0,
        "y": 0.0,
        "width": DEFAULT_BACKGROUND_WIDTH,
        "rotation": 0,
        "flip_h": False,
        "visible": True,
    }


def normalize_background_rotation(value) -> int:
    """Clamp rotation to 0/90/180/270 degrees."""
    try:
        degrees = int(round(float(value))) % 360
    except (TypeError, ValueError):
        return 0
    # Snap to nearest 90°
    return int(round(degrees / 90.0) * 90) % 360


def normalize_background(background: dict | None) -> dict:
    """Sanitize background dict from JSON."""
    data = default_background()
    if not isinstance(background, dict):
        return data
    data["path"] = str(background.get("path", "") or "")
    try:
        data["x"] = float(background.get("x", 0.0))
        data["y"] = float(background.get("y", 0.0))
        width = float(background.get("width", DEFAULT_BACKGROUND_WIDTH))
    except (TypeError, ValueError):
        width = DEFAULT_BACKGROUND_WIDTH
    data["width"] = max(1.0, width)
    data["rotation"] = normalize_background_rotation(background.get("rotation", 0))
    data["flip_h"] = bool(background.get("flip_h", False))
    data["visible"] = bool(background.get("visible", True))
    return data


def normalize_backgrounds(backgrounds=None, legacy_background=None) -> list[dict]:
    """Sanitize background list; migrate legacy single ``background`` dict."""
    if isinstance(backgrounds, list):
        return [
            normalize_background(entry)
            for entry in backgrounds
            if isinstance(entry, dict) and str(entry.get("path", "") or "")
        ]

    # Older saves used a single "background" object
    if isinstance(legacy_background, dict) and str(legacy_background.get("path", "") or ""):
        return [normalize_background(legacy_background)]
    return []


def find_picker_images(folder: str | Path) -> list[Path]:
    """Find jpg/png background images in the anim_picker folder."""
    folder_path = Path(folder)
    if not folder_path.is_dir():
        return []
    found: list[Path] = []
    for path in sorted(folder_path.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() in IMAGE_EXTENSIONS:
            found.append(path)
    return found


def is_picker_json_name(filename: str) -> bool:
    """True if filename looks like an anim picker JSON (anim_picker / animpicker)."""
    path = Path(filename)
    if path.suffix.lower() != ".json":
        return False
    stem = path.stem.lower()
    compact = stem.replace("_", "").replace("-", "").replace(" ", "")
    return "animpicker" in compact


def find_picker_json(folder: str | Path) -> Path | None:
    """Return the first anim_picker*.json in folder, or None if missing."""
    folder_path = Path(folder)
    if not folder_path.is_dir():
        return None
    for path in sorted(folder_path.iterdir()):
        if path.is_file() and is_picker_json_name(path.name):
            return path
    return None


def picker_folder_for_rig(rig_folder: str | Path) -> Path:
    """Return ``<rig_folder>/anim_picker`` for JSON + background images."""
    return Path(rig_folder) / PICKER_SUBFOLDER


def expand_rig_folderpath(folderpath: str) -> Path | None:
    """Expand env vars in a rig_context folderpath and return Path if valid."""
    if not folderpath:
        return None
    resolved = Path(os.path.expandvars(folderpath))
    if "$" in str(resolved):
        print(f"[AnimPicker] Unresolved environment variable in path: {resolved}")
        return None
    return resolved


def load_rig_context() -> dict:
    """Load rig_context.json contents."""
    if not RIG_CONTEXT_JSON.is_file():
        return {"rigs": [], "environment_variables": []}
    with open(RIG_CONTEXT_JSON) as f:
        return json.load(f)


def list_rig_contexts() -> list[dict]:
    """Return named rig entries from rig_context.json: name, folderpath, active."""
    data = load_rig_context()
    rigs = []
    for rig in data.get("rigs", []):
        name = str(rig.get("name", "") or "").strip()
        if not name:
            continue
        rigs.append(
            {
                "name": name,
                "folderpath": str(rig.get("folderpath", "") or ""),
                "active": bool(rig.get("active", False)),
            },
        )
    return rigs


def get_active_rig_context() -> dict | None:
    """Return the active rig entry, or None."""
    for rig in list_rig_contexts():
        if rig["active"]:
            return rig
    return None


def set_active_rig_context(rig_name: str) -> bool:
    """Set the active rig in rig_context.json by name. Returns True on success."""
    if not rig_name:
        return False
    data = load_rig_context()
    found = False
    for rig in data.get("rigs", []):
        is_match = str(rig.get("name", "") or "") == rig_name
        rig["active"] = is_match
        if is_match:
            found = True
    if not found:
        return False
    RIG_CONTEXT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(RIG_CONTEXT_JSON, "w") as f:
        json.dump(data, f, indent=4)
    print(f'[AnimPicker] Set active rig: "{rig_name}"')
    return True


def resolve_rig_maya_filepath(rig: dict | None) -> Path | None:
    """Return ``<character_folder>/{name}_rig.ma`` next to the auto-rig folder.

    Matches Multi Tool's Open Rig File path convention.
    """
    if not rig:
        return None
    name = str(rig.get("name", "") or "").strip()
    folder = expand_rig_folderpath(rig.get("folderpath", ""))
    if not name or folder is None:
        return None
    return folder.parent / f"{name}_rig.ma"


def resolve_picker_filepath_for_rig(rig: dict | None) -> Path | None:
    """Resolve anim picker JSON path for a rig entry.

    Looks under ``<rig_folder>/anim_picker/`` for the first *anim_picker*.json,
    or uses ``anim_picker/anim_picker.json`` as the save target when none exists.
    Returns None if no valid rig folder.
    """
    if not rig:
        return None

    folder = expand_rig_folderpath(rig.get("folderpath", ""))
    if folder is None or not folder.is_dir():
        print(
            f"[AnimPicker] Rig folder missing for '{rig.get('name', '')}': "
            f"{rig.get('folderpath', '')}",
        )
        return None

    picker_folder = picker_folder_for_rig(folder)
    found = find_picker_json(picker_folder)
    if found is not None:
        return found
    return picker_folder / DEFAULT_PICKER_FILENAME


def default_picker_data() -> dict:
    """Return empty picker document structure."""
    return {
        "version": 1,
        "grid_size": DEFAULT_GRID_SIZE,
        "view": default_view(),
        "backgrounds": [],
        "buttons": [],
    }


def make_button(
    label: str = "New",
    x: int = 0,
    y: int = 0,
    w: int = DEFAULT_BUTTON_W,
    h: int = DEFAULT_BUTTON_H,
    color: list[int] | None = None,
    targets: list[str] | None = None,
    button_id: str | None = None,
    corner_radius: int = DEFAULT_CORNER_RADIUS,
    font_size: int = DEFAULT_FONT_SIZE,
    font_bold: bool = DEFAULT_FONT_BOLD,
    font_family: str = DEFAULT_FONT_FAMILY,
    text_dark: bool = DEFAULT_TEXT_DARK,
) -> dict:
    """Create one picker button dict."""
    family = str(font_family or DEFAULT_FONT_FAMILY).strip() or DEFAULT_FONT_FAMILY
    return {
        "id": button_id or uuid.uuid4().hex[:8],
        # Empty string is allowed (blank button); default arg "New" is only for new buttons.
        "label": "" if label is None else str(label),
        "color": list(color or DEFAULT_BUTTON_COLOR),
        "x": int(x),
        "y": int(y),
        "w": max(1, int(w)),
        "h": max(1, int(h)),
        "corner_radius": max(0, min(MAX_CORNER_RADIUS, int(corner_radius))),
        "font_size": max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, int(font_size))),
        "font_bold": bool(font_bold),
        "font_family": family,
        "text_dark": bool(text_dark),
        "targets": list(targets or []),
    }


class AnimPickerData:
    """Load/save anim picker layout JSON for the active rig.

    Files live under ``<rig_folder>/anim_picker/`` — JSON plus background images.
    Uses the first *anim_picker*.json there, or ``anim_picker.json`` when saving new.
    """

    def __init__(self, filepath: str | Path | None = None) -> None:
        """Args:
        filepath: Optional custom picker JSON path. Otherwise uses active rig.
        """
        if filepath:
            self.filepath: Path | None = Path(filepath)
        else:
            self.filepath = resolve_picker_filepath_for_rig(get_active_rig_context())

        self.data = default_picker_data()

    def use_rig(self, rig: dict | None) -> Path | None:
        """Resolve and switch to a specific rig entry's picker JSON path."""
        self.filepath = resolve_picker_filepath_for_rig(rig)
        return self.filepath

    @property
    def folder(self) -> Path | None:
        """Folder that holds the picker JSON and background images."""
        return self.filepath.parent if self.filepath is not None else None

    def resolve_image_path(self, path_value: str) -> Path | None:
        """Resolve a saved image path (filename or absolute) under the picker folder."""
        if not path_value:
            return None
        path = Path(path_value)
        if path.is_file():
            return path.resolve()
        if self.folder is None:
            return None
        candidate = (self.folder / path.name).resolve()
        if candidate.is_file():
            return candidate
        return None

    def path_for_save(self, image_path: str | Path) -> str:
        """Store image as filename when it lives in the picker folder."""
        path = Path(image_path).resolve()
        if self.folder is None:
            return str(path)
        try:
            if path.parent.resolve() == self.folder.resolve():
                return path.name
        except OSError:
            pass
        return str(path)

    def load(self) -> dict:
        """Load picker data from JSON. Returns empty defaults if missing/unavailable."""
        if self.filepath is None:
            self.data = default_picker_data()
            print("[AnimPicker] No rig picker path — select a Rig Context")
            return deepcopy(self.data)

        if not self.filepath.is_file():
            self.data = default_picker_data()
            print(f"[AnimPicker] No save file yet: {self.filepath}")
            return deepcopy(self.data)

        with open(self.filepath) as f:
            loaded = json.load(f)

        data = default_picker_data()
        data["version"] = int(loaded.get("version", 1))
        data["grid_size"] = int(loaded.get("grid_size", DEFAULT_GRID_SIZE))
        data["view"] = normalize_view(loaded.get("view"))
        data["backgrounds"] = normalize_backgrounds(
            loaded.get("backgrounds"),
            legacy_background=loaded.get("background"),
        )
        data["buttons"] = [self._normalize_button(b) for b in loaded.get("buttons", [])]
        self.data = data
        print(
            f"[AnimPicker] Loaded: {self.filepath} "
            f"({len(data['buttons'])} buttons, {len(data['backgrounds'])} backgrounds)",
        )
        return deepcopy(self.data)

    def save(self, data: dict | None = None) -> Path | None:
        """Write picker data to JSON. Returns None if no rig path is set."""
        if data is not None:
            self.data = {
                "version": int(data.get("version", 1)),
                "grid_size": int(data.get("grid_size", DEFAULT_GRID_SIZE)),
                "view": normalize_view(data.get("view")),
                "backgrounds": normalize_backgrounds(
                    data.get("backgrounds"),
                    legacy_background=data.get("background"),
                ),
                "buttons": [self._normalize_button(b) for b in data.get("buttons", [])],
            }

        if self.filepath is None:
            print("[AnimPicker] No rig picker path — cannot save")
            return None

        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4)

        print(f"[AnimPicker] Saved: {self.filepath} ({len(self.data['buttons'])} buttons)")
        return self.filepath

    @staticmethod
    def _normalize_button(button: dict) -> dict:
        # Preserve explicit empty labels from JSON; only default when key is missing.
        if "label" in button:
            label = "" if button.get("label") is None else str(button.get("label"))
        else:
            label = "New"
        return make_button(
            label=label,
            x=int(button.get("x", 0)),
            y=int(button.get("y", 0)),
            w=int(button.get("w", DEFAULT_BUTTON_W)),
            h=int(button.get("h", DEFAULT_BUTTON_H)),
            color=list(button.get("color", DEFAULT_BUTTON_COLOR)),
            targets=list(button.get("targets", [])),
            button_id=str(button.get("id") or uuid.uuid4().hex[:8]),
            corner_radius=int(button.get("corner_radius", DEFAULT_CORNER_RADIUS)),
            font_size=int(button.get("font_size", DEFAULT_FONT_SIZE)),
            font_bold=bool(button.get("font_bold", DEFAULT_FONT_BOLD)),
            font_family=str(button.get("font_family", DEFAULT_FONT_FAMILY)),
            text_dark=bool(button.get("text_dark", DEFAULT_TEXT_DARK)),
        )
