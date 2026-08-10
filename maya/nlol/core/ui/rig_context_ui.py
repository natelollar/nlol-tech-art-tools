import json
from importlib import reload
from pathlib import Path

from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from nlol import defaults
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_folder_path)

set_environment_variables = rig_folder_path.set_environment_variables

RIG_CONTEXT_JSON = Path(defaults.__file__).parent / "rig_context.json"

RIGS_KEY = "rigs"
ENV_VARS_KEY = "environment_variables"

RIG_COL_ACTIVE = 0
RIG_COL_NAME = 1
RIG_COL_FOLDERPATH = 2

ENV_COL_NAME = 0
ENV_COL_FOLDERPATH = 1

RIGS_TAB_INDEX = 0
ENV_VARS_TAB_INDEX = 1
# NOTE: tabs must be added in this order (see build_ui) for these indices to be correct

logger = get_logger()


class RigContextUI(DockableMayaUI):
    """UI for editing rig context from rig_context.json.
    Ability to select active rig folder and edit environment variables.
    """

    def get_window_title(self) -> str:
        return "nLol Rig Context UI"

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI code setup."""
        button_row = QHBoxLayout()

        self.build_skeletal_mesh_btn = QPushButton("Build Skeletal Mesh")
        self.build_skeletal_mesh_btn.setToolTip(
            "Build only skeletal mesh. Stop before rig is built.",
        )
        self.build_skeletal_mesh_btn.clicked.connect(self.on_build_skeletal_mesh)
        button_row.addWidget(self.build_skeletal_mesh_btn)

        self.build_rig_btn = QPushButton("Build Rig")
        self.build_rig_btn.setToolTip("Build rig files from active rig folder.")
        self.build_rig_btn.clicked.connect(self.on_build_rig)
        button_row.addWidget(self.build_rig_btn)

        self.build_rig_btn = QPushButton("Build Save Active")
        self.build_rig_btn.setToolTip("Build active rig. Update materials. Save files.")
        self.build_rig_btn.clicked.connect(self.on_build_save_active)
        button_row.addWidget(self.build_rig_btn)

        self.build_rig_btn = QPushButton("Build Save All")
        self.build_rig_btn.setToolTip(
            "Build and save all auto-rigs in Character folder. Update materials too.\n"
            "Character folder is parent folder of current active rig.",
        )
        self.build_rig_btn.clicked.connect(self.on_build_save_all)
        button_row.addWidget(self.build_rig_btn)

        button_row.addStretch()
        layout.addLayout(button_row)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget, 1)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.rigs_table = self.build_rigs_tab()
        self.env_table = self.build_env_vars_tab()

        refresh_row = QHBoxLayout()

        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setToolTip("Reload the current tab from rig_context.json.")
        self.refresh_btn.clicked.connect(lambda: self.on_refresh_clicked())
        refresh_row.addWidget(self.refresh_btn)

        refresh_row.addStretch()

        self.add_btn = QPushButton("+")
        self.add_btn.setToolTip("Add a new entry to the current tab.")
        self.add_btn.clicked.connect(lambda: self.on_add_clicked())
        refresh_row.addWidget(self.add_btn)

        self.remove_btn = QPushButton("-")
        self.remove_btn.setToolTip("Remove the selected entry from the current tab.")
        self.remove_btn.clicked.connect(lambda: self.on_remove_clicked())
        refresh_row.addWidget(self.remove_btn)

        layout.addLayout(refresh_row)

        self.populate_rigs()
        self.populate_env_vars()

    def build_rigs_tab(self) -> QTableWidget:
        """Build the "Rigs" tab: Active / Name / Folderpath table."""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Active", "Name", "Folderpath"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.DoubleClicked)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.setSelectionBehavior(QTableWidget.SelectRows)

        header = table.horizontalHeader()
        header.setSectionResizeMode(RIG_COL_ACTIVE, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(RIG_COL_NAME, QHeaderView.Interactive)
        header.setSectionResizeMode(RIG_COL_FOLDERPATH, QHeaderView.Stretch)

        table.itemChanged.connect(self.on_rig_item_changed)

        tab_layout.addWidget(table)
        self.tab_widget.addTab(tab, "Rigs")

        return table

    def build_env_vars_tab(self) -> QTableWidget:
        """Build the "Environment Variables" tab: Name / Folderpath table."""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Name", "Folderpath"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.DoubleClicked)
        table.setSelectionMode(QTableWidget.SingleSelection)
        table.setSelectionBehavior(QTableWidget.SelectRows)

        header = table.horizontalHeader()
        header.setSectionResizeMode(ENV_COL_NAME, QHeaderView.Interactive)
        header.setSectionResizeMode(ENV_COL_FOLDERPATH, QHeaderView.Stretch)

        table.itemChanged.connect(self.on_env_item_changed)

        tab_layout.addWidget(table)

        apply_row = QHBoxLayout()
        self.apply_env_vars_btn = QPushButton("Apply Env Vars")
        self.apply_env_vars_btn.setToolTip(
            "Apply these environment variables to the current Maya session,\n"
            "without needing to restart Maya.",
        )
        self.apply_env_vars_btn.clicked.connect(lambda: self.on_apply_env_vars())
        apply_row.addWidget(self.apply_env_vars_btn)
        apply_row.addStretch()
        tab_layout.addLayout(apply_row)

        self.tab_widget.addTab(tab, "Environment Variables")

        return table

    def pad_column_to_contents(self, table: QTableWidget, col: int) -> None:
        """Resize a column to fit its content, plus a couple characters of padding."""
        table.resizeColumnToContents(col)
        padding = table.fontMetrics().horizontalAdvance("MM")
        table.setColumnWidth(col, table.columnWidth(col) + padding)

    def on_build_skeletal_mesh(self) -> None:
        """Build only skeletal mesh. Stop before rig is built."""
        from importlib import reload

        from nlol.core.rig_setup import rig_build_mesh_skeleton

        reload(rig_build_mesh_skeleton)
        rig_build_mesh_skeleton.run_mesh_skeleton_build()

    def on_build_rig(self) -> None:
        """Build rig files from active rig folder."""
        from importlib import reload

        from nlol.core.rig_setup import rig_build

        reload(rig_build)
        rig_build.run_rig_build()

    def on_build_save_active(self) -> None:
        """Build active rig. Update materials. Save files."""
        from importlib import reload

        from nlol.core.rig_setup import rig_build_all

        reload(rig_build_all)
        rig_build_all.RigBuildSaveAll().build_active_only()

    def on_build_save_all(self) -> None:
        """Build and save all auto-rigs in Character folder. Update materials too.
        Character folder is parent folder of current active rig.
        """
        from importlib import reload

        from nlol.core.rig_setup import rig_build_all

        reload(rig_build_all)
        rig_build_all.RigBuildSaveAll().build()

    # ----- shared refresh / add / remove, dispatched by current tab -----
    def refresh_all_tabs(self) -> None:
        """Refresh all tabs from json.
        Useful for updating active rig radio button from outside class.
        """
        self.populate_rigs()
        self.populate_env_vars()

    def on_refresh_clicked(self) -> None:
        """Reload whichever tab is currently active."""
        if self.tab_widget.currentIndex() == RIGS_TAB_INDEX:
            self.populate_rigs()
        else:
            self.populate_env_vars()

    def on_add_clicked(self) -> None:
        """Add a new entry to whichever tab is currently active."""
        if self.tab_widget.currentIndex() == RIGS_TAB_INDEX:
            self.on_add_rig()
        else:
            self.on_add_env_var()

    def on_remove_clicked(self) -> None:
        """Remove the selected entry from whichever tab is currently active."""
        if self.tab_widget.currentIndex() == RIGS_TAB_INDEX:
            self.on_remove_rig()
        else:
            self.on_remove_env_var()

    # ----- rigs tab -----

    def populate_rigs(self) -> None:
        """Read rig_context.json and build a table row per rig entry."""
        # detach old radio buttons from the group before the table deletes them
        for btn in self.button_group.buttons():
            self.button_group.removeButton(btn)

        # block signals so building the table doesn't trigger on_rig_item_changed
        self.rigs_table.blockSignals(True)

        self.rigs_table.setRowCount(0)

        data = self.load_rig_context()
        rigs = [rig for rig in data.get(RIGS_KEY, []) if rig.get("name", "")]

        self.rigs_table.setRowCount(len(rigs))
        self.row_rig_names = []

        for row, rig in enumerate(rigs):
            name = rig["name"]
            folderpath = rig.get("folderpath", "")
            self.row_rig_names.append(name)

            radio = QRadioButton()
            radio.setChecked(rig.get("active", False))
            radio.toggled.connect(
                lambda checked, rig_name=name: self.on_rig_toggled(rig_name, checked),
            )
            self.button_group.addButton(radio)
            self.rigs_table.setCellWidget(row, RIG_COL_ACTIVE, radio)

            self.rigs_table.setItem(row, RIG_COL_NAME, QTableWidgetItem(name))
            self.rigs_table.setItem(
                row,
                RIG_COL_FOLDERPATH,
                QTableWidgetItem(folderpath),
            )

        self.rigs_table.blockSignals(False)
        self.pad_column_to_contents(self.rigs_table, RIG_COL_NAME)

    def on_rig_toggled(self, rig_name: str, checked: bool) -> None:
        """Update rig_context.json when a radio button is toggled active."""
        if not checked:
            return

        data = self.load_rig_context()
        for rig in data.get(RIGS_KEY, []):
            rig["active"] = rig.get("name", "") == rig_name

        if self.write_context(data):
            logger.info(f'Set active rig: "{rig_name}"')

    def on_rig_item_changed(self, item: QTableWidgetItem) -> None:
        """Update rig_context.json when a rig Name or Folderpath cell is edited."""
        row = item.row()
        col = item.column()

        old_name = self.row_rig_names[row]
        data = self.load_rig_context()
        rig = next(
            (r for r in data.get(RIGS_KEY, []) if r.get("name", "") == old_name),
            None,
        )
        if rig is None:
            return

        if col == RIG_COL_NAME:
            new_name = item.text().strip()
            if not new_name:
                self.populate_rigs()  # revert, empty name not allowed
                return
            rig["name"] = new_name
        elif col == RIG_COL_FOLDERPATH:
            rig["folderpath"] = item.text().strip()
        else:
            return

        if self.write_context(data):
            self.row_rig_names[row] = rig["name"]
            logger.info(f'Updated rig "{old_name}"')

    def on_add_rig(self) -> None:
        """Add a new rig entry with a generic name/folderpath, not active."""
        data = self.load_rig_context()
        rigs = data.setdefault(RIGS_KEY, [])

        existing_names = {rig.get("name", "") for rig in rigs}
        new_name = "new_rig"
        i = 1
        while new_name in existing_names:
            new_name = f"new_rig_{i}"
            i += 1

        rigs.append({"name": new_name, "folderpath": "", "active": False})

        if self.write_context(data):
            self.populate_rigs()
            logger.info(f'Added rig: "{new_name}"')

    def on_remove_rig(self) -> None:
        """Remove the selected rig entry."""
        row = self.rigs_table.currentRow()
        if row < 0 or row >= len(self.row_rig_names):
            return

        rig_name = self.row_rig_names[row]

        confirm = QMessageBox.question(
            self,
            "Remove Rig",
            f'Remove "{rig_name}" from rig_context.json?',
        )
        if confirm != QMessageBox.Yes:
            return

        data = self.load_rig_context()
        data[RIGS_KEY] = [rig for rig in data.get(RIGS_KEY, []) if rig.get("name", "") != rig_name]

        if self.write_context(data):
            self.populate_rigs()
            logger.info(f'Removed rig: "{rig_name}"')

    # ----- environment variables tab -----

    def populate_env_vars(self) -> None:
        """Read rig_context.json and build a table row per environment variable."""
        self.env_table.blockSignals(True)

        self.env_table.setRowCount(0)

        data = self.load_rig_context()
        env_vars = [ev for ev in data.get(ENV_VARS_KEY, []) if ev.get("name", "")]

        self.env_table.setRowCount(len(env_vars))
        self.row_env_names = []

        for row, env_var in enumerate(env_vars):
            name = env_var["name"]
            folderpath = env_var.get("folderpath", "")
            self.row_env_names.append(name)

            self.env_table.setItem(row, ENV_COL_NAME, QTableWidgetItem(name))
            self.env_table.setItem(
                row,
                ENV_COL_FOLDERPATH,
                QTableWidgetItem(folderpath),
            )

        self.env_table.blockSignals(False)
        self.pad_column_to_contents(self.env_table, ENV_COL_NAME)

    def on_env_item_changed(self, item: QTableWidgetItem) -> None:
        """Update rig_context.json when an env var Name or Folderpath cell is edited."""
        row = item.row()
        col = item.column()

        old_name = self.row_env_names[row]
        data = self.load_rig_context()
        env_var = next(
            (ev for ev in data.get(ENV_VARS_KEY, []) if ev.get("name", "") == old_name),
            None,
        )
        if env_var is None:
            return

        if col == ENV_COL_NAME:
            new_name = item.text().strip()
            if not new_name:
                self.populate_env_vars()  # revert, empty name not allowed
                return
            env_var["name"] = new_name
        elif col == ENV_COL_FOLDERPATH:
            env_var["folderpath"] = item.text().strip()
        else:
            return

        if self.write_context(data):
            self.row_env_names[row] = env_var["name"]
            logger.info(f'Updated environment variable "{old_name}"')

    def on_apply_env_vars(self) -> None:
        """Apply environment variables from "rig_context.json".
        Calls the "set_environment_variables(force=True)" so edits made in
        this UI take effect in current Maya session, including overwriting
        existing env vars.
        """
        set_environment_variables(force=True)

        QMessageBox.information(
            self,
            "Environment Variables Applied",
            "Environment variables applied. Existing variables overwritten.\n"
            "Restart Maya to remove old variables.",
        )

    def on_add_env_var(self) -> None:
        """Add a new environment variable entry with a generic name/folderpath."""
        data = self.load_rig_context()
        env_vars = data.setdefault(ENV_VARS_KEY, [])

        existing_names = {ev.get("name", "") for ev in env_vars}
        new_name = "NEW_ENV_VAR"
        i = 1
        while new_name in existing_names:
            new_name = f"NEW_ENV_VAR_{i}"
            i += 1

        env_vars.append({"name": new_name, "folderpath": ""})

        if self.write_context(data):
            self.populate_env_vars()
            logger.info(f'Added environment variable: "{new_name}"')

    def on_remove_env_var(self) -> None:
        """Remove the selected environment variable entry."""
        row = self.env_table.currentRow()
        if row < 0 or row >= len(self.row_env_names):
            return

        env_name = self.row_env_names[row]

        confirm = QMessageBox.question(
            self,
            "Remove Environment Variable",
            f'Remove "{env_name}" from rig_context.json?',
        )
        if confirm != QMessageBox.Yes:
            return

        data = self.load_rig_context()
        data[ENV_VARS_KEY] = [
            ev for ev in data.get(ENV_VARS_KEY, []) if ev.get("name", "") != env_name
        ]

        if self.write_context(data):
            self.populate_env_vars()
            logger.info(f'Removed environment variable: "{env_name}"')

    # ----- shared json load / save -----

    def write_context(self, data: dict) -> bool:
        """Save rig_context.json. Warn and revert the UI if the file is locked.

        Returns:
            True if the save succeeded, False otherwise.

        """
        try:
            self.save_rig_context(data)
        except PermissionError:
            logger.error(f'Permission denied writing: "{RIG_CONTEXT_JSON}"')
            QMessageBox.warning(
                self,
                "Rig Context Locked",
                "<Check Out> in Perforce!\n\n<rig_context.json> "
                "is READ-ONLY and change was not saved.",
            )
            self.populate_rigs()
            self.populate_env_vars()
            return False

        return True

    def load_rig_context(self) -> dict:
        """Load rig_context.json contents."""
        with open(RIG_CONTEXT_JSON) as f:
            return json.load(f)

    def save_rig_context(self, data: dict) -> None:
        """Write rig_context.json contents."""
        with open(RIG_CONTEXT_JSON, "w") as f:
            json.dump(data, f, indent=4)


# entry points
def show_tool():
    """Launch and show tool UI window."""
    RigContextUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    RigContextUI().reload_tool()


def refresh_if_open() -> None:
    """Refresh the Rig Context UI if an instance already exists. Safe to call from anywhere."""
    instance = RigContextUI._instances.get(RigContextUI)
    if instance is None:
        return

    try:
        instance.refresh_all_tabs()
    except RuntimeError:
        # underlying Qt C++ object was deleted (workspaceControl torn down)
        RigContextUI._instances.pop(RigContextUI, None)
