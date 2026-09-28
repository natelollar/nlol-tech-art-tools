"""Dockable Maya UI for the USD tool."""

from importlib import reload

from PySide6.QtWidgets import QPushButton, QVBoxLayout

from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.core.ui.usd_tool import usd_tool_core

reload(usd_tool_core)


class UsdToolUI(DockableMayaUI):
    """USD tool for MaterialX save, viewport refresh, and duplicating onto Maya objects."""

    def get_window_title(self) -> str:
        return "USD Tool"

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Build the main UI."""
        save_btn = QPushButton("Save MaterialX to Source")
        save_btn.setToolTip(
            "Write value edits on the selected MaterialX material back to its source .mtlx file."
        )
        save_btn.clicked.connect(usd_tool_core.save_selected_mtlx)
        layout.addWidget(save_btn)

        refresh_btn = QPushButton("USD Viewport Refresh")
        refresh_btn.setToolTip("Redraw every Maya USD proxy, including materials and textures.")
        refresh_btn.clicked.connect(usd_tool_core.refresh_usd_scenes)
        layout.addWidget(refresh_btn)

        duplicate_btn = QPushButton("Duplicate USD to Maya Objects")
        duplicate_btn.setToolTip(
            "Duplicate the selected USD Xform onto each selected Maya object. "
            "Copies translate, rotate, and scale."
        )
        duplicate_btn.clicked.connect(usd_tool_core.duplicate_usd_to_maya_objects)
        layout.addWidget(duplicate_btn)


def show_tool():
    """Launch and show the USD tool."""
    UsdToolUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    UsdToolUI().reload_tool()
