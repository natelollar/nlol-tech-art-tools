from nlol.core.general_utils import maya_undo
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from maya import cmds

logger = get_logger()


class RenamerToolUI(DockableMayaUI):
    """Maya object renamer tool with UI and functionality."""

    def get_window_title(self) -> str:
        return "Renamer Tool UI"

    def get_settings_keys(self) -> dict:
        return {
            "name_input": self.name_input,
            "prefix_input": self.prefix_input,
            "suffix_input": self.suffix_input,
            "find_input": self.find_input,
            "replace_input": self.replace_input,
        }

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI code setup."""
        # rename button
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        rename_btn = QPushButton("Rename")
        rename_btn.clicked.connect(self.rename)
        layout.addWidget(rename_btn)

        # prefix/suffix  button
        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("Prefix:"))
        self.prefix_input = QLineEdit()
        prefix_layout.addWidget(self.prefix_input)
        layout.addLayout(prefix_layout)

        suffix_layout = QHBoxLayout()
        suffix_layout.addWidget(QLabel("Suffix:"))
        self.suffix_input = QLineEdit()
        suffix_layout.addWidget(self.suffix_input)
        layout.addLayout(suffix_layout)

        apply_btn = QPushButton("Apply Prefix/Suffix")
        apply_btn.clicked.connect(self.apply_prefix_suffix)
        layout.addWidget(apply_btn)

        # find-replace  button
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)

        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input)
        layout.addLayout(replace_layout)

        replace_btn = QPushButton("Replace in Names")
        replace_btn.clicked.connect(self.replace_in_names)
        layout.addWidget(replace_btn)

    @maya_undo
    def rename(self):
        """Rename Maya object."""
        try:
            selected = cmds.ls(selection=True)
            if not selected:
                logger.info("Select objects...")
                return

            new_name = self.name_input.text().strip()
            if not new_name:
                logger.info("Enter a name...")
                return

            if len(selected) == 1:
                cmds.rename(selected[0], new_name)
            else:
                for i, obj in enumerate(selected):
                    cmds.rename(obj, f"{new_name}_{i + 1:02d}")
        finally:
            self.save_settings()

    @maya_undo
    def apply_prefix_suffix(self):
        """Add prefix/suffix to Maya object name."""
        try:
            selected = cmds.ls(selection=True)
            if not selected:
                logger.info("Select objects...")
                return

            prefix = self.prefix_input.text().strip()
            suffix = self.suffix_input.text().strip()
            if not prefix and not suffix:
                logger.info("Enter a prefix or suffix...")
                return

            for obj in selected:
                short_name = obj.split("|")[-1]
                cmds.rename(obj, f"{prefix}{short_name}{suffix}")
        finally:
            self.save_settings()

    @maya_undo
    def replace_in_names(self):
        """Replace specified string in name."""
        try:
            selected = cmds.ls(selection=True)
            if not selected:
                logger.info("Select objects...")
                return

            find_str = self.find_input.text().strip()
            replace_str = self.replace_input.text().strip()
            if not find_str:
                logger.info("Enter a string to find...")
                return

            for obj in selected:
                if find_str not in obj:
                    logger.info(f'"{find_str}" not in "{obj}"')
                    continue
                new_name = obj.replace(find_str, replace_str)
                cmds.rename(obj, new_name)
        finally:
            self.save_settings()


# entry points
def show_tool():
    """Launch and show tool UI window."""
    RenamerToolUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    RenamerToolUI().reload_tool()
