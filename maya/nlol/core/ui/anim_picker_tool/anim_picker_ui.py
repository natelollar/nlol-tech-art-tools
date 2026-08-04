"""Dockable Maya anim picker: grid canvas, editable buttons, background images."""

from __future__ import annotations

from importlib import reload
from pathlib import Path

from PySide6.QtCore import QEvent, QPointF, QRect, QRectF, QSize, QTimer, Qt, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QComboBox,
    QFontComboBox,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from shiboken6 import isValid

from nlol.core.general_utils import swap_side_str
from nlol.core.ui.anim_picker_tool import anim_picker_core as picker_core
from nlol.core.ui.anim_picker_tool import anim_picker_small_functions as picker_fns
from nlol.core.ui.dockable_maya_ui import DockableMayaUI

reload(picker_core)
reload(picker_fns)

# Set while reloading so Save-on-Close cannot wipe JSON mid-teardown.
# Needed because importlib.reload() creates a new AnimPickerUI class, so the
# docked singleton may be a different class object than AnimPickerUI().
_skip_save_on_reload = False
_WINDOW_TITLE = "nLol Anim Picker UI"

RESIZE_ZONE = 14
HANDLE_SIZE = 9
BUTTON_INSET = 2
MIN_BACKGROUND_WIDTH = 20.0
NEW_BG_STACK_OFFSET = 40.0
BG_Z_BASE = -1.0
BG_Z_STEP = 0.01
ZOOM_FACTOR = 1.15
SCENE_PAD = 2500.0
NEW_BUTTON_ROW_WRAP = 24
# Square buttons created by Add Selection / Add Group Selection
SELECTION_BUTTON_SIZE = picker_core.DEFAULT_BUTTON_H * 2
SELECTION_BUTTON_COLOR = [128, 24, 24]
GROUP_SELECTION_BUTTON_SIZE = SELECTION_BUTTON_SIZE * 2
GROUP_SELECTION_BUTTON_COLOR = [160, 130, 20]
# Grid cells added/removed per Layout → Increase/Decrease Distance click
LAYOUT_DISTANCE_STEP = 1
CORNER_CURSORS = {
    "tl": Qt.SizeFDiagCursor,
    "br": Qt.SizeFDiagCursor,
    "tr": Qt.SizeBDiagCursor,
    "bl": Qt.SizeBDiagCursor,
}


def _corner_hit(rect: QRectF, pos, zone: float) -> str | None:
    """Return corner name if ``pos`` is inside a resize zone, else None."""
    left = pos.x() <= rect.left() + zone
    right = pos.x() >= rect.right() - zone
    top = pos.y() <= rect.top() + zone
    bottom = pos.y() >= rect.bottom() - zone
    if left and top:
        return "tl"
    if right and top:
        return "tr"
    if left and bottom:
        return "bl"
    if right and bottom:
        return "br"
    return None


class WheelGatedComboBox(QComboBox):
    """Combo that ignores mouse-wheel selection changes unless enabled."""

    def __init__(self, parent=None, *, wheel_scroll_enabled: bool = False) -> None:
        super().__init__(parent)
        self.wheel_scroll_enabled = bool(wheel_scroll_enabled)

    def wheelEvent(self, event) -> None:
        if self.wheel_scroll_enabled:
            super().wheelEvent(event)
        else:
            # Let the side-panel scroll area receive the wheel instead
            event.ignore()


class WheelGatedFontComboBox(QFontComboBox):
    """Font combo that ignores mouse-wheel family changes unless enabled."""

    def __init__(self, parent=None, *, wheel_scroll_enabled: bool = False) -> None:
        super().__init__(parent)
        self.wheel_scroll_enabled = bool(wheel_scroll_enabled)

    def wheelEvent(self, event) -> None:
        if self.wheel_scroll_enabled:
            super().wheelEvent(event)
        else:
            event.ignore()


class WheelGatedSlider(QSlider):
    """Slider that ignores mouse-wheel value changes unless enabled."""

    def __init__(self, orientation=Qt.Horizontal, parent=None, *, wheel_scroll_enabled: bool = False) -> None:
        super().__init__(orientation, parent)
        self.wheel_scroll_enabled = bool(wheel_scroll_enabled)

    def wheelEvent(self, event) -> None:
        if self.wheel_scroll_enabled:
            super().wheelEvent(event)
        else:
            event.ignore()


class PickerButtonItem(QGraphicsRectItem):
    """Grid-snapped picker button. Movable/resizable in edit mode; clicks select in anim mode."""

    def __init__(self, data: dict, grid_size: int, edit_mode: bool = True) -> None:
        super().__init__()
        self.button_id = data["id"]
        self.targets = list(data.get("targets", []))
        self._grid_size = grid_size
        # Missing key → "New"; explicit "" stays empty (allowed on rename).
        self._label = "New" if "label" not in data else str(data.get("label") or "")
        self._color = QColor(*data.get("color", picker_core.DEFAULT_BUTTON_COLOR))
        self._cells_w = max(1, int(data.get("w", picker_core.DEFAULT_BUTTON_W)))
        self._cells_h = max(1, int(data.get("h", picker_core.DEFAULT_BUTTON_H)))
        self._corner_radius = max(
            0,
            min(
                picker_core.MAX_CORNER_RADIUS,
                int(data.get("corner_radius", picker_core.DEFAULT_CORNER_RADIUS)),
            ),
        )
        self._font_size = max(
            picker_core.MIN_FONT_SIZE,
            min(
                picker_core.MAX_FONT_SIZE,
                int(data.get("font_size", picker_core.DEFAULT_FONT_SIZE)),
            ),
        )
        self._font_bold = bool(data.get("font_bold", picker_core.DEFAULT_FONT_BOLD))
        self._font_family = str(
            data.get("font_family", picker_core.DEFAULT_FONT_FAMILY) or picker_core.DEFAULT_FONT_FAMILY,
        )
        self._text_dark = bool(data.get("text_dark", picker_core.DEFAULT_TEXT_DARK))
        self._edit_mode = bool(edit_mode)
        self._resizing = False
        self._resize_corner = None
        self._fixed_left = 0
        self._fixed_top = 0
        self._fixed_right = 0
        self._fixed_bottom = 0
        self._resize_peers: list[dict] = []

        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(1)

        self._text_item = QGraphicsSimpleTextItem(self._label, self)
        self._text_item.setAcceptedMouseButtons(Qt.NoButton)
        # Keep labels out of rubber-band selection (band should hit the button).
        self._text_item.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self._apply_font()
        self._apply_text_color()

        self._handles = {}
        for corner in CORNER_CURSORS:
            handle = QGraphicsRectItem(self)
            handle.setBrush(QBrush(QColor(235, 235, 235)))
            handle.setPen(QPen(QColor(40, 40, 40), 1))
            handle.setAcceptedMouseButtons(Qt.NoButton)
            handle.setZValue(2)
            self._handles[corner] = handle

        self._apply_geometry()
        self.setPos(int(data.get("x", 0)) * grid_size, int(data.get("y", 0)) * grid_size)
        self.set_edit_mode(self._edit_mode)
        self._update_appearance()

    def set_edit_mode(self, enabled: bool) -> None:
        self._edit_mode = bool(enabled)
        self._resizing = False
        self._resize_corner = None
        # Always selectable so anim mode can rubber-band multi-select.
        # Only edit mode allows moving/resizing.
        self.setFlag(QGraphicsItem.ItemIsMovable, self._edit_mode)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        if not self._edit_mode:
            self.unsetCursor()
        self._update_handles()
        self._update_appearance()

    def _apply_geometry(self) -> None:
        width = self._cells_w * self._grid_size
        height = self._cells_h * self._grid_size
        inset = BUTTON_INSET
        self.setRect(inset, inset, width - inset * 2, height - inset * 2)
        self._center_label()
        self._update_handles()

    def _apply_font(self) -> None:
        font = QFont(self._font_family)
        font.setPointSize(self._font_size)
        font.setBold(self._font_bold)
        self._text_item.setFont(font)

    def _apply_text_color(self) -> None:
        rgb = (
            picker_core.TEXT_COLOR_DARK
            if self._text_dark
            else picker_core.TEXT_COLOR_LIGHT
        )
        self._text_item.setBrush(QBrush(QColor(*rgb)))

    def _center_label(self) -> None:
        text_rect = self._text_item.boundingRect()
        button_rect = self.rect()
        self._text_item.setPos(
            button_rect.center().x() - text_rect.width() / 2,
            button_rect.center().y() - text_rect.height() / 2,
        )

    def _update_handles(self) -> None:
        visible = self._edit_mode and self.isSelected()
        rect = self.rect()
        positions = {
            "tl": (rect.left(), rect.top()),
            "tr": (rect.right() - HANDLE_SIZE, rect.top()),
            "bl": (rect.left(), rect.bottom() - HANDLE_SIZE),
            "br": (rect.right() - HANDLE_SIZE, rect.bottom() - HANDLE_SIZE),
        }
        for corner, handle in self._handles.items():
            handle.setVisible(visible)
            if not visible:
                continue
            x, y = positions[corner]
            handle.setRect(x, y, HANDLE_SIZE, HANDLE_SIZE)

    def _update_appearance(self) -> None:
        # Pen is used by paint() for the selected outline; fill is painted manually.
        if self.isSelected():
            self.setPen(QPen(QColor(240, 240, 240), 2))
        else:
            self.setPen(QPen(QColor(40, 40, 40), 1))
        self._text_item.setText(self._label)
        self._apply_font()
        self._apply_text_color()
        self._center_label()
        self._update_handles()
        self.update()

    def _clamped_corner_radius(self) -> float:
        rect = self.rect()
        max_radius = min(rect.width(), rect.height()) / 2.0
        return min(float(self._corner_radius), max_radius)

    @staticmethod
    def _shade_color(color: QColor, *, value_scale: float, sat_scale: float = 1.0) -> QColor:
        """Darken/lighten via HSV so shaded tones stay chromatic (less muddy black)."""
        shaded = QColor(color)
        h, s, v, a = shaded.getHsvF()
        if h < 0:
            # Achromatic — just scale value
            shaded.setHsvF(0.0, 0.0, max(0.0, min(1.0, v * value_scale)), a)
            return shaded
        shaded.setHsvF(
            h,
            max(0.0, min(1.0, s * sat_scale)),
            max(0.0, min(1.0, v * value_scale)),
            a,
        )
        return shaded

    def paint(self, painter, option, widget=None) -> None:
        """Convex / 'bulging' button shading (Apple-style top-down lighting).

        Formula from classic iOS rounded-rect craft (Flyosity et al.):
        1) soft contact shadow, 2) light→dark vertical gradient,
        3) darker rim as the surface curves away, 4) glossy specular on top.
        """
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        radius = self._clamped_corner_radius()
        base = QColor(self._color)

        # 1) Contact shadow — sits on the surface
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 70))
        painter.drawRoundedRect(rect.translated(0.0, 2.0), radius, radius)

        shape = QPainterPath()
        shape.addRoundedRect(rect, radius, radius)
        painter.setClipPath(shape)

        # 2) Vertical body gradient (light catches the top, falls off at bottom).
        # Bottom shade is only slightly darker + a touch more saturated — not black mud.
        top = self._shade_color(base, value_scale=1.18, sat_scale=0.92)
        mid = QColor(base)
        bot = self._shade_color(base, value_scale=0.78, sat_scale=1.12)
        body = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        body.setColorAt(0.0, top)
        body.setColorAt(0.45, mid)
        body.setColorAt(1.0, bot)
        painter.fillPath(shape, body)

        # 3) Sphere-ish rim — edges curve away from the light
        lit_center = QPointF(rect.center().x(), rect.top() + rect.height() * 0.32)
        rim_radius = max(rect.width(), rect.height()) * 0.78
        sphere = QRadialGradient(lit_center, rim_radius)
        gloss = QColor(255, 255, 255, 22)
        clear = QColor(255, 255, 255, 0)
        edge = QColor(0, 0, 0, 55)
        sphere.setColorAt(0.0, gloss)
        sphere.setColorAt(0.35, clear)
        sphere.setColorAt(0.75, clear)
        sphere.setColorAt(1.0, edge)
        painter.fillRect(rect, sphere)

        # 4) Soft specular sheen on the upper face (kept subtle)
        hi = QRectF(
            rect.left() + rect.width() * 0.12,
            rect.top() + rect.height() * 0.08,
            rect.width() * 0.76,
            rect.height() * 0.32,
        )
        specular = QLinearGradient(hi.topLeft(), hi.bottomLeft())
        specular.setColorAt(0.0, QColor(255, 255, 255, 36))
        specular.setColorAt(0.4, QColor(255, 255, 255, 14))
        specular.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.setBrush(specular)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(hi)

        painter.setClipping(False)

        # 5) Thin rim stroke (selection keeps the bright outline)
        if self.isSelected():
            painter.setPen(self.pen())
        else:
            border = QColor(base).darker(170)
            border.setAlpha(200)
            painter.setPen(QPen(border, 1.0))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)

    def _hit_corner(self, pos) -> str | None:
        return _corner_hit(self.rect(), pos, RESIZE_ZONE)

    def _grid_origin(self) -> tuple[int, int]:
        grid = self._grid_size
        return (
            int(round(self.pos().x() / grid)),
            int(round(self.pos().y() / grid)),
        )

    def _begin_resize(self, corner: str) -> None:
        grid_x, grid_y = self._grid_origin()
        self._resizing = True
        self._resize_corner = corner
        self._fixed_left = grid_x
        self._fixed_top = grid_y
        self._fixed_right = grid_x + self._cells_w
        self._fixed_bottom = grid_y + self._cells_h
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        # Snapshot all currently selected buttons so they share this corner delta.
        peers: list[PickerButtonItem] = []
        scene = self.scene()
        if scene is not None:
            peers = [
                item
                for item in scene.selectedItems()
                if isinstance(item, PickerButtonItem)
            ]
        if self not in peers:
            peers.append(self)
        self._resize_peers = []
        for item in peers:
            gx, gy = item._grid_origin()
            self._resize_peers.append(
                {
                    "item": item,
                    "x": gx,
                    "y": gy,
                    "w": item._cells_w,
                    "h": item._cells_h,
                    "right": gx + item._cells_w,
                    "bottom": gy + item._cells_h,
                },
            )
        self.setSelected(True)

    def _apply_resize_at_scene_pos(self, scene_pos: QPointF) -> None:
        grid = self._grid_size
        mx = int(round(scene_pos.x() / grid))
        my = int(round(scene_pos.y() / grid))
        corner = self._resize_corner

        if corner == "br":
            new_x, new_y = self._fixed_left, self._fixed_top
            new_w = max(1, mx - self._fixed_left)
            new_h = max(1, my - self._fixed_top)
        elif corner == "bl":
            new_y = self._fixed_top
            new_x = min(self._fixed_right - 1, mx)
            new_w = max(1, self._fixed_right - new_x)
            new_h = max(1, my - self._fixed_top)
        elif corner == "tr":
            new_x = self._fixed_left
            new_y = min(self._fixed_bottom - 1, my)
            new_w = max(1, mx - self._fixed_left)
            new_h = max(1, self._fixed_bottom - new_y)
        else:  # tl
            new_x = min(self._fixed_right - 1, mx)
            new_y = min(self._fixed_bottom - 1, my)
            new_w = max(1, self._fixed_right - new_x)
            new_h = max(1, self._fixed_bottom - new_y)

        if (
            new_x == self._grid_origin()[0]
            and new_y == self._grid_origin()[1]
            and new_w == self._cells_w
            and new_h == self._cells_h
        ):
            return

        self_start = next(
            (peer for peer in self._resize_peers if peer["item"] is self),
            None,
        )
        dw = new_w - self_start["w"] if self_start else 0
        dh = new_h - self_start["h"] if self_start else 0

        self._cells_w = new_w
        self._cells_h = new_h
        self.setPos(new_x * grid, new_y * grid)
        self._apply_geometry()

        if not self_start or (dw == 0 and dh == 0 and len(self._resize_peers) <= 1):
            return

        for peer in self._resize_peers:
            item = peer["item"]
            if item is self:
                continue
            peer_w = max(1, peer["w"] + dw)
            peer_h = max(1, peer["h"] + dh)
            if corner == "br":
                peer_x, peer_y = peer["x"], peer["y"]
            elif corner == "bl":
                peer_x = peer["right"] - peer_w
                peer_y = peer["y"]
            elif corner == "tr":
                peer_x = peer["x"]
                peer_y = peer["bottom"] - peer_h
            else:  # tl
                peer_x = peer["right"] - peer_w
                peer_y = peer["bottom"] - peer_h
            item._cells_w = peer_w
            item._cells_h = peer_h
            item.setPos(peer_x * grid, peer_y * grid)
            item._apply_geometry()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self._edit_mode and not self._resizing:
            grid = self._grid_size
            return QPointF(
                round(value.x() / grid) * grid,
                round(value.y() / grid) * grid,
            )
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self._update_appearance()
        return super().itemChange(change, value)

    def hoverMoveEvent(self, event) -> None:
        if self._edit_mode:
            corner = self._hit_corner(event.pos())
            if corner:
                self.setCursor(CORNER_CURSORS[corner])
            else:
                self.setCursor(Qt.SizeAllCursor)
        else:
            self.setCursor(Qt.PointingHandCursor)
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.unsetCursor()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.LeftButton:
            super().mousePressEvent(event)
            return

        if self._edit_mode:
            corner = self._hit_corner(event.pos())
            if corner:
                self._begin_resize(corner)
                event.accept()
                return
            # Ctrl+click deselect is handled by PickerCanvas eventFilter so it
            # isn't eaten by move/RubberBandDrag.
            super().mousePressEvent(event)
            return

        # Anim mode clicks are handled by PickerCanvas eventFilter.
        event.accept()

    def mouseMoveEvent(self, event) -> None:
        if self._resizing:
            self._apply_resize_at_scene_pos(event.scenePos())
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self._resizing and event.button() == Qt.LeftButton:
            self._resizing = False
            self._resize_corner = None
            self._resize_peers = []
            self.setFlag(QGraphicsItem.ItemIsMovable, self._edit_mode)
            event.accept()
            return

        super().mouseReleaseEvent(event)

    def set_label(self, label: str) -> None:
        self._label = "" if label is None else str(label)
        self._update_appearance()

    def set_color(self, color: QColor) -> None:
        self._color = QColor(color)
        self._update_appearance()

    def set_corner_radius(self, radius: int) -> None:
        self._corner_radius = max(0, min(picker_core.MAX_CORNER_RADIUS, int(radius)))
        self._update_appearance()

    def set_font_size(self, size: int) -> None:
        self._font_size = max(
            picker_core.MIN_FONT_SIZE,
            min(picker_core.MAX_FONT_SIZE, int(size)),
        )
        self._update_appearance()

    def set_font_bold(self, bold: bool) -> None:
        self._font_bold = bool(bold)
        self._update_appearance()

    def set_font_family(self, family: str) -> None:
        self._font_family = str(family or picker_core.DEFAULT_FONT_FAMILY).strip() or (
            picker_core.DEFAULT_FONT_FAMILY
        )
        self._update_appearance()

    def set_text_dark(self, dark: bool) -> None:
        self._text_dark = bool(dark)
        self._update_appearance()

    def set_targets(self, targets: list[str]) -> None:
        self.targets = list(targets)

    def label(self) -> str:
        return self._label

    def grid_x(self) -> int:
        return int(round(self.pos().x() / self._grid_size))

    def grid_y(self) -> int:
        return int(round(self.pos().y() / self._grid_size))

    def cells_w(self) -> int:
        return self._cells_w

    def cells_h(self) -> int:
        return self._cells_h

    def set_grid_pos(self, x: int, y: int) -> None:
        self.setPos(int(x) * self._grid_size, int(y) * self._grid_size)

    def set_cells_size(self, w: int, h: int) -> None:
        self._cells_w = max(1, int(w))
        self._cells_h = max(1, int(h))
        self._apply_geometry()

    def color(self) -> QColor:
        return QColor(self._color)

    def corner_radius(self) -> int:
        return self._corner_radius

    def font_size(self) -> int:
        return self._font_size

    def font_bold(self) -> bool:
        return self._font_bold

    def font_family(self) -> str:
        return self._font_family

    def text_dark(self) -> bool:
        return self._text_dark

    def to_data(self) -> dict:
        return picker_core.make_button(
            label=self._label,
            x=int(round(self.pos().x() / self._grid_size)),
            y=int(round(self.pos().y() / self._grid_size)),
            w=self._cells_w,
            h=self._cells_h,
            color=[self._color.red(), self._color.green(), self._color.blue()],
            targets=self.targets,
            button_id=self.button_id,
            corner_radius=self._corner_radius,
            font_size=self._font_size,
            font_bold=self._font_bold,
            font_family=self._font_family,
            text_dark=self._text_dark,
        )


class BackgroundImageItem(QGraphicsPixmapItem):
    """Character reference image behind picker buttons. Aspect-locked resize in edit mode."""

    def __init__(
        self,
        image_path: Path,
        data: dict,
        edit_mode: bool = True,
        grid_size: int = picker_core.DEFAULT_GRID_SIZE,
        snap_enabled: bool = False,
        locked: bool = False,
    ) -> None:
        super().__init__()
        self.image_path = Path(image_path)
        self._native_pixmap = QPixmap(str(self.image_path))
        if self._native_pixmap.isNull():
            raise ValueError(f"Could not load image: {self.image_path}")

        self._edit_mode = bool(edit_mode)
        self._grid_size = max(1, int(grid_size))
        self._snap_enabled = bool(snap_enabled)
        self._locked = bool(locked)
        self._resizing = False
        self._resize_corner: str | None = None
        self._aspect = (
            self._native_pixmap.height() / max(1, self._native_pixmap.width())
        )

        self.setPixmap(self._native_pixmap)
        self.setTransformationMode(Qt.SmoothTransformation)
        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self.setZValue(-1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

        width = float(data.get("width", picker_core.DEFAULT_BACKGROUND_WIDTH))
        self._rotation = picker_core.normalize_background_rotation(data.get("rotation", 0))
        self._flip_h = bool(data.get("flip_h", False))
        self.set_display_width(width)
        self.setPos(float(data.get("x", 0.0)), float(data.get("y", 0.0)))
        self._apply_visual_transform()
        self.setVisible(bool(data.get("visible", True)))
        self._apply_interaction()
        if self._snap_enabled:
            self.snap_center_to_grid()

    def _is_interactive(self) -> bool:
        return self._edit_mode and not self._locked

    def _apply_interaction(self) -> None:
        """Movable/selectable only in edit mode when unlocked; else click-through."""
        self._resizing = False
        interactive = self._is_interactive()
        self.setFlag(QGraphicsItem.ItemIsMovable, interactive)
        self.setFlag(QGraphicsItem.ItemIsSelectable, interactive)
        if interactive:
            self.setAcceptedMouseButtons(Qt.LeftButton)
        else:
            self.setSelected(False)
            self.setAcceptedMouseButtons(Qt.NoButton)
            self.unsetCursor()
        # Shape drives hit-testing; empty shape when locked/anim = true click-through.
        self.prepareGeometryChange()
        self.update()

    def shape(self):
        """Empty hit shape when not interactive so anim-mode clicks pass through."""
        if not self._is_interactive():
            return QPainterPath()
        return super().shape()

    def set_edit_mode(self, enabled: bool) -> None:
        self._edit_mode = bool(enabled)
        self._apply_interaction()

    def set_locked(self, locked: bool) -> None:
        self._locked = bool(locked)
        self._apply_interaction()

    def set_grid_size(self, grid_size: int) -> None:
        self._grid_size = max(1, int(grid_size))

    def set_snap_enabled(self, enabled: bool) -> None:
        self._snap_enabled = bool(enabled)
        if self._snap_enabled:
            self.snap_center_to_grid()
        self.update()

    def display_width(self) -> float:
        return self._native_pixmap.width() * self.scale()

    def display_height(self) -> float:
        return self.display_width() * self._aspect

    def set_display_width(self, width: float) -> None:
        width = max(MIN_BACKGROUND_WIDTH, float(width))
        self.setScale(width / max(1, self._native_pixmap.width()))
        self._apply_visual_transform()

    def rotation_degrees(self) -> int:
        return int(self._rotation)

    def _apply_visual_transform(self) -> None:
        """Bake rotation + optional horizontal flip around the image center."""
        cx = self._local_center().x()
        cy = self._local_center().y()
        transform = QTransform()
        transform.translate(cx, cy)
        transform.rotate(self._rotation)
        if self._flip_h:
            transform.scale(-1, 1)
        transform.translate(-cx, -cy)
        self.setTransform(transform)
        self.setRotation(0)

    def rotate_clockwise_90(self) -> None:
        """Rotate 90° clockwise around the image center (photo-style)."""
        self._rotation = (int(self._rotation) + 90) % 360
        self._apply_visual_transform()
        self.update()

    def center_scene_pos(self) -> QPointF:
        return self.sceneBoundingRect().center()

    def set_center_scene_pos(self, center: QPointF) -> None:
        """Move item so its visual center sits at ``center``."""
        delta = center - self.center_scene_pos()
        self.setPos(self.pos() + delta)

    def _snapped_top_left(self, top_left: QPointF) -> QPointF:
        """Top-left that places the image center on the nearest grid point."""
        # Pure translation keeps bounds size; shift current center by the same delta.
        center = self.sceneBoundingRect().center() + (top_left - self.pos())
        grid = float(self._grid_size)
        snap_cx = round(center.x() / grid) * grid
        snap_cy = round(center.y() / grid) * grid
        return top_left + QPointF(snap_cx - center.x(), snap_cy - center.y())

    def snap_center_to_grid(self) -> None:
        """Snap image center to the nearest grid intersection."""
        center = self.sceneBoundingRect().center()
        grid = float(self._grid_size)
        snap_cx = round(center.x() / grid) * grid
        snap_cy = round(center.y() / grid) * grid
        self.setPos(self.pos() + QPointF(snap_cx - center.x(), snap_cy - center.y()))

    def to_data(self, path_for_save: str) -> dict:
        return picker_core.normalize_background(
            {
                "path": path_for_save,
                "x": self.pos().x(),
                "y": self.pos().y(),
                "width": self.display_width(),
                "rotation": self._rotation,
                "flip_h": self._flip_h,
                "visible": self.isVisible(),
            },
        )

    def _local_rect(self) -> QRectF:
        return QRectF(self.pixmap().rect())

    def _local_center(self) -> QPointF:
        rect = self._local_rect()
        return rect.center()

    def _hit_corner(self, pos) -> str | None:
        zone = RESIZE_ZONE / max(self.scale(), 0.001)
        return _corner_hit(self._local_rect(), pos, zone)

    def paint(self, painter, option, widget=None) -> None:
        super().paint(painter, option, widget)
        if not (self._is_interactive() and self.isSelected()):
            return

        pen = QPen(QColor(240, 240, 240), 2)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self._local_rect())

        # Center anchor (snap point) — stays readable at any zoom
        center = self._local_center()
        arm = 8.0 / max(self.scale(), 0.001)
        anchor_pen = QPen(QColor(80, 220, 120), 2)
        anchor_pen.setCosmetic(True)
        painter.setPen(anchor_pen)
        painter.drawLine(
            QPointF(center.x() - arm, center.y()),
            QPointF(center.x() + arm, center.y()),
        )
        painter.drawLine(
            QPointF(center.x(), center.y() - arm),
            QPointF(center.x(), center.y() + arm),
        )

    def itemChange(self, change, value):
        if (
            change == QGraphicsItem.ItemPositionChange
            and self._is_interactive()
            and not self._resizing
            and self._snap_enabled
        ):
            return self._snapped_top_left(value)
        if change == QGraphicsItem.ItemSelectedHasChanged:
            self.update()
        return super().itemChange(change, value)

    def hoverMoveEvent(self, event) -> None:
        if self._is_interactive():
            corner = self._hit_corner(event.pos())
            if corner:
                self.setCursor(CORNER_CURSORS[corner])
            else:
                self.setCursor(Qt.SizeAllCursor)
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.unsetCursor()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event) -> None:
        if self._is_interactive() and event.button() == Qt.LeftButton:
            corner = self._hit_corner(event.pos())
            if corner:
                self._resizing = True
                self._resize_corner = corner
                self.setFlag(QGraphicsItem.ItemIsMovable, False)
                self.setSelected(True)
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._resizing and self._resize_corner:
            scene_pos = event.scenePos()
            pos = self.pos()
            right = pos.x() + self.display_width()
            bottom = pos.y() + self.display_height()
            corner = self._resize_corner

            if corner == "br":
                new_w = max(MIN_BACKGROUND_WIDTH, scene_pos.x() - pos.x())
                self.set_display_width(new_w)
            elif corner == "bl":
                new_w = max(MIN_BACKGROUND_WIDTH, right - scene_pos.x())
                self.set_display_width(new_w)
                self.setPos(right - self.display_width(), pos.y())
            elif corner == "tr":
                new_w = max(MIN_BACKGROUND_WIDTH, scene_pos.x() - pos.x())
                self.set_display_width(new_w)
                self.setPos(pos.x(), bottom - self.display_height())
            else:  # tl
                new_w = max(MIN_BACKGROUND_WIDTH, right - scene_pos.x())
                self.set_display_width(new_w)
                self.setPos(right - self.display_width(), bottom - self.display_height())
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self._resizing and event.button() == Qt.LeftButton:
            self._resizing = False
            self._resize_corner = None
            self.setFlag(QGraphicsItem.ItemIsMovable, self._is_interactive())
            if self._snap_enabled:
                self.snap_center_to_grid()
            event.accept()
            return
        super().mouseReleaseEvent(event)


class PickerView(QGraphicsView):
    """Graphics view that procedurally paints a scalable light-grey grid."""

    def __init__(self, scene: QGraphicsScene, grid_size: int) -> None:
        super().__init__(scene)
        self._grid_size = grid_size
        self._grid_visible = True
        self.on_zoom = None  # optional callable after wheel zoom
        self.on_delete_key = None  # optional callable; return True if handled

        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # NoBrush so our drawBackground owns the fill + grid (view brush can hide it)
        self.setBackgroundBrush(Qt.NoBrush)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFocusPolicy(Qt.StrongFocus)

    def set_grid_size(self, grid_size: int) -> None:
        self._grid_size = max(1, int(grid_size))
        self.viewport().update()

    def set_grid_visible(self, visible: bool) -> None:
        self._grid_visible = bool(visible)
        self.viewport().update()

    def wheelEvent(self, event) -> None:
        factor = ZOOM_FACTOR if event.angleDelta().y() > 0 else 1.0 / ZOOM_FACTOR
        self.scale(factor, factor)
        if callable(self.on_zoom):
            self.on_zoom()
        event.accept()

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Delete, Qt.Key_Backspace) and callable(self.on_delete_key):
            if self.on_delete_key():
                event.accept()
                return
        super().keyPressEvent(event)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.fillRect(rect, QColor(55, 55, 55))
        if not self._grid_visible:
            return

        grid = self._grid_size
        left = int(rect.left()) - (int(rect.left()) % grid)
        top = int(rect.top()) - (int(rect.top()) % grid)

        minor = QPen(QColor(85, 85, 85))
        minor.setCosmetic(True)
        major = QPen(QColor(105, 105, 105))
        major.setCosmetic(True)
        # Origin axes: green = vertical center (x=0), red = horizontal center (y=0)
        center_v = QPen(QColor(70, 160, 90))
        center_v.setCosmetic(True)
        center_h = QPen(QColor(180, 70, 70))
        center_h.setCosmetic(True)

        x = left
        while x < rect.right():
            if x == 0:
                painter.setPen(center_v)
            else:
                painter.setPen(major if x % (grid * 5) == 0 else minor)
            painter.drawLine(QPointF(x, rect.top()), QPointF(x, rect.bottom()))
            x += grid

        y = top
        while y < rect.bottom():
            if y == 0:
                painter.setPen(center_h)
            else:
                painter.setPen(major if y % (grid * 5) == 0 else minor)
            painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))
            y += grid


class PickerCanvas(QWidget):
    """Graphics view canvas for creating/dragging picker buttons."""

    selection_changed = Signal()
    anim_selection_committed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._grid_size = picker_core.DEFAULT_GRID_SIZE
        self._edit_mode = True
        self._image_snap = False
        self._images_locked = False
        # Anim rubber-band: None | "add" (Shift) | "subtract" (Ctrl)
        self._anim_rubber_band_mode: str | None = None
        self._anim_pre_rubber_selection: list[PickerButtonItem] = []
        self._restoring_modifier_selection = False
        # Sticky Layout pivot for Separate + Rotate (until selection set changes)
        self._layout_pivot_id: str | None = None
        self._layout_pivot_selection_key: frozenset[str] | None = None

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(-5000, -5000, 10000, 10000)

        self.view = PickerView(self.scene, self._grid_size)
        self.view.on_zoom = self._update_scene_rect
        self.view.on_delete_key = self._on_delete_key

        # Middle-mouse pan; anim-mode click / Shift|Ctrl rubber-band via viewport filter
        self._panning = False
        self._pan_start = QPointF()
        self.view.viewport().installEventFilter(self)

        self.scene.selectionChanged.connect(self._on_scene_selection_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
        self._update_scene_rect()

    def eventFilter(self, watched, event):
        if watched is not self.view.viewport():
            return super().eventFilter(watched, event)

        etype = event.type()
        if etype == QEvent.MouseButtonPress and event.button() == Qt.MiddleButton:
            self._panning = True
            self._pan_start = event.position()
            self.view.setCursor(Qt.ClosedHandCursor)
            return True
        if etype == QEvent.MouseMove and self._panning:
            delta = event.position() - self._pan_start
            self._pan_start = event.position()
            self.view.horizontalScrollBar().setValue(
                self.view.horizontalScrollBar().value() - int(delta.x()),
            )
            self.view.verticalScrollBar().setValue(
                self.view.verticalScrollBar().value() - int(delta.y()),
            )
            return True
        if etype == QEvent.MouseButtonRelease and event.button() == Qt.MiddleButton:
            self._panning = False
            self.view.unsetCursor()
            return True
        if etype == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            return self._on_canvas_press(event)
        if etype == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            # Capture band rect before the view clears it; finish after the
            # release is fully processed so ReplaceSelection has settled.
            band_rect = QRect(self.view.rubberBandRect())
            QTimer.singleShot(0, lambda r=band_rect: self._deferred_selection_release(r))
        return super().eventFilter(watched, event)

    def _deferred_selection_release(self, band_rect: QRect | None = None) -> None:
        self._update_scene_rect()
        self._finish_modifier_rubber_band(band_rect)

    def _on_scene_selection_changed(self) -> None:
        """Keep prior highlights visible during Shift-add / Ctrl-subtract drags."""
        self._preview_modifier_rubber_band()
        sel_key = frozenset(b.button_id for b in self.selected_buttons())
        if sel_key != self._layout_pivot_selection_key:
            self._layout_pivot_id = None
            self._layout_pivot_selection_key = None
        self.selection_changed.emit()

    def _preview_modifier_rubber_band(self) -> None:
        """Keep prior highlights visible during Shift-add rubber-band drags.

        Only used for add mode. Ctrl-subtract is applied on release from the
        band rect — live subtract previews fight ReplaceSelection and break
        the final deselect.
        """
        if self._restoring_modifier_selection:
            return
        if self._anim_rubber_band_mode != "add":
            return
        prior = [b for b in self._anim_pre_rubber_selection if b.scene() is self.scene]
        if not prior:
            return
        self._restoring_modifier_selection = True
        try:
            # Band replace cleared prior; put those highlights back during drag.
            for button in prior:
                if not button.isSelected():
                    button.setSelected(True)
        finally:
            self._restoring_modifier_selection = False

    def _on_canvas_press(self, event) -> bool:
        """Left press in edit/anim: Ctrl/Shift selection, or start rubber-band."""
        button = self._picker_button_at(event.position().toPoint())
        mods = event.modifiers()

        if button is not None:
            if mods & Qt.ControlModifier:
                # Always remove from selection (never add with Ctrl).
                button.setSelected(False)
                self._anim_rubber_band_mode = None
                self._anim_pre_rubber_selection = []
                return True
            if mods & Qt.ShiftModifier:
                # Add to selection (RubberBandDrag would otherwise replace).
                button.setSelected(True)
                self._anim_rubber_band_mode = None
                self._anim_pre_rubber_selection = []
                return True
            if self._edit_mode:
                # Edit: let normal click/drag/resize through.
                self._anim_rubber_band_mode = None
                self._anim_pre_rubber_selection = []
                return False
            # Anim mode: handle selection here so RubberBandDrag cannot wipe it.
            self.scene.clearSelection()
            button.setSelected(True)
            self._anim_rubber_band_mode = None
            self._anim_pre_rubber_selection = []
            return True

        # Empty / click-through: start rubber-band (Shift add / Ctrl subtract).
        if mods & Qt.ControlModifier:
            self._anim_rubber_band_mode = "subtract"
            self._anim_pre_rubber_selection = list(self.selected_buttons())
        elif mods & Qt.ShiftModifier:
            self._anim_rubber_band_mode = "add"
            self._anim_pre_rubber_selection = list(self.selected_buttons())
        else:
            self._anim_rubber_band_mode = None
            self._anim_pre_rubber_selection = []
        return False

    def _picker_buttons_in_view_rect(self, view_rect: QRect | None) -> set[PickerButtonItem]:
        """Picker buttons intersecting a viewport rubber-band rect."""
        if view_rect is None or view_rect.isEmpty() or view_rect.isNull():
            return set()
        buttons: set[PickerButtonItem] = set()
        for item in self.view.items(view_rect):
            candidate = item
            while candidate is not None:
                if isinstance(candidate, PickerButtonItem):
                    buttons.add(candidate)
                    break
                if isinstance(candidate, BackgroundImageItem):
                    break
                candidate = candidate.parentItem()
        return buttons

    def _finish_modifier_rubber_band(self, band_rect: QRect | None = None) -> None:
        """Apply Shift-add / Ctrl-subtract from the rubber-band rect.

        Band membership comes from the rubber-band rectangle (not
        ``selectedItems``), because child label items can steal band hits.
        """
        mode = self._anim_rubber_band_mode
        prior = [b for b in self._anim_pre_rubber_selection if b.scene() is self.scene]
        band = self._picker_buttons_in_view_rect(band_rect)
        if mode in ("add", "subtract"):
            # Keep any selected backgrounds (edit mode) while rebuilding buttons.
            kept_backgrounds = [
                item for item in self.selected_backgrounds() if item.scene() is self.scene
            ]
            self.scene.clearSelection()
            for item in kept_backgrounds:
                item.setSelected(True)
            if mode == "add":
                for button in set(prior) | band:
                    button.setSelected(True)
            else:
                for button in prior:
                    if button not in band:
                        button.setSelected(True)
        self._anim_rubber_band_mode = None
        self._anim_pre_rubber_selection = []
        if not self._edit_mode:
            self.anim_selection_committed.emit()

    def _on_delete_key(self) -> bool:
        if not self._edit_mode:
            return False
        self.delete_selected()
        return True

    def _picker_button_at(self, view_pos) -> PickerButtonItem | None:
        """Return the topmost picker button under a viewport position, if any.

        Skips background images so buttons under a reference image still hit.
        """
        for item in self.view.items(view_pos):
            candidate = item
            while candidate is not None:
                if isinstance(candidate, PickerButtonItem):
                    return candidate
                if isinstance(candidate, BackgroundImageItem):
                    break
                candidate = candidate.parentItem()
        return None

    def _update_scene_rect(self) -> None:
        """Expand scene bounds around buttons/backgrounds so pan can always reach them."""
        items: list[QGraphicsItem] = list(self.button_items()) + list(self.background_items())

        if items:
            bounds = items[0].sceneBoundingRect()
            for item in items[1:]:
                bounds = bounds.united(item.sceneBoundingRect())
        else:
            bounds = QRectF(-500, -500, 1000, 1000)

        view_bounds = self.view.mapToScene(self.view.viewport().rect()).boundingRect()
        pad_x = max(SCENE_PAD, view_bounds.width())
        pad_y = max(SCENE_PAD, view_bounds.height())
        self.scene.setSceneRect(bounds.adjusted(-pad_x, -pad_y, pad_x, pad_y))

    def clear_buttons(self) -> None:
        for item in list(self.scene.items()):
            if isinstance(item, PickerButtonItem):
                self.scene.removeItem(item)

    def clear_backgrounds(self) -> None:
        for item in self.background_items():
            self.scene.removeItem(item)
        self._update_scene_rect()

    def background_items(self) -> list[BackgroundImageItem]:
        return [i for i in self.scene.items() if isinstance(i, BackgroundImageItem)]

    def selected_backgrounds(self) -> list[BackgroundImageItem]:
        return [i for i in self.scene.selectedItems() if isinstance(i, BackgroundImageItem)]

    def add_background(
        self,
        image_path: Path | str,
        data: dict | None = None,
        *,
        select: bool = True,
        offset_if_default: bool = True,
    ) -> BackgroundImageItem | None:
        """Add a background image to the canvas (does not replace existing ones)."""
        path = Path(image_path)
        if not path.is_file():
            return None

        bg_data = picker_core.normalize_background(data)
        if data is None and offset_if_default:
            # Nudge newly added images so they don't stack exactly on top of each other
            n = len(self.background_items())
            bg_data["x"] = float(bg_data["x"]) + n * NEW_BG_STACK_OFFSET
            bg_data["y"] = float(bg_data["y"]) + n * NEW_BG_STACK_OFFSET

        try:
            item = BackgroundImageItem(
                path,
                bg_data,
                edit_mode=self._edit_mode,
                grid_size=self._grid_size,
                snap_enabled=self._image_snap,
                locked=self._images_locked,
            )
        except ValueError as exc:
            print(f"[AnimPicker] {exc}")
            return None

        # Later images draw above earlier ones, still behind buttons (z < 1)
        item.setZValue(BG_Z_BASE + (BG_Z_STEP * len(self.background_items())))
        self.scene.addItem(item)
        if select:
            self.scene.clearSelection()
            item.setSelected(True)
        self._update_scene_rect()
        return item

    def duplicate_selected_backgrounds(self) -> list[BackgroundImageItem]:
        """Duplicate selected backgrounds, offset right by each image's visual width."""
        if not self._edit_mode or self._images_locked:
            return []
        sources = self.selected_backgrounds()
        if not sources:
            return []

        duplicates: list[BackgroundImageItem] = []
        for source in sources:
            data = source.to_data(str(source.image_path))
            data["x"] = source.pos().x() + source.sceneBoundingRect().width()
            data["y"] = source.pos().y()
            item = self.add_background(
                source.image_path,
                data,
                select=False,
                offset_if_default=False,
            )
            if item is not None:
                duplicates.append(item)

        if duplicates:
            self.scene.clearSelection()
            for item in duplicates:
                item.setSelected(True)
        return duplicates

    def rotate_selected_backgrounds(self) -> int:
        """Rotate selected backgrounds 90° clockwise around their centers."""
        if not self._edit_mode or self._images_locked:
            return 0
        selected = self.selected_backgrounds()
        if not selected:
            return 0
        for item in selected:
            item.rotate_clockwise_90()
            if self._image_snap:
                item.snap_center_to_grid()
        return len(selected)

    def mirror_selected_backgrounds(self) -> list[BackgroundImageItem]:
        """Create copies mirrored across the vertical axis (x=0), with horizontal flip."""
        if not self._edit_mode or self._images_locked:
            return []
        sources = self.selected_backgrounds()
        if not sources:
            return []

        mirrors: list[BackgroundImageItem] = []
        for source in sources:
            center = source.center_scene_pos()
            data = source.to_data(str(source.image_path))
            data["flip_h"] = not bool(data.get("flip_h", False))
            item = self.add_background(
                source.image_path,
                data,
                select=False,
                offset_if_default=False,
            )
            if item is None:
                continue
            item.set_center_scene_pos(QPointF(-center.x(), center.y()))
            if self._image_snap:
                item.snap_center_to_grid()
            mirrors.append(item)

        if mirrors:
            self.scene.clearSelection()
            for item in mirrors:
                item.setSelected(True)
        return mirrors

    def remove_selected_backgrounds(self) -> int:
        if not self._edit_mode or self._images_locked:
            return 0
        selected = self.selected_backgrounds()
        for item in selected:
            self.scene.removeItem(item)
        if selected:
            self._update_scene_rect()
        return len(selected)

    def _ordered_backgrounds(self) -> list[BackgroundImageItem]:
        """Backgrounds from back to front."""
        return sorted(self.background_items(), key=lambda i: i.zValue())

    def _rewrite_background_z(self, ordered: list[BackgroundImageItem]) -> None:
        for i, item in enumerate(ordered):
            item.setZValue(BG_Z_BASE + BG_Z_STEP * i)
        self.scene.update()

    def _nudge_backgrounds(self, direction: int) -> int:
        """Move selected backgrounds one step. ``direction``: +1 forward, -1 back."""
        if not self._edit_mode or self._images_locked:
            return 0
        selected = set(self.selected_backgrounds())
        if not selected:
            return 0

        ordered = self._ordered_backgrounds()
        moved = 0
        if direction > 0:
            # Front-most first so stacked selection can all step forward
            walk = reversed(sorted(selected, key=lambda i: i.zValue()))
            for item in walk:
                idx = ordered.index(item)
                if idx >= len(ordered) - 1:
                    continue
                ordered[idx], ordered[idx + 1] = ordered[idx + 1], ordered[idx]
                moved += 1
        else:
            # Back-most first so stacked selection can all step backward
            for item in sorted(selected, key=lambda i: i.zValue()):
                idx = ordered.index(item)
                if idx <= 0:
                    continue
                ordered[idx - 1], ordered[idx] = ordered[idx], ordered[idx - 1]
                moved += 1

        if moved:
            self._rewrite_background_z(ordered)
        return moved

    def bring_backgrounds_forward(self) -> int:
        """Move selected backgrounds one step toward the front."""
        return self._nudge_backgrounds(+1)

    def send_backgrounds_back(self) -> int:
        """Move selected backgrounds one step toward the back."""
        return self._nudge_backgrounds(-1)

    def button_items(self) -> list[PickerButtonItem]:
        return [i for i in self.scene.items() if isinstance(i, PickerButtonItem)]

    def selected_button(self) -> PickerButtonItem | None:
        selected = self.selected_buttons()
        return selected[0] if selected else None

    def selected_buttons(self) -> list[PickerButtonItem]:
        return [i for i in self.scene.selectedItems() if isinstance(i, PickerButtonItem)]

    def collect_view(self) -> dict:
        """Current canvas pan/zoom for JSON save."""
        center = self.view.mapToScene(self.view.viewport().rect().center())
        scale = self.view.transform().m11()
        return picker_core.normalize_view(
            {
                "center_x": center.x(),
                "center_y": center.y(),
                "scale": scale,
            },
        )

    def apply_view(self, view: dict | None) -> None:
        """Restore canvas pan/zoom from saved view data."""
        data = picker_core.normalize_view(view)
        self.view.resetTransform()
        self.view.scale(data["scale"], data["scale"])
        self._update_scene_rect()
        self.view.centerOn(data["center_x"], data["center_y"])
        self.view.viewport().update()

    def center_on_origin(self) -> None:
        """Jump the view to the grid center (0, 0), keeping current zoom."""
        self._update_scene_rect()
        self.view.centerOn(0.0, 0.0)
        self.view.viewport().update()

    def collect_data(self, path_for_save=None) -> dict:
        # Bottom-most first so load order restores draw order
        backgrounds = []
        for item in sorted(self.background_items(), key=lambda i: i.zValue()):
            save_path = (
                path_for_save(item.image_path)
                if callable(path_for_save)
                else str(item.image_path)
            )
            backgrounds.append(item.to_data(save_path))
        return {
            "version": 1,
            "grid_size": self._grid_size,
            "view": self.collect_view(),
            "backgrounds": backgrounds,
            "buttons": [item.to_data() for item in self.button_items()],
        }

    def load_data(self, data: dict, resolve_image=None) -> None:
        self.clear_buttons()
        self.clear_backgrounds()
        self._grid_size = int(data.get("grid_size", picker_core.DEFAULT_GRID_SIZE))
        self.view.set_grid_size(self._grid_size)
        for button_data in data.get("buttons", []):
            item = PickerButtonItem(button_data, self._grid_size, edit_mode=self._edit_mode)
            self.scene.addItem(item)

        backgrounds = picker_core.normalize_backgrounds(
            data.get("backgrounds"),
            legacy_background=data.get("background"),
        )
        for bg_data in backgrounds:
            if not callable(resolve_image):
                continue
            image_path = resolve_image(bg_data["path"])
            if image_path is not None:
                self.add_background(
                    image_path,
                    bg_data,
                    select=False,
                    offset_if_default=False,
                )
            else:
                print(f"[AnimPicker] Background image not found: {bg_data['path']}")

        self._update_scene_rect()
        self.apply_view(data.get("view"))
        self.view.viewport().update()

    def add_button(
        self,
        label: str = "New",
        *,
        x: int | None = None,
        y: int | None = None,
        w: int | None = None,
        h: int | None = None,
        color: list[int] | None = None,
        targets: list[str] | None = None,
        select: bool = True,
    ) -> PickerButtonItem | None:
        if not self._edit_mode:
            return None
        if x is None or y is None:
            free_x, free_y = self._next_free_cell()
            x = free_x if x is None else x
            y = free_y if y is None else y
        kwargs = {
            "label": label,
            "x": int(x),
            "y": int(y),
            "targets": targets,
        }
        if w is not None:
            kwargs["w"] = int(w)
        if h is not None:
            kwargs["h"] = int(h)
        if color is not None:
            kwargs["color"] = list(color)
        data = picker_core.make_button(**kwargs)
        item = PickerButtonItem(data, self._grid_size, edit_mode=True)
        self.scene.addItem(item)
        if select:
            self.scene.clearSelection()
            item.setSelected(True)
        self._update_scene_rect()
        return item

    def add_buttons_horizontal(
        self,
        specs: list[tuple[str, list[str]]],
        *,
        w: int | None = None,
        h: int | None = None,
        color: list[int] | None = None,
    ) -> list[PickerButtonItem]:
        """Create buttons in selection order, laid out left-to-right from a free cell."""
        if not self._edit_mode or not specs:
            return []
        start_x, start_y = self._next_free_cell()
        button_w = int(w) if w is not None else picker_core.DEFAULT_BUTTON_W
        step = button_w
        created: list[PickerButtonItem] = []
        for index, (label, targets) in enumerate(specs):
            item = self.add_button(
                label,
                x=start_x + index * step,
                y=start_y,
                w=w,
                h=h,
                color=color,
                targets=targets,
                select=False,
            )
            if item is not None:
                created.append(item)
        if created:
            self.scene.clearSelection()
            for item in created:
                item.setSelected(True)
            self._update_scene_rect()
        return created

    def delete_selected(self) -> int:
        if not self._edit_mode:
            return 0
        selected = []
        for item in self.scene.selectedItems():
            if isinstance(item, PickerButtonItem):
                selected.append(item)
            elif isinstance(item, BackgroundImageItem) and not self._images_locked:
                selected.append(item)
        for item in selected:
            self.scene.removeItem(item)
        if selected:
            self._update_scene_rect()
        return len(selected)

    def _clone_button_from_data(self, data: dict, **overrides) -> PickerButtonItem:
        """Create a new button item from saved button data plus field overrides."""
        button_data = picker_core.make_button(
            label=overrides.get("label", data["label"]),
            x=overrides.get("x", data["x"]),
            y=overrides.get("y", data["y"]),
            w=overrides.get("w", data["w"]),
            h=overrides.get("h", data["h"]),
            color=overrides.get("color", data["color"]),
            targets=overrides.get("targets", data.get("targets", [])),
            corner_radius=overrides.get(
                "corner_radius",
                data.get("corner_radius", picker_core.DEFAULT_CORNER_RADIUS),
            ),
            font_size=overrides.get(
                "font_size",
                data.get("font_size", picker_core.DEFAULT_FONT_SIZE),
            ),
            font_bold=overrides.get(
                "font_bold",
                data.get("font_bold", picker_core.DEFAULT_FONT_BOLD),
            ),
            font_family=overrides.get(
                "font_family",
                data.get("font_family", picker_core.DEFAULT_FONT_FAMILY),
            ),
            text_dark=overrides.get(
                "text_dark",
                data.get("text_dark", picker_core.DEFAULT_TEXT_DARK),
            ),
        )
        item = PickerButtonItem(button_data, self._grid_size, edit_mode=True)
        self.scene.addItem(item)
        return item

    def _select_only(self, items: list[PickerButtonItem]) -> None:
        self.scene.clearSelection()
        for item in items:
            item.setSelected(True)
        self._update_scene_rect()

    def duplicate_selected(self) -> list[PickerButtonItem]:
        """Duplicate selected buttons, each offset to the right by its own width."""
        if not self._edit_mode:
            return []
        sources = self.selected_buttons()
        if not sources:
            return []

        duplicates = []
        for source in sources:
            data = source.to_data()
            duplicates.append(self._clone_button_from_data(data, x=data["x"] + data["w"]))

        self._select_only(duplicates)
        return duplicates

    def mirror_selected(self) -> list[PickerButtonItem]:
        """Create mirrored copies of selected buttons across the vertical (Y) axis.

        Position mirrors around x=0. Label and Maya targets swap L/R via swap_side_str.
        """
        if not self._edit_mode:
            return []
        sources = self.selected_buttons()
        if not sources:
            return []

        mirrors: list[PickerButtonItem] = []
        for source in sources:
            data = source.to_data()
            mirrors.append(
                self._clone_button_from_data(
                    data,
                    label=swap_side_str(str(data["label"])),
                    x=-int(data["x"]) - int(data["w"]),
                    targets=[swap_side_str(str(t)) for t in data.get("targets", [])],
                ),
            )

        self._select_only(mirrors)
        return mirrors

    @staticmethod
    def _button_center(button: PickerButtonItem) -> tuple[float, float]:
        return (
            button.grid_x() + button.cells_w() * 0.5,
            button.grid_y() + button.cells_h() * 0.5,
        )

    @staticmethod
    def _dist2_edge_to_grid_origin(button: PickerButtonItem) -> float:
        """Squared distance from grid origin (0,0) to the button's nearest edge/point."""
        x0 = float(button.grid_x())
        y0 = float(button.grid_y())
        x1 = x0 + float(button.cells_w())
        y1 = y0 + float(button.cells_h())
        # Closest point on the button rect to the grid center.
        nx = 0.0 if x0 <= 0.0 <= x1 else (x0 if 0.0 < x0 else x1)
        ny = 0.0 if y0 <= 0.0 <= y1 else (y0 if 0.0 < y0 else y1)
        return nx * nx + ny * ny

    def _center_most_button(self, buttons: list[PickerButtonItem]) -> PickerButtonItem:
        """Button whose edge is closest to the grid origin (green/red center)."""
        return min(
            buttons,
            key=lambda b: (self._dist2_edge_to_grid_origin(b), b.button_id),
        )

    def _layout_axis(self, buttons: list[PickerButtonItem], pivot: PickerButtonItem) -> str:
        """Dominant axis from sticky pivot toward the farthest-from-pivot button."""
        px, py = self._button_center(pivot)

        def _far_key(button: PickerButtonItem) -> tuple:
            bx, by = self._button_center(button)
            return ((bx - px) ** 2 + (by - py) ** 2, button.button_id)

        farthest = max(buttons, key=_far_key)
        fx, fy = self._button_center(farthest)
        return "x" if abs(fx - px) >= abs(fy - py) else "y"

    def _layout_pivot_button(
        self,
        buttons: list[PickerButtonItem],
    ) -> PickerButtonItem:
        """Shared sticky pivot for Separate + Rotate while selection is unchanged.

        First Layout op in a selection picks the grid-center-most button; later
        Separate/Rotate ops reuse that same button until the selection set changes.
        """
        sel_key = frozenset(b.button_id for b in buttons)
        if self._layout_pivot_id and self._layout_pivot_selection_key == sel_key:
            for button in buttons:
                if button.button_id == self._layout_pivot_id:
                    return button
        pivot = self._center_most_button(buttons)
        self._layout_pivot_id = pivot.button_id
        self._layout_pivot_selection_key = sel_key
        return pivot

    def adjust_distance_selected(self, delta: int) -> tuple[int, str]:
        """Stretch/compress selected buttons from the sticky Layout pivot.

        Pivot stays put (same sticky button as Rotate). Along the auto axis from
        pivot → farthest button, the 1st neighbor moves by ``delta``, the 2nd by
        ``2*delta``, etc. Returns ``(count, axis)``.
        """
        if not self._edit_mode:
            return 0, ""
        buttons = self.selected_buttons()
        if len(buttons) < 2:
            return 0, ""

        step = int(delta)
        if step == 0:
            return 0, ""

        pivot = self._layout_pivot_button(buttons)
        axis = self._layout_axis(buttons, pivot)

        if axis == "x":
            ordered = sorted(
                buttons,
                key=lambda b: (b.grid_x(), b.grid_y(), b.button_id),
            )
        else:
            ordered = sorted(
                buttons,
                key=lambda b: (b.grid_y(), b.grid_x(), b.button_id),
            )

        try:
            pivot_index = ordered.index(pivot)
        except ValueError:
            return 0, ""

        # Higher along axis: +1*step, +2*step, ...
        for rank, button in enumerate(ordered[pivot_index + 1 :], start=1):
            offset = rank * step
            if axis == "x":
                button.set_grid_pos(button.grid_x() + offset, button.grid_y())
            else:
                button.set_grid_pos(button.grid_x(), button.grid_y() + offset)

        # Lower along axis: -1*step, -2*step, ... (away from pivot when step > 0)
        for rank, button in enumerate(reversed(ordered[:pivot_index]), start=1):
            offset = -rank * step
            if axis == "x":
                button.set_grid_pos(button.grid_x() + offset, button.grid_y())
            else:
                button.set_grid_pos(button.grid_x(), button.grid_y() + offset)

        self._update_scene_rect()
        return len(buttons), axis

    def rotate_selected(self, degrees: int) -> int:
        """Rotate selected buttons 90° around the sticky Layout pivot's center.

        Pivot = sticky grid-center-most button (shared with Separate; reused until
        the selection set changes). All buttons orbit that center and swap
        width/height (so a long pivot button turns in place too).
        ``degrees``: ``+90`` CW / ``-90`` CCW.
        """
        if not self._edit_mode:
            return 0
        buttons = self.selected_buttons()
        if not buttons:
            return 0

        turns = int(degrees) // 90
        if turns == 0:
            return 0
        # Normalize to a single 90° step per click (CW positive).
        turns = 1 if turns > 0 else -1

        pivot = self._layout_pivot_button(buttons)
        px, py = self._button_center(pivot)

        for button in buttons:
            cx, cy = self._button_center(button)
            dx = cx - px
            dy = cy - py
            if turns > 0:
                # 90° clockwise: (dx, dy) -> (dy, -dx)
                ndx, ndy = dy, -dx
            else:
                # 90° counter-clockwise: (dx, dy) -> (-dy, dx)
                ndx, ndy = -dy, dx
            new_cx = px + ndx
            new_cy = py + ndy
            new_w = button.cells_h()
            new_h = button.cells_w()
            new_x = int(round(new_cx - new_w * 0.5))
            new_y = int(round(new_cy - new_h * 0.5))
            button.set_cells_size(new_w, new_h)
            button.set_grid_pos(new_x, new_y)

        self._update_scene_rect()
        return len(buttons)

    def set_grid_visible(self, visible: bool) -> None:
        self.view.set_grid_visible(visible)

    def set_image_snap(self, enabled: bool) -> None:
        """Snap background image centers to grid intersections when dragging."""
        self._image_snap = bool(enabled)
        for item in self.background_items():
            item.set_grid_size(self._grid_size)
            item.set_snap_enabled(self._image_snap)
        self._update_scene_rect()

    def set_images_locked(self, locked: bool) -> None:
        """When locked, backgrounds ignore clicks so button editing is safer."""
        self._images_locked = bool(locked)
        for item in self.background_items():
            item.set_locked(self._images_locked)

    def set_edit_mode(self, enabled: bool) -> None:
        self._edit_mode = bool(enabled)
        for item in self.button_items():
            item.set_edit_mode(self._edit_mode)
        for item in self.background_items():
            item.set_edit_mode(self._edit_mode)
        # Rubber-band multi-select in both edit and anim modes
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self._anim_rubber_band_mode = None
        self._anim_pre_rubber_selection = []
        if not self._edit_mode:
            self.scene.clearSelection()

    def is_edit_mode(self) -> bool:
        return self._edit_mode

    def combined_selected_targets(self) -> list[str]:
        """Deduped Maya targets from all currently selected picker buttons."""
        return picker_fns.combine_targets(
            *[button.targets for button in self.selected_buttons()],
        )

    def _next_free_cell(self) -> tuple[int, int]:
        occupied = {
            (
                int(round(item.pos().x() / self._grid_size)),
                int(round(item.pos().y() / self._grid_size)),
            )
            for item in self.button_items()
        }
        x = y = 0
        while (x, y) in occupied:
            x += picker_core.DEFAULT_BUTTON_W
            if x > NEW_BUTTON_ROW_WRAP:
                x = 0
                y += picker_core.DEFAULT_BUTTON_H + 1
        return x, y


class AnimPickerUI(DockableMayaUI):
    """Anim picker window: grid canvas + edit/save side panel."""

    SIDE_PANEL_WIDTH = 260
    _PLAIN_BTN_RGB = (65, 65, 65)
    _REFRESH_BTN_RGB = (50, 50, 52)

    def get_window_title(self) -> str:
        return _WINDOW_TITLE

    def get_settings_keys(self) -> dict:
        keys = {
            "show_grid_checkbox": self.show_grid_checkbox,
            "snap_images_checkbox": self.snap_images_checkbox,
            "lock_images_checkbox": self.lock_images_checkbox,
            "edit_mode_checkbox": self.edit_mode_checkbox,
            "save_on_close_checkbox": self.save_on_close_checkbox,
            "save_on_refresh_checkbox": self.save_on_refresh_checkbox,
            "font_scroll_checkbox": self.font_scroll_checkbox,
            "hierarchy_order_checkbox": self.hierarchy_order_checkbox,
            "side_panel_toggle": self.side_panel_toggle,
            "muted_button_colors": self.muted_colors_setting,
            "target_find_input": self.target_find_input,
            "target_replace_input": self.target_replace_input,
        }
        for name, toggle in self._section_toggles.items():
            keys[f"section_{name}"] = toggle
        return keys

    def load_settings(self) -> None:
        """Load prefs; default Show Grid / Edit Mode / Save on Close to on when unset."""
        super().load_settings()
        self.settings.beginGroup(self.get_object_name())
        if not self.settings.contains("show_grid_checkbox"):
            self.show_grid_checkbox.setChecked(True)
        if not self.settings.contains("edit_mode_checkbox"):
            self.edit_mode_checkbox.setChecked(True)
        if not self.settings.contains("save_on_close_checkbox"):
            self.save_on_close_checkbox.setChecked(True)
        if not self.settings.contains("side_panel_toggle"):
            self.side_panel_toggle.setChecked(True)
        # Sections default expanded except Help
        for name, toggle in self._section_toggles.items():
            key = f"section_{name}"
            if not self.settings.contains(key):
                toggle.setChecked(name != "help")
        self.settings.endGroup()
        self._apply_loaded_muted_colors()
        self.canvas.set_grid_visible(self.show_grid_checkbox.isChecked())
        self.canvas.set_image_snap(self.snap_images_checkbox.isChecked())
        self.canvas.set_images_locked(self.lock_images_checkbox.isChecked())
        self.canvas.set_edit_mode(self.edit_mode_checkbox.isChecked())
        self._set_edit_widgets_enabled(self.edit_mode_checkbox.isChecked())
        self._apply_side_panel_visible(self.side_panel_toggle.isChecked())
        self._apply_font_scroll_enabled(self.font_scroll_checkbox.isChecked())

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI setup."""
        self._picker_io = picker_core.AnimPickerData()
        self._saved_on_close = False
        self._skip_save_on_close = False
        self._copied_color: QColor | None = None
        self._copied_font: dict | None = None
        self._active_namespace = ""

        body = QHBoxLayout()
        body.setSpacing(0)
        body.setContentsMargins(0, 0, 0, 0)

        self.canvas = PickerCanvas()
        self.canvas.setMinimumWidth(0)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.selection_changed.connect(self._on_selection_changed)
        self.canvas.anim_selection_committed.connect(self.on_anim_selection_committed)
        body.addWidget(self.canvas, stretch=1)
        body.addWidget(self._build_side_panel_host(), stretch=0)

        layout.addLayout(body, 1)

        self._refresh_rig_context_ui(autoload=True)
        self._on_selection_changed()

    def _build_side_panel_host(self) -> QWidget:
        """Side panel plus a thin edge toggle to show/hide the whole panel."""
        host = QWidget()
        host.setMinimumWidth(0)
        host_layout = QHBoxLayout(host)
        host_layout.setContentsMargins(0, 0, 0, 0)
        host_layout.setSpacing(0)

        self.side_panel_toggle = QToolButton()
        self.side_panel_toggle.setCheckable(True)
        self.side_panel_toggle.setChecked(True)
        self.side_panel_toggle.setArrowType(Qt.LeftArrow)
        self.side_panel_toggle.setToolTip("Hide side panel")
        self.side_panel_toggle.setFixedWidth(18)
        self.side_panel_toggle.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.side_panel_toggle.setStyleSheet(
            "QToolButton {"
            "  background-color: rgb(60, 60, 60);"
            "  border: none;"
            "  border-left: 1px solid rgb(90, 90, 90);"
            "  border-right: 1px solid rgb(90, 90, 90);"
            "  color: rgb(210, 210, 210);"
            "}"
            "QToolButton:hover { background-color: rgb(80, 80, 80); }"
            "QToolButton:checked { background-color: rgb(60, 60, 60); }",
        )
        self.side_panel_toggle.toggled.connect(self.on_side_panel_toggled)

        self.side_panel = self._build_side_panel()

        host_layout.addWidget(self.side_panel_toggle)
        host_layout.addWidget(self.side_panel, stretch=1)
        return host

    def _apply_side_panel_visible(self, visible: bool) -> None:
        self.side_panel.setVisible(visible)
        # Open: ◀ hide panel. Closed: ▶ show panel.
        self.side_panel_toggle.setArrowType(Qt.LeftArrow if visible else Qt.RightArrow)
        self.side_panel_toggle.setToolTip(
            "Hide side panel" if visible else "Show side panel",
        )

    def on_side_panel_toggled(self, visible: bool) -> None:
        self._apply_side_panel_visible(visible)
        self.save_settings()

    def _build_side_panel(self) -> QWidget:
        """Scrollable side panel with collapsible sections; can shrink with the window."""
        self._section_toggles: dict[str, QToolButton] = {}

        content = QWidget()
        content.setStyleSheet("background-color: rgb(70, 70, 70);")
        content.setMinimumWidth(0)
        # Ignored horizontal: follow scroll viewport width (avoids right-edge clip when scrollbar shows).
        content.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        panel_layout = QVBoxLayout(content)
        panel_layout.setContentsMargins(8, 8, 8, 8)
        panel_layout.setSpacing(6)

        # ----- Rig Context -----
        rig_layout = self._add_collapsible_section(panel_layout, "Rig Context", "rig_context")

        self.rig_context_combo = QComboBox()
        self.rig_context_combo.setMinimumWidth(0)
        self.rig_context_combo.setToolTip(
            "Active character/rig from rig_context.json. "
            "Changing this sets the active rig and loads its anim_picker JSON.",
        )
        self.rig_context_combo.setStyleSheet(self._combo_stylesheet())
        self.rig_context_combo.currentIndexChanged.connect(self.on_rig_context_changed)
        rig_layout.addWidget(self.rig_context_combo)

        self.namespace_combo = QComboBox()
        self.namespace_combo.setMinimumWidth(0)
        self.namespace_combo.setToolTip(
            "Rig Context namespace (e.g. a referenced character). "
            "Only this namespace is stripped when assigning targets and "
            "re-applied on select. Nested import namespaces are kept "
            "(e.g. tubeClaw_left_rig:ctrl).",
        )
        self.namespace_combo.setStyleSheet(self._combo_stylesheet())
        self.namespace_combo.currentIndexChanged.connect(self.on_namespace_changed)
        rig_layout.addWidget(self.namespace_combo)

        rig_refresh_row = QHBoxLayout()
        self.refresh_rig_btn = self._action_button(
            "Refresh",
            self.on_refresh_rig_context,
            help_note=(
                "Reload rig list from rig_context.json and scene namespaces, "
                "then autoload the active rig's picker."
            ),
        )
        self.refresh_rig_btn.setStyleSheet(self._tinted_button_stylesheet(*self._REFRESH_BTN_RGB))
        rig_refresh_row.addWidget(self.refresh_rig_btn, stretch=1)

        self.save_on_refresh_checkbox = self._checkbox("Save on Refresh")
        self.save_on_refresh_checkbox.setChecked(False)
        self.save_on_refresh_checkbox.setToolTip(
            "When on, save the current picker before Refresh reloads from disk. "
            "Turn off to reload a manually edited JSON without overwriting it.",
        )
        self.save_on_refresh_checkbox.toggled.connect(self.on_save_on_refresh_toggled)
        rig_refresh_row.addWidget(self.save_on_refresh_checkbox, stretch=1)
        rig_layout.addLayout(rig_refresh_row)

        open_row = QHBoxLayout()
        self.open_rig_btn = self._action_button(
            "Open Rig",
            self.on_open_rig_file,
            help_note=(
                "Open the selected character's saved *_rig.ma file "
                "(next to the auto-rig folder). Replaces the current scene."
            ),
        )
        self.open_rig_context_ui_btn = self._action_button(
            "Rig Context UI",
            self.on_open_rig_context_ui,
            help_note="Open the Rig Context UI to manage rigs and active folder.",
        )
        self.open_rig_context_ui_btn.setStyleSheet(
            self._tinted_button_stylesheet(*self._REFRESH_BTN_RGB),
        )
        open_row.addWidget(self.open_rig_btn, stretch=1)
        open_row.addWidget(self.open_rig_context_ui_btn, stretch=1)
        rig_layout.addLayout(open_row)

        # ----- Mode -----
        mode_layout = self._add_collapsible_section(panel_layout, "Mode", "mode")
        self.edit_mode_checkbox = self._checkbox("Edit Mode")
        self.edit_mode_checkbox.setChecked(True)
        self.edit_mode_checkbox.setToolTip(
            "On: move, resize, and edit buttons.\n"
            "Off: animation mode — click buttons to select targets.",
        )
        self.edit_mode_checkbox.toggled.connect(self.on_edit_mode_toggled)
        mode_layout.addWidget(self.edit_mode_checkbox)

        # ----- Edit -----
        edit_layout = self._add_collapsible_section(panel_layout, "Edit", "edit")
        self.add_button_btn = self._action_button(
            "Add Button",
            self.on_add_button,
            help_note="Add a new empty picker button at the next free grid cell.",
        )
        self.add_from_selection_btn = self._action_button(
            "Add Selection",
            self.on_add_from_selection,
            help_note=(
                "Create one blank dark-red square button per Maya-selected object. "
                "Order follows Maya selection unless Hierarchy Order is on "
                "(then Outliner/hierarchy order). Each object becomes that button's target."
            ),
        )
        self.hierarchy_order_checkbox = self._checkbox("Hierarchy Order")
        self.hierarchy_order_checkbox.setChecked(False)
        self.hierarchy_order_checkbox.setToolTip(
            "When on, Add Selection lays out buttons in Outliner/hierarchy order. "
            "When off (default), uses pure Maya selection order.",
        )
        self.hierarchy_order_checkbox.toggled.connect(self.save_settings)
        self.add_from_group_selection_btn = self._action_button(
            "Add Group Selection",
            self.on_add_from_group_selection,
            help_note=(
                "Create one blank dark-yellow square button "
                "(twice the Add Selection size) and assign all "
                "Maya-selected objects as its targets."
            ),
        )
        self.duplicate_button_btn = self._action_button(
            "Duplicate",
            self.on_duplicate_selected,
            help_note="Duplicate the selected picker button(s).",
        )
        self.mirror_button_btn = self._action_button(
            "Mirror",
            self.on_mirror_selected,
            help_note=(
                "Create copies of selected buttons mirrored across the vertical center axis. "
                "Swaps left/right in names and Maya targets (e.g. _l ↔ _r)."
            ),
        )
        self.delete_button_btn = self._action_button(
            "Delete Buttons",
            self.on_delete_selected,
            help_note="Delete selected picker buttons and/or unlocked backgrounds.",
        )
        edit_layout.addWidget(self.add_button_btn)
        add_sel_row = QHBoxLayout()
        add_sel_row.addWidget(self.add_from_selection_btn, stretch=1)
        add_sel_row.addWidget(self.hierarchy_order_checkbox, stretch=0)
        edit_layout.addLayout(add_sel_row)
        edit_layout.addWidget(self.add_from_group_selection_btn)
        dup_mirror_row = QHBoxLayout()
        dup_mirror_row.addWidget(self.duplicate_button_btn)
        dup_mirror_row.addWidget(self.mirror_button_btn)
        edit_layout.addLayout(dup_mirror_row)
        edit_layout.addWidget(self.delete_button_btn)

        label_row = QHBoxLayout()
        label_row.addWidget(self._field_label("Name:"))
        self.label_input = QLineEdit()
        self.label_input.setPlaceholderText("Button name")
        self.label_input.editingFinished.connect(self.on_label_edited)
        self.label_input.setStyleSheet(self._line_edit_stylesheet())
        label_row.addWidget(self.label_input)
        edit_layout.addLayout(label_row)

        self.rename_from_target_btn = self._action_button(
            "Rename from Target",
            self.on_rename_from_first_target,
            help_note=(
                "Set each selected button's name to the short name of its first assigned target."
            ),
        )
        edit_layout.addWidget(self.rename_from_target_btn)

        # ----- Targets -----
        targets_layout = self._add_collapsible_section(panel_layout, "Targets", "targets")
        self.assign_targets_btn = self._action_button(
            "Assign Selection",
            self.on_assign_selection,
            help_note=(
                "Assign the current Maya selection to the selected picker button(s). "
                "Only the Rig Context namespace is stripped; nested import namespaces are kept."
            ),
        )
        self.clear_targets_btn = self._action_button(
            "Clear Targets",
            self.on_clear_targets,
            help_note="Remove assigned Maya objects from selected buttons.",
        )
        targets_layout.addWidget(self.assign_targets_btn)
        targets_layout.addWidget(self.clear_targets_btn)

        replace_row = QHBoxLayout()
        self.target_find_input = QLineEdit()
        self.target_find_input.setPlaceholderText("Find")
        self.target_find_input.setMinimumWidth(0)
        self.target_find_input.setToolTip(
            "Substring to find in target names on selected buttons "
            '(e.g. "left").',
        )
        self.target_find_input.setStyleSheet(self._line_edit_stylesheet())
        self.target_find_input.editingFinished.connect(self.save_settings)
        self.target_replace_input = QLineEdit()
        self.target_replace_input.setPlaceholderText("Replace")
        self.target_replace_input.setMinimumWidth(0)
        self.target_replace_input.setToolTip(
            "Replacement substring "
            '(e.g. "center"). Leave empty to remove the find text.',
        )
        self.target_replace_input.setStyleSheet(self._line_edit_stylesheet())
        self.target_replace_input.editingFinished.connect(self.save_settings)
        self.replace_targets_btn = self._action_button(
            "Replace",
            self.on_replace_targets,
            help_note="Replace find→replace in all targets on the selected picker button(s).",
        )
        replace_row.addWidget(self.target_find_input, stretch=1)
        replace_row.addWidget(self.target_replace_input, stretch=1)
        replace_row.addWidget(self.replace_targets_btn, stretch=0)
        targets_layout.addLayout(replace_row)

        self.targets_label = QLabel("Targets: (none)")
        self.targets_label.setWordWrap(True)
        self.targets_label.setStyleSheet(
            "background-color: transparent; border: none; color: rgb(180, 180, 180);",
        )
        targets_layout.addWidget(self.targets_label)

        # ----- Layout -----
        layout_section = self._add_collapsible_section(panel_layout, "Layout", "layout")
        separate_row = QHBoxLayout()
        separate_row.addWidget(self._field_label("Separate:"), stretch=0)
        self.increase_distance_btn = self._action_button(
            "",
            lambda: self.on_adjust_distance(LAYOUT_DISTANCE_STEP),
            help_note=(
                "Nearest neighbor moves 1 cell from the pivot, next 2, next 3, etc. "
                "Uses the same sticky Layout pivot as Rotate (first op picks closest to "
                "grid center; reused until selection changes). Axis auto-detected."
            ),
            help_title="Separate → (Increase)",
        )
        self.decrease_distance_btn = self._action_button(
            "",
            lambda: self.on_adjust_distance(-LAYOUT_DISTANCE_STEP),
            help_note=(
                "Nearest neighbor moves 1 cell toward the pivot, next 2, etc. "
                "Uses the same sticky Layout pivot as Rotate (first op picks closest to "
                "grid center; reused until selection changes). Axis auto-detected."
            ),
            help_title="Separate ← (Decrease)",
        )
        self.increase_distance_btn.setIcon(self._separate_arrow_icon("right", size=14))
        self.decrease_distance_btn.setIcon(self._separate_arrow_icon("left", size=14))
        for btn in (self.increase_distance_btn, self.decrease_distance_btn):
            btn.setIconSize(QSize(14, 14))
            btn.setMinimumWidth(36)
            btn.setMaximumWidth(40)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setStyleSheet(
                self._tinted_button_stylesheet(*self._PLAIN_BTN_RGB)
                + "QPushButton {"
                "  text-align: center;"
                "  padding: 3px 6px;"
                "}"
            )
        separate_row.addWidget(self.increase_distance_btn, stretch=0)
        separate_row.addWidget(self.decrease_distance_btn, stretch=0)
        separate_row.addStretch(1)
        layout_section.addLayout(separate_row)

        rotate_row = QHBoxLayout()
        rotate_row.addWidget(self._field_label("Rotate:"), stretch=0)
        self.rotate_ccw_btn = self._action_button(
            "",
            lambda: self.on_rotate_selected(-90),
            help_note=(
                "Rotate selected button(s) 90° counter-clockwise around the pivot "
                "button's center (works on a single rectangular button too). Shares the "
                "sticky Layout pivot with Separate when multiple are selected."
            ),
            help_title="Rotate ↺ (CCW)",
        )
        self.rotate_cw_btn = self._action_button(
            "",
            lambda: self.on_rotate_selected(90),
            help_note=(
                "Rotate selected button(s) 90° clockwise around the pivot button's "
                "center (works on a single rectangular button too). Shares the sticky "
                "Layout pivot with Separate when multiple are selected."
            ),
            help_title="Rotate ↻ (CW)",
        )
        self.rotate_ccw_btn.setIcon(self._rotate_arrow_icon("ccw", size=14))
        self.rotate_cw_btn.setIcon(self._rotate_arrow_icon("cw", size=14))
        for btn in (self.rotate_ccw_btn, self.rotate_cw_btn):
            btn.setIconSize(QSize(14, 14))
            btn.setMinimumWidth(36)
            btn.setMaximumWidth(40)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setStyleSheet(
                self._tinted_button_stylesheet(*self._PLAIN_BTN_RGB)
                + "QPushButton {"
                "  text-align: center;"
                "  padding: 3px 6px;"
                "}"
            )
        rotate_row.addWidget(self.rotate_ccw_btn, stretch=0)
        rotate_row.addWidget(self.rotate_cw_btn, stretch=0)
        rotate_row.addStretch(1)
        layout_section.addLayout(rotate_row)

        # ----- Style -----
        style_layout = self._add_collapsible_section(panel_layout, "Style", "style")
        self.pick_color_btn = self._action_button(
            "Pick Color...",
            self.on_pick_color,
            help_note="Open a color dialog and apply the chosen color to selected buttons.",
        )
        self.pick_color_btn.setStyleSheet(self._pick_color_button_stylesheet())
        style_layout.addWidget(self.pick_color_btn)

        self._muted_colors = picker_core.copy_muted_button_colors()
        self._muted_selected_index = 0
        # Hidden field persisted by DockableMayaUI get_settings_keys / QSettings.
        self.muted_colors_setting = QLineEdit(self)
        self.muted_colors_setting.hide()
        self.muted_colors_setting.setText(picker_core.serialize_muted_colors(self._muted_colors))

        preset_row = QHBoxLayout()
        preset_row.setSpacing(2)
        self._muted_swatch_buttons: list[QToolButton] = []
        for i in range(len(self._muted_colors)):
            btn = QToolButton()
            btn.setAutoRaise(True)
            btn.setFixedHeight(18)
            btn.setMinimumWidth(0)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setToolTip(
                f"Preset {i + 1}: click to select and apply to selected buttons.",
            )
            btn.clicked.connect(lambda _checked=False, idx=i: self.on_apply_muted_preset(idx))
            preset_row.addWidget(btn)
            self._muted_swatch_buttons.append(btn)
        style_layout.addLayout(preset_row)
        self._refresh_muted_color_ui(selected_index=0)

        self.update_swatch_btn = self._action_button(
            "Update Color Swatch",
            self.on_update_color_swatch,
            help_note=(
                "Set the selected swatch to the color of the first selected button. "
                "Saved with tool prefs on Save / Save on Close / Save on Refresh."
            ),
        )
        style_layout.addWidget(self.update_swatch_btn)

        color_row = QHBoxLayout()
        self.copy_color_btn = self._action_button(
            "Copy Color",
            self.on_copy_color,
            help_note="Copy color from the first selected button.",
        )
        self.paste_color_btn = self._action_button(
            "Paste Color",
            self.on_paste_color,
            help_note="Paste copied color onto all selected buttons.",
        )
        color_row.addWidget(self.copy_color_btn, stretch=1)
        color_row.addWidget(self.paste_color_btn, stretch=1)
        style_layout.addLayout(color_row)

        round_row = QHBoxLayout()
        round_row.addWidget(self._field_label("Round:"))
        self.corner_radius_slider = WheelGatedSlider(Qt.Horizontal, wheel_scroll_enabled=False)
        self.corner_radius_slider.setRange(0, picker_core.MAX_CORNER_RADIUS)
        self.corner_radius_slider.setValue(picker_core.DEFAULT_CORNER_RADIUS)
        self.corner_radius_slider.setToolTip(
            "Corner roundness for selected buttons. "
            "At max (and equal width/height), the button becomes a circle. "
            "Mouse-wheel changes require Font Scroll.",
        )
        self.corner_radius_slider.valueChanged.connect(self.on_corner_radius_changed)
        self.corner_radius_slider.setStyleSheet(self._slider_stylesheet())
        self.corner_radius_slider.setMinimumWidth(0)
        round_row.addWidget(self.corner_radius_slider, stretch=1)
        self.corner_radius_value = self._plain_label("0")
        self.corner_radius_value.setFixedWidth(40)
        self.corner_radius_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        round_row.addWidget(self.corner_radius_value)
        style_layout.addLayout(round_row)

        self.font_family_combo = WheelGatedFontComboBox(wheel_scroll_enabled=False)
        self.font_family_combo.setMinimumWidth(0)
        self.font_family_combo.setCurrentFont(QFont(picker_core.DEFAULT_FONT_FAMILY))
        self.font_family_combo.setToolTip(
            "Font family for selected buttons. "
            "Mouse-wheel scrolling is off unless Font Scroll is enabled.",
        )
        self.font_family_combo.currentFontChanged.connect(self.on_font_family_changed)
        self.font_family_combo.setStyleSheet(self._combo_stylesheet())
        style_layout.addWidget(self.font_family_combo)

        self.font_scroll_checkbox = self._checkbox("Font Scroll")
        self.font_scroll_checkbox.setChecked(False)
        self.font_scroll_checkbox.setToolTip(
            "When on, the mouse wheel can change font family, size, and roundness. "
            "Off by default so scrolling the side panel does not change style by accident.",
        )
        self.font_scroll_checkbox.toggled.connect(self.on_font_scroll_toggled)
        style_layout.addWidget(self.font_scroll_checkbox)

        font_row = QHBoxLayout()
        font_row.addWidget(self._field_label("Size:"))
        self.font_size_slider = WheelGatedSlider(Qt.Horizontal, wheel_scroll_enabled=False)
        self.font_size_slider.setRange(picker_core.MIN_FONT_SIZE, picker_core.MAX_FONT_SIZE)
        self.font_size_slider.setValue(picker_core.DEFAULT_FONT_SIZE)
        self.font_size_slider.setToolTip(
            "Label font size for selected buttons. "
            "Mouse-wheel changes require Font Scroll.",
        )
        self.font_size_slider.valueChanged.connect(self.on_font_size_changed)
        self.font_size_slider.setStyleSheet(self._slider_stylesheet())
        self.font_size_slider.setMinimumWidth(0)
        font_row.addWidget(self.font_size_slider, stretch=1)
        self.font_size_value = self._plain_label(str(picker_core.DEFAULT_FONT_SIZE))
        self.font_size_value.setFixedWidth(36)
        self.font_size_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        font_row.addWidget(self.font_size_value)
        style_layout.addLayout(font_row)

        font_style_row = QHBoxLayout()
        self.font_bold_checkbox = self._checkbox("Bold")
        self.font_bold_checkbox.setChecked(picker_core.DEFAULT_FONT_BOLD)
        self.font_bold_checkbox.setToolTip("Bold label text for selected buttons.")
        self.font_bold_checkbox.toggled.connect(self.on_font_bold_toggled)
        font_style_row.addWidget(self.font_bold_checkbox, stretch=1)

        self.text_dark_checkbox = self._checkbox("Black Text")
        self.text_dark_checkbox.setChecked(picker_core.DEFAULT_TEXT_DARK)
        self.text_dark_checkbox.setToolTip(
            "Off: white label text. On: black label text.",
        )
        self.text_dark_checkbox.toggled.connect(self.on_text_dark_toggled)
        font_style_row.addWidget(self.text_dark_checkbox, stretch=1)
        style_layout.addLayout(font_style_row)

        font_copy_row = QHBoxLayout()
        self.copy_font_btn = self._action_button(
            "Copy Font",
            self.on_copy_font,
            help_note=(
                "Copy font family, size, bold, and text color from the first selected button."
            ),
        )
        self.paste_font_btn = self._action_button(
            "Paste Font",
            self.on_paste_font,
            help_note="Paste copied font onto all selected buttons.",
        )
        font_copy_row.addWidget(self.copy_font_btn, stretch=1)
        font_copy_row.addWidget(self.paste_font_btn, stretch=1)
        style_layout.addLayout(font_copy_row)

        # ----- Background Images -----
        bg_layout = self._add_collapsible_section(panel_layout, "Background Images", "backgrounds")

        bg_toggle_row = QHBoxLayout()
        self.snap_images_checkbox = self._checkbox("Snap Images")
        self.snap_images_checkbox.setChecked(False)
        self.snap_images_checkbox.setToolTip(
            "When on, each background image's center snaps to grid intersections "
            "(so you can align it to the green/red center axes).",
        )
        self.snap_images_checkbox.toggled.connect(self.on_image_snap_toggled)
        bg_toggle_row.addWidget(self.snap_images_checkbox, stretch=1)

        self.lock_images_checkbox = self._checkbox("Lock Images")
        self.lock_images_checkbox.setChecked(False)
        self.lock_images_checkbox.setToolTip(
            "When on, background images cannot be selected or moved "
            "(clicks pass through so you can edit buttons freely).",
        )
        self.lock_images_checkbox.toggled.connect(self.on_lock_images_toggled)
        bg_toggle_row.addWidget(self.lock_images_checkbox, stretch=1)
        bg_layout.addLayout(bg_toggle_row)

        self.background_combo = WheelGatedComboBox(wheel_scroll_enabled=False)
        self.background_combo.setMinimumWidth(0)
        self.background_combo.setToolTip(
            "JPG/PNG files in the rig's anim_picker/ folder. "
            "Use Add to place one on the canvas; you can add several. "
            "Mouse-wheel scrolling is disabled (click to choose).",
        )
        self.background_combo.setStyleSheet(self._combo_stylesheet())
        bg_layout.addWidget(self.background_combo)

        bg_add_row = QHBoxLayout()
        self.add_bg_btn = self._action_button(
            "Add",
            self.on_add_background,
            help_note="Add the selected folder image to the canvas.",
        )
        self.remove_bg_btn = self._action_button(
            "Remove",
            self.on_remove_background,
            help_note=(
                "Remove selected background image(s) from the canvas (or press Delete)."
            ),
        )
        bg_add_row.addWidget(self.add_bg_btn, stretch=1)
        bg_add_row.addWidget(self.remove_bg_btn, stretch=1)
        bg_layout.addLayout(bg_add_row)

        bg_order_row = QHBoxLayout()
        self.bg_forward_btn = self._action_button(
            "Forward",
            self.on_background_forward,
            help_note=(
                "Bring selected background image(s) one step forward "
                "(in front of the next one)."
            ),
        )
        self.bg_back_btn = self._action_button(
            "Back",
            self.on_background_back,
            help_note=(
                "Send selected background image(s) one step back "
                "(behind the previous one)."
            ),
        )
        bg_order_row.addWidget(self.bg_forward_btn, stretch=1)
        bg_order_row.addWidget(self.bg_back_btn, stretch=1)
        bg_layout.addLayout(bg_order_row)

        bg_edit_row = QHBoxLayout()
        self.duplicate_bg_btn = self._action_button(
            "Duplicate",
            self.on_duplicate_background,
            help_note=(
                "Duplicate selected background image(s), offset to the right by image width."
            ),
        )
        self.rotate_bg_btn = self._action_button(
            "Rotate 90°",
            self.on_rotate_background,
            help_note=(
                "Rotate selected background image(s) 90° clockwise. Saved with the picker."
            ),
        )
        self.mirror_bg_btn = self._action_button(
            "Mirror",
            self.on_mirror_background,
            help_note=(
                "Create mirrored copies across the vertical center axis "
                "(flips horizontally, like button Mirror)."
            ),
        )
        bg_edit_row.addWidget(self.duplicate_bg_btn, stretch=1)
        bg_edit_row.addWidget(self.rotate_bg_btn, stretch=1)
        bg_edit_row.addWidget(self.mirror_bg_btn, stretch=1)
        bg_layout.addLayout(bg_edit_row)

        bg_util_row = QHBoxLayout()
        self.refresh_bg_btn = self._action_button(
            "Refresh",
            self.on_refresh_backgrounds,
            help_note="Rescan the rig's anim_picker/ folder for images.",
        )
        self.refresh_bg_btn.setStyleSheet(self._tinted_button_stylesheet(*self._REFRESH_BTN_RGB))
        self.clear_bg_btn = self._action_button(
            "Clear All",
            self.on_clear_backgrounds,
            help_note="Remove all background images from the canvas.",
        )
        bg_util_row.addWidget(self.refresh_bg_btn, stretch=1)
        bg_util_row.addWidget(self.clear_bg_btn, stretch=1)
        bg_layout.addLayout(bg_util_row)

        # ----- Display -----
        display_layout = self._add_collapsible_section(panel_layout, "Display", "display")
        self.show_grid_checkbox = self._checkbox("Show Grid")
        self.show_grid_checkbox.setChecked(True)
        self.show_grid_checkbox.setToolTip("Toggle light grey grid lines on the picker canvas.")
        self.show_grid_checkbox.toggled.connect(self.on_grid_toggled)
        display_layout.addWidget(self.show_grid_checkbox)

        self.center_view_btn = self._action_button(
            "Center View",
            self.on_center_view,
            help_note=(
                "Jump the canvas to the grid origin (green/red center lines). Keeps current zoom."
            ),
        )
        display_layout.addWidget(self.center_view_btn)

        # ----- File -----
        file_layout = self._add_collapsible_section(panel_layout, "File", "file")
        self.save_on_close_checkbox = self._checkbox("Save on Close")
        self.save_on_close_checkbox.setChecked(True)
        self.save_on_close_checkbox.setToolTip(
            "When on, automatically save the picker JSON when the window is closed.",
        )
        self.save_on_close_checkbox.toggled.connect(self.on_save_on_close_toggled)
        file_layout.addWidget(self.save_on_close_checkbox)

        file_io_row = QHBoxLayout()
        save_btn = self._action_button(
            "Save",
            self.on_save,
            help_note="Save the picker layout JSON for the active Rig Context.",
        )
        save_btn.setStyleSheet(self._tinted_button_stylesheet(49, 52, 50))
        load_btn = self._action_button(
            "Load",
            self.on_load,
            help_note="Reload the picker layout JSON for the active Rig Context from disk.",
        )
        load_btn.setStyleSheet(self._tinted_button_stylesheet(53, 52, 48))
        file_io_row.addWidget(save_btn, stretch=1)
        file_io_row.addWidget(load_btn, stretch=1)
        file_layout.addLayout(file_io_row)

        self.refresh_file_btn = self._action_button(
            "Refresh",
            self.on_refresh_file,
            help_note=(
                "Reload the current anim_picker JSON from disk "
                "(picks up manual edits to the file)."
            ),
        )
        self.refresh_file_btn.setStyleSheet(self._tinted_button_stylesheet(*self._REFRESH_BTN_RGB))
        file_layout.addWidget(self.refresh_file_btn)

        status_header = self._sub_label("--- Status ---")
        status_header.setAlignment(Qt.AlignCenter)
        file_layout.addWidget(status_header)

        self.status_label = self._console_label("Ready")
        self.status_label.setToolTip("Status messages from picker actions.")
        file_layout.addWidget(self.status_label)

        # ----- Help -----
        help_layout = self._add_collapsible_section(panel_layout, "Help", "help")
        self.help_context_label = self._console_label(
            "Click a tool button to see notes for that action.",
        )
        help_layout.addWidget(self.help_context_label)
        self.help_generic_label = QLabel(
            "<b>Rig Context:</b> pick active rig "
            "(loads its anim_picker JSON).<br><br>"
            "<b>Namespace:</b> only the Rig Context "
            "namespace is stripped/applied; "
            "nested import namespaces are kept.<br><br>"
            "<b>Edit Mode:</b> assign targets, "
            "move/resize buttons &amp; images "
            "(corner-drag resizes all selected by the "
            "same amount).<br><br>"
            "<b>Layout:</b> Separate and Rotate share a "
            "sticky pivot (closest to grid center on first "
            "use; kept until selection changes).<br><br>"
            "<b>Shift</b> adds, <b>Ctrl</b> removes buttons "
            "from the picker selection "
            "(click or drag) in Edit and Anim.<br><br>"
            "<b>Middle-mouse</b> pan. <b>Wheel</b> zoom.",
        )
        self.help_generic_label.setTextFormat(Qt.RichText)
        self.help_generic_label.setWordWrap(True)
        self.help_generic_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.help_generic_label.setStyleSheet(
            "QLabel {"
            "  background-color: rgb(58, 58, 58);"
            "  color: rgb(200, 200, 200);"
            "  border: 1px solid rgb(85, 85, 85);"
            "  border-radius: 4px;"
            "  padding: 6px 8px;"
            "  font-size: 11px;"
            "}"
        )
        help_layout.addWidget(self.help_generic_label)

        # ----- Functions/UIs -----
        functions_layout = self._add_collapsible_section(
            panel_layout,
            "Functions/UIs",
            "functions",
        )
        self.reset_all_controls_btn = self._action_button(
            "Reset All Controls",
            self.on_reset_all_controls,
            help_note=(
                "Resets selected ctrls and their descendants, or all ctrls under groups "
                'containing "_rigGrp" if nothing is selected. Resets translate, rotate, '
                "and scale (plus a small set of custom attrs)."
            ),
        )
        functions_layout.addWidget(self.reset_all_controls_btn)

        self.space_matcher_ui_btn = self._action_button(
            "Space Matcher UI",
            self.on_open_space_matcher_ui,
            help_note=(
                "Open the Space Matcher UI for parent-space switch matching. "
                "Keeps ctrl transforms when switching parent spaces."
            ),
        )
        self.space_matcher_ui_btn.setStyleSheet(
            self._tinted_button_stylesheet(*self._REFRESH_BTN_RGB),
        )
        functions_layout.addWidget(self.space_matcher_ui_btn)

        panel_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setFixedWidth(self.SIDE_PANEL_WIDTH)
        scroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        scroll.setStyleSheet("QScrollArea { background-color: rgb(70, 70, 70); border: none; }")
        return scroll

    def _add_collapsible_section(
        self,
        parent_layout: QVBoxLayout,
        title: str,
        key: str,
    ) -> QVBoxLayout:
        """Add a collapsible section; returns the content layout for widgets."""
        section = QWidget()
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(4)

        toggle = QToolButton()
        toggle.setText(title)
        toggle.setCheckable(True)
        toggle.setChecked(True)
        toggle.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toggle.setArrowType(Qt.DownArrow)
        toggle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        toggle.setStyleSheet(
            "QToolButton {"
            "  background-color: rgb(55, 55, 55);"
            "  color: rgb(220, 220, 220);"
            "  border: 1px solid rgb(90, 90, 90);"
            "  border-radius: 4px;"
            "  padding: 4px 6px;"
            "  font-weight: bold;"
            "  text-align: left;"
            "}"
            "QToolButton:hover { background-color: rgb(65, 65, 65); }",
        )

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(4, 2, 0, 4)
        body_layout.setSpacing(6)

        def _on_toggled(expanded: bool, button=toggle, content=body, name=key) -> None:
            content.setVisible(expanded)
            button.setArrowType(Qt.DownArrow if expanded else Qt.RightArrow)
            self.save_settings()

        toggle.toggled.connect(_on_toggled)
        self._section_toggles[key] = toggle

        section_layout.addWidget(toggle)
        section_layout.addWidget(body)
        parent_layout.addWidget(section)
        return body_layout

    def _plain_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(
            "background-color: transparent; border: none; color: rgb(210, 210, 210);",
        )
        return label

    def _field_label(self, text: str) -> QLabel:
        """Name/Round/Size style labels matching plain button grey."""
        r, g, b = self._PLAIN_BTN_RGB
        label = QLabel(text)
        label.setStyleSheet(
            "QLabel {"
            f"  background-color: rgb({r}, {g}, {b});"
            "  color: rgb(210, 210, 210);"
            "  border: 2px solid rgb(80, 80, 80);"
            "  border-radius: 8px;"
            "  padding: 3px 10px;"
            "  font-size: 12px;"
            "}"
        )
        return label

    @staticmethod
    def _line_edit_stylesheet() -> str:
        return (
            "QLineEdit {"
            "  background-color: rgb(45, 45, 45);"
            "  color: rgb(220, 220, 220);"
            "  border: 1px solid rgb(90, 90, 90);"
            "  border-radius: 4px;"
            "  padding: 3px 6px;"
            "  selection-background-color: rgb(70, 70, 70);"
            "}"
            "QLineEdit:disabled {"
            "  background-color: rgb(55, 55, 55);"
            "  color: rgb(140, 140, 140);"
            "}"
        )

    _checkmark_icon_cache: str | None = None

    @classmethod
    def _checkmark_icon_path(cls) -> str:
        """Path to the checkbox checkmark PNG (generate once if missing)."""
        if cls._checkmark_icon_cache:
            return cls._checkmark_icon_cache
        path = Path(__file__).parent / "checkbox_check.png"
        if not path.is_file():
            pixmap = QPixmap(13, 13)
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(QColor(230, 230, 230), 1.6)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(2, 7, 5, 10)
            painter.drawLine(5, 10, 11, 3)
            painter.end()
            pixmap.save(str(path), "PNG")
        cls._checkmark_icon_cache = path.as_posix()
        return cls._checkmark_icon_cache

    def _checkbox(self, text: str) -> QCheckBox:
        """Checkbox styled to match plain button grey, with a white check mark."""
        r, g, b = self._PLAIN_BTN_RGB
        check_icon = self._checkmark_icon_path()
        checkbox = QCheckBox(text)
        checkbox.setMinimumWidth(0)
        checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        checkbox.setStyleSheet(
            "QCheckBox {"
            f"  background-color: rgb({r}, {g}, {b});"
            "  color: rgb(210, 210, 210);"
            "  border: 2px solid rgb(80, 80, 80);"
            "  border-radius: 8px;"
            "  padding: 3px 6px;"
            "  font-size: 12px;"
            "  spacing: 6px;"
            "}"
            "QCheckBox::indicator {"
            "  width: 13px;"
            "  height: 13px;"
            "  border: 1px solid rgb(110, 110, 110);"
            "  border-radius: 2px;"
            "  background-color: rgb(45, 45, 45);"
            "}"
            "QCheckBox::indicator:unchecked:hover,"
            "QCheckBox::indicator:checked:hover {"
            "  border: 1px solid rgb(140, 140, 140);"
            "}"
            "QCheckBox::indicator:checked {"
            "  background-color: rgb(45, 45, 45);"
            "  border: 1px solid rgb(110, 110, 110);"
            f'  image: url("{check_icon}");'
            "}"
        )
        return checkbox

    def _sub_label(self, text: str) -> QLabel:
        """Section sub-header matching collapsible tab button colors."""
        label = QLabel(text)
        label.setStyleSheet(
            "QLabel {"
            "  background-color: rgb(60, 60, 60);"
            "  color: rgb(220, 220, 220);"
            "  border: 1px solid rgb(90, 90, 90);"
            "  border-radius: 2px;"
            "  padding: 2px 6px;"
            "  font-size: 11px;"
            "}"
        )
        return label

    @staticmethod
    def _slider_stylesheet() -> str:
        """High-contrast sliders so Round/Size stay visible on the panel."""
        return (
            "QSlider::groove:horizontal {"
            "  height: 6px;"
            "  background: rgb(35, 35, 35);"
            "  border: 1px solid rgb(110, 110, 110);"
            "  border-radius: 3px;"
            "  margin: 4px 0;"
            "}"
            "QSlider::sub-page:horizontal {"
            "  background: rgb(90, 110, 140);"
            "  border: 1px solid rgb(110, 110, 110);"
            "  border-radius: 3px;"
            "}"
            "QSlider::add-page:horizontal {"
            "  background: rgb(35, 35, 35);"
            "  border-radius: 3px;"
            "}"
            "QSlider::handle:horizontal {"
            "  background: rgb(225, 225, 225);"
            "  border: 1px solid rgb(40, 40, 40);"
            "  width: 14px;"
            "  height: 14px;"
            "  margin: -5px 0;"
            "  border-radius: 7px;"
            "}"
            "QSlider::handle:horizontal:hover {"
            "  background: rgb(245, 245, 245);"
            "}"
            "QSlider::groove:horizontal:disabled {"
            "  background: rgb(50, 50, 50);"
            "  border: 1px solid rgb(75, 75, 75);"
            "}"
            "QSlider::sub-page:horizontal:disabled {"
            "  background: rgb(60, 68, 80);"
            "  border: 1px solid rgb(75, 75, 75);"
            "}"
            "QSlider::handle:horizontal:disabled {"
            "  background: rgb(130, 130, 130);"
            "  border: 1px solid rgb(70, 70, 70);"
            "}"
        )

    def _apply_loaded_muted_colors(self) -> None:
        """Parse muted presets from the hidden settings field after load_settings."""
        parsed = picker_core.parse_muted_colors(self.muted_colors_setting.text())
        if parsed is None:
            self._muted_colors = picker_core.copy_muted_button_colors()
            self.muted_colors_setting.setText(
                picker_core.serialize_muted_colors(self._muted_colors),
            )
        else:
            self._muted_colors = parsed
        self._refresh_muted_color_ui(selected_index=self._muted_selected_index)

    def _commit_muted_colors(self) -> None:
        """Persist muted presets to Maya prefs — only call when picker JSON is saved."""
        self.muted_colors_setting.setText(
            picker_core.serialize_muted_colors(self._muted_colors),
        )
        self.save_settings()

    def _refresh_muted_color_ui(self, selected_index: int | None = None) -> None:
        """Refresh clickable preset swatches from ``_muted_colors``."""
        if selected_index is None:
            selected_index = self._muted_selected_index
        selected_index = max(0, min(max(0, len(self._muted_colors) - 1), int(selected_index)))
        self._muted_selected_index = selected_index
        for i, btn in enumerate(self._muted_swatch_buttons):
            if i >= len(self._muted_colors):
                break
            r, g, b = self._muted_colors[i]
            border = "rgb(240, 240, 240)" if i == selected_index else "rgb(70, 70, 70)"
            width = 2 if i == selected_index else 1
            btn.setStyleSheet(
                "QToolButton {"
                f"  background-color: rgb({r}, {g}, {b});"
                f"  border: {width}px solid {border};"
                "  border-radius: 2px;"
                "}"
                "QToolButton:hover {"
                "  border: 2px solid rgb(220, 220, 220);"
                "}"
                "QToolButton:disabled {"
                "  background-color: rgb(60, 60, 60);"
                "  border: 1px solid rgb(50, 50, 50);"
                "}"
            )

    @staticmethod
    def _combo_stylesheet() -> str:
        """Darker combo styling so dropdowns read against the panel background."""
        # Forward slashes: Qt stylesheet urls on Windows
        arrow = (Path(__file__).parent / "combo_down_arrow.svg").as_posix()
        return (
            "QComboBox, QFontComboBox {"
            "  background-color: rgb(45, 45, 45);"
            "  color: rgb(220, 220, 220);"
            "  border: 1px solid rgb(90, 90, 90);"
            "  border-radius: 4px;"
            "  padding: 3px 22px 3px 6px;"
            "  min-height: 22px;"
            "}"
            "QComboBox:hover, QFontComboBox:hover {"
            "  background-color: rgb(55, 55, 55);"
            "  border: 1px solid rgb(110, 110, 110);"
            "}"
            "QComboBox:disabled, QFontComboBox:disabled {"
            "  background-color: rgb(55, 55, 55);"
            "  color: rgb(140, 140, 140);"
            "}"
            "QComboBox::drop-down, QFontComboBox::drop-down {"
            "  subcontrol-origin: padding;"
            "  subcontrol-position: center right;"
            "  width: 20px;"
            "  border: none;"
            "  border-left: 1px solid rgb(90, 90, 90);"
            "  background-color: rgb(55, 55, 55);"
            "  border-top-right-radius: 4px;"
            "  border-bottom-right-radius: 4px;"
            "}"
            "QComboBox::drop-down:hover, QFontComboBox::drop-down:hover {"
            "  background-color: rgb(70, 70, 70);"
            "}"
            "QComboBox::down-arrow, QFontComboBox::down-arrow {"
            f"  image: url(\"{arrow}\");"
            "  width: 10px;"
            "  height: 6px;"
            "}"
            "QComboBox QAbstractItemView, QFontComboBox QAbstractItemView {"
            "  background-color: rgb(45, 45, 45);"
            "  color: rgb(220, 220, 220);"
            "  selection-background-color: rgb(70, 70, 70);"
            "  border: 1px solid rgb(90, 90, 90);"
            "}"
        )

    @staticmethod
    def _separate_arrow_icon(direction: str, size: int = 22) -> QIcon:
        """Filled triangle arrow for Separate increase/decrease buttons."""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(235, 235, 235)))
        painter.setPen(QPen(QColor(40, 40, 40), 1.2))
        mid = size * 0.5
        inset = size * 0.18
        if direction == "right":
            points = [
                QPointF(inset + 1, inset),
                QPointF(size - inset, mid),
                QPointF(inset + 1, size - inset),
            ]
        else:
            points = [
                QPointF(size - inset - 1, inset),
                QPointF(inset, mid),
                QPointF(size - inset - 1, size - inset),
            ]
        painter.drawPolygon(QPolygonF(points))
        painter.end()
        return QIcon(pixmap)

    @staticmethod
    def _rotate_arrow_icon(direction: str, size: int = 14) -> QIcon:
        """Curved rotate arrow for Layout Rotate CW / CCW buttons."""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(235, 235, 235)
        pen = QPen(color, max(1.4, size * 0.14))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        rect = QRectF(size * 0.18, size * 0.18, size * 0.64, size * 0.64)
        if direction == "cw":
            painter.drawArc(rect, 60 * 16, -240 * 16)
            tip = QPointF(size * 0.78, size * 0.32)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawPolygon(
                QPolygonF(
                    [
                        tip,
                        QPointF(tip.x() - size * 0.28, tip.y() - size * 0.06),
                        QPointF(tip.x() - size * 0.08, tip.y() + size * 0.22),
                    ],
                ),
            )
        else:
            painter.drawArc(rect, 120 * 16, 240 * 16)
            tip = QPointF(size * 0.22, size * 0.32)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawPolygon(
                QPolygonF(
                    [
                        tip,
                        QPointF(tip.x() + size * 0.28, tip.y() - size * 0.06),
                        QPointF(tip.x() + size * 0.08, tip.y() + size * 0.22),
                    ],
                ),
            )
        painter.end()
        return QIcon(pixmap)

    def _console_label(self, text: str, *, compact: bool = False) -> QLabel:
        """Status/help note label matching the File status console look."""
        label = QLabel(text)
        label.setWordWrap(not compact)
        label.setMinimumWidth(0)
        if compact:
            label.setFixedHeight(26)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        else:
            label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        label.setStyleSheet(self._console_label_stylesheet(compact=compact))
        return label

    @staticmethod
    def _console_label_stylesheet(*, compact: bool = False) -> str:
        padding = "3px 8px" if compact else "6px 8px"
        return (
            "QLabel {"
            "  background-color: rgb(45, 45, 45);"
            "  color: rgb(180, 220, 160);"
            "  border: 1px solid rgb(90, 90, 90);"
            "  border-radius: 4px;"
            f"  padding: {padding};"
            "  font-family: Consolas, 'Courier New', monospace;"
            "  font-size: 11px;"
            "}"
        )

    def _set_help_context(self, note: str, *, title: str = "") -> None:
        """Show notes for the last clicked tool button in the Help section."""
        if not hasattr(self, "help_context_label"):
            return
        body = str(note or "").strip()
        header = str(title or "").strip()
        if header and body:
            text = f"{header}\n{body}"
        else:
            text = body or header or "Click a tool button to see notes for that action."
        self.help_context_label.setText(text)

    def _action_button(
        self,
        label: str,
        callback,
        *,
        help_note: str | None = None,
        help_title: str | None = None,
    ) -> QPushButton:
        btn = QPushButton(label)

        def _on_clicked(
            _checked: bool = False,
            cb=callback,
            note=help_note,
            name=help_title or label,
        ) -> None:
            if note:
                self._set_help_context(note, title=name)
            cb()

        btn.clicked.connect(_on_clicked)
        btn.setMinimumWidth(0)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # Darker than panel fill so plain buttons read a bit more clearly
        btn.setStyleSheet(self._tinted_button_stylesheet(*self._PLAIN_BTN_RGB))
        return btn

    @staticmethod
    def _tinted_button_stylesheet(r: int, g: int, b: int) -> str:
        """Slight color tint for action buttons (keeps dark UI look)."""
        hover = (min(255, r + 20), min(255, g + 20), min(255, b + 20))
        return (
            "QPushButton {"
            f"  background-color: rgb({r}, {g}, {b});"
            "  color: rgb(210, 210, 210);"
            "  border: 2px solid rgb(80, 80, 80);"
            "  border-radius: 8px;"
            "  padding: 3px 10px;"
            "  font-size: 12px;"
            "  text-align: left;"
            "}"
            "QPushButton:hover {"
            f"  background-color: rgb({hover[0]}, {hover[1]}, {hover[2]});"
            "}"
            "QPushButton:pressed {"
            f"  background-color: rgb({r}, {g}, {b});"
            "  border: 1px solid rgb(90, 90, 90);"
            "}"
        )

    @staticmethod
    def _pick_color_button_stylesheet() -> str:
        """Muted blue → muted yellow gradient for the Pick Color button."""
        return (
            "QPushButton {"
            "  background-color: qlineargradient("
            "    x1:0, y1:0, x2:1, y2:0,"
            "    stop:0 rgb(48, 52, 58),"
            "    stop:1 rgb(58, 56, 46)"
            "  );"
            "  color: rgb(210, 210, 210);"
            "  border: 2px solid rgb(80, 80, 80);"
            "  border-radius: 8px;"
            "  padding: 3px 10px;"
            "  font-size: 12px;"
            "  text-align: left;"
            "}"
            "QPushButton:hover {"
            "  background-color: qlineargradient("
            "    x1:0, y1:0, x2:1, y2:0,"
            "    stop:0 rgb(54, 58, 66),"
            "    stop:1 rgb(66, 64, 52)"
            "  );"
            "}"
            "QPushButton:pressed {"
            "  background-color: qlineargradient("
            "    x1:0, y1:0, x2:1, y2:0,"
            "    stop:0 rgb(48, 52, 58),"
            "    stop:1 rgb(58, 56, 46)"
            "  );"
            "  border: 1px solid rgb(90, 90, 90);"
            "}"
            "QPushButton:disabled {"
            "  background-color: rgb(50, 50, 50);"
            "  color: rgb(140, 140, 140);"
            "}"
        )

    def _set_status(self, message: str) -> None:
        text = str(message).strip() if message else "Ready"
        self.status_label.setText(text)
        self.status_label.setToolTip(text)

    def _set_edit_widgets_enabled(self, enabled: bool) -> None:
        self.add_button_btn.setEnabled(enabled)
        self.add_from_selection_btn.setEnabled(enabled)
        self.hierarchy_order_checkbox.setEnabled(enabled)
        self.add_from_group_selection_btn.setEnabled(enabled)
        self.duplicate_button_btn.setEnabled(enabled)
        self.mirror_button_btn.setEnabled(enabled)
        self.delete_button_btn.setEnabled(enabled)
        can_edit_images = enabled and not self.lock_images_checkbox.isChecked()
        self.add_bg_btn.setEnabled(enabled)
        self.remove_bg_btn.setEnabled(can_edit_images)
        self.bg_forward_btn.setEnabled(can_edit_images)
        self.bg_back_btn.setEnabled(can_edit_images)
        self.duplicate_bg_btn.setEnabled(can_edit_images)
        self.rotate_bg_btn.setEnabled(can_edit_images)
        self.mirror_bg_btn.setEnabled(can_edit_images)
        self.clear_bg_btn.setEnabled(enabled)
        self.pick_color_btn.setEnabled(enabled)
        self.copy_color_btn.setEnabled(enabled)
        self.paste_color_btn.setEnabled(enabled)
        self.copy_font_btn.setEnabled(enabled)
        self.paste_font_btn.setEnabled(enabled)
        buttons = self.canvas.selected_buttons() if enabled else []
        has_selection = bool(buttons)
        has_multi = len(buttons) >= 2
        for btn in (self.decrease_distance_btn, self.increase_distance_btn):
            btn.setEnabled(enabled and has_multi)
        for btn in (self.rotate_ccw_btn, self.rotate_cw_btn):
            btn.setEnabled(enabled and has_selection)
        self.label_input.setEnabled(enabled and has_selection)
        self.rename_from_target_btn.setEnabled(enabled and has_selection)
        self.assign_targets_btn.setEnabled(enabled and has_selection)
        self.clear_targets_btn.setEnabled(enabled and has_selection)
        self.target_find_input.setEnabled(enabled and has_selection)
        self.target_replace_input.setEnabled(enabled and has_selection)
        self.replace_targets_btn.setEnabled(enabled and has_selection)
        for btn in self._muted_swatch_buttons:
            btn.setEnabled(enabled)
        self.update_swatch_btn.setEnabled(enabled and has_selection)
        self.corner_radius_slider.setEnabled(enabled and has_selection)
        self.font_family_combo.setEnabled(enabled and has_selection)
        self.font_size_slider.setEnabled(enabled and has_selection)
        self.font_bold_checkbox.setEnabled(enabled and has_selection)
        self.text_dark_checkbox.setEnabled(enabled and has_selection)

    def _sync_style_sliders(self, buttons: list[PickerButtonItem]) -> None:
        self.corner_radius_slider.blockSignals(True)
        self.font_family_combo.blockSignals(True)
        self.font_size_slider.blockSignals(True)
        self.font_bold_checkbox.blockSignals(True)
        self.text_dark_checkbox.blockSignals(True)
        if buttons:
            self.corner_radius_slider.setValue(buttons[0].corner_radius())
            self.corner_radius_value.setText(str(buttons[0].corner_radius()))
            self.font_family_combo.setCurrentFont(QFont(buttons[0].font_family()))
            self.font_size_slider.setValue(buttons[0].font_size())
            self.font_size_value.setText(str(buttons[0].font_size()))
            self.font_bold_checkbox.setChecked(buttons[0].font_bold())
            self.text_dark_checkbox.setChecked(buttons[0].text_dark())
        else:
            self.corner_radius_slider.setValue(picker_core.DEFAULT_CORNER_RADIUS)
            self.corner_radius_value.setText(str(picker_core.DEFAULT_CORNER_RADIUS))
            self.font_family_combo.setCurrentFont(QFont(picker_core.DEFAULT_FONT_FAMILY))
            self.font_size_slider.setValue(picker_core.DEFAULT_FONT_SIZE)
            self.font_size_value.setText(str(picker_core.DEFAULT_FONT_SIZE))
            self.font_bold_checkbox.setChecked(picker_core.DEFAULT_FONT_BOLD)
            self.text_dark_checkbox.setChecked(picker_core.DEFAULT_TEXT_DARK)
        self.corner_radius_slider.blockSignals(False)
        self.font_family_combo.blockSignals(False)
        self.font_size_slider.blockSignals(False)
        self.font_bold_checkbox.blockSignals(False)
        self.text_dark_checkbox.blockSignals(False)

    def _on_selection_changed(self) -> None:
        buttons = self.canvas.selected_buttons()
        edit = self.canvas.is_edit_mode()
        self._sync_style_sliders(buttons)
        self._set_edit_widgets_enabled(edit)

        if not buttons:
            self.label_input.setText("")
            self.targets_label.setText("Targets: (none)")
            return

        combined = self.canvas.combined_selected_targets()
        if len(buttons) == 1:
            self.targets_label.setText(picker_fns.format_targets_summary(buttons[0].targets))
        else:
            self.targets_label.setText(
                f"{len(buttons)} buttons — {picker_fns.format_targets_summary(combined)}",
            )
        self.label_input.setText(buttons[0].label())

    def on_anim_selection_committed(self) -> None:
        """Select combined Maya targets after anim-mode click / rubber-band."""
        if self.canvas.is_edit_mode():
            return
        buttons = self.canvas.selected_buttons()
        if not buttons:
            picker_fns.clear_selection()
            self._set_status("Cleared selection")
            return
        targets = self.canvas.combined_selected_targets()
        label = buttons[0].label() if len(buttons) == 1 else f"{len(buttons)} buttons"
        picker_fns.select_picker_targets(
            targets,
            label=label,
            namespace=self._active_namespace,
        )
        self._set_status(f"Selected {len(targets)} object(s) from {len(buttons)} button(s)")

    def on_edit_mode_toggled(self, checked: bool) -> None:
        self.canvas.set_edit_mode(checked)
        self._on_selection_changed()
        self._set_status("Edit Mode" if checked else "Animation Mode")
        self.save_settings()

    def on_add_button(self) -> None:
        if self.canvas.add_button("New") is None:
            self._set_status("Enable Edit Mode to add buttons")
            return
        self._set_status("Added button")

    def on_add_from_selection(self) -> None:
        """One blank dark-red square button per Maya selection item."""
        if not self.canvas._edit_mode:
            self._set_status("Enable Edit Mode to add buttons")
            return
        raw_sel = picker_fns.get_maya_selection()
        if not raw_sel:
            self._set_status("Select Maya object(s) first")
            return
        if self.hierarchy_order_checkbox.isChecked():
            maya_sel = picker_fns.selection_for_add_buttons(raw_sel)
        else:
            maya_sel = raw_sel
        ns = self._active_namespace
        specs: list[tuple[str, list[str]]] = []
        for node in maya_sel:
            stored = picker_fns.strip_namespaces([node], namespace=ns)
            if not stored:
                continue
            specs.append(("", stored))
        if not specs:
            self._set_status("Select Maya object(s) first")
            return
        size = SELECTION_BUTTON_SIZE
        items = self.canvas.add_buttons_horizontal(
            specs,
            w=size,
            h=size,
            color=SELECTION_BUTTON_COLOR,
        )
        if not items:
            self._set_status("Enable Edit Mode to add buttons")
            return
        self._on_selection_changed()
        if len(items) == 1:
            self._set_status("Added 1 button from selection")
        else:
            self._set_status(f"Added {len(items)} buttons from selection")

    def on_add_from_group_selection(self) -> None:
        """One blank dark-yellow square with all Maya-selected objects as targets."""
        if not self.canvas._edit_mode:
            self._set_status("Enable Edit Mode to add buttons")
            return
        maya_sel = picker_fns.get_maya_selection()
        if not maya_sel:
            self._set_status("Select Maya object(s) first")
            return
        targets = picker_fns.strip_namespaces(maya_sel, namespace=self._active_namespace)
        if not targets:
            self._set_status("Select Maya object(s) first")
            return
        size = GROUP_SELECTION_BUTTON_SIZE
        item = self.canvas.add_button(
            "",
            w=size,
            h=size,
            color=GROUP_SELECTION_BUTTON_COLOR,
            targets=targets,
        )
        if item is None:
            self._set_status("Enable Edit Mode to add buttons")
            return
        self._on_selection_changed()
        self._set_status(f"Added group button with {len(targets)} target(s)")

    def on_duplicate_selected(self) -> None:
        items = self.canvas.duplicate_selected()
        if not items:
            self._set_status("Select button(s) to duplicate")
            return
        if len(items) == 1:
            self._set_status(f'Duplicated "{items[0].label()}"')
        else:
            self._set_status(f"Duplicated {len(items)} buttons")

    def on_mirror_selected(self) -> None:
        items = self.canvas.mirror_selected()
        if not items:
            self._set_status("Select button(s) to mirror")
            return
        if len(items) == 1:
            self._set_status(f'Mirrored → "{items[0].label()}"')
        else:
            self._set_status(f"Mirrored {len(items)} buttons")

    def on_delete_selected(self) -> None:
        count = self.canvas.delete_selected()
        if count:
            self._set_status(f"Deleted {count} item(s)")
        else:
            self._set_status("Select button(s) or background(s) to delete")

    def on_adjust_distance(self, delta: int) -> None:
        count, axis = self.canvas.adjust_distance_selected(delta)
        if count:
            axis_name = "horizontal" if axis == "x" else "vertical"
            action = "Increased" if delta > 0 else "Decreased"
            self._set_status(f"{action} distance on {count} buttons ({axis_name})")
        else:
            self._set_status("Select 2+ buttons to adjust distance")

    def on_rotate_selected(self, degrees: int) -> None:
        count = self.canvas.rotate_selected(degrees)
        if count:
            way = "CW" if degrees > 0 else "CCW"
            self._set_status(f"Rotated {count} buttons 90° {way}")
        else:
            self._set_status("Select a button to rotate")

    def on_label_edited(self) -> None:
        button = self.canvas.selected_button()
        if button is None:
            return
        button.set_label(self.label_input.text().strip())

    def on_rename_from_first_target(self) -> None:
        """Rename selected buttons from the short name of their first target."""
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select button(s) first")
            return
        renamed = 0
        skipped = 0
        for button in buttons:
            targets = list(button.targets or [])
            if not targets:
                skipped += 1
                continue
            name = picker_fns.short_node_name(targets[0])
            if not name:
                skipped += 1
                continue
            button.set_label(name)
            renamed += 1
        if renamed and len(buttons) == 1:
            self.label_input.setText(buttons[0].label())
            self._set_status(f'Renamed to "{buttons[0].label()}"')
        elif renamed:
            self.label_input.setText(buttons[0].label())
            msg = f"Renamed {renamed} button(s) from first target"
            if skipped:
                msg += f" ({skipped} skipped)"
            self._set_status(msg)
        else:
            self._set_status("No targets to rename from")

    def on_assign_selection(self) -> None:
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select picker button(s) first")
            return
        maya_sel = picker_fns.strip_namespaces(
            picker_fns.get_maya_selection(),
            namespace=self._active_namespace,
        )
        if not maya_sel:
            self._set_status("Select Maya object(s) to assign")
            return
        for button in buttons:
            button.set_targets(maya_sel)
        self.targets_label.setText(picker_fns.format_targets_summary(maya_sel))
        if len(buttons) == 1:
            self._set_status(f'Assigned {len(maya_sel)} object(s) to "{buttons[0].label()}"')
        else:
            self._set_status(f"Assigned {len(maya_sel)} object(s) to {len(buttons)} buttons")

    def on_clear_targets(self) -> None:
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select picker button(s) first")
            return
        for button in buttons:
            button.set_targets([])
        self.targets_label.setText("Targets: (none)")
        if len(buttons) == 1:
            self._set_status(f'Cleared targets on "{buttons[0].label()}"')
        else:
            self._set_status(f"Cleared targets on {len(buttons)} buttons")

    def on_replace_targets(self) -> None:
        """Replace find→replace in targets on all selected picker buttons."""
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select picker button(s) first")
            return
        find_text = self.target_find_input.text()
        if not find_text:
            self._set_status("Enter text to find")
            return
        self.save_settings()
        replace_text = self.target_replace_input.text()
        total_changed = 0
        buttons_changed = 0
        for button in buttons:
            updated, changed = picker_fns.replace_in_targets(
                button.targets,
                find_text,
                replace_text,
            )
            if changed:
                button.set_targets(updated)
                total_changed += changed
                buttons_changed += 1
        self._on_selection_changed()
        if total_changed:
            self._set_status(
                f'Replaced "{find_text}" → "{replace_text}" in '
                f"{total_changed} target(s) on {buttons_changed} button(s)",
            )
        else:
            self._set_status(f'No targets contained "{find_text}"')

    def on_apply_muted_preset(self, index: int) -> None:
        """Left-click a preset swatch to apply it to selected buttons."""
        colors = self._muted_colors
        if not colors:
            return
        index = max(0, min(len(colors) - 1, int(index)))
        self._refresh_muted_color_ui(selected_index=index)
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select button(s) first")
            return
        color = QColor(*colors[index])
        for button in buttons:
            button.set_color(color)
        self._copied_color = QColor(color)
        if len(buttons) == 1:
            self._set_status(f'Preset {index + 1} → "{buttons[0].label()}"')
        else:
            self._set_status(f"Preset {index + 1} → {len(buttons)} buttons")

    def on_update_color_swatch(self) -> None:
        """Set the selected swatch from the first selected button's color."""
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select a button first")
            return
        colors = self._muted_colors
        if not colors:
            return
        index = max(0, min(len(colors) - 1, int(self._muted_selected_index)))
        color = buttons[0].color()
        self._muted_colors[index] = [color.red(), color.green(), color.blue()]
        self._refresh_muted_color_ui(selected_index=index)
        self._set_status(
            f'Preset {index + 1} ← "{buttons[0].label()}" (Save to keep prefs)',
        )

    def on_pick_color(self) -> None:
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select button(s) first")
            return
        color = QColorDialog.getColor(buttons[0].color(), self, "Picker Button Color")
        if not color.isValid():
            return
        for button in buttons:
            button.set_color(color)
        self._copied_color = QColor(color)
        if len(buttons) == 1:
            self._set_status(f'Color applied to "{buttons[0].label()}"')
        else:
            self._set_status(f"Color applied to {len(buttons)} buttons")

    def on_copy_color(self) -> None:
        button = self.canvas.selected_button()
        if button is None:
            self._set_status("Select a button to copy color from")
            return
        self._copied_color = button.color()
        self._set_status(f'Copied color from "{button.label()}"')

    def on_paste_color(self) -> None:
        if self._copied_color is None or not self._copied_color.isValid():
            self._set_status("Copy a color first")
            return
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select button(s) to paste color onto")
            return
        for button in buttons:
            button.set_color(self._copied_color)
        if len(buttons) == 1:
            self._set_status(f'Pasted color onto "{buttons[0].label()}"')
        else:
            self._set_status(f"Pasted color onto {len(buttons)} buttons")

    def on_corner_radius_changed(self, value: int) -> None:
        self.corner_radius_value.setText(str(value))
        buttons = self.canvas.selected_buttons()
        if not buttons:
            return
        for button in buttons:
            button.set_corner_radius(value)

    def _apply_font_scroll_enabled(self, enabled: bool) -> None:
        """Gate mouse-wheel on font family, size, and roundness controls."""
        enabled = bool(enabled)
        self.font_family_combo.wheel_scroll_enabled = enabled
        self.font_size_slider.wheel_scroll_enabled = enabled
        self.corner_radius_slider.wheel_scroll_enabled = enabled

    def on_font_scroll_toggled(self, checked: bool) -> None:
        self._apply_font_scroll_enabled(checked)
        self.save_settings()
        self._set_status("Font Scroll on" if checked else "Font Scroll off")

    def on_font_family_changed(self, font: QFont) -> None:
        buttons = self.canvas.selected_buttons()
        if not buttons:
            return
        family = font.family()
        for button in buttons:
            button.set_font_family(family)

    def on_font_size_changed(self, value: int) -> None:
        self.font_size_value.setText(str(value))
        buttons = self.canvas.selected_buttons()
        if not buttons:
            return
        for button in buttons:
            button.set_font_size(value)

    def on_font_bold_toggled(self, checked: bool) -> None:
        buttons = self.canvas.selected_buttons()
        if not buttons:
            return
        for button in buttons:
            button.set_font_bold(checked)

    def on_text_dark_toggled(self, checked: bool) -> None:
        buttons = self.canvas.selected_buttons()
        if not buttons:
            return
        for button in buttons:
            button.set_text_dark(checked)

    def on_copy_font(self) -> None:
        button = self.canvas.selected_button()
        if button is None:
            self._set_status("Select a button to copy font from")
            return
        self._copied_font = {
            "font_family": button.font_family(),
            "font_size": button.font_size(),
            "font_bold": button.font_bold(),
            "text_dark": button.text_dark(),
        }
        self._set_status(f'Copied font from "{button.label()}"')

    def on_paste_font(self) -> None:
        if not self._copied_font:
            self._set_status("Copy a font first")
            return
        buttons = self.canvas.selected_buttons()
        if not buttons:
            self._set_status("Select button(s) to paste font onto")
            return
        for button in buttons:
            button.set_font_family(self._copied_font["font_family"])
            button.set_font_size(self._copied_font["font_size"])
            button.set_font_bold(self._copied_font["font_bold"])
            button.set_text_dark(self._copied_font.get("text_dark", False))
        self._sync_style_sliders(buttons)
        if len(buttons) == 1:
            self._set_status(f'Pasted font onto "{buttons[0].label()}"')
        else:
            self._set_status(f"Pasted font onto {len(buttons)} buttons")

    def on_grid_toggled(self, checked: bool) -> None:
        self.canvas.set_grid_visible(checked)
        self.save_settings()

    def on_image_snap_toggled(self, checked: bool) -> None:
        self.canvas.set_image_snap(checked)
        self.save_settings()
        if checked:
            self._set_status("Image center snap on")
        else:
            self._set_status("Image center snap off")

    def on_lock_images_toggled(self, checked: bool) -> None:
        self.canvas.set_images_locked(checked)
        self._set_edit_widgets_enabled(self.edit_mode_checkbox.isChecked())
        self.save_settings()
        self._set_status("Images locked" if checked else "Images unlocked")

    def on_center_view(self) -> None:
        self.canvas.center_on_origin()
        self._set_status("Centered on grid origin")

    def on_reset_all_controls(self) -> None:
        """Reset selected ctrls (and descendants) or all rig ctrls if nothing selected."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.reset_all_ctrls()
        self._set_status("Reset all controls")

    def on_open_space_matcher_ui(self) -> None:
        """Open the Space Matcher UI (same entry point as the shelf button)."""
        from nlol.core.ui import space_matcher_ui

        space_matcher_ui.reload_tool()
        self._set_status("Opened Space Matcher UI")

    def on_refresh_backgrounds(self) -> None:
        self._refresh_background_combo()
        count = self.background_combo.count()
        self._set_status(f"Found {count} image(s) in anim_picker/")

    def on_add_background(self) -> None:
        path = self.background_combo.currentData()
        if not path:
            self._set_status("No anim_picker images in folder")
            return
        item = self.canvas.add_background(Path(path))
        if item is not None:
            self._set_status(f"Added background: {Path(path).name}")
        else:
            self._set_status(f"Could not load {Path(path).name}")

    def on_remove_background(self) -> None:
        count = self.canvas.remove_selected_backgrounds()
        if count:
            self._set_status(f"Removed {count} background(s)")
        else:
            self._set_status("Select a background image to remove")

    def on_background_forward(self) -> None:
        count = self.canvas.bring_backgrounds_forward()
        if count:
            self._set_status(f"Brought {count} background(s) forward")
        else:
            self._set_status("Select a background to bring forward")

    def on_background_back(self) -> None:
        count = self.canvas.send_backgrounds_back()
        if count:
            self._set_status(f"Sent {count} background(s) back")
        else:
            self._set_status("Select a background to send back")

    def on_duplicate_background(self) -> None:
        items = self.canvas.duplicate_selected_backgrounds()
        if not items:
            self._set_status("Select a background image to duplicate")
            return
        if len(items) == 1:
            self._set_status(f'Duplicated "{items[0].image_path.name}"')
        else:
            self._set_status(f"Duplicated {len(items)} backgrounds")

    def on_rotate_background(self) -> None:
        count = self.canvas.rotate_selected_backgrounds()
        if not count:
            self._set_status("Select a background image to rotate")
            return
        if count == 1:
            degrees = self.canvas.selected_backgrounds()[0].rotation_degrees()
            self._set_status(f"Rotated to {degrees}°")
        else:
            self._set_status(f"Rotated {count} backgrounds 90°")

    def on_mirror_background(self) -> None:
        items = self.canvas.mirror_selected_backgrounds()
        if not items:
            self._set_status("Select a background image to mirror")
            return
        if len(items) == 1:
            self._set_status(f'Mirrored "{items[0].image_path.name}"')
        else:
            self._set_status(f"Mirrored {len(items)} backgrounds")

    def on_clear_backgrounds(self) -> None:
        count = len(self.canvas.background_items())
        self.canvas.clear_backgrounds()
        self._set_status(f"Cleared {count} background(s)" if count else "No backgrounds")

    def on_save_on_refresh_toggled(self, checked: bool) -> None:
        self.save_settings()

    def _selected_rig_entry(self) -> dict | None:
        """Return the rig_context entry for the current dropdown selection."""
        name = str(self.rig_context_combo.currentData() or "")
        if not name:
            return None
        for entry in picker_core.list_rig_contexts():
            if entry["name"] == name:
                return entry
        return None

    def on_open_rig_file(self) -> None:
        """Open the selected character's ``*_rig.ma`` (same path as Multi Tool)."""
        rig = self._selected_rig_entry()
        if rig is None:
            self._set_status("Select a Rig Context first")
            return
        filepath = picker_core.resolve_rig_maya_filepath(rig)
        if filepath is None:
            self._set_status("Could not resolve rig file path")
            return
        if not filepath.is_file():
            self._set_status(f"Not found: {filepath.name}")
            print(f"[AnimPicker] File not found: {filepath}")
            return
        if picker_fns.open_maya_file(filepath):
            self._refresh_namespace_combo(prefer_rig_name=str(rig.get("name", "")))
            self._set_status(f"Opened {filepath.name}")
        else:
            self._set_status("Open cancelled")

    def on_open_rig_context_ui(self) -> None:
        """Open the Rig Context UI (same entry point as the shelf button)."""
        from nlol.core.ui import rig_context_ui

        reload(rig_context_ui)
        rig_context_ui.reload_tool()
        self._set_status("Opened Rig Context UI")

    def on_refresh_rig_context(self) -> None:
        """Reload rig_context.json + namespaces and autoload the active rig picker."""
        if self.save_on_refresh_checkbox.isChecked():
            path = self._try_save_picker()
            if path is None:
                if self._picker_io.filepath is None:
                    self._set_status("Select a Rig Context before saving")
                return
            self._commit_muted_colors()
        self._refresh_rig_context_ui(autoload=True, save_current=False)
        self._on_selection_changed()
        if self.save_on_refresh_checkbox.isChecked():
            name = self._picker_io.filepath.name if self._picker_io.filepath else "(none)"
            self._set_status(f"Saved + refreshed {name}")

    def on_rig_context_changed(self, _index: int = 0) -> None:
        """User picked a different rig — persist existing picker if any, then autoload."""
        self._save_existing_picker()
        self._apply_selected_rig_context(set_active=True)
        self._refresh_namespace_combo(
            prefer_rig_name=str(self.rig_context_combo.currentData() or ""),
        )
        self._on_selection_changed()

    def on_namespace_changed(self, _index: int = 0) -> None:
        self._active_namespace = str(self.namespace_combo.currentData() or "")
        ns = self._active_namespace or "(none)"
        self._set_status(f"Namespace: {ns}")

    def _warn_picker_locked(self, filepath: Path | None) -> bool:
        """Warn that the picker JSON is read-only. Returns True if user chose Retry."""
        name = filepath.name if filepath is not None else "anim_picker.json"
        print(f'[AnimPicker] Permission denied writing: "{filepath}"')
        result = QMessageBox.warning(
            self,
            "Anim Picker Locked",
            f"<Check Out> in Perforce!\n\n<{name}> "
            "is READ-ONLY and change was not saved.\n\n"
            "Check out the file, then click Retry.",
            QMessageBox.Retry | QMessageBox.Cancel,
            QMessageBox.Retry,
        )
        if result != QMessageBox.Retry:
            self._set_status(f"Save failed — check out {name}")
            return False
        return True

    def _try_save_picker(self) -> Path | None:
        """Save picker JSON; offer Retry if the file is locked (e.g. not checked out)."""
        while True:
            try:
                return self._picker_io.save(self._collect_picker_data())
            except PermissionError:
                if not self._warn_picker_locked(self._picker_io.filepath):
                    return None
            except OSError as exc:
                print(f"[AnimPicker] Could not save picker: {exc}")
                self._set_status(f"Save failed: {exc}")
                return None

    def _save_existing_picker(self) -> Path | None:
        """Save only if anim_picker.json already exists — never auto-create on switch."""
        path = self._picker_io.filepath
        if path is None or not path.is_file():
            return None
        return self._try_save_picker()

    def _refresh_rig_context_ui(
        self,
        *,
        autoload: bool = True,
        save_current: bool = False,
    ) -> None:
        """Rebuild rig dropdown from rig_context.json and optionally load picker."""
        if save_current:
            self._save_existing_picker()

        rigs = picker_core.list_rig_contexts()
        active = picker_core.get_active_rig_context()
        active_name = active["name"] if active else ""

        self.rig_context_combo.blockSignals(True)
        self.rig_context_combo.clear()
        select_index = 0
        if not rigs:
            self.rig_context_combo.addItem("(no rigs in rig_context.json)", "")
        else:
            for i, rig in enumerate(rigs):
                self.rig_context_combo.addItem(rig["name"], rig["name"])
                if rig["name"] == active_name:
                    select_index = i
            self.rig_context_combo.setCurrentIndex(select_index)
        self.rig_context_combo.blockSignals(False)

        prefer = str(self.rig_context_combo.currentData() or active_name)
        self._refresh_namespace_combo(prefer_rig_name=prefer)

        if autoload:
            self._apply_selected_rig_context(set_active=False)

    def _apply_selected_rig_context(self, *, set_active: bool) -> None:
        """Point picker IO at the selected rig and load its anim_picker JSON."""
        name = str(self.rig_context_combo.currentData() or "")
        rig = None
        if name:
            if set_active:
                picker_core.set_active_rig_context(name)
            for entry in picker_core.list_rig_contexts():
                if entry["name"] == name:
                    rig = entry
                    break

        self._picker_io.use_rig(rig)
        self._load_picker_data()
        file_name = self._picker_io.filepath.name if self._picker_io.filepath else "(none)"
        if name:
            self._set_status(f"Rig: {name} | {file_name}")
        else:
            self._set_status("No active rig — select a Rig Context")

    def _refresh_namespace_combo(self, prefer_rig_name: str = "") -> None:
        """Rebuild namespace dropdown from the Maya scene."""
        namespaces = picker_fns.list_scene_namespaces()
        previous = self.namespace_combo.currentData()
        if previous is None:
            previous = self._active_namespace
        guessed = picker_fns.guess_namespace_for_rig(prefer_rig_name, namespaces)

        self.namespace_combo.blockSignals(True)
        self.namespace_combo.clear()
        self.namespace_combo.addItem("(no namespace)", "")
        select_index = 0
        for i, ns in enumerate(namespaces, start=1):
            self.namespace_combo.addItem(ns, ns)
            if previous and ns == previous:
                select_index = i
            elif (not previous) and guessed and ns == guessed:
                select_index = i
        self.namespace_combo.setCurrentIndex(select_index)
        self._active_namespace = str(self.namespace_combo.currentData() or "")
        self.namespace_combo.blockSignals(False)

    def _collect_picker_data(self) -> dict:
        return self.canvas.collect_data(path_for_save=self._picker_io.path_for_save)

    def _load_picker_data(self) -> None:
        data = self._picker_io.load()
        self.canvas.load_data(data, resolve_image=self._picker_io.resolve_image_path)
        self.canvas.set_edit_mode(self.edit_mode_checkbox.isChecked())
        self.canvas.set_image_snap(self.snap_images_checkbox.isChecked())
        self.canvas.set_images_locked(self.lock_images_checkbox.isChecked())
        self._refresh_background_combo()

    def _refresh_background_combo(self) -> None:
        """Rescan picker folder and rebuild the background dropdown."""
        folder = self._picker_io.folder
        images = picker_core.find_picker_images(folder) if folder is not None else []
        previous = self.background_combo.currentData()

        self.background_combo.clear()
        select_index = 0
        for i, image_path in enumerate(images):
            self.background_combo.addItem(image_path.name, str(image_path))
            if previous and str(image_path) == str(previous):
                select_index = i

        if images:
            self.background_combo.setCurrentIndex(select_index)

    def on_save_on_close_toggled(self, checked: bool) -> None:
        self.save_settings()

    def on_save(self) -> None:
        path = self._try_save_picker()
        if path is None:
            if self._picker_io.filepath is None:
                self._set_status("Select a Rig Context before saving")
            return
        self._commit_muted_colors()
        self._set_status(f"Saved {path.name}")

    def _reload_picker_from_disk(self, status_verb: str) -> None:
        """Reload the current picker JSON from disk and refresh the edit panel."""
        self._load_picker_data()
        self._on_selection_changed()
        name = self._picker_io.filepath.name if self._picker_io.filepath else "(none)"
        self._set_status(f"{status_verb} {name}")

    def on_load(self) -> None:
        self._reload_picker_from_disk("Loaded")

    def on_refresh_file(self) -> None:
        """Reload the current picker JSON from disk after manual edits."""
        self._reload_picker_from_disk("Refreshed")

    def _maybe_save_on_close(self) -> None:
        """Save picker JSON if Save on Close is enabled. Safe during Maya dock teardown."""
        if (
            _skip_save_on_reload
            or self._saved_on_close
            or getattr(self, "_skip_save_on_close", False)
        ):
            return
        try:
            # deleteUI can destroy the canvas before hide/close runs — never
            # write that half-dead empty state over a good anim_picker.json.
            if not isValid(self) or not isValid(self.canvas):
                return
            if not self.save_on_close_checkbox.isChecked():
                return
            # Dialog blocks here so they can Check Out + Retry before close finishes.
            path = self._try_save_picker()
            # Mark done either way so hide+close don't prompt twice.
            self._saved_on_close = True
            if path is None:
                return
            self._commit_muted_colors()
            print(f"[AnimPicker] Saved on close: {path}")
        except RuntimeError:
            # Qt object already deleted during workspaceControl teardown
            pass

    def showEvent(self, event) -> None:
        global _skip_save_on_reload
        self._saved_on_close = False
        self._skip_save_on_close = False
        _skip_save_on_reload = False
        super().showEvent(event)

    def hideEvent(self, event) -> None:
        # Maya dock X typically hides the workspace control rather than destroying it
        self.save_settings()
        self._maybe_save_on_close()
        super().hideEvent(event)

    def closeEvent(self, event) -> None:
        self.save_settings()
        self._maybe_save_on_close()
        super().closeEvent(event)

    def reload_tool(self):
        """Reload without Save-on-Close wiping the picker mid-teardown."""
        _prepare_reload_skip_save()
        super().reload_tool()


def _prepare_reload_skip_save() -> None:
    """Disable Save-on-Close for every live picker instance before dock teardown.

    ``importlib.reload(anim_picker_ui)`` replaces the AnimPickerUI class object.
    The docked singleton stays keyed under the *old* class in DockableMayaUI._instances,
    while ``AnimPickerUI()`` constructs a *new* instance. Skip must hit the docked one.
    """
    global _skip_save_on_reload
    _skip_save_on_reload = True
    for inst in list(DockableMayaUI._instances.values()):
        try:
            if getattr(inst, "get_window_title", lambda: "")() == _WINDOW_TITLE:
                inst._skip_save_on_close = True
        except RuntimeError:
            continue


def show_tool():
    """Launch and show tool UI window."""
    AnimPickerUI().show_tool()


def reload_tool():
    """Force reload the tool (safe even if the module was importlib.reload'd first)."""
    _prepare_reload_skip_save()
    AnimPickerUI().reload_tool()
