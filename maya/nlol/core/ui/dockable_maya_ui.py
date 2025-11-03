import sys
from importlib import reload
from pathlib import Path

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from nlol.utilities.nlol_maya_logger import get_logger
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
from shiboken6 import wrapInstance

from maya import OpenMayaUI as omui
from maya import cmds

logger = get_logger()

stylesheet_filepath = Path(__file__).parent / "stylesheet.qss"


class DockableMayaUI(MayaQWidgetDockableMixin, QWidget):
    """Base class for dockable Maya UIs."""

    _instances = {}

    def __new__(cls, *args, **kwargs):
        """Singleton pattern per subclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    def __init__(self, parent=None):
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        super().__init__(parent)

        # basic properties
        self.setObjectName(self.get_object_name())

        # build ui
        layout = QVBoxLayout(self)
        self.build_ui(layout)
        layout.addStretch()

        # load qss stylesheet
        self.setStyleSheet(self.load_stylesheet())

        # initialize settings
        prefs_dir = cmds.internalVar(userPrefDir=True)
        self.prefs_path = str(Path(prefs_dir) / "nlol_tool_prefs.ini")
        self.settings = QSettings(self.prefs_path, QSettings.IniFormat)
        self.load_settings()

    def get_window_title(self) -> str:
        """Return window title."""
        raise NotImplementedError("Subclasses must implement get_window_title()")

    def get_object_name(self) -> str:
        """Return unique object name for this window."""
        window_title = self.get_window_title()
        object_name = "".join(window_title.split())
        return object_name

    def get_workspace_control_name(self) -> str:
        """Return unique name for workspace control."""
        return f"{self.get_object_name()}WorkspaceControl"

    def get_settings_keys(self) -> dict:
        """Return dict of UI widget attributes for saving text fields. Implement in subclass.
        Example: {"name_input": self.name_input}
        """
        return {}

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Contains Qt UI code. Must be implemented by subclass."""
        raise NotImplementedError("Subclasses must implement build_ui()")

    def load_stylesheet(self) -> str:
        """Load stylesheet from ".qss" file."""
        try:
            return stylesheet_filepath.read_text()
        except FileNotFoundError:
            msg = f"Failed to load QSS stylesheet: {stylesheet_filepath}"
            logger.error(msg)
            raise

    def load_settings(self):
        """Get previously saved text fields from ".ini" config file and load them."""
        settings_group = self.get_object_name()
        self.settings.beginGroup(settings_group)

        for key, widget in self.get_settings_keys().items():
            value = self.settings.value(key, "", str)
            if hasattr(widget, "setText"):
                widget.setText(value)
        # Example: self.name_input.setText(self.settings.value("name_input", "", str))

        self.settings.endGroup()
        logger.info(f"[{self.get_window_title()}] Loaded from: {self.prefs_path}")

    def save_settings(self):
        """Save text fields to ".ini" config file."""
        settings_group = self.get_object_name()
        self.settings.beginGroup(settings_group)

        for key, widget in self.get_settings_keys().items():
            if hasattr(widget, "text"):
                self.settings.setValue(key, widget.text())
        # Example: self.settings.setValue("name_input", self.name_input.text())

        self.settings.endGroup()
        logger.info(f"[{self.get_window_title()}] Saved to: {self.prefs_path}")

    def show_tool(self):
        """Show tool UI. Will have previous position and size."""
        workspace_control_name = self.get_workspace_control_name()

        if cmds.workspaceControl(workspace_control_name, query=True, exists=True):
            cmds.workspaceControl(workspace_control_name, edit=True, restore=True, visible=True)
            return

        module_path = self.__class__.__module__
        class_name = self.__class__.__name__
        cmds.workspaceControl(
            workspace_control_name,
            label=self.get_window_title(),
            initialWidth=300,
            initialHeight=200,
            uiScript=f"from {module_path} import {class_name}\n{class_name}()._rebuild_ui()",
        )

    def _rebuild_ui(self):
        """Re-create widget inside restored workspaceControl.
        Needed for saving tool window position and docking location
        between Maya sessions.
        """
        workspace_control_name = self.get_workspace_control_name()
        pointer = omui.MQtUtil.findControl(workspace_control_name)
        if not pointer:
            return

        control = wrapInstance(int(pointer), QWidget)
        layout = control.layout()

        if layout is None:
            layout = QVBoxLayout(control)
            control.setLayout(layout)

        layout.addWidget(self.__class__())

    def reload_tool(self):
        """Force reload the tool by closing the workspace control object
        and resetting the singleton.
        """
        workspace_control_name = self.get_workspace_control_name()
        if cmds.workspaceControl(workspace_control_name, query=True, exists=True):
            cmds.deleteUI(workspace_control_name)

        reload(sys.modules[DockableMayaUI.__module__])
        reload(sys.modules[self.__class__.__module__])

        self.__class__._instances.pop(self.__class__, None)
        self.__class__().show_tool()
