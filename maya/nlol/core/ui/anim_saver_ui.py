from importlib import reload
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from maya import cmds
from nlol.core.animation_tools import animation_saver_loader
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger

reload(animation_saver_loader)

AnimationSaverLoader = animation_saver_loader.AnimationSaverLoader
DEFAULT_SAVE_LOCATION = str(animation_saver_loader.SAVE_LOCATION)

logger = get_logger()


class AnimationSaverLoaderUI(DockableMayaUI):
    """UI for saving and loading animation data to/from JSON,
    including namespace handling.
    """

    def get_window_title(self) -> str:
        return "Animation Saver Loader UI"

    def get_settings_keys(self) -> dict:
        return {
            "filepath_input": self.filepath_input,
            "export_remove_ns_checkbox": self.export_remove_ns_checkbox,
            "import_ns_input": self.import_ns_input,
        }

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI code setup."""
        # ----- FILE PATH SECTION -----
        filepath_layout = QHBoxLayout()
        filepath_label = QLabel("File:")
        filepath_label.setFixedWidth(60)
        filepath_layout.addWidget(filepath_label)
        self.filepath_input = QLineEdit()
        self.filepath_input.setPlaceholderText(DEFAULT_SAVE_LOCATION)
        self.filepath_input.setText(DEFAULT_SAVE_LOCATION)
        filepath_layout.addWidget(self.filepath_input)
        browse_btn = QPushButton("...")
        browse_btn.setFixedWidth(30)
        browse_btn.clicked.connect(self.browse_filepath)
        filepath_layout.addWidget(browse_btn)
        layout.addLayout(filepath_layout)

        # ----- EXPORT SECTION -----
        layout.addWidget(QLabel("========== SAVE =========="))

        # remove namespace on export checkbox
        export_ns_layout = QHBoxLayout()
        self.export_remove_ns_checkbox = QCheckBox("Save w/o Namespace:  ")
        self.export_remove_ns_checkbox.setFixedWidth(170)
        self.export_remove_ns_checkbox.setLayoutDirection(Qt.RightToLeft)
        export_ns_layout.addWidget(self.export_remove_ns_checkbox)
        export_ns_layout.addStretch()
        layout.addLayout(export_ns_layout)

        # export button
        export_btn = QPushButton("Save Ctrls Keyframes --->")
        export_btn.setFixedWidth(200)
        export_btn.clicked.connect(self.export_animation)
        layout.addWidget(export_btn)

        # ----- IMPORT SECTION -----
        layout.addWidget(QLabel("========== LOAD =========="))

        # namespace to apply on import
        import_ns_layout = QHBoxLayout()
        import_ns_label = QLabel("Add Namespace:")
        import_ns_label.setFixedWidth(120)
        import_ns_layout.addWidget(import_ns_label)
        self.import_ns_input = QLineEdit()
        self.import_ns_input.setFixedWidth(200)
        import_ns_layout.addWidget(self.import_ns_input)
        import_ns_layout.addStretch()
        layout.addLayout(import_ns_layout)

        # import button
        import_btn = QPushButton("Load Keyframe Data <---")
        import_btn.setFixedWidth(200)
        import_btn.clicked.connect(self.import_animation)
        layout.addWidget(import_btn)

    # ------------------------------------------------------------------
    # helpers

    def _get_filepath(self) -> Path | None:
        """Return the current filepath from input, or None if blank."""
        text = self.filepath_input.text().strip()
        return Path(text) if text else None

    def _get_saver_loader(self) -> AnimationSaverLoader:
        return AnimationSaverLoader(save_filepath=self._get_filepath())

    # ------------------------------------------------------------------
    # actions

    def browse_filepath(self):
        """Open file browser to choose save/load JSON path."""
        result = cmds.fileDialog2(
            fileMode=0,  # single file, new or existing
            caption="Choose Animation JSON File:",
            dialogStyle=2,
            okCaption="Accept",
            fileFilter="JSON Files (*.json)",
            startingDirectory=str(Path(self.filepath_input.text()).parent),
        )
        if result:
            self.filepath_input.setText(result[0])
            self.save_settings()

    def export_animation(self):
        """Export animation data from selected objects to JSON."""
        objects = cmds.ls(selection=True)
        if not objects:
            logger.info("Select objects to export animation from...")
            return

        filepath = self._get_filepath()
        if filepath and not filepath.parent.exists():
            logger.info(f"Directory does not exist: {filepath.parent}")
            return

        remove_ns = self.export_remove_ns_checkbox.isChecked()

        self._get_saver_loader().get_animation_data(
            objects=objects,
            remove_namespace=remove_ns,
        )
        self.save_settings()

    def import_animation(self):
        """Load and apply animation data from JSON to scene objects."""
        filepath = self._get_filepath()
        if not filepath or not filepath.exists():
            logger.info(f"File not found: {filepath}")
            return

        namespace = self.import_ns_input.text().strip() or None

        self._get_saver_loader().apply_animation_data(namespace=namespace)
        self.save_settings()


# entry points
def show_tool():
    """Launch and show tool UI window."""
    AnimationSaverLoaderUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    AnimationSaverLoaderUI().reload_tool()
