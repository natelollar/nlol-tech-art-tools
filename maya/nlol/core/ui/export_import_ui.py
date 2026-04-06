from importlib import reload
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
)

from maya import cmds, mel
from nlol.core.modeling_tools import export_import_multiple
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger

reload(export_import_multiple)
ExportImportMultiple = export_import_multiple.ExportImportMultiple

logger = get_logger()


class ExportImportUI(DockableMayaUI):
    """UI for exporting and importing multiple objects to Maya
    including Arnold proxies.
    """

    EXPORT_TYPES = [
        ("OBJ", "OBJexport"),
        ("FBX", "FBX export"),
        ("MA", "mayaAscii"),
        ("MB", "mayaBinary"),
        ("ASS", "ASS Export"),
    ]

    def get_window_title(self) -> str:
        return "Export Import UI"

    def get_settings_keys(self) -> dict:
        return {
            "folder_input": self.folder_input,
            "radio_group": self.radio_group,
            "auto_remove_ns_checkbox": self.auto_remove_ns_checkbox,
        }

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI code setup."""
        # ----- EXPORT SECTION -----
        layout.addWidget(QLabel("==================== EXPORT ===================="))

        # folder path
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Folder:")
        folder_label.setFixedWidth(60)
        folder_layout.addWidget(folder_label)
        self.folder_input = QLineEdit()
        folder_layout.addWidget(self.folder_input)
        browse_btn = QPushButton("...")
        browse_btn.setFixedWidth(30)
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)

        # export type radio buttons
        radio_layout = QHBoxLayout()
        radio_label = QLabel("Type:")
        radio_label.setFixedWidth(60)
        radio_layout.addWidget(radio_label)
        self.radio_group = QButtonGroup()
        for i, (label, _) in enumerate(self.EXPORT_TYPES):
            btn = QRadioButton(label)
            btn.setFixedWidth(50)
            self.radio_group.addButton(btn, i)
            radio_layout.addWidget(btn)
            if i == 0:
                btn.setChecked(True)
        radio_layout.addStretch()
        layout.addLayout(radio_layout)

        # export button
        export_btn = QPushButton("Export Selected ----->")
        export_btn.setFixedWidth(200)
        export_btn.clicked.connect(self.export_selected)
        layout.addWidget(export_btn)

        # ----- IMPORT SECTION -----
        layout.addWidget(QLabel("==================== IMPORT ===================="))

        # import button
        import_btn = QPushButton("Import Files <-----")
        import_btn.setFixedWidth(200)
        import_btn.clicked.connect(self.import_files)
        layout.addWidget(import_btn)

        # auto remove ns checkbox
        import_utility_layout = QHBoxLayout()
        self.auto_remove_ns_checkbox = QCheckBox("Auto Remove Namespace:  ")
        self.auto_remove_ns_checkbox.setFixedWidth(200)
        self.auto_remove_ns_checkbox.setLayoutDirection(Qt.RightToLeft)
        import_utility_layout.addWidget(self.auto_remove_ns_checkbox)

        # delete ns button
        delete_imp_ns_btn = QPushButton('Remove "ImportedNs:"')
        delete_imp_ns_btn.setFixedWidth(200)
        delete_imp_ns_btn.clicked.connect(self.delete_import_namespace)
        import_utility_layout.addWidget(delete_imp_ns_btn)

        import_utility_layout.addStretch()
        layout.addLayout(import_utility_layout)

        # delete unused nodes button
        delete_unused_nds_btn = QPushButton("Cleanup Unused Nodes...")
        delete_unused_nds_btn.setFixedWidth(200)
        delete_unused_nds_btn.clicked.connect(self.delete_unused_nodes)
        layout.addWidget(delete_unused_nds_btn)

    def browse_folder(self):
        """Open folder browser dialog. Choose export folder."""
        folder = cmds.fileDialog2(
            fileMode=3,
            caption="Choose Folder Path:",
            dialogStyle=2,
            okCaption="Accept",
        )
        if folder:
            self.folder_input.setText(folder[0])
            self.save_settings()

    def export_selected(self):
        """Export selected Maya objects to folder."""
        folder = self.folder_input.text().strip()
        if not folder:
            logger.info("Enter a folder path...")
            return

        if not Path(folder).exists():
            logger.info(f"Folder does not exist: {folder}")
            return

        selected_id = self.radio_group.checkedId()
        if selected_id == -1:  # when no button checked
            logger.info("Select an export type...")
            return

        _, object_type = self.EXPORT_TYPES[selected_id]

        objects = cmds.ls(selection=True)
        if not objects:
            logger.info("Select objects to export...")
            return

        ExportImportMultiple().export_multiple(
            folderpath=folder,
            object_type=object_type,
            objects=objects,
        )
        self.save_settings()

    def import_files(self):
        """Open file browser and import selected files."""
        file_filter = (
            "Supported Files (.obj, .fbx, .ma, .mb, .ass) (*.obj *.fbx *.ma *.mb *.ass);;"
            "Maya Scenes (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;"
            "OBJ (*.obj);;FBX (*.fbx);;ASS (*.ass)"
        )
        files = cmds.fileDialog2(
            fileMode=4,
            caption="Choose Files to Import:",
            dialogStyle=2,
            okCaption="Import",
            fileFilter=file_filter,
        )
        if not files:
            return

        self.auto_remove_ns_bool = self.auto_remove_ns_checkbox.isChecked()
        ExportImportMultiple().import_multiple(
            filepaths=files,
            auto_remove_ns=self.auto_remove_ns_bool,
        )
        self.save_settings()

    def delete_import_namespace(self):
        """Remove namespace added to import objects."""
        cmds.namespace(removeNamespace="importedNs", mergeNamespaceWithRoot=True)

    def delete_unused_nodes(self):
        """Remove unused nodes.
        Useful when testing object imports and shading nodes leftover.
        """
        mel.eval("MLdeleteUnused;")


# entry points
def show_tool():
    """Launch and show tool UI window."""
    ExportImportUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    ExportImportUI().reload_tool()
