from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from maya import cmds
from nlol.core.animation_tools.space_switch_match import SpaceSwitchMatch
from nlol.core.general_utils import maya_undo, swap_side_str
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()

PARENT_SPACE_ATTRS = [
    "parentSpaces",
    "pointSpace",
    "baseParent",
    "translateSpace",
    "rotateSpace",
    "scaleSpace",
]


def get_enum_options(ctrl: str, attr: str) -> list[str] | None:
    """Return list of enum label strings for ctrl.attr, or None if not an enum."""
    full_attr = f"{ctrl}.{attr}"
    if not cmds.objExists(full_attr):
        return None
    attr_type = cmds.getAttr(full_attr, type=True)
    if attr_type != "enum":
        return None
    try:
        enum_str = cmds.attributeQuery(attr, node=ctrl, listEnum=True)
        if not enum_str:
            return None
        return enum_str[0].split(":")
    except Exception:
        return None


def get_ctrl_space_data(ctrl: str) -> dict[str, list[str]]:
    """Return {attr_name: [enum_labels]} for all present parent space attrs on ctrl."""
    result = {}
    for attr in PARENT_SPACE_ATTRS:
        options = get_enum_options(ctrl, attr)
        if options is not None:
            result[attr] = options
    return result


def get_current_index(ctrl: str, attr: str) -> int:
    """Return current integer value of a parent space attr."""
    try:
        return int(cmds.getAttr(f"{ctrl}.{attr}"))
    except Exception:
        return 0


class SpaceSwitchMatchUI(DockableMayaUI):
    """UI for switching parent spaces across multiple controls simultaneously."""

    def get_window_title(self) -> str:
        return "Parent Space Match UI"

    def get_settings_keys(self) -> dict:
        return {}

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Build the main UI."""
        # ----- header --------------------
        header_layout = QHBoxLayout()

        self.query_btn = QPushButton("Load Selection")
        self.query_btn.setToolTip(
            "Load currently selected Maya controls and check their parent spaces.",
        )
        self.query_btn.clicked.connect(self.query_selection)
        header_layout.addWidget(self.query_btn)

        self.status_label = QLabel("No controls loaded.")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header_layout.addWidget(self.status_label, stretch=1)

        layout.addLayout(header_layout)

        # ----- loaded controls display --------------------
        self.ctrls_label = QLabel("")
        self.ctrls_label.setObjectName("ctrlsLabel")
        self.ctrls_label.setWordWrap(True)
        layout.addWidget(self.ctrls_label)

        # ----- space dropdowns container --------------------
        self.spaces_widget = QWidget()
        self.spaces_layout = QFormLayout(self.spaces_widget)
        self.spaces_layout.setLabelAlignment(Qt.AlignRight)
        self.spaces_layout.setSpacing(6)
        self.spaces_layout.setContentsMargins(0, 8, 0, 0)
        layout.addWidget(self.spaces_widget)
        self.spaces_widget.hide()

        # internal state
        self._ctrls: list[str] = []
        self._space_combos: dict[str, QComboBox] = {}  # attr -> combo

        # load any existing selection on launch
        self.query_selection()

    # ----- query & validate --------------------
    def query_selection(self):
        """Load selected rig ctrls and build the space switching UI."""
        selected = cmds.ls(selection=True, type="transform") or []

        while self.spaces_layout.rowCount():  # remove rows from the spaces form layout
            self.spaces_layout.removeRow(0)
        self._space_combos = {}

        self._ctrls = []

        if not selected:
            self.status_label.setText("Nothing selected.")
            self.ctrls_label.setText("")
            self.spaces_widget.hide()
            return

        self._ctrls = selected

        # show ctrl names
        names_text = "  ·  ".join(selected)
        self.ctrls_label.setText(names_text)

        # gather space data per ctrl
        all_data = {ctrl: get_ctrl_space_data(ctrl) for ctrl in selected}

        if not self._validate_match(all_data):
            return

        # all match - build dropdowns
        reference_data = all_data[selected[0]]
        self._build_spaces_ui(reference_data)

    def _validate_match(self, all_data: dict[str, dict[str, list[str]]]) -> bool:
        """Check that all ctrls share the same parent space attrs and enum options."""
        if not self._ctrls:
            return False

        reference = all_data[self._ctrls[0]]

        for ctrl in self._ctrls[1:]:
            ctrl_data = all_data[ctrl]

            # same attr keys?
            if set(ctrl_data.keys()) != set(reference.keys()):
                self.status_label.setText(
                    "Mismatch: controls have different parent space attributes.",
                )
                self.spaces_widget.hide()
                return False

            # same enum options per attr?
            for attr, options in reference.items():
                if (
                    ctrl_data.get(attr) != options
                    and [swap_side_str(at) for at in ctrl_data.get(attr)] != options
                ):
                    self.status_label.setText(
                        f"Mismatch: '{attr}' enum options differ between controls.",
                    )
                    self.spaces_widget.hide()
                    return False

        if not reference:
            self.status_label.setText(
                "No parent space attributes found on selected controls.",
            )
            self.spaces_widget.hide()
            return False

        attr_names = ", ".join(reference.keys())
        count = len(self._ctrls)
        noun = "control" if count == 1 else "controls"
        self.status_label.setText(
            f"{count} {noun} match  ·  {attr_names}",
        )
        return True

    # ----- build dropdowns --------------------
    def _build_spaces_ui(self, space_data: dict[str, list[str]]):
        """Create one labelled combo per parent space attr."""
        self._space_combos = {}

        for attr, options in space_data.items():
            combo = QComboBox()
            for i, label in enumerate(options):
                combo.addItem(f"{label}  [{i}]", userData=i)

            # set combo to the current value on the first ctrl (if single)
            if len(self._ctrls) == 1:
                current_idx = get_current_index(self._ctrls[0], attr)
                combo.setCurrentIndex(current_idx)
            else:
                # check if all ctrls share the same current index
                indices = [get_current_index(c, attr) for c in self._ctrls]
                if len(set(indices)) == 1:
                    combo.setCurrentIndex(indices[0])
                # else leave at 0 — mixed state

            label_widget = QLabel(f"{attr}:")
            label_widget.setObjectName("attrLabel")

            self.spaces_layout.addRow(label_widget, combo)
            self._space_combos[attr] = combo

            # connect AFTER setting initial index to avoid triggering switch
            combo.currentIndexChanged.connect(
                lambda idx, a=attr: self._on_space_changed(a, idx),
            )

        self.spaces_widget.show()

    def _clear_spaces_ui(self):
        """Remove all rows from the spaces form layout."""
        while self.spaces_layout.rowCount():
            self.spaces_layout.removeRow(0)
        self._space_combos = {}

    # ----- space switching --------------------
    @maya_undo
    def _on_space_changed(self, attr: str, combo_index: int):
        """Called when user changes a parent space dropdown.
        Runs SpaceSwitchMatch on all loaded controls for the changed attr.
        """
        if not self._ctrls:
            return

        combo = self._space_combos.get(attr)
        if combo is None:
            return

        space_value = combo.itemData(combo_index)
        if space_value is None:
            return

        new_parentspaces = {attr: space_value}
        switcher = SpaceSwitchMatch()

        for ctrl in self._ctrls:
            if not cmds.objExists(ctrl):
                logger.warning(f"Control no longer exists: {ctrl}")
                continue
            switcher.switch_match(ctrl, new_parentspaces)

        attr_display = f"{attr} -> {combo.currentText()}"
        logger.info(
            f"Space switched [{', '.join(self._ctrls)}]  {attr_display}",
        )


# ----- entry points --------------------
def show_tool():
    """Launch and show the Space Switch Match UI."""
    SpaceSwitchMatchUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    SpaceSwitchMatchUI().reload_tool()
