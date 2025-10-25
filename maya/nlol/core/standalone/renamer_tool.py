import sys
from pathlib import Path

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from shiboken6 import wrapInstance

from maya import OpenMayaUI as omui
from maya import cmds
from nlol.core.general_utils import maya_undo
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


class RenamerTool(MayaQWidgetDockableMixin, QWidget):
    """Maya object renamer tool with UI and functionality."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        super().__init__(parent)

        self.setObjectName("nLolRenamerTool")
        self.setWindowTitle("nLol Renamer Tool")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        rename_btn = QPushButton("Rename")
        rename_btn.clicked.connect(self.rename)
        layout.addWidget(rename_btn)

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

        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))
        self.find_input = QLineEdit()
        find_layout.addWidget(self.find_input)
        layout.addLayout(find_layout)

        replace_with_layout = QHBoxLayout()
        replace_with_layout.addWidget(QLabel("Replace:"))
        self.replace_with_input = QLineEdit()
        replace_with_layout.addWidget(self.replace_with_input)
        layout.addLayout(replace_with_layout)

        replace_btn = QPushButton("Replace in Names")
        replace_btn.clicked.connect(self.replace_in_names)
        layout.addWidget(replace_btn)

        layout.addStretch()

        # --------------------
        prefs_dir = cmds.internalVar(userPrefDir=True)
        self.prefs_path = str(Path(prefs_dir) / "nlol_tool_prefs.ini")
        self.settings = QSettings(self.prefs_path, QSettings.IniFormat)
        self.load_settings()

    @maya_undo
    def rename(self):
        """Rename Maya object."""
        try:
            selected = cmds.ls(selection=True)
            if not selected:
                logger.info("Select objects...")
                return

            new_name = self.name_input.text().strip()  # retrieve Qt string
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
        """Add prefix and/or suffix to Maya object name."""
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
            replace_str = self.replace_with_input.text().strip()
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

    def load_settings(self):
        """Get previously saved text fields from ".ini" config file and load them."""
        self.settings.beginGroup("RenamerTool")
        self.name_input.setText(self.settings.value("name_input", "", str))
        self.prefix_input.setText(self.settings.value("prefix_input", "", str))
        self.suffix_input.setText(self.settings.value("suffix_input", "", str))
        self.find_input.setText(self.settings.value("find_input", "", str))
        self.replace_with_input.setText(self.settings.value("replace_with_input", "", str))
        self.settings.endGroup()
        logger.info(f"[nLol Renamer Tool] Loaded from: {self.prefs_path}")

    def save_settings(self):
        """Save text fields to ".ini" config file."""
        self.settings.beginGroup("RenamerTool")
        self.settings.setValue("name_input", self.name_input.text())
        self.settings.setValue("prefix_input", self.prefix_input.text())
        self.settings.setValue("suffix_input", self.suffix_input.text())
        self.settings.setValue("find_input", self.find_input.text())
        self.settings.setValue("replace_with_input", self.replace_with_input.text())
        self.settings.endGroup()
        logger.debug(f"[nLol Renamer Tool] Saved to: {self.prefs_path}")


def _rebuild_ui():
    """Re-create widget inside restored workspaceControl.
    Needed for saving tool window position and docking location
    between Maya sessions.
    """
    workspace_control_name = "nLolRenamerToolWorkspaceControl"
    pointer = omui.MQtUtil.findControl(workspace_control_name)
    if not pointer:
        return
    control = wrapInstance(int(pointer), QWidget)

    from importlib import reload

    from nlol.core.standalone import renamer_tool

    reload(renamer_tool)
    widget = renamer_tool.RenamerTool()

    layout = control.layout()
    if layout is None:
        from PySide6.QtWidgets import QVBoxLayout

        layout = QVBoxLayout(control)
        control.setLayout(layout)
    layout.addWidget(widget)


def show_tool():
    """Entry point.
    --------------------------------------------------
    Launch and show tool UI window.
    Also, saves "next Maya session" "reload script" to "workspaceControl".
    """
    workspace_control_name = "nLolRenamerToolWorkspaceControl"

    if cmds.workspaceControl(workspace_control_name, query=True, exists=True):
        cmds.workspaceControl(workspace_control_name, edit=True, restore=True, visible=True)
        return

    tool = RenamerTool()
    tool.show(dockable=True, floating=True)

    cmds.workspaceControl(
        workspace_control_name,
        edit=True,
        label="nLol Renamer Tool",
        uiScript=(
            "from nlol.core.standalone import renamer_tool\n"
            "from importlib import reload\n"
            "reload(renamer_tool)\n"
            "renamer_tool._rebuild_ui()"
        ),
    )


def reload_tool():
    """Force reload the tool by closing the workspace and resetting the singleton."""
    if cmds.workspaceControl("nLolRenamerToolWorkspaceControl", query=True, exists=True):
        cmds.deleteUI("nLolRenamerToolWorkspaceControl")

    from importlib import reload

    reload(sys.modules[__name__])

    RenamerTool._instance = None
    show_tool()


if __name__ == "__main__":
    cmds.evalDeferred(show_tool)
