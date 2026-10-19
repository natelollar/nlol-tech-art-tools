"""Dockable Maya UI for replacing objects with another Arnold .ass version."""

from importlib import reload

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.core.ui.replace_obj_tool import replace_obj_tool_core
from nlol.utilities.nlol_maya_logger import get_logger

reload(replace_obj_tool_core)

logger = get_logger()


class ReplaceObjToolUI(DockableMayaUI):
    """List .ass versions for the first selected standin, then replace the selection."""

    def get_window_title(self) -> str:
        return "Replace Object UI"

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Build the main UI."""
        header_layout = QHBoxLayout()

        self.query_btn = QPushButton("Load Selection")
        self.query_btn.setToolTip(
            "Read the first selected Arnold standin and list .ass versions from its folder.",
        )
        self.query_btn.clicked.connect(self.query_selection)
        header_layout.addWidget(self.query_btn)

        self.status_label = QLabel("No standin loaded.")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(self.status_label, stretch=1)

        layout.addLayout(header_layout)

        self.version_combo = QComboBox()
        self.version_combo.setToolTip(
            "Other .ass files that share the first name token. "
            "Changing this does not replace anything.",
        )
        layout.addWidget(self.version_combo)

        self.load_btn = QPushButton("Import - Replace Selected")
        self.load_btn.setToolTip(
            "Import the chosen .ass as a new standin and instance-replace the current selection.",
        )
        self.load_btn.clicked.connect(self.on_load)
        layout.addWidget(self.load_btn)

        layout.addStretch(1)

        note = QLabel(
            "Currently works with Arnold proxy .ass files and the nLol naming convention "
            "<name>_<direction>_<id>_<type>.",
        )
        note.setObjectName("noteLabel")
        note.setWordWrap(True)
        note.setTextFormat(Qt.PlainText)
        note.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(note)

        self.query_selection()

    def query_selection(self) -> None:
        """Fill the version list from the first selected standin."""
        self.version_combo.clear()
        result = replace_obj_tool_core.query_first_selection()
        self.status_label.setText(result["status"])

        current = result["current"]
        for path in result["versions"]:
            label = path.stem
            if current is not None and replace_obj_tool_core.paths_match(path, current):
                label = f"{label} (current)"
            self.version_combo.addItem(label, str(path))

    def on_load(self) -> None:
        """Import the chosen version and replace the current selection."""
        index = self.version_combo.currentIndex()
        if index < 0:
            logger.warning("Choose a version to load.")
            self.status_label.setText("Choose a version to load.")
            return
        replace_obj_tool_core.replace_selected(self.version_combo.itemData(index))


def show_tool():
    """Launch and show the replace object tool."""
    ReplaceObjToolUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    ReplaceObjToolUI().reload_tool()
