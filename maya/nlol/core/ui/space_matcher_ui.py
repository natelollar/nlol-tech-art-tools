"""
Space Match System for Maya Rigs
Switches control parent spaces while maintaining world position
"""
'''
import maya.cmds as cmds
import maya.api.OpenMaya as om2
from nlol.core.general_utils import maya_undo
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
)

logger = get_logger()


def match_space(control, new_parent):
    """
    Switch a control's parent while maintaining its world space position.
    
    Args:
        control (str): The control to reparent
        new_parent (str): The new parent object
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    # Validate inputs
    if not cmds.objExists(control):
        logger.warning(f"Control '{control}' does not exist")
        return False
    
    if not cmds.objExists(new_parent):
        logger.warning(f"Parent '{new_parent}' does not exist")
        return False
    
    try:
        # Get current world space position and rotation
        world_pos = cmds.xform(control, q=True, ws=True, t=True)
        world_rot = cmds.xform(control, q=True, ws=True, ro=True)
        
        # Get current parent constraints (if any)
        constraints = cmds.listRelatives(control, type='parentConstraint')
        
        # Create locator at control's current position
        locator = cmds.spaceLocator(n=f"{control}_matchLocator")[0]
        cmds.xform(locator, ws=True, t=world_pos)
        cmds.xform(locator, ws=True, ro=world_rot)
        
        # Parent constrain control to locator to freeze position
        cmds.parentConstraint(locator, control, mo=False)
        
        # Delete old parent constraint if it exists
        if constraints:
            for constraint in constraints:
                cmds.delete(constraint)
        
        # Now constrain control to new parent
        cmds.parentConstraint(new_parent, control, mo=True)
        
        # Delete locator
        cmds.delete(locator)
        
        logger.info(f"Successfully matched {control} to {new_parent}")
        return True
    
    except Exception as e:
        logger.error(f"Error during space match: {str(e)}")
        return False


def match_translate(control, new_parent):
    """
    Match only translation to new parent (keeps rotation offset).
    
    Args:
        control (str): The control to reparent
        new_parent (str): The new parent object
    """
    
    if not cmds.objExists(control):
        logger.warning(f"Control '{control}' does not exist")
        return False
    
    if not cmds.objExists(new_parent):
        logger.warning(f"Parent '{new_parent}' does not exist")
        return False
    
    try:
        world_pos = cmds.xform(control, q=True, ws=True, t=True)
        
        # Create locator and constrain
        locator = cmds.spaceLocator(n=f"{control}_matchLocator")[0]
        cmds.xform(locator, ws=True, t=world_pos)
        cmds.pointConstraint(locator, control, mo=False)
        
        # Delete old constraint
        constraints = cmds.listRelatives(control, type='pointConstraint')
        if constraints:
            for constraint in constraints:
                cmds.delete(constraint)
        
        # Apply new parent constraint
        cmds.pointConstraint(new_parent, control, mo=True)
        
        cmds.delete(locator)
        logger.info(f"Successfully matched translation for {control} to {new_parent}")
        return True
    
    except Exception as e:
        logger.error(f"Error during translate match: {str(e)}")
        return False


class SpaceMatcherUI(DockableMayaUI):
    """Maya space matcher tool with PySide6 UI."""

    def get_window_title(self) -> str:
        return "Space Matcher"

    def get_settings_keys(self) -> dict:
        return {
            "control_combo": self.control_combo,
            "parent_combo": self.parent_combo,
        }

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Build the space matcher UI."""
        
        # Control selection
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Control:"))
        self.control_combo = QComboBox()
        self.control_combo.currentTextChanged.connect(self.on_control_changed)
        control_layout.addWidget(self.control_combo)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_controls)
        control_layout.addWidget(refresh_btn)
        layout.addLayout(control_layout)
        
        # Parent space selection
        parent_layout = QHBoxLayout()
        parent_layout.addWidget(QLabel("Parent Space:"))
        self.parent_combo = QComboBox()
        parent_layout.addWidget(self.parent_combo)
        layout.addLayout(parent_layout)
        
        # Match buttons
        match_btn = QPushButton("Match Space (T+R)")
        match_btn.clicked.connect(self.on_match_space)
        layout.addWidget(match_btn)
        
        translate_btn = QPushButton("Match Translate")
        translate_btn.clicked.connect(self.on_match_translate)
        layout.addWidget(translate_btn)
        
        # Populate controls on init
        self.refresh_controls()

    def refresh_controls(self):
        """Find all controls with parentSpaces attribute."""
        self.control_combo.blockSignals(True)
        self.control_combo.clear()
        
        # Find all transforms with parentSpaces attribute
        all_transforms = cmds.ls(type='transform', long=True) or []
        controls_with_spaces = []
        
        for obj in all_transforms:
            if cmds.attributeQuery('parentSpaces', node=obj, exists=True):
                controls_with_spaces.append(obj)
        
        # Populate combo with short names
        for ctrl in sorted(controls_with_spaces):
            short_name = ctrl.split("|")[-1]
            self.control_combo.addItem(short_name, userData=ctrl)
        
        self.control_combo.blockSignals(False)
        logger.info(f"Found {len(controls_with_spaces)} controls with parentSpaces attribute")

    def on_control_changed(self, control_name):
        """Update parent spaces dropdown when control changes."""
        self.parent_combo.blockSignals(True)
        self.parent_combo.clear()
        
        if not control_name:
            self.parent_combo.blockSignals(False)
            return
        
        # Get full path from userData
        control_index = self.control_combo.currentIndex()
        if control_index >= 0:
            control_path = self.control_combo.itemData(control_index)
        else:
            control_path = control_name
        
        try:
            # Get parentSpaces attribute
            if cmds.attributeQuery('parentSpaces', node=control_path, exists=True):
                attr_type = cmds.attributeQuery('parentSpaces', node=control_path, attributeType=True)
                
                if attr_type == 'enum':
                    # Enum type - get the field options
                    enum_opts = cmds.attributeQuery('parentSpaces', node=control_path, listEnum=True)
                    if enum_opts:
                        spaces = enum_opts[0].split(':')
                        for space in spaces:
                            if space:  # Skip empty strings
                                self.parent_combo.addItem(space)
                else:
                    # Try to read as string attribute
                    spaces_str = cmds.getAttr(f"{control_path}.parentSpaces")
                    if spaces_str:
                        spaces = spaces_str.split()
                        for space in spaces:
                            self.parent_combo.addItem(space)
                
                logger.info(f"Loaded parent spaces for {control_name}")
        
        except Exception as e:
            logger.error(f"Error reading parentSpaces: {str(e)}")
        
        self.parent_combo.blockSignals(False)

    @maya_undo
    def on_match_space(self):
        """Match full space (translation + rotation)."""
        try:
            control_index = self.control_combo.currentIndex()
            if control_index < 0:
                logger.warning("Select a control...")
                return
            
            control = self.control_combo.itemData(control_index)
            parent_space = self.parent_combo.currentText()
            
            if not parent_space:
                logger.warning("Select a parent space...")
                return
            
            match_space(control, parent_space)
        finally:
            self.save_settings()

    @maya_undo
    def on_match_translate(self):
        """Match translation only."""
        try:
            control_index = self.control_combo.currentIndex()
            if control_index < 0:
                logger.warning("Select a control...")
                return
            
            control = self.control_combo.itemData(control_index)
            parent_space = self.parent_combo.currentText()
            
            if not parent_space:
                logger.warning("Select a parent space...")
                return
            
            match_translate(control, parent_space)
        finally:
            self.save_settings()


# Entry points
def show_tool():
    """Launch and show tool UI window."""
    SpaceMatcherUI().show_tool()
'''

def reload_tool():
    """Force reload the tool."""
    # SpaceMatcherUI().reload_tool()
    print("WIP!!!")


# get ui to change parent spaces with dop down, like normal
# then just space match a locator when that ctrl changes