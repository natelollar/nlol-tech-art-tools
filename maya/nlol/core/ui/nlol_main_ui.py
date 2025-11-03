import os
from pathlib import Path

from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.shelves_menus import (
    animation_list,
    nurbs_curve_list,
    rigging_list,
    utility_list,
)
from nlol.utilities.nlol_maya_logger import get_logger
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

logger = get_logger()

CATEGORIES = {
    "Rigging": rigging_list.build_rigging_list,
    "Animation": animation_list.build_animation_list,
    "Nurbs Curves": nurbs_curve_list.build_curve_list,
    "Utils": utility_list.build_utility_list,
}


class NlolMainUI(DockableMayaUI):
    """Maya nLol Main UI with category switcher and tool buttons."""

    def get_window_title(self) -> str:
        return "nLol Main UI"

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI code setup."""
        # category dropdown
        dropdown_layout = QVBoxLayout()

        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES.keys())
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        dropdown_layout.addWidget(self.category_combo)
        layout.addLayout(dropdown_layout)

        # scrollable area for buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.buttons_container = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_container)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setSpacing(1)

        scroll_area.setWidget(self.buttons_container)
        layout.addWidget(scroll_area, 1)

        # populate initial category
        self.on_category_changed(self.category_combo.currentText())

    def on_category_changed(self, category_name: str) -> None:
        """Populate buttons for selected category."""
        # clear existing buttons
        while self.buttons_layout.count():  # loop runs while count > 0
            child = self.buttons_layout.takeAt(0)  # removes item at index 0
            if child.widget():  # check if child contains widget
                child.widget().deleteLater()

        # get items for this category
        items = CATEGORIES[category_name]()

        # create buttons
        for item in items:
            label = item["label"]
            command = item["command"]
            image = item.get("image", "")
            annotation = item.get("annotation", "")

            btn = QPushButton(label)
            btn.setToolTip(annotation)

            # add icon if available
            if image:
                try:
                    icon_path = self.resolve_icon_path(image)
                    if icon_path:
                        btn.setIcon(QIcon(icon_path))
                        btn.setIconSize(QSize(20, 20))
                except Exception as e:
                    logger.warning(f"Could not load icon {image}: {e}")

            # connect button to command
            btn.clicked.connect(lambda checked=False, cmd=command: exec(cmd))
            self.buttons_layout.addWidget(btn)

        self.buttons_layout.addStretch()

    def resolve_icon_path(self, image_name: str) -> str | None:
        """Resolve icon paths. Factory style paths (":/image.png") or xbml paths."""
        try:
            image_name = image_name.strip()

            # handle factory icons directly via Qt resource system
            if image_name.startswith(":/") or not Path(image_name).exists():
                # test if it's a valid factory resource
                factory_path = f":/{image_name}" if not image_name.startswith(":/") else image_name
                if QIcon(factory_path).availableSizes():  # non-empty sizes = valid icon
                    return factory_path

            # get xbml icon paths
            xbml_paths = os.environ.get("XBMLANGPATH", "")
            xbml_paths = [p for p in xbml_paths.split(os.pathsep) if p] if xbml_paths else []

            for base_path in xbml_paths:
                icon_path = Path(base_path) / image_name
                if icon_path.exists():
                    return str(icon_path)

            return None
        except Exception as e:
            logger.warning(f"Error resolving icon path for {image_name}: {e}")
            return None


# entry points
def show_tool():
    """Launch and show tool UI window."""
    NlolMainUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    NlolMainUI().reload_tool()
