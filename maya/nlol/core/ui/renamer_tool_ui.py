import re

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from maya import cmds
from nlol.core.general_utils import maya_undo
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger

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
            "nlol_name_input": self.nlol_name_input,
            "nlol_direction_input": self.nlol_direction_input,
            "nlol_id_input": self.nlol_id_input,
            "nlol_type_input": self.nlol_type_input,
        }

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI code setup."""
        # ----- rename button
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        # -
        layout.addLayout(name_layout)

        rename_btn = QPushButton("Rename")
        rename_btn.clicked.connect(self.rename)
        # -
        layout.addWidget(rename_btn)

        # ----- prefix/suffix  button
        prefix_layout = QHBoxLayout()
        prefix_layout.addWidget(QLabel("Prefix:"))
        self.prefix_input = QLineEdit()
        prefix_layout.addWidget(self.prefix_input)
        # -
        layout.addLayout(prefix_layout)

        suffix_layout = QHBoxLayout()
        suffix_layout.addWidget(QLabel("Suffix:"))
        self.suffix_input = QLineEdit()
        suffix_layout.addWidget(self.suffix_input)
        # -
        layout.addLayout(suffix_layout)

        apply_btn = QPushButton("Prefix/ Suffix")
        apply_btn.clicked.connect(self.apply_prefix_suffix)
        # -
        layout.addWidget(apply_btn)

        # ----- find-replace  button
        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input)
        # -
        layout.addLayout(find_layout)

        replace_layout = QHBoxLayout()
        replace_layout.addWidget(QLabel("Replace:"))
        self.replace_input = QLineEdit()
        replace_layout.addWidget(self.replace_input)
        # -
        layout.addLayout(replace_layout)

        replace_btn = QPushButton("Replace")
        replace_btn.clicked.connect(self.replace_in_names)
        # -
        layout.addWidget(replace_btn)

        # ----- nlol rename button
        # name component
        nlol_component_layout = QHBoxLayout()
        nlol_component_layout.addWidget(QLabel("name:"))
        self.nlol_name_input = QLineEdit()
        nlol_component_layout.addWidget(self.nlol_name_input)
        # direction/side component
        nlol_component_layout.addWidget(QLabel("side:"))
        self.nlol_direction_input = QLineEdit()
        nlol_component_layout.addWidget(self.nlol_direction_input)
        # id component
        nlol_component_layout.addWidget(QLabel("id:"))
        self.nlol_id_input = QLineEdit()
        nlol_component_layout.addWidget(self.nlol_id_input)
        # type component
        nlol_component_layout.addWidget(QLabel("type:"))
        self.nlol_type_input = QLineEdit()
        nlol_component_layout.addWidget(self.nlol_type_input)
        # -
        layout.addLayout(nlol_component_layout)
        # button
        nlol_rename_btn = QPushButton("nLol Rename")
        nlol_rename_btn.clicked.connect(self.nlol_rename)
        # -
        layout.addWidget(nlol_rename_btn)

    @maya_undo
    def rename(self) -> None:
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

            selected_uuids = cmds.ls(selection=True, uuid=True)  # keep original order
            selected.sort(key=lambda x: x.count("|"), reverse=True)  # avoid dup name errors

            if len(selected) == 1:
                cmds.rename(selected[0], new_name)
            else:
                for i, obj in enumerate(selected):
                    cmds.rename(obj, f"tmp_object_string_{i + 1:02d}")
                for i, obj_uuid in enumerate(selected_uuids):
                    obj = cmds.ls(obj_uuid, long=True)[0]
                    cmds.rename(obj, f"{new_name}_{i + 1:02d}")
        finally:
            self.save_settings()

    @maya_undo
    def apply_prefix_suffix(self) -> None:
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

            selected.sort(key=lambda x: x.count("|"), reverse=True)  # avoid dup name errors
            for obj in selected:
                short_name = obj.split("|")[-1]  # avoid dup name errors
                cmds.rename(obj, f"{prefix}{short_name}{suffix}")
        finally:
            self.save_settings()

    @maya_undo
    def replace_in_names(self) -> None:
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

            selected.sort(key=lambda x: x.count("|"), reverse=True)  # avoid dup name errors
            for obj in selected:
                if find_str not in obj:
                    logger.info(f'"{find_str}" not in "{obj}"')
                    continue
                short_name = obj.split("|")[-1]  # avoid dup name errors
                new_name = short_name.replace(find_str, replace_str)
                cmds.rename(obj, new_name)
        finally:
            self.save_settings()

    @maya_undo
    def nlol_rename(self) -> None:
        """Rename using nLol naming convention; "<name>_<direction>_<id>_<type>"."""
        try:
            selected = cmds.ls(selection=True)
            if not selected:
                logger.info("Select objects...")
                return

            name_comp = self.remove_ws(self.nlol_name_input.text())
            direction_comp = self.remove_ws(self.nlol_direction_input.text())
            id_comp = self.remove_ws(self.nlol_id_input.text())
            type_comp = self.remove_ws(self.nlol_type_input.text())

            new_name = self.build_name(name_comp, direction_comp, id_comp, type_comp)
            if not new_name:
                logger.info("Enter a name...")
                return

            selected_uuids = cmds.ls(selection=True, uuid=True)  # keep original order
            selected.sort(key=lambda x: x.count("|"), reverse=True)  # avoid dup name errors

            if len(selected) == 1:
                cmds.rename(selected[0], new_name)
            else:
                for i, obj in enumerate(selected):
                    cmds.rename(obj, f"tmp_object_string_{i + 1:02d}")
                id_comp_update = id_comp
                for i, obj_uuid in enumerate(selected_uuids):
                    obj = cmds.ls(obj_uuid, long=True)[0]
                    new_name = self.build_name(name_comp, direction_comp, id_comp_update, type_comp)
                    cmds.rename(obj, new_name)
                    id_comp_update = self.increment_id(id_comp_update)
                    print(new_name)
        finally:
            self.save_settings()

    def increment_id(self, id_str: str) -> str:
        """Inrement nLol <id> component by 1. For instance, "a11b", will become "a12b"."""
        digits = re.search(r"(\d+)", id_str)
        if not digits:
            return id_str  # no digits, return as-is

        digits_update = int(digits.group(1)) + 1
        width = len(digits.group(1))  # number of digit characters.
        return id_str[: digits.start()] + str(digits_update).zfill(width) + id_str[digits.end() :]

    def build_name(self, name, direction, id_, type_):
        """Combine nLol name components.  Remove double underscores from string."""
        raw = f"{name}_{direction}_{id_}_{type_}"
        return re.sub(r"_+", "_", raw)  # replace double underscore w/ single

    def remove_ws(self, text: str) -> str:
        """Remove whitespace from string."""
        return re.sub(r"\s+", "", text)


# entry points
def show_tool():
    """Launch and show tool UI window."""
    RenamerToolUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    RenamerToolUI().reload_tool()
