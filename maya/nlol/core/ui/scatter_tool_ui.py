from importlib import reload

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from nlol.core.general_utils import maya_undo
from nlol.core.modeling_tools import scatter_objects
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger

reload(scatter_objects)

logger = get_logger()


class ScatterToolUI(DockableMayaUI):
    """Maya object scatter tool with UI and functionality."""

    def get_window_title(self) -> str:
        return "Scatter Tool UI"

    def get_settings_keys(self) -> dict:
        return {
            "updown_input": self.updown_input,
            "normal_orient_checkbox": self.normal_orient_checkbox,
            "normal_orient_rand_checkbox": self.normal_orient_rand_checkbox,
            "rand_rot_checkbox": self.rand_rot_checkbox,
            "super_rand_rot_checkbox": self.super_rand_rot_checkbox,
            "bb_normal_orient_checkbox": self.bb_normal_orient_checkbox,
            "bb_2d_checkbox": self.bb_2d_checkbox,
            "xminus_input": self.xminus_input,
            "xplus_input": self.xplus_input,
            "yminus_input": self.yminus_input,
            "yplus_input": self.yplus_input,
            "zminus_input": self.zminus_input,
            "zplus_input": self.zplus_input,
            "scale_low_input": self.scale_low_input,
            "scale_high_input": self.scale_high_input,
            "scale_stretch_input": self.scale_stretch_input,
            "tx_input": self.tx_input,
            "ty_input": self.ty_input,
            "tz_input": self.tz_input,
        }

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI code setup."""
        # --------------------
        scatter_to_verts_layout = QHBoxLayout()
        scatter_to_verts_btn = QPushButton("Scatter to Vertices")
        scatter_to_verts_btn.setToolTip("Scatter objects to last selected object vertices.")
        scatter_to_verts_btn.clicked.connect(self.scatter_to_verts)
        scatter_to_verts_layout.addWidget(scatter_to_verts_btn, stretch=1)

        updown_label = QLabel("Up\nDown:")
        updown_label.setAlignment(Qt.AlignCenter)
        updown_label_tip = 'Normal orient "y" translate offset.'
        updown_label.setToolTip(updown_label_tip)
        scatter_to_verts_layout.addWidget(updown_label)
        self.updown_input = QLineEdit()
        self.updown_input.setText("0.0")
        self.updown_input.setFixedWidth(50)
        self.updown_input.setToolTip(updown_label_tip)
        scatter_to_verts_layout.addWidget(self.updown_input)

        self.normal_orient_checkbox = QCheckBox("Normal\nOrient")
        self.normal_orient_checkbox.setToolTip("Orient scattered objects to surface normals.")
        scatter_to_verts_layout.addWidget(self.normal_orient_checkbox)
        self.normal_orient_rand_checkbox = QCheckBox("Normal\nOrient Rand")
        self.normal_orient_rand_checkbox.setToolTip("Randomly offset normal orient tilt.")
        scatter_to_verts_layout.addWidget(self.normal_orient_rand_checkbox)
        self.rand_rot_checkbox = QCheckBox("Rand\nRotate")
        self.rand_rot_checkbox.setToolTip("Randomly rotate scattered objects.")
        scatter_to_verts_layout.addWidget(self.rand_rot_checkbox)
        self.super_rand_rot_checkbox = QCheckBox("Super\nRand Rotate")
        self.super_rand_rot_checkbox.setToolTip("Randomly rotate scattered objects again.")
        scatter_to_verts_layout.addWidget(self.super_rand_rot_checkbox)

        layout.addLayout(scatter_to_verts_layout)

        # --------------------
        boundingbox_scatter_layout = QHBoxLayout()
        boundingbox_scatter_btn = QPushButton("Bounding Box Scatter")
        boundingbox_scatter_btn.setToolTip(
            "Scatter objects to last selected object bounding box. Then closest surface.",
        )
        boundingbox_scatter_btn.clicked.connect(self.boundingbox_scatter)
        boundingbox_scatter_layout.addWidget(boundingbox_scatter_btn)

        self.bb_2d_checkbox = QCheckBox("Surface\nSnap")
        self.bb_2d_checkbox.setFixedWidth(85)
        self.bb_2d_checkbox.setToolTip("Snap objects to surface after 3D bounding box scatter.")
        boundingbox_scatter_layout.addWidget(self.bb_2d_checkbox)

        self.bb_normal_orient_checkbox = QCheckBox("Normal\nOrient")
        self.bb_normal_orient_checkbox.setFixedWidth(85)
        self.bb_normal_orient_checkbox.setToolTip("Orient scattered objects to surface normals.")
        boundingbox_scatter_layout.addWidget(self.bb_normal_orient_checkbox)

        reset_translate_btn = QPushButton("Reset Translate")
        reset_translate_btn.setStyleSheet("text-align: center;")
        reset_translate_btn.setFixedWidth(130)
        reset_translate_btn.clicked.connect(
            lambda: scatter_objects.ScatterObjects().reset_transforms(translate=True),
        )
        boundingbox_scatter_layout.addWidget(reset_translate_btn)
        reset_rotate_btn = QPushButton("Reset Rotate")
        reset_rotate_btn.setStyleSheet("text-align: center;")
        reset_rotate_btn.setFixedWidth(130)
        reset_rotate_btn.clicked.connect(
            lambda: scatter_objects.ScatterObjects().reset_transforms(rotate=True),
        )
        boundingbox_scatter_layout.addWidget(reset_rotate_btn)
        reset_scale_btn = QPushButton("Reset Scale")
        reset_scale_btn.setStyleSheet("text-align: center;")
        reset_scale_btn.setFixedWidth(130)
        reset_scale_btn.clicked.connect(
            lambda: scatter_objects.ScatterObjects().reset_transforms(scale=True),
        )
        boundingbox_scatter_layout.addWidget(reset_scale_btn)

        layout.addLayout(boundingbox_scatter_layout)

        # --------------------
        random_rotate_layout = QHBoxLayout()
        random_rotate_btn = QPushButton("Random Rotate")
        random_rotate_btn.clicked.connect(self.random_rotate)
        random_rotate_layout.addWidget(random_rotate_btn)

        xplusminus_label = QLabel("X\n-+")
        xplusminus_label.setAlignment(Qt.AlignCenter)
        xplusminus_label.setFixedWidth(50)
        random_rotate_layout.addWidget(xplusminus_label)
        self.xminus_input = QLineEdit()
        self.xminus_input.setText("-20")
        self.xminus_input.setFixedWidth(50)
        random_rotate_layout.addWidget(self.xminus_input)
        self.xplus_input = QLineEdit()
        self.xplus_input.setText("20")
        self.xplus_input.setFixedWidth(50)
        random_rotate_layout.addWidget(self.xplus_input)

        yplusminus_label = QLabel("Y\n-+")
        yplusminus_label.setAlignment(Qt.AlignCenter)
        yplusminus_label.setFixedWidth(50)
        random_rotate_layout.addWidget(yplusminus_label)
        self.yminus_input = QLineEdit()
        self.yminus_input.setText("-360")
        self.yminus_input.setFixedWidth(50)
        random_rotate_layout.addWidget(self.yminus_input)
        self.yplus_input = QLineEdit()
        self.yplus_input.setText("360")
        self.yplus_input.setFixedWidth(50)
        random_rotate_layout.addWidget(self.yplus_input)

        zplusminus_label = QLabel("Z\n-+")
        zplusminus_label.setAlignment(Qt.AlignCenter)
        zplusminus_label.setFixedWidth(50)
        random_rotate_layout.addWidget(zplusminus_label)
        self.zminus_input = QLineEdit()
        self.zminus_input.setText("-20")
        self.zminus_input.setFixedWidth(50)
        random_rotate_layout.addWidget(self.zminus_input)
        self.zplus_input = QLineEdit()
        self.zplus_input.setText("20")
        self.zplus_input.setFixedWidth(50)
        random_rotate_layout.addWidget(self.zplus_input)

        layout.addLayout(random_rotate_layout)

        # --------------------
        random_scale_layout = QHBoxLayout()
        random_scale_btn = QPushButton("Random Scale")
        random_scale_btn.clicked.connect(self.random_scale)
        random_scale_layout.addWidget(random_scale_btn)
        scale_label = QLabel("Scale\n-+")
        scale_label.setAlignment(Qt.AlignCenter)
        scale_label.setFixedWidth(50)
        random_scale_layout.addWidget(scale_label)
        self.scale_low_input = QLineEdit()
        self.scale_low_input.setText("0.5")
        self.scale_low_input.setFixedWidth(50)
        random_scale_layout.addWidget(self.scale_low_input)
        self.scale_high_input = QLineEdit()
        self.scale_high_input.setText("3")
        self.scale_high_input.setFixedWidth(50)
        random_scale_layout.addWidget(self.scale_high_input)
        scale_stretch_label = QLabel("Scale\nStretch")
        scale_stretch_label.setAlignment(Qt.AlignCenter)
        scale_stretch_label.setFixedWidth(60)
        random_scale_layout.addWidget(scale_stretch_label)
        self.scale_stretch_input = QLineEdit()
        self.scale_stretch_input.setText("2")
        self.scale_stretch_input.setFixedWidth(50)
        random_scale_layout.addWidget(self.scale_stretch_input)

        layout.addLayout(random_scale_layout)

        # --------------------
        simple_move_layout = QHBoxLayout()
        simple_move_btn = QPushButton("Simple Move")
        simple_move_btn.clicked.connect(self.simple_move)
        simple_move_layout.addWidget(simple_move_btn)
        tx_label = QLabel("X\n-+")
        tx_label.setAlignment(Qt.AlignCenter)
        tx_label.setFixedWidth(50)
        simple_move_layout.addWidget(tx_label)
        self.tx_input = QLineEdit()
        self.tx_input.setText("0.0")
        self.tx_input.setFixedWidth(50)
        simple_move_layout.addWidget(self.tx_input)
        ty_label = QLabel("Y\n-+")
        ty_label.setAlignment(Qt.AlignCenter)
        ty_label.setFixedWidth(50)
        simple_move_layout.addWidget(ty_label)
        self.ty_input = QLineEdit()
        self.ty_input.setText("-5.0")
        self.ty_input.setFixedWidth(50)
        simple_move_layout.addWidget(self.ty_input)
        tz_label = QLabel("Z\n-+")
        tz_label.setAlignment(Qt.AlignCenter)
        tz_label.setFixedWidth(50)
        simple_move_layout.addWidget(tz_label)
        self.tz_input = QLineEdit()
        self.tz_input.setText("0.0")
        self.tz_input.setFixedWidth(50)
        simple_move_layout.addWidget(self.tz_input)

        layout.addLayout(simple_move_layout)

        # --------------------
        create_random_objs_btn = QPushButton("Create Random Objects")
        create_random_objs_btn.clicked.connect(self.create_random_objs)
        layout.addWidget(create_random_objs_btn)

        # --------------------
        layout.setSpacing(4)

    @maya_undo
    def scatter_to_verts(self) -> None:
        """Scatter selected objects to last selected object's vertices."""
        normal_orient_bool = self.normal_orient_checkbox.isChecked()
        normal_orient_rand_bool = self.normal_orient_rand_checkbox.isChecked()
        rand_rot_bool = self.rand_rot_checkbox.isChecked()
        super_rand_rot_bool = self.super_rand_rot_checkbox.isChecked()

        updown_float = self.float_or_zero(self.updown_input)

        scatter_objects.ScatterObjects().scatter_to_verts(
            normal_orient=normal_orient_bool,
            move_up_down=updown_float,
            normal_orient_rand=normal_orient_rand_bool,
            rand_rot=rand_rot_bool,
            super_rand_rot=super_rand_rot_bool,
        )

        self.save_settings()

    @maya_undo
    def boundingbox_scatter(self) -> None:
        """Scatter selected objects to last selected object based on bounding box."""
        scatter_2d_bool = self.bb_2d_checkbox.isChecked()
        normal_orient_bool = self.bb_normal_orient_checkbox.isChecked()
        scatter_objects.ScatterObjects().boundingbox_scatter(
            normal_orient=normal_orient_bool,
            scatter_2d=scatter_2d_bool,
        )

        self.save_settings()

    @maya_undo
    def random_rotate(self) -> None:
        """Randomly rotate selected objects."""
        xminus_float = self.float_or_zero(self.xminus_input)
        xplus_float = self.float_or_zero(self.xplus_input)
        yminus_float = self.float_or_zero(self.yminus_input)
        yplus_float = self.float_or_zero(self.yplus_input)
        zminus_float = self.float_or_zero(self.zminus_input)
        zplus_float = self.float_or_zero(self.zplus_input)

        scatter_objects.ScatterObjects().random_rotate(
            x_rot_low=xminus_float,
            x_rot_high=xplus_float,
            y_rot_low=yminus_float,
            y_rot_high=yplus_float,
            z_rot_low=zminus_float,
            z_rot_high=zplus_float,
        )

        self.save_settings()

    @maya_undo
    def random_scale(self) -> None:
        """Randomly scale selected objects uniformly."""
        scale_low_float = self.float_or_zero(self.scale_low_input, 1.0)
        scale_high_float = self.float_or_zero(self.scale_high_input, 1.0)
        scale_stretch_float = self.float_or_zero(self.scale_stretch_input, 1.0)

        scatter_objects.ScatterObjects().random_scale(
            scale_low=scale_low_float,
            scale_high=scale_high_float,
            scale_stretch=scale_stretch_float,
        )

        self.save_settings()

    @maya_undo
    def simple_move(self) -> None:
        """Move the selected objects with simple tranformation values.
        Useful to push objects up or down. Helpful after scattering.
        """
        tx_float = self.float_or_zero(self.tx_input)
        ty_float = self.float_or_zero(self.ty_input)
        tz_float = self.float_or_zero(self.tz_input)

        scatter_objects.ScatterObjects().simple_move(
            x_trans_amnt=tx_float,
            y_trans_amnt=ty_float,
            z_trans_amnt=tz_float,
        )

        self.save_settings()

    @maya_undo
    def create_random_objs(self) -> None:
        """Create random polygon objects."""
        scatter_objects.ScatterObjects().create_random_objs()

        self.save_settings()

    def float_or_zero(self, line_edit: QLineEdit, default_float: float = 0.0) -> float:
        """Make sure a float gets returned.

        Args:
            line_edit: A QLineEdit widget.
            default_float: Backup float incase input fails.

        Returns:
            A float or a default zero float value.

        """
        txt = line_edit.text().strip()
        try:
            return float(txt)
        except ValueError:
            return default_float


# entry points
def show_tool():
    """Launch and show tool UI window."""
    ScatterToolUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    ScatterToolUI().reload_tool()
