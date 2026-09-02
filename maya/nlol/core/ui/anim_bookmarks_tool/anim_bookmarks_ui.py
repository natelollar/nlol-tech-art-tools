from importlib import reload

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from nlol.core.ui.anim_bookmarks_tool import anim_bookmarks_functions
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger

reload(anim_bookmarks_functions)

logger = get_logger()

HINT_TEXT = (
    "Offsets bookmarks in the timeslider selection,\n"
    "or the playback range if none."
)


class AnimBookmarksUI(DockableMayaUI):
    """UI for offsetting Maya timeslider bookmarks."""

    def get_window_title(self) -> str:
        return "Anim Bookmarks UI"

    def get_settings_keys(self) -> dict:
        return {
            "offset_input": self.offset_input,
        }

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Build the main UI."""
        hint = QLabel(HINT_TEXT)
        hint.setWordWrap(False)
        hint.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hint.setToolTip(HINT_TEXT.replace("\n", " "))
        hint.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        layout.addWidget(hint)

        row = QHBoxLayout()
        row.setSpacing(6)

        left_btn = QPushButton("<")
        left_btn.setFixedWidth(40)
        left_btn.setStyleSheet("text-align: center;")
        left_btn.setToolTip("Offset bookmarks earlier by the amount.")
        left_btn.clicked.connect(lambda: self.on_offset(-1))
        row.addWidget(left_btn)

        offset_label = QLabel("Offset:")
        offset_label.setFixedWidth(60)
        row.addWidget(offset_label)

        self.offset_input = QLineEdit()
        self.offset_input.setText("1")
        self.offset_input.setFixedWidth(60)
        self.offset_input.setAlignment(Qt.AlignCenter)
        self.offset_input.setToolTip("Frame amount to offset bookmarks by.")
        row.addWidget(self.offset_input)

        frames_label = QLabel("frames")
        frames_label.setFixedWidth(60)
        row.addWidget(frames_label)

        right_btn = QPushButton(">")
        right_btn.setFixedWidth(40)
        right_btn.setStyleSheet("text-align: center;")
        right_btn.setToolTip("Offset bookmarks later by the amount.")
        right_btn.clicked.connect(lambda: self.on_offset(1))
        row.addWidget(right_btn)

        row.addStretch()
        layout.addLayout(row)

    def on_offset(self, direction: int) -> None:
        """Offset bookmarks earlier (direction -1) or later (direction +1)."""
        text = self.offset_input.text().strip()
        try:
            amount = abs(int(float(text)))
        except ValueError:
            logger.warning(f"Invalid offset: {text!r}. Enter a number.")
            return
        if amount == 0:
            logger.info("Offset is 0. Nothing to do.")
            return

        anim_bookmarks_functions.offset_bookmarks(amount * direction)
        self.save_settings()


# ----- entry points --------------------
def show_tool():
    """Launch and show the Anim Bookmarks UI."""
    AnimBookmarksUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    AnimBookmarksUI().reload_tool()
