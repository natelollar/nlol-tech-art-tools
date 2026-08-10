import json
import os
from importlib import reload
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSlider,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from maya import cmds, mel
from nlol import defaults
from nlol.core.ui.dockable_maya_ui import DockableMayaUI
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()

RIG_CONTEXT_JSON = Path(defaults.__file__).parent / "rig_context.json"
AUTO_RIG_TAB_INDEX = 0

# Mid palette: cooler dark greys, sparse accents
CLR_BASE = (56, 56, 60)
CLR_BASE_ALT = (62, 62, 66)
CLR_SECTION = (40, 46, 48)
CLR_ACCENT = (38, 50, 44)
CLR_UI = (46, 50, 68)  # muted blue for buttons that open other UIs
CLR_RED = (92, 56, 56)
CLR_RED_SOFT = (84, 54, 54)
CLR_STATUS_OK = CLR_ACCENT
CLR_STATUS_WARN = (78, 50, 52)


class MultiToolUI(DockableMayaUI):
    """Dockable multi-tool UI. Modern nLol rebuild of the old Nate Tools tabs."""

    def get_window_title(self) -> str:
        return "nLol Multi Tool UI"

    def load_stylesheet(self) -> str:
        """Base QSS plus a muted multi-tool tint (this UI only)."""
        base = super().load_stylesheet()
        multi_tool_qss = """
        QWidget {
            background-color: rgb(38, 38, 42);
            color: rgb(215, 215, 215);
        }
        QTabWidget::pane {
            border: 1px solid rgb(68, 68, 72);
            background-color: rgb(38, 38, 42);
            top: -1px;
        }
        QTabBar::tab {
            background-color: rgb(48, 48, 52);
            color: rgb(200, 200, 200);
            border: 1px solid rgb(66, 66, 70);
            padding: 6px 10px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: rgb(60, 60, 66);
            border-bottom: 2px solid rgb(38, 50, 44);
        }
        QTabBar::tab:hover {
            background-color: rgb(54, 54, 58);
        }
        QScrollArea {
            border: none;
            background-color: rgb(38, 38, 42);
        }
        QLineEdit {
            background-color: rgb(32, 32, 36);
            border: 2px solid rgb(72, 72, 78);
            border-radius: 6px;
            color: rgb(215, 215, 215);
            padding: 2px;
        }
        QSlider::groove:horizontal {
            height: 6px;
            background: rgb(68, 72, 76);
            border: none;
            border-radius: 3px;
            margin: 4px 0;
        }
        QSlider::sub-page:horizontal {
            background: rgb(54, 68, 60);
            border: none;
            border-radius: 3px;
            height: 6px;
        }
        QSlider::add-page:horizontal {
            background: rgb(68, 72, 76);
            border: none;
            border-radius: 3px;
            height: 6px;
        }
        QSlider::handle:horizontal {
            background: rgb(210, 214, 216);
            border: none;
            width: 14px;
            height: 14px;
            margin: -5px 0;
            border-radius: 7px;
        }
        QSlider::handle:horizontal:hover {
            background: rgb(230, 234, 236);
        }
        """
        return base + multi_tool_qss

    def build_ui(self, layout: QVBoxLayout) -> None:
        """Main Qt UI code setup."""
        layout.addWidget(self._section_label("nLol Multi Tool", decorate=False))

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget, 1)

        self.tab_widget.addTab(self._wrap_scroll(self.build_auto_rig_tab()), "Auto Rig")
        self.tab_widget.addTab(self._wrap_scroll(self.build_rigging_tab()), "Rigging")
        self.tab_widget.addTab(self._wrap_scroll(self.build_animation_tab()), "Animation")
        self.tab_widget.addTab(self._wrap_scroll(self.build_modeling_tab()), "Modeling")
        self.tab_widget.addTab(self._wrap_scroll(self.build_color_tab()), "Color")
        self.tab_widget.addTab(self._wrap_scroll(self.build_shading_tab()), "Shading")
        self.tab_widget.addTab(self._wrap_scroll(self.build_misc_tab()), "Misc")

        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def get_settings_keys(self) -> dict:
        """Persist last-selected tab between sessions."""
        return {
            "last_tab_index": self.tab_widget,
        }

    def _wrap_scroll(self, content: QWidget) -> QScrollArea:
        """Wrap tab content in a scroll area for denser layouts."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)
        return scroll

    # -------------------- helpers --------------------
    def _section_label(
        self,
        text: str,
        rgb: tuple[int, int, int] = CLR_SECTION,
        *,
        decorate: bool = True,
        uppercase: bool = True,
    ) -> QLabel:
        """Section divider / title bar — flat square bar, distinct from rounded buttons."""
        r, g, b = rgb
        display = text.upper() if uppercase else text
        label_text = f"---  {display}  ---" if decorate else text
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setMinimumHeight(28)
        label.setStyleSheet(
            f"background-color: rgb({r}, {g}, {b}); color: rgb(205, 215, 215); "
            "font-weight: bold; font-size: 11px; letter-spacing: 1px; "
            "padding: 4px 8px; border: none; border-radius: 0px;",
        )
        return label

    def _style_button(
        self,
        btn: QPushButton,
        rgb: tuple[int, int, int] = CLR_BASE,
        *,
        min_height: int | None = None,
    ) -> QPushButton:
        """Apply muted button style with a bit more contrast (this UI only)."""
        r, g, b = rgb
        hr, hg, hb = (min(255, r + 22), min(255, g + 22), min(255, b + 22))
        btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: rgb({r}, {g}, {b});
                color: rgb(230, 230, 230);
                border: none;
                border-radius: 6px;
                padding: 4px 8px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: rgb({hr}, {hg}, {hb});
                border: none;
            }}
            QPushButton:pressed {{
                background-color: rgb({max(0, r - 10)}, {max(0, g - 10)}, {max(0, b - 10)});
                border: none;
            }}
            """,
        )
        if min_height is not None:
            btn.setMinimumHeight(min_height)
        return btn

    def _make_button(
        self,
        label: str,
        tip: str,
        callback,
        rgb: tuple[int, int, int] = CLR_BASE,
        *,
        min_height: int | None = None,
        fixed_width: int | None = None,
    ) -> QPushButton:
        """Create a styled button connected to a callback."""
        btn = QPushButton(label)
        btn.setToolTip(tip)
        btn.clicked.connect(callback)
        self._style_button(btn, rgb, min_height=min_height)
        if fixed_width is not None:
            btn.setFixedWidth(fixed_width)
        return btn

    # -------------------- Auto Rig tab --------------------
    def build_auto_rig_tab(self) -> QWidget:
        """Auto Rig tab aligned with current nLol build / skin / prep tools."""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignTop)
        tab_layout.setSpacing(6)
        tab_layout.setContentsMargins(6, 6, 6, 6)

        # ----- active rig status -----
        status_row = QHBoxLayout()
        self.active_rig_label = QLabel()
        self.active_rig_label.setWordWrap(True)
        self.active_rig_label.setToolTip(
            'Active rig from "rig_context.json". Change via Rig Context UI.',
        )
        status_row.addWidget(self.active_rig_label, stretch=1)
        status_row.addWidget(
            self._make_button(
                "Refresh",
                "Reload active rig status from rig_context.json.",
                self.refresh_active_rig_status,
                fixed_width=70,
            ),
        )
        tab_layout.addLayout(status_row)
        self.refresh_active_rig_status()

        open_row = QHBoxLayout()
        open_row.addWidget(
            self._make_button(
                "Open Rig File",
                "Open the active character's saved *_rig.ma file "
                "(next to the auto-rig folder).",
                self.on_open_active_rig_file,
            ),
        )
        open_row.addWidget(
            self._make_button(
                "Open Skeletal Mesh",
                "Open the active character's saved *_skeletalMesh.ma file "
                "(next to the auto-rig folder).",
                self.on_open_active_skeletal_mesh_file,
            ),
        )
        tab_layout.addLayout(open_row)

        # ----- build actions -----
        tab_layout.addWidget(self._section_label("Build"))
        build_row = QHBoxLayout()
        build_row.addWidget(
            self._make_button(
                "Build Skeletal Mesh",
                "Build only skeletal mesh. Stop before rig is built.",
                self.on_build_skeletal_mesh,
                min_height=40,
            ),
        )
        build_row.addWidget(
            self._make_button(
                "Build Rig",
                "Build rig files from active rig folder.\n"
                'Change active folder in Rig Context UI / "rig_context.json".',
                self.on_build_rig,
                rgb=CLR_STATUS_OK,
                min_height=40,
            ),
            stretch=1,
        )
        build_row.addWidget(
            self._make_button(
                "Build Save Active",
                "Build active rig. Update materials. Save files.",
                self.on_build_save_active,
                min_height=40,
            ),
        )
        build_row.addWidget(
            self._make_button(
                "Build Save All",
                "Build and save all auto-rigs in Character folder. Update materials too.\n"
                "Character folder is parent folder of current active rig.",
                self.on_build_save_all,
                min_height=40,
            ),
        )
        tab_layout.addLayout(build_row)

        # ----- context / cleanup -----
        tab_layout.addWidget(self._section_label("Context / Cleanup"))
        context_row = QHBoxLayout()
        context_row.addWidget(
            self._make_button(
                "Rig Context UI",
                "Open Rig Context UI to set active rig folder.",
                self.on_open_rig_context_ui,
                rgb=CLR_UI,
            ),
        )
        context_row.addWidget(
            self._make_button(
                "Delete Rig",
                "Delete current nLol rig in scene, but leave the skeletal mesh. Reset bind pose.",
                self.on_delete_rig,
                rgb=CLR_RED,
            ),
        )
        context_row.addWidget(
            self._make_button(
                "Save Rig Control Curves",
                "Save control curve shape attributes to load back in when building the rig.",
                self.on_save_rig_control_curves,
            ),
        )
        context_row.addWidget(
            self._make_button(
                "Go to Bind Pose",
                "Return the skeleton to its bind pose.",
                self.on_go_to_bind_pose,
            ),
        )
        tab_layout.addLayout(context_row)

        # ----- skeleton prep -----
        tab_layout.addWidget(self._section_label("Skeleton Prep"))
        prep_row_1 = QHBoxLayout()
        prep_row_1.addWidget(
            self._make_button(
                "Show Joint Attributes",
                "Show useful joint attributes in channel box "
                "(jointOrient, rotateAxis, displayLocalAxis, etc).",
                lambda: self.on_show_joint_attrs(True),
            ),
        )
        prep_row_1.addWidget(
            self._make_button(
                "Hide",
                "Hide joint attributes from channel box.",
                lambda: self.on_show_joint_attrs(False),
                rgb=CLR_RED_SOFT,
                fixed_width=50,
            ),
        )
        prep_row_1.addWidget(
            self._make_button(
                "Joint Axis Locator",
                "Create locator at joints for manual axis alignment.",
                self.on_axis_locator,
            ),
        )
        prep_row_1.addWidget(
            self._make_button(
                "Del",
                "Delete joint axis locators.",
                self.on_axis_locator_del,
                rgb=CLR_RED_SOFT,
                fixed_width=50,
            ),
        )
        tab_layout.addLayout(prep_row_1)

        prep_row_2 = QHBoxLayout()
        prep_row_2.addWidget(
            self._make_button(
                "Show Local Axis",
                "Enable displayLocalAxis on selected.",
                lambda: self.on_display_local_axis(True),
            ),
        )
        prep_row_2.addWidget(
            self._make_button(
                "Hide",
                "Disable displayLocalAxis on selected.",
                lambda: self.on_display_local_axis(False),
                rgb=CLR_RED_SOFT,
                fixed_width=50,
            ),
        )
        prep_row_2.addWidget(
            self._make_button(
                "Select Hierarchy",
                "Select hierarchy of current selection.",
                self.on_select_hierarchy,
            ),
        )
        prep_row_2.addStretch()
        tab_layout.addLayout(prep_row_2)

        # ----- skin weights -----
        tab_layout.addWidget(self._section_label("Skin Weights"))
        skin_row = QHBoxLayout()
        skin_row.addWidget(
            self._make_button(
                "Export Skin Clusters",
                "Select one or more skinned meshes and export their skin clusters to xml.\n"
                "Exports to current nLol rig folder.",
                self.on_export_skin,
            ),
        )
        skin_row.addWidget(
            self._make_button(
                "Import Skin Clusters",
                "Import xml skinCluster files from nLol rig folderpath and apply them.\n"
                "No mesh selection required.",
                lambda: self.on_import_skin(False),
            ),
        )
        skin_row.addWidget(
            self._make_button(
                "Import Skin Selected",
                "Import skin clusters for selected geometry only.",
                lambda: self.on_import_skin(True),
            ),
        )
        tab_layout.addLayout(skin_row)

        skin_row_2 = QHBoxLayout()
        skin_row_2.addWidget(
            self._make_button(
                "Rename Skin Cluster",
                "Rename selected mesh skin clusters using nLol naming.",
                self.on_rename_skincluster,
            ),
        )
        skin_row_2.addWidget(
            self._make_button(
                "Select Skinned Joints",
                "Select skinned joints from first selected mesh.",
                self.on_select_skinned_joints,
            ),
        )
        skin_row_2.addStretch()
        tab_layout.addLayout(skin_row_2)

        tab_layout.addStretch()
        return tab

    # -------------------- Rigging tab --------------------
    def build_rigging_tab(self) -> QWidget:
        """Rigging helpers: curves, mirror/replace, joint aim tools."""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignTop)
        tab_layout.setSpacing(6)
        tab_layout.setContentsMargins(6, 6, 6, 6)

        # ----- joint helpers -----
        tab_layout.addWidget(self._section_label("Joint Helpers"))
        jnt_row = QHBoxLayout()
        jnt_row.addWidget(
            self._make_button("Create Joint", "Create a single joint.", self.on_create_joint),
        )
        jnt_row.addWidget(
            self._make_button(
                "Snap Closest Axis",
                "Snap first selected (children) to last selected closest pointing axis.",
                self.on_snap_closest_axis,
            ),
        )
        jnt_row.addWidget(
            self._make_button(
                "Joint Orient X",
                "Orient joint main axis toward second joint (Skeleton > Orient Joint).",
                self.on_joint_orient_x,
            ),
        )
        jnt_row.addWidget(
            self._make_button(
                "Snap Align X",
                "Snap/align first joint main axis to second joint.",
                self.on_snap_align_x,
            ),
        )
        tab_layout.addLayout(jnt_row)

        # ----- control curves -----
        tab_layout.addWidget(self._section_label("Control Curves"))
        for labels in (
            (("Box Curve", "box_curve"), ("Circle Curve", "circle_curve"), ("Sphere Curve", "sphere_curve")),
            (("Tri Circle", "tri_circle_curve"), ("Pyramid", "pyramid_curve"), ("Cylinder", "cylinder_curve")),
            (("Arrow Twist", "arrow_twist_curve"), ("Four Arrow", "four_arrow_curve"), ("Global", "global_curve")),
        ):
            row = QHBoxLayout()
            for label, method in labels:
                row.addWidget(
                    self._make_button(
                        label,
                        f"Create {label.lower()} control curve.",
                        lambda checked=False, m=method: self.on_create_curve(m),
                        rgb=CLR_BASE_ALT,
                        min_height=36,
                    ),
                )
            tab_layout.addLayout(row)

        # ----- curve edit tools -----
        tab_layout.addWidget(self._section_label("Curve Edit"))
        edit_row = QHBoxLayout()
        edit_row.addWidget(
            self._make_button(
                "Replace Curve Shapes",
                "Replace last selected curve shapes with the first selected curve.",
                self.on_replace_curve_shapes,
            ),
        )
        edit_row.addWidget(
            self._make_button(
                "Shape Vis Off",
                "Hide shapes under selected transforms.",
                lambda: self.on_shape_visibility(False),
                rgb=CLR_RED_SOFT,
            ),
        )
        edit_row.addWidget(
            self._make_button(
                "Shape Vis On",
                "Show shapes under selected transforms.",
                lambda: self.on_shape_visibility(True),
            ),
        )
        tab_layout.addLayout(edit_row)

        mirror_row = QHBoxLayout()
        mirror_row.addWidget(
            self._make_button(
                "Mirror Control Curves",
                "Mirror selected control curve shapes to the opposite side across X.",
                self.on_mirror_control_curves,
                rgb=CLR_STATUS_OK,
            ),
        )
        mirror_row.addWidget(
            self._make_button(
                "Save Curves (defaults)",
                'Save control curve shapes to "maya/nlol/defaults" generic location.',
                self.on_save_default_control_curves,
            ),
        )
        mirror_row.addWidget(
            self._make_button(
                "Load Curves (defaults)",
                'Apply curve shapes from "maya/nlol/defaults" generic location.',
                self.on_load_default_control_curves,
            ),
        )
        tab_layout.addLayout(mirror_row)

        # ----- utilities -----
        tab_layout.addWidget(self._section_label("Utilities"))
        util_row = QHBoxLayout()
        util_row.addWidget(
            self._make_button(
                "Print Object Type",
                "Print Maya object type for selected.",
                self.on_print_object_type,
            ),
        )
        util_row.addStretch()
        tab_layout.addLayout(util_row)

        tab_layout.addStretch()
        return tab

    # -------------------- Animation tab --------------------
    def build_animation_tab(self) -> QWidget:
        """Animation helpers aligned with current nLol animation shelf tools."""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignTop)
        tab_layout.setSpacing(6)
        tab_layout.setContentsMargins(6, 6, 6, 6)

        # ----- controls -----
        tab_layout.addWidget(self._section_label("Controls"))
        ctrl_row = QHBoxLayout()
        ctrl_row.addWidget(
            self._make_button(
                "Select All Controls",
                "Select all controls under rig group / selection.",
                self.on_select_all_ctrls,
            ),
        )
        ctrl_row.addWidget(
            self._make_button(
                "Reset All Controls",
                "Reset selected/all rig controls to defaults.",
                self.on_reset_all_ctrls,
                rgb=CLR_RED,
            ),
        )
        ctrl_row.addWidget(
            self._make_button(
                "Reset All (Keyable)",
                "Reset all keyable attributes on selected/all rig controls.",
                self.on_reset_all_ctrls_keyable,
                rgb=CLR_RED_SOFT,
            ),
        )
        tab_layout.addLayout(ctrl_row)

        pivot_row = QHBoxLayout()
        pivot_row.addWidget(
            self._make_button(
                "Temp Locator",
                "Create temporary locator at world origin. "
                "Useful for a temp pivot with multi parent constraint.",
                self.on_temp_locator,
            ),
        )
        pivot_row.addWidget(
            self._make_button(
                "Multi Parent Constraint",
                "Constrain multiple ctrls to last selected object (often a locator).",
                self.on_multi_parent_const,
            ),
        )
        pivot_row.addWidget(
            self._make_button(
                "Space Matcher UI",
                "Open Space Switch Matcher UI.",
                self.on_open_space_matcher_ui,
                rgb=CLR_UI,
            ),
        )
        pivot_row.addWidget(
            self._make_button(
                "Anim Picker UI",
                "Open the nLol anim picker.",
                self.on_open_anim_picker_ui,
                rgb=CLR_UI,
            ),
        )
        tab_layout.addLayout(pivot_row)

        ref_row = QHBoxLayout()
        ref_row.addWidget(
            self._make_button(
                "Reference Ctrl Shapes",
                "Make selected control shapes unselectable (reference display).",
                lambda: self.on_ctrl_shapes_reference(True),
                rgb=CLR_RED_SOFT,
            ),
        )
        ref_row.addWidget(
            self._make_button(
                "Unreference Ctrl Shapes",
                "Make selected control shapes selectable again (normal display).",
                lambda: self.on_ctrl_shapes_reference(False),
            ),
        )
        ref_row.addStretch()
        tab_layout.addLayout(ref_row)

        # ----- mirror -----
        tab_layout.addWidget(self._section_label("Mirror"))
        mirror_row = QHBoxLayout()
        mirror_row.addWidget(
            self._make_button(
                "Mirror Opposite Ctrl",
                'Mirror selected ctrl/s left/right. Opposite ctrl receives the values.',
                lambda: self.on_mirror_selected_ctrls(True),
                rgb=CLR_ACCENT,
            ),
        )
        mirror_row.addWidget(
            self._make_button(
                "Mirror Selected Ctrl",
                'Mirror selected ctrl/s left/right. Selected ctrl receives the values.',
                lambda: self.on_mirror_selected_ctrls(False),
            ),
        )
        tab_layout.addLayout(mirror_row)

        mirror_attr_row = QHBoxLayout()
        mirror_attr_row.addWidget(
            self._make_button(
                "Add Mirror Attrs",
                'Add mirror attributes to selected objects (e.g. ".mirrorTranslateX").',
                self.on_add_mirror_attrs,
            ),
        )
        mirror_attr_row.addWidget(
            self._make_button(
                "Save Mirror Attrs",
                "Save mirror attributes for selected ctrls to active rig folder.",
                self.on_save_mirror_attrs,
            ),
        )
        mirror_attr_row.addWidget(
            self._make_button(
                "Load Mirror Attrs",
                'Load mirror attrs from "mirror_attributes.json" in active rig folder.',
                self.on_load_mirror_attrs,
            ),
        )
        tab_layout.addLayout(mirror_attr_row)

        mirror_vis_row = QHBoxLayout()
        mirror_vis_row.addWidget(
            self._make_button(
                "Show Mirror Attrs",
                "Show mirror attributes in channel box for selected ctrls.",
                lambda: self.on_show_mirror_attrs(True),
            ),
        )
        mirror_vis_row.addWidget(
            self._make_button(
                "Hide Mirror Attrs",
                "Hide mirror attributes in channel box for selected ctrls.",
                lambda: self.on_show_mirror_attrs(False),
                rgb=CLR_RED_SOFT,
            ),
        )
        mirror_vis_row.addWidget(
            self._make_button(
                "Save Mirror Attrs (Generic)",
                "Save mirror attributes to generic nlol defaults folder.",
                self.on_save_mirror_attrs_generic,
            ),
        )
        tab_layout.addLayout(mirror_vis_row)

        # ----- transforms -----
        tab_layout.addWidget(self._section_label("Transforms"))
        xform_row = QHBoxLayout()
        xform_row.addWidget(
            self._make_button(
                "Save Transforms",
                "Save translate/rotate/scale for selected objects to json.",
                self.on_save_transforms,
            ),
        )
        xform_row.addWidget(
            self._make_button(
                "Load Transforms",
                "Load translate/rotate/scale from json. No selection required.",
                self.on_load_transforms,
            ),
        )
        xform_row.addWidget(
            self._make_button(
                "Paste Transforms to Selected",
                "Load transforms onto selected objects in the same save order.",
                self.on_paste_transforms,
            ),
        )
        tab_layout.addLayout(xform_row)

        hier_row = QHBoxLayout()
        hier_row.addWidget(
            self._make_button(
                "Select Hierarchy Transforms",
                "Select hierarchy transform nodes only; leave out the initial selection.",
                self.on_select_hierarchy_transforms,
            ),
        )
        hier_row.addStretch()
        tab_layout.addLayout(hier_row)

        # ----- keyframes -----
        tab_layout.addWidget(self._section_label("Keyframes"))
        key_row = QHBoxLayout()
        key_row.addWidget(
            self._make_button(
                "Save Keyframe",
                "Save current keyframe data for selected objects.",
                self.on_save_keyframe,
            ),
        )
        key_row.addWidget(
            self._make_button(
                "Load Keyframe (Saved)",
                "Load keyframe data for saved objects on the current frame.",
                self.on_load_keyframe_saved,
            ),
        )
        key_row.addWidget(
            self._make_button(
                "Load Keyframe (Selected)",
                "Load keyframe data for selected objects on the current frame.",
                self.on_load_keyframe_selected,
            ),
        )
        tab_layout.addLayout(key_row)

        key_all_row = QHBoxLayout()
        key_all_row.addWidget(
            self._make_button(
                "Save All Keyframes",
                "Save all keyframe data for selected objects within the animation range.",
                self.on_save_all_keyframes,
            ),
        )
        key_all_row.addWidget(
            self._make_button(
                "Load All Keyframes",
                "Load all saved keyframe data across the saved playback range.",
                self.on_load_all_keyframes,
            ),
        )
        key_all_row.addWidget(
            self._make_button(
                "Animation Saver UI",
                "Open UI for saving and loading animation data.",
                self.on_open_anim_saver_ui,
                rgb=CLR_UI,
            ),
        )
        tab_layout.addLayout(key_all_row)

        # ----- retarget -----
        tab_layout.addWidget(self._section_label("Retarget"))
        retarget_row = QHBoxLayout()
        retarget_row.addWidget(
            self._make_button(
                "Source Target Connect",
                "Connect source/target ctrls for anim retarget "
                '(uses "retarget_data.toml").',
                self.on_retarget_connect,
            ),
        )
        retarget_row.addWidget(
            self._make_button(
                "Delete Connections",
                "Delete constraint connections created for anim retarget.",
                self.on_retarget_delete,
                rgb=CLR_RED_SOFT,
            ),
        )
        retarget_row.addWidget(
            self._make_button(
                "Copy Keyframes",
                "Bake keyframes from source to target controls.",
                self.on_retarget_copy_keys,
            ),
        )
        tab_layout.addLayout(retarget_row)

        tab_layout.addStretch()
        return tab

    # -------------------- status / events --------------------
    def get_active_rig_info(self) -> tuple[str, str]:
        """Return (name, folderpath) for the active rig in rig_context.json."""
        try:
            with open(RIG_CONTEXT_JSON) as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.warning(f"Could not read rig_context.json: {e}")
            return "", ""

        for rig in data.get("rigs", []):
            if rig.get("active"):
                return rig.get("name", ""), rig.get("folderpath", "")
        return "", ""

    def get_active_build_filepaths(self) -> tuple[Path | None, Path | None]:
        """Return saved (*_rig.ma, *_skeletalMesh.ma) paths for the active rig.

        These are written next to the auto-rig folder by Build Save Active/All.
        """
        name, folderpath = self.get_active_rig_info()
        if not name or not folderpath:
            return None, None

        resolved = Path(os.path.expandvars(folderpath))
        if "$" in str(resolved):
            logger.warning(f"Unresolved environment variable in path: {resolved}")
            return None, None

        character_folder = resolved.parent
        return (
            character_folder / f"{name}_rig.ma",
            character_folder / f"{name}_skeletalMesh.ma",
        )

    def open_maya_file(self, filepath: Path | None) -> None:
        """Open a Maya ascii/binary file in the current session."""
        if filepath is None:
            logger.warning("No active rig set. Open Rig Context UI to choose one.")
            return
        if not filepath.is_file():
            logger.warning(f"File not found: {filepath}")
            return

        yes_string = "Yes"
        no_string = "No"
        dialog_result = cmds.confirmDialog(
            title="Confirm",
            message=f"Open file? This will replace the current scene.\n\n{filepath.name}",
            button=[yes_string, no_string],
            defaultButton=yes_string,
            cancelButton=no_string,
            dismissString=no_string,
            bgc=(0.2, 0.2, 0.2),
        )
        if dialog_result == no_string:
            logger.info("Open file cancelled.")
            return

        cmds.file(
            filepath.as_posix(),
            open=True,
            force=True,
            ignoreVersion=True,
            options="v=0;",
        )
        logger.info(f"Opened: {filepath}")

    def refresh_active_rig_status(self) -> None:
        """Update the Auto Rig active-rig status label."""
        if not hasattr(self, "active_rig_label"):
            return

        name, folderpath = self.get_active_rig_info()
        if name:
            self.active_rig_label.setText(f"Active Rig: {name}\n{folderpath}")
            r, g, b = CLR_STATUS_OK
        else:
            self.active_rig_label.setText("Active Rig: (none set)\nOpen Rig Context UI.")
            r, g, b = CLR_STATUS_WARN

        self.active_rig_label.setStyleSheet(
            f"background-color: rgb({r}, {g}, {b}); color: rgb(230, 230, 230); "
            "padding: 6px; border: none; border-radius: 4px;",
        )

    def on_tab_changed(self, index: int) -> None:
        """Save last tab and refresh active rig status on Auto Rig."""
        self.save_settings()
        if index == AUTO_RIG_TAB_INDEX:
            self.refresh_active_rig_status()

    def showEvent(self, event) -> None:
        """Refresh active rig status when the UI is shown again."""
        super().showEvent(event)
        self.refresh_active_rig_status()

    # -------------------- Auto Rig actions --------------------
    def on_open_active_rig_file(self) -> None:
        """Open the active character's saved *_rig.ma file."""
        rig_file, _ = self.get_active_build_filepaths()
        self.open_maya_file(rig_file)

    def on_open_active_skeletal_mesh_file(self) -> None:
        """Open the active character's saved *_skeletalMesh.ma file."""
        _, skeletal_mesh_file = self.get_active_build_filepaths()
        self.open_maya_file(skeletal_mesh_file)

    def on_build_skeletal_mesh(self) -> None:
        """Build only skeletal mesh. Stop before rig is built."""
        from nlol.core.rig_setup import rig_build_mesh_skeleton

        reload(rig_build_mesh_skeleton)
        rig_build_mesh_skeleton.run_mesh_skeleton_build()

    def on_build_rig(self) -> None:
        """Build rig files from active rig folder."""
        from nlol.core.rig_setup import rig_build

        reload(rig_build)
        rig_build.run_rig_build()

    def on_build_save_active(self) -> None:
        """Build active rig. Update materials. Save files."""
        from nlol.core.rig_setup import rig_build_all

        reload(rig_build_all)
        rig_build_all.RigBuildSaveAll().build_active_only()

    def on_build_save_all(self) -> None:
        """Build and save all auto-rigs in Character folder."""
        from nlol.core.rig_setup import rig_build_all

        reload(rig_build_all)
        rig_build_all.RigBuildSaveAll().build()

    def on_open_rig_context_ui(self) -> None:
        """Open the Rig Context UI."""
        from nlol.core.ui import rig_context_ui

        rig_context_ui.reload_tool()
        self.refresh_active_rig_status()

    def on_delete_rig(self) -> None:
        """Delete current nLol rig, leave skeletal mesh."""
        from nlol.core.rig_tools import rig_delete

        reload(rig_delete)
        rig_delete.remove_nlol_rig()

    def on_save_rig_control_curves(self) -> None:
        """Save control curve shapes for the active rig folder."""
        from nlol.core.rig_setup import save_control_curves

        reload(save_control_curves)
        save_control_curves.SaveControlCurves().write_curve_attributes()

    def on_go_to_bind_pose(self) -> None:
        """Return skeleton to bind pose."""
        mel.eval("GoToBindPose;")

    def on_show_joint_attrs(self, show: bool) -> None:
        """Show or hide useful joint attributes in the channel box."""
        from nlol.core.rig_tools import show_attributes

        reload(show_attributes)
        show_attributes.ShowAttributes(show_attrs=show).show_joint_attrs()

    def on_axis_locator(self) -> None:
        """Create axis locators under selected joints."""
        from nlol.core.rig_components import create_locators

        reload(create_locators)
        create_locators.axis_locator()

    def on_axis_locator_del(self) -> None:
        """Delete joint axis locators."""
        from nlol.core.rig_components import create_locators

        reload(create_locators)
        create_locators.axis_locator_del()

    def on_display_local_axis(self, enabled: bool) -> None:
        """Toggle displayLocalAxis on selected."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.set_display_local_axis(enabled)

    def on_select_hierarchy(self) -> None:
        """Select hierarchy of current selection."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.select_hierarchy()

    def on_export_skin(self) -> None:
        """Export skin clusters for selected meshes."""
        from nlol.core.rig_tools import skin_export_import

        reload(skin_export_import)
        skin_export_import.export_skin_weights()

    def on_import_skin(self, selected_only: bool) -> None:
        """Import skin clusters from active rig folder."""
        from nlol.core.rig_tools import skin_export_import

        reload(skin_export_import)
        skin_export_import.import_skin_weights(selected_only=selected_only)

    def on_rename_skincluster(self) -> None:
        """Rename selected mesh skin clusters to nLol naming."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.rename_skincluster()

    def on_select_skinned_joints(self) -> None:
        """Select joints skinned to the first selected mesh."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.query_skinned_joints()

    # -------------------- Rigging actions --------------------
    def on_create_joint(self) -> None:
        """Create a single joint."""
        from nlol.core.rig_components import create_joint

        reload(create_joint)
        create_joint.single_joint()

    def on_snap_closest_axis(self) -> None:
        """Snap selection to closest pointing axis of last selected."""
        from nlol.core.rig_tools import get_aligned_axis

        reload(get_aligned_axis)
        get_aligned_axis.snap_to_closest_axis()

    def on_joint_orient_x(self) -> None:
        """Orient joint main axis toward second selected joint."""
        from nlol.core.rig_tools import aim_axis

        reload(aim_axis)
        aim_axis.aim_axis_orient_joint()

    def on_snap_align_x(self) -> None:
        """Snap/align first joint main axis to second joint."""
        from nlol.core.rig_tools import aim_axis

        reload(aim_axis)
        aim_axis.snap_alignment()

    def on_create_curve(self, method_name: str) -> None:
        """Create a control curve by CreateCurves method name."""
        from nlol.core.rig_components import create_nurbs_curves

        reload(create_nurbs_curves)
        curves = create_nurbs_curves.CreateCurves(use_curve_defaults=True, show_attrs=True)
        getattr(curves, method_name)()

    def on_replace_curve_shapes(self) -> None:
        """Replace last selected curve shapes with first selected."""
        from nlol.core.rig_tools import replace_curves

        reload(replace_curves)
        replace_curves.replace_crv_shps()

    def on_shape_visibility(self, visible: bool) -> None:
        """Show or hide shapes under selected transforms."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.set_shape_visibility(visible)

    def on_mirror_control_curves(self) -> None:
        """Mirror selected control curve shapes across X."""
        from nlol.core.rig_tools import mirror_curve_shapes

        reload(mirror_curve_shapes)
        mirror_curve_shapes.mirror_curves()

    def on_save_default_control_curves(self) -> None:
        """Save control curves to generic defaults location."""
        from nlol.core.rig_setup import save_control_curves

        reload(save_control_curves)
        save_control_curves.SaveControlCurves(use_generic_filepath=True).write_curve_attributes()

    def on_load_default_control_curves(self) -> None:
        """Load control curves from generic defaults location."""
        from nlol.core.rig_setup import save_control_curves

        reload(save_control_curves)
        save_control_curves.SaveControlCurves(use_generic_filepath=True).apply_curve_attributes()

    def on_print_object_type(self) -> None:
        """Print Maya object type for selected."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.get_selection_type()

    def on_open_space_matcher_ui(self) -> None:
        """Open Space Switch Matcher UI."""
        from nlol.core.ui import space_matcher_ui

        space_matcher_ui.reload_tool()

    def on_select_all_ctrls(self) -> None:
        """Select all rig controls."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.select_all_ctrls()

    def on_reset_all_ctrls(self) -> None:
        """Reset rig controls to defaults."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.reset_all_ctrls()

    def on_reset_all_ctrls_keyable(self) -> None:
        """Reset all keyable attributes on rig controls."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.reset_all_ctrls(all_keyable=True)

    def on_temp_locator(self) -> None:
        """Create a temporary world-origin locator."""
        from nlol.core.rig_components import create_locators

        reload(create_locators)
        create_locators.temp_locator()

    def on_multi_parent_const(self) -> None:
        """Parent-constrain selection to the last selected object."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.multi_parent_const()

    def on_ctrl_shapes_reference(self, enabled: bool) -> None:
        """Set selected control shapes to reference or normal display."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.set_ctrl_shapes_reference(enabled)

    def on_mirror_selected_ctrls(self, to_other_side: bool) -> None:
        """Mirror selected controls to opposite or selected side."""
        from nlol.core.animation_tools import mirror_ctrls

        reload(mirror_ctrls)
        mirror_ctrls.mirror_selected_ctrls(to_other_side=to_other_side)

    def on_add_mirror_attrs(self) -> None:
        """Add mirror attributes to selected objects."""
        from nlol.core.animation_tools import mirror_attrs_export_import

        reload(mirror_attrs_export_import)
        mirror_attrs_export_import.MirrorAttrsExportImport().add_mirror_attrs()

    def on_save_mirror_attrs(self) -> None:
        """Save mirror attributes to active rig folder."""
        from nlol.core.animation_tools import mirror_attrs_export_import

        reload(mirror_attrs_export_import)
        mirror_attrs_export_import.MirrorAttrsExportImport().get_save_mirror_attrs()

    def on_save_mirror_attrs_generic(self) -> None:
        """Save mirror attributes to generic defaults folder."""
        from nlol.core.animation_tools import mirror_attrs_export_import

        reload(mirror_attrs_export_import)
        mirror_attrs_export_import.MirrorAttrsExportImport(
            use_generic_filepath=True,
        ).get_save_mirror_attrs()

    def on_load_mirror_attrs(self) -> None:
        """Load mirror attributes from active rig folder."""
        from nlol.core.animation_tools import mirror_attrs_export_import

        reload(mirror_attrs_export_import)
        mirror_attrs_export_import.MirrorAttrsExportImport().apply_mirror_attrs()

    def on_show_mirror_attrs(self, show: bool) -> None:
        """Show or hide mirror attributes in the channel box."""
        from nlol.core.animation_tools import mirror_attrs_export_import

        reload(mirror_attrs_export_import)
        mirror_attrs_export_import.MirrorAttrsExportImport().show_hide_mirror_attrs(
            show_attrs=show,
        )

    def on_save_transforms(self) -> None:
        """Save transforms for selected objects."""
        from nlol.core.standalone import transforms_save_load

        reload(transforms_save_load)
        transforms_save_load.save_transforms()

    def on_load_transforms(self) -> None:
        """Load transforms from save file."""
        from nlol.core.standalone import transforms_save_load

        reload(transforms_save_load)
        transforms_save_load.load_transforms()

    def on_paste_transforms(self) -> None:
        """Paste saved transforms onto selected objects in save order."""
        from nlol.core.standalone import transforms_save_load

        reload(transforms_save_load)
        transforms_save_load.load_selected_transforms_same_order()

    def on_select_hierarchy_transforms(self) -> None:
        """Select hierarchy transform nodes only."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.select_hierarchy_transform_nodes()

    def on_save_keyframe(self) -> None:
        """Save current-frame keyframe data for selected objects."""
        from nlol.core.animation_tools import keyframe_export_import

        reload(keyframe_export_import)
        keyframe_export_import.KeyframeExportImport().get_keyframe_data()

    def on_load_keyframe_saved(self) -> None:
        """Load keyframe data onto saved objects for the current frame."""
        from nlol.core.animation_tools import keyframe_export_import

        reload(keyframe_export_import)
        keyframe_export_import.KeyframeExportImport().apply_keyframe_data()

    def on_load_keyframe_selected(self) -> None:
        """Load keyframe data onto selected objects for the current frame."""
        from nlol.core.animation_tools import keyframe_export_import

        reload(keyframe_export_import)
        keyframe_export_import.KeyframeExportImport().apply_keyframe_data_to_selected()

    def on_save_all_keyframes(self) -> None:
        """Save all keyframes for selected objects in the animation range."""
        from nlol.core.animation_tools import keyframe_export_import

        reload(keyframe_export_import)
        keyframe_export_import.KeyframeExportImport().get_keyframe_data_all()

    def on_load_all_keyframes(self) -> None:
        """Load all saved keyframes across the saved playback range."""
        from nlol.core.animation_tools import keyframe_export_import

        reload(keyframe_export_import)
        keyframe_export_import.KeyframeExportImport().apply_keyframe_data_all()

    def on_open_anim_saver_ui(self) -> None:
        """Open Animation Saver / Loader UI."""
        from nlol.core.ui import anim_saver_ui

        anim_saver_ui.reload_tool()

    def on_open_anim_picker_ui(self) -> None:
        """Open the nLol Anim Picker UI."""
        from nlol.core.ui.anim_picker_tool import anim_picker_ui

        anim_picker_ui.reload_tool()

    def on_retarget_connect(self) -> None:
        """Connect source/target controls for anim retarget."""
        from nlol.core.animation_tools import retarget_animation

        reload(retarget_animation)
        retarget_animation.RetargetAnimation().apply_ctrl_connections()

    def on_retarget_delete(self) -> None:
        """Delete anim retarget constraint connections."""
        from nlol.core.animation_tools import retarget_animation

        reload(retarget_animation)
        retarget_animation.RetargetAnimation().delete_ctrl_connections()

    def on_retarget_copy_keys(self) -> None:
        """Copy/bake keyframes from source to target for anim retarget."""
        from nlol.core.animation_tools import retarget_animation

        reload(retarget_animation)
        retarget_animation.RetargetAnimation().copy_keyframes()

    # -------------------- Modeling tab --------------------
    def build_modeling_tab(self) -> QWidget:
        """Modeling layout, proxy, and mesh helpers. Materials live on Shading."""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignTop)
        tab_layout.setSpacing(6)
        tab_layout.setContentsMargins(6, 6, 6, 6)

        # ----- layout -----
        tab_layout.addWidget(self._section_label("Layout"))
        layout_row = QHBoxLayout()
        layout_row.addWidget(
            self._make_button(
                "Grid Layout",
                "Lay selected objects out in a basic grid.",
                self.on_grid_layout,
            ),
        )
        layout_row.addWidget(
            self._make_button(
                "Reset Object Transforms",
                "Reset selected object transforms.",
                self.on_reset_obj_transforms,
                rgb=CLR_RED_SOFT,
            ),
        )
        layout_row.addWidget(
            self._make_button(
                "Instance to Regular",
                "Duplicate and replace instanced objects with regular objects.",
                self.on_instance_to_regular,
            ),
        )
        tab_layout.addLayout(layout_row)

        dup_row = QHBoxLayout()
        dup_row.addWidget(
            self._make_button(
                "Dup Replace (Instance)",
                "Replace selected objects with first selected (instanced). "
                "Maintain target transforms.",
                self.on_dup_replace_instance,
            ),
        )
        dup_row.addWidget(
            self._make_button(
                "Dup Replace (Instance, Source First)",
                "Instanced duplicate replace; source becomes first new target.",
                self.on_dup_replace_instance_source_first,
            ),
        )
        dup_row.addWidget(
            self._make_button(
                "Dup Replace (No Instance)",
                "Replace selected objects with first selected (copied, not instanced).",
                self.on_dup_replace_no_instance,
            ),
        )
        tab_layout.addLayout(dup_row)

        # ----- proxies -----
        tab_layout.addWidget(self._section_label("Proxies"))
        proxy_row = QHBoxLayout()
        proxy_row.addWidget(
            self._make_button(
                "Random Proxy Color",
                "Assign random color to selected Arnold standin proxy objects.",
                self.on_random_proxy_color,
            ),
        )
        proxy_row.addWidget(
            self._make_button(
                "Proxy View: Shaded",
                "Arnold standin view mode: shaded.",
                lambda: self.on_proxy_view_mode(6),
            ),
        )
        proxy_row.addWidget(
            self._make_button(
                "Proxy View: Polywire",
                "Arnold standin view mode: shaded polywire.",
                lambda: self.on_proxy_view_mode(5),
            ),
        )
        proxy_row.addWidget(
            self._make_button(
                "Proxy View: Wireframe",
                "Arnold standin view mode: wireframe.",
                lambda: self.on_proxy_view_mode(3),
            ),
        )
        tab_layout.addLayout(proxy_row)

        # ----- mesh tools -----
        tab_layout.addWidget(self._section_label("Mesh Tools"))
        mesh_row = QHBoxLayout()
        mesh_row.addWidget(
            self._make_button(
                "Vert Snapper",
                "Snap first selected object verts to closest verts on second selected object.",
                self.on_vert_snapper,
            ),
        )
        mesh_row.addWidget(
            self._make_button(
                "Hard Edge UV Seams",
                "Create UV seams at hard edges for selected objects.",
                self.on_hard_edge_uv_seams,
            ),
        )
        mesh_row.addWidget(
            self._make_button(
                "Copy IFF Mask (Xgen)",
                "Copy Xgen Core IFF mask from 3D Paint Tool to character xgen paintmaps folder.",
                self.on_copy_iff_mask,
            ),
        )
        tab_layout.addLayout(mesh_row)

        # ----- uis -----
        tab_layout.addWidget(self._section_label("UIs", uppercase=False))
        ui_row = QHBoxLayout()
        ui_row.addWidget(
            self._make_button(
                "Scatter Tool UI",
                "Scatter selected objects to last selected object.",
                self.on_open_scatter_ui,
                rgb=CLR_UI,
            ),
        )
        ui_row.addWidget(
            self._make_button(
                "Export Import Tool UI",
                "Export and import multiple selected objects.",
                self.on_open_export_import_ui,
                rgb=CLR_UI,
            ),
        )
        ui_row.addStretch()
        tab_layout.addLayout(ui_row)

        tab_layout.addStretch()
        return tab

    # -------------------- Shading tab --------------------
    def build_shading_tab(self) -> QWidget:
        """Materials and Arnold / OpenPBR helpers (replaces old Redshift / Stingray tools)."""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignTop)
        tab_layout.setSpacing(6)
        tab_layout.setContentsMargins(6, 6, 6, 6)

        # ----- materials -----
        tab_layout.addWidget(self._section_label("Materials"))
        mat_row = QHBoxLayout()
        mat_row.addWidget(
            self._make_button(
                "Export Materials",
                "Export materials for selected mesh objects to nLol rig folder path.",
                self.on_export_materials,
            ),
        )
        mat_row.addWidget(
            self._make_button(
                "Import Materials (Mesh Name)",
                "Import materials to selected meshes by matching mesh name components.",
                self.on_import_materials_selected,
            ),
        )
        mat_row.addWidget(
            self._make_button(
                "Update Materials",
                "Update scene/selected materials that already have exported matches.",
                self.on_update_scene_materials,
            ),
        )
        tab_layout.addLayout(mat_row)

        rand_row = QHBoxLayout()
        rand_row.addWidget(
            self._make_button(
                "Assign Random Material",
                "Assign standardSurface materials with random colors to selected objects.",
                self.on_assign_random_material,
            ),
        )
        rand_row.addStretch()
        tab_layout.addLayout(rand_row)

        # ----- arnold / openpbr -----
        tab_layout.addWidget(self._section_label("Arnold / OpenPBR"))
        arnold_row = QHBoxLayout()
        arnold_row.addWidget(
            self._make_button(
                "Substance Arnold Mat",
                "Setup Arnold material from Substance textures + shading group. "
                "Select Color, Mix, Normal file nodes and shadingEngine.",
                self.on_substance_arnold_mat,
            ),
        )
        arnold_row.addWidget(
            self._make_button(
                "Toolbag Arnold Mat",
                "Setup Arnold material from Toolbag textures + shading group. "
                "Select Color, Mix, Normal file nodes and shadingEngine.",
                self.on_toolbag_arnold_mat,
            ),
        )
        arnold_row.addWidget(
            self._make_button(
                "Megascans Arnold Mat",
                "Setup Arnold material from Megascans textures + shading group. "
                "Select Albedo, Roughness, Normal file nodes and shadingEngine.",
                self.on_megascans_arnold_mat,
            ),
        )
        tab_layout.addLayout(arnold_row)

        openpbr_row = QHBoxLayout()
        openpbr_row.addWidget(
            self._make_button(
                "OpenPBR Connect",
                "Connect selected file nodes to OpenPBR material / shading group.",
                self.on_openpbr_connect,
            ),
        )
        openpbr_row.addWidget(
            self._make_button(
                "OpenPBR Connect (Megascans)",
                "Connect selected file nodes to OpenPBR; rename after texture folder.",
                self.on_openpbr_connect_megascans,
            ),
        )
        openpbr_row.addWidget(
            self._make_button(
                "Rename Megascans Obj",
                'Rename selected Megascans objects from shading group; "_suffix" -> "_geo".',
                self.on_rename_megascans_obj,
            ),
        )
        tab_layout.addLayout(openpbr_row)

        file_row = QHBoxLayout()
        file_row.addWidget(
            self._make_button(
                "file to aiImage",
                "Convert Maya file nodes to Arnold aiImage; delete old file/place2d nodes.",
                self.on_file_to_aiimage,
            ),
        )
        file_row.addWidget(
            self._make_button(
                "file to aiImage (Keep Old)",
                "Convert Maya file nodes to Arnold aiImage; keep old nodes.",
                self.on_file_to_aiimage_keep,
            ),
        )
        file_row.addStretch()
        tab_layout.addLayout(file_row)

        tab_layout.addStretch()
        return tab

    def on_export_materials(self) -> None:
        """Export materials for selected mesh objects."""
        from nlol.core.modeling_tools import materials_export_import

        reload(materials_export_import)
        materials_export_import.export_materials()

    def on_import_materials_selected(self) -> None:
        """Import materials onto selected meshes by mesh name match."""
        from nlol.core.modeling_tools import materials_export_import

        reload(materials_export_import)
        materials_export_import.import_materials_to_selected()

    def on_update_scene_materials(self) -> None:
        """Update scene/selected materials from exported matches."""
        from nlol.core.modeling_tools import materials_export_import

        reload(materials_export_import)
        materials_export_import.update_scene_materials()

    def on_substance_arnold_mat(self) -> None:
        """Setup Substance Painter Arnold material from selected textures."""
        from nlol.core.modeling_tools import arnold_material_setup

        reload(arnold_material_setup)
        arnold_material_setup.ArnoldMaterialSetup().arnold_basic_mat(
            substance_material=True,
            use_arnold_file_nodes=True,
        )

    def on_toolbag_arnold_mat(self) -> None:
        """Setup Marmoset Toolbag Arnold material from selected textures."""
        from nlol.core.modeling_tools import arnold_material_setup

        reload(arnold_material_setup)
        arnold_material_setup.ArnoldMaterialSetup().arnold_basic_mat()

    def on_megascans_arnold_mat(self) -> None:
        """Setup Megascans Arnold material from selected textures."""
        from nlol.core.modeling_tools import arnold_material_setup

        reload(arnold_material_setup)
        arnold_material_setup.ArnoldMaterialSetup().arnold_basic_mat(megascans_material=True)

    def on_rename_megascans_obj(self) -> None:
        """Rename selected Megascans objects from assigned shading group."""
        from nlol.core.modeling_tools import arnold_material_setup

        reload(arnold_material_setup)
        arnold_material_setup.ArnoldMaterialSetup().rename_megascans_obj()

    def on_openpbr_connect(self) -> None:
        """Connect selected file nodes to OpenPBR material."""
        from nlol.core.modeling_tools import arnold_material_setup

        reload(arnold_material_setup)
        arnold_material_setup.OpenPBRSetup().create()

    def on_openpbr_connect_megascans(self) -> None:
        """Connect selected file nodes to OpenPBR; rename after folder."""
        from nlol.core.modeling_tools import arnold_material_setup

        reload(arnold_material_setup)
        arnold_material_setup.OpenPBRSetup().create(rename_after_folder=True)

    def on_file_to_aiimage(self) -> None:
        """Convert Maya file nodes to Arnold aiImage; delete old nodes."""
        from nlol.core.modeling_tools import arnold_material_setup

        reload(arnold_material_setup)
        arnold_material_setup.ArnoldMaterialSetup().convert_file_to_aiimage()

    def on_file_to_aiimage_keep(self) -> None:
        """Convert Maya file nodes to Arnold aiImage; keep old nodes."""
        from nlol.core.modeling_tools import arnold_material_setup

        reload(arnold_material_setup)
        arnold_material_setup.ArnoldMaterialSetup().convert_file_to_aiimage(delete_old=False)

    def on_grid_layout(self) -> None:
        """Lay selected objects out in a basic grid."""
        from nlol.core.modeling_tools import basic_layout

        reload(basic_layout)
        basic_layout.grid_layout()

    def on_reset_obj_transforms(self) -> None:
        """Reset selected object transforms."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.reset_obj_attributes()

    def on_dup_replace_instance(self) -> None:
        """Duplicate-replace selected with first selected (instanced)."""
        from nlol.core.modeling_tools import basic_layout

        reload(basic_layout)
        basic_layout.duplicate_replace()

    def on_dup_replace_instance_source_first(self) -> None:
        """Instanced duplicate-replace with source as first new target."""
        from nlol.core.modeling_tools import basic_layout

        reload(basic_layout)
        basic_layout.duplicate_replace(source_as_first_new_target=True)

    def on_dup_replace_no_instance(self) -> None:
        """Duplicate-replace selected with first selected (not instanced)."""
        from nlol.core.modeling_tools import basic_layout

        reload(basic_layout)
        basic_layout.duplicate_replace(
            instance_target_obs=False,
            source_as_first_new_target=False,
        )

    def on_instance_to_regular(self) -> None:
        """Convert selected instances to regular objects."""
        from nlol.core.modeling_tools import basic_layout

        reload(basic_layout)
        basic_layout.instanced_to_objects()

    def on_random_proxy_color(self) -> None:
        """Assign random color to selected Arnold standin proxies."""
        from nlol.core.standalone import assign_random_colors

        reload(assign_random_colors)
        assign_random_colors.random_proxy_color()

    def on_proxy_view_mode(self, view_mode: int) -> None:
        """Set Arnold standin proxy view mode."""
        from nlol.core.standalone import assign_random_colors

        reload(assign_random_colors)
        assign_random_colors.prox_view_mode(view_mode=view_mode)

    def on_vert_snapper(self) -> None:
        """Snap verts from first selected mesh to closest on second."""
        from nlol.core.modeling_tools import vert_snapper

        reload(vert_snapper)
        vert_snapper.vert_snapper()

    def on_hard_edge_uv_seams(self) -> None:
        """Create UV seams at hard edges for selected objects."""
        from nlol.core.modeling_tools import modeling_functions

        reload(modeling_functions)
        modeling_functions.auto_seams_hard_edges()

    def on_copy_iff_mask(self) -> None:
        """Copy Xgen IFF mask from 3D Paint Tool to paintmaps folder."""
        from nlol.core.standalone import xgen_utils

        reload(xgen_utils)
        xgen_utils.copy_3d_paint_iff()

    def on_open_scatter_ui(self) -> None:
        """Open Scatter Tool UI."""
        from nlol.core.ui import scatter_tool_ui

        scatter_tool_ui.reload_tool()

    def on_open_export_import_ui(self) -> None:
        """Open Export / Import Tool UI."""
        from nlol.core.ui import export_import_ui

        export_import_ui.reload_tool()

    # -------------------- Color tab --------------------
    def build_color_tab(self) -> QWidget:
        """Viewport / outliner / curve color helpers from the old Color tab."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        max_color = len(small_functions.COLOR_PRESETS) - 1

        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignTop)
        tab_layout.setSpacing(6)
        tab_layout.setContentsMargins(6, 6, 6, 6)

        tab_layout.addWidget(self._section_label("Channel Box"))
        attr_row = QHBoxLayout()
        attr_row.addWidget(
            self._make_button(
                "Show Curve Shape Attrs",
                "Select curve shapes under selection and show wire/color attrs in channel box.",
                lambda: self.on_show_curve_shape_attrs(True),
            ),
        )
        attr_row.addWidget(
            self._make_button(
                "Hide",
                "Hide curve shape wire/color attrs from channel box.",
                lambda: self.on_show_curve_shape_attrs(False),
                rgb=CLR_RED_SOFT,
                fixed_width=50,
            ),
        )
        attr_row.addWidget(
            self._make_button(
                "Show Joint Attributes",
                "Show useful joint attributes in channel box "
                "(including wire/color related attrs).",
                lambda: self.on_show_joint_attrs(True),
            ),
        )
        attr_row.addWidget(
            self._make_button(
                "Hide",
                "Hide joint attributes from channel box.",
                lambda: self.on_show_joint_attrs(False),
                rgb=CLR_RED_SOFT,
                fixed_width=50,
            ),
        )
        attr_row.addStretch()
        tab_layout.addLayout(attr_row)

        tab_layout.addWidget(self._section_label("Override Color"))
        tab_layout.addLayout(
            self._make_color_slider(
                "Shapes",
                "Drawing override color on selected shapes. 0 = off.",
                max_color,
                lambda i: self.on_override_color(i, on_shapes=True),
            ),
        )
        tab_layout.addLayout(
            self._make_color_slider(
                "Transforms",
                "Drawing override color on selected transforms. 0 = off.",
                max_color,
                lambda i: self.on_override_color(i, on_shapes=False),
            ),
        )

        tab_layout.addWidget(self._section_label("Wire Color"))
        tab_layout.addLayout(
            self._make_color_slider(
                "Shapes",
                "Wire color on selected shapes (useObjectColor RGB). 0 = off.",
                max_color,
                lambda i: self.on_wire_color(i, on_shapes=True),
            ),
        )
        tab_layout.addLayout(
            self._make_color_slider(
                "Transforms",
                "Wire color on selected transforms (useObjectColor RGB). 0 = off.",
                max_color,
                lambda i: self.on_wire_color(i, on_shapes=False),
            ),
        )

        tab_layout.addWidget(self._section_label("Outliner"))
        tab_layout.addLayout(
            self._make_color_slider(
                "Selection",
                "Outliner color for selected objects. 0 = off.",
                max_color,
                self.on_outliner_color,
            ),
        )

        tab_layout.addWidget(self._section_label("Curve Width"))
        tab_layout.addLayout(
            self._make_color_slider(
                "Line Width",
                "Nurbs curve lineWidth under selection. 0 = Maya default (-1).",
                11,
                self.on_curve_width,
                is_width=True,
            ),
        )

        tab_layout.addStretch()
        return tab

    def _make_color_slider(
        self,
        label: str,
        tip: str,
        maximum: int,
        callback,
        *,
        is_width: bool = False,
    ) -> QHBoxLayout:
        """Build a labeled slider row with a live color/width swatch."""
        row = QHBoxLayout()
        name = QLabel(label)
        name.setFixedWidth(90)
        name.setToolTip(tip)
        row.addWidget(name)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(maximum)
        slider.setValue(0)
        slider.setToolTip(tip)
        row.addWidget(slider, stretch=1)

        value_label = QLabel("0")
        value_label.setFixedWidth(28)
        value_label.setAlignment(Qt.AlignCenter)
        row.addWidget(value_label)

        swatch = QLabel()
        swatch.setFixedSize(28, 22)
        swatch.setToolTip(tip)
        row.addWidget(swatch)

        def _update_swatch(index: int) -> None:
            value_label.setText(str(index))
            if is_width:
                shade = 20 + int((index / max(1, maximum)) * 200)
                swatch.setStyleSheet(
                    f"background-color: rgb({shade}, {shade}, {shade}); "
                    "border: none; border-radius: 3px;",
                )
            else:
                from nlol.core.standalone.small_functions import get_color_preset

                r, g, b = get_color_preset(index)
                swatch.setStyleSheet(
                    f"background-color: rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)}); "
                    "border: none; border-radius: 3px;",
                )

        def _on_changed(index: int) -> None:
            _update_swatch(index)
            callback(index)

        slider.valueChanged.connect(_on_changed)
        _update_swatch(0)
        return row

    def on_override_color(self, index: int, *, on_shapes: bool) -> None:
        """Apply drawing override color to selection."""
        from nlol.core.standalone.small_functions import set_selection_override_color

        set_selection_override_color(index, on_shapes=on_shapes)

    def on_wire_color(self, index: int, *, on_shapes: bool) -> None:
        """Apply wire color to selection."""
        from nlol.core.standalone.small_functions import set_selection_wire_color

        set_selection_wire_color(index, on_shapes=on_shapes)

    def on_outliner_color(self, index: int) -> None:
        """Apply outliner color to selection."""
        from nlol.core.standalone.small_functions import set_selection_outliner_color

        set_selection_outliner_color(index)

    def on_curve_width(self, index: int) -> None:
        """Apply curve line width to selection."""
        from nlol.core.standalone.small_functions import set_selection_curve_width

        set_selection_curve_width(index)

    def on_assign_random_material(self) -> None:
        """Assign random standardSurface materials to selected objects."""
        from nlol.core.standalone import assign_random_colors

        reload(assign_random_colors)
        assign_random_colors.assign_rand_mat()

    def on_show_curve_shape_attrs(self, show: bool) -> None:
        """Select curve shapes and show or hide useful curve shape attributes."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.select_shapes_show_attrs(show_attrs=show)

    # -------------------- Misc tab --------------------
    def build_misc_tab(self) -> QWidget:
        """Misc helpers aligned with nLol utility shelf + useful old Misc tools."""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setAlignment(Qt.AlignTop)
        tab_layout.setSpacing(6)
        tab_layout.setContentsMargins(6, 6, 6, 6)

        # ----- info / debug -----
        tab_layout.addWidget(self._section_label("Info / Debug"))
        info_row = QHBoxLayout()
        info_row.addWidget(
            self._make_button(
                "Maya / Python / Qt Info",
                "Print Maya, Python, Qt/PySide6, and OS version info.",
                self.on_print_maya_python_info,
            ),
        )
        info_row.addWidget(
            self._make_button(
                "Maya Debugger",
                "Configure debugpy python path for Maya and listen on port.",
                self.on_maya_debugger,
            ),
        )
        info_row.addWidget(
            self._make_button(
                "Port Connection",
                "Connect Maya to port 7001 for external tool connections.",
                self.on_port_connection,
            ),
        )
        tab_layout.addLayout(info_row)

        reg_row = QHBoxLayout()
        reg_row.addWidget(
            self._make_button(
                "Check Registry",
                "Check nLol registry data for Maya objects.",
                self.on_check_registry,
            ),
        )
        reg_row.addWidget(
            self._make_button(
                "Clear Registry",
                "Clear nLol registry data.",
                self.on_clear_registry,
                rgb=CLR_RED_SOFT,
            ),
        )
        reg_row.addStretch()
        tab_layout.addLayout(reg_row)

        # ----- windows / layers -----
        tab_layout.addWidget(self._section_label("Windows / Layers"))
        win_row = QHBoxLayout()
        win_row.addWidget(
            self._make_button(
                "Center All Windows",
                "Center all Maya windows including custom PySide6 windows.",
                self.on_center_all_windows,
            ),
        )
        win_row.addWidget(
            self._make_button(
                "New Display Layer",
                'Create display layer without "makeCurrent" flag.',
                self.on_create_display_layer,
            ),
        )
        win_row.addStretch()
        tab_layout.addLayout(win_row)

        # ----- camera / viewport -----
        tab_layout.addWidget(self._section_label("Camera / Viewport"))
        cam_hotkey_row = QHBoxLayout()
        cam_hotkey_row.addWidget(
            self._make_button(
                "Hotkey: Pivot To Mouse",
                'Set "Camera Pivot To Mouse" hotkey to alt+f.',
                self.on_cam_pivot_mouse_hotkey,
            ),
        )
        cam_hotkey_row.addWidget(
            self._make_button(
                "Del",
                "Delete Camera Pivot To Mouse hotkey.",
                self.on_del_cam_pivot_mouse_hotkey,
                rgb=CLR_RED_SOFT,
                fixed_width=50,
            ),
        )
        cam_hotkey_row.addWidget(
            self._make_button(
                "Hotkey: Pivot To Selected",
                'Set "Camera Pivot To Selected" hotkey to shift+f.',
                self.on_cam_pivot_selected_hotkey,
            ),
        )
        cam_hotkey_row.addWidget(
            self._make_button(
                "Del",
                "Delete Camera Pivot To Selected hotkey.",
                self.on_del_cam_pivot_selected_hotkey,
                rgb=CLR_RED_SOFT,
                fixed_width=50,
            ),
        )
        tab_layout.addLayout(cam_hotkey_row)

        tumble_row = QHBoxLayout()
        tumble_row.addWidget(
            self._make_button(
                "Set Tumble Tool Settings",
                "Set tumble tool settings needed for camera pivot to mouse.",
                self.on_apply_tumble_settings,
                rgb=CLR_ACCENT,
            ),
        )
        tumble_row.addWidget(
            self._make_button(
                "Reset Tumble Settings",
                "Reset camera tumble tool settings to defaults.",
                self.on_reset_tumble_settings,
                rgb=CLR_RED_SOFT,
            ),
        )
        tumble_row.addStretch()
        tab_layout.addLayout(tumble_row)

        cam_loc_row = QHBoxLayout()
        cam_loc_row.addWidget(
            self._make_button(
                "Camera Pivot Locator",
                "Create locator curve to show camera tumble pivot.",
                lambda: self.on_cam_pivot_locator(False),
            ),
        )
        cam_loc_row.addWidget(
            self._make_button(
                "Small Locator",
                "Create small locator curve to show camera tumble pivot.",
                lambda: self.on_cam_pivot_locator(True),
            ),
        )
        cam_loc_row.addWidget(
            self._make_button(
                "Del",
                "Delete camera pivot locator.",
                self.on_del_cam_pivot_locator,
                rgb=CLR_RED_SOFT,
                fixed_width=50,
            ),
        )
        cam_loc_row.addStretch()
        tab_layout.addLayout(cam_loc_row)

        # ----- uis -----
        tab_layout.addWidget(self._section_label("UIs", uppercase=False))
        ui_row = QHBoxLayout()
        ui_row.addWidget(
            self._make_button(
                "nLol Main UI",
                "Reload the main UI for nLol Toolset.",
                self.on_open_nlol_main_ui,
                rgb=CLR_UI,
            ),
        )
        ui_row.addWidget(
            self._make_button(
                "Rig Context UI",
                "Open Rig Context UI to set active rig folder.",
                self.on_open_rig_context_ui,
                rgb=CLR_UI,
            ),
        )
        ui_row.addWidget(
            self._make_button(
                "Renamer Tool",
                "Open Renamer Tool UI.",
                self.on_open_renamer_ui,
                rgb=CLR_UI,
            ),
        )
        tab_layout.addLayout(ui_row)

        # ----- selection / print -----
        tab_layout.addWidget(self._section_label("Selection / Print"))
        sel_row = QHBoxLayout()
        sel_row.addWidget(
            self._make_button(
                "Select Hierarchy",
                "Select hierarchy of the current selection.",
                self.on_select_hierarchy,
            ),
        )
        sel_row.addWidget(
            self._make_button(
                "Print Object Type",
                "Print Maya object type for selected.",
                self.on_print_object_type,
            ),
        )
        sel_row.addWidget(
            self._make_button(
                "Print Object Info",
                "Print selected object names with world translate/rotate.",
                self.on_print_object_xform_info,
            ),
        )
        tab_layout.addLayout(sel_row)

        curve_row = QHBoxLayout()
        curve_row.addWidget(
            self._make_button(
                "Curve CV Positions",
                "Print selected curve CV world positions formatted for cmds.curve().",
                self.on_print_curve_cv_positions,
            ),
        )
        curve_row.addStretch()
        tab_layout.addLayout(curve_row)

        # ----- outliner -----
        tab_layout.addWidget(self._section_label("Outliner"))
        out_row = QHBoxLayout()
        out_row.addWidget(
            self._make_button(
                "Move Up 1",
                "Reorder selected objects up 1 in the outliner.",
                lambda: self.on_outliner_reorder(-1),
            ),
        )
        out_row.addWidget(
            self._make_button(
                "Move Down 1",
                "Reorder selected objects down 1 in the outliner.",
                lambda: self.on_outliner_reorder(1),
                rgb=CLR_RED_SOFT,
            ),
        )
        out_row.addWidget(
            self._make_button(
                "Move Up 5",
                "Reorder selected objects up 5 in the outliner.",
                lambda: self.on_outliner_reorder(-5),
            ),
        )
        out_row.addWidget(
            self._make_button(
                "Move Down 5",
                "Reorder selected objects down 5 in the outliner.",
                lambda: self.on_outliner_reorder(5),
                rgb=CLR_RED_SOFT,
            ),
        )
        tab_layout.addLayout(out_row)

        # ----- joints -----
        tab_layout.addWidget(self._section_label("Joints"))
        jnt_row = QHBoxLayout()
        jnt_row.addWidget(
            self._make_button(
                "Scale Comp On",
                "Enable segmentScaleCompensate on selected joints.",
                lambda: self.on_segment_scale_compensate(True),
            ),
        )
        jnt_row.addWidget(
            self._make_button(
                "Scale Comp Off",
                "Disable segmentScaleCompensate on selected joints.",
                lambda: self.on_segment_scale_compensate(False),
                rgb=CLR_RED_SOFT,
            ),
        )
        jnt_row.addStretch()
        tab_layout.addLayout(jnt_row)

        tab_layout.addStretch()
        return tab

    def on_print_maya_python_info(self) -> None:
        """Print Maya / Python / Qt / OS version info."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.print_maya_python_info()

    def on_maya_debugger(self) -> None:
        """Start Maya debugpy listener."""
        from nlol.core.standalone import maya_debug

        reload(maya_debug)
        maya_debug.main()

    def on_port_connection(self) -> None:
        """Connect Maya command port for external tools."""
        from nlol.core.standalone import maya_debug

        reload(maya_debug)
        maya_debug.connect_port()

    def on_check_registry(self) -> None:
        """Check nLol registry values."""
        from nlol.utilities import check_registry

        reload(check_registry)
        check_registry.verify_registry()

    def on_clear_registry(self) -> None:
        """Clear nLol registry data."""
        from nlol.utilities.nlol_maya_registry import get_registry

        get_registry().clear_registry()

    def on_center_all_windows(self) -> None:
        """Center all Maya / PySide windows."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.center_all_windows()

    def on_create_display_layer(self) -> None:
        """Create a display layer without makeCurrent."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.create_display_layer()

    def on_cam_pivot_mouse_hotkey(self) -> None:
        """Set camera pivot to mouse hotkey."""
        from nlol.core.standalone.viewport_navigation import camera_pivot_set_hotkeys

        reload(camera_pivot_set_hotkeys)
        camera_pivot_set_hotkeys.cam_pivot_to_mouse_hotkey()

    def on_del_cam_pivot_mouse_hotkey(self) -> None:
        """Delete camera pivot to mouse hotkey."""
        from nlol.core.standalone.viewport_navigation import camera_pivot_set_hotkeys

        reload(camera_pivot_set_hotkeys)
        camera_pivot_set_hotkeys.delete_cam_mouse_hotkey()

    def on_cam_pivot_selected_hotkey(self) -> None:
        """Set camera pivot to selected hotkey."""
        from nlol.core.standalone.viewport_navigation import camera_pivot_set_hotkeys

        reload(camera_pivot_set_hotkeys)
        camera_pivot_set_hotkeys.cam_pivot_to_selected_hotkey()

    def on_del_cam_pivot_selected_hotkey(self) -> None:
        """Delete camera pivot to selected hotkey."""
        from nlol.core.standalone.viewport_navigation import camera_pivot_set_hotkeys

        reload(camera_pivot_set_hotkeys)
        camera_pivot_set_hotkeys.delete_cam_selected_hotkey()

    def on_cam_pivot_locator(self, small_locator: bool) -> None:
        """Create camera pivot locator curve."""
        from nlol.core.standalone.viewport_navigation import camera_pivot_locator

        reload(camera_pivot_locator)
        camera_pivot_locator.create_curve_locator(small_locator=small_locator)

    def on_del_cam_pivot_locator(self) -> None:
        """Delete camera pivot locator curve."""
        from nlol.core.standalone.viewport_navigation import camera_pivot_locator

        reload(camera_pivot_locator)
        camera_pivot_locator.delete_curve_locator()

    def on_apply_tumble_settings(self) -> None:
        """Apply camera tumble tool settings for pivot-to-mouse."""
        from nlol.core.standalone.viewport_navigation import tumble_tool_settings

        reload(tumble_tool_settings)
        tumble_tool_settings.apply_tumble_settings()

    def on_reset_tumble_settings(self) -> None:
        """Reset camera tumble tool settings to defaults."""
        from nlol.core.standalone.viewport_navigation import tumble_tool_settings

        reload(tumble_tool_settings)
        tumble_tool_settings.reset_tumble_settings()

    def on_open_nlol_main_ui(self) -> None:
        """Open nLol Main UI."""
        from nlol.core.ui import nlol_main_ui

        nlol_main_ui.reload_tool()

    def on_open_renamer_ui(self) -> None:
        """Open Renamer Tool UI."""
        from nlol.core.ui import renamer_tool_ui

        renamer_tool_ui.reload_tool()

    def on_print_object_xform_info(self) -> None:
        """Print selected object world translate/rotate."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.print_object_xform_info()

    def on_print_curve_cv_positions(self) -> None:
        """Print selected curve CV positions for cmds.curve()."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.print_curve_cv_positions()

    def on_outliner_reorder(self, relative: int) -> None:
        """Reorder selected objects in the outliner."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.outliner_reorder(relative)

    def on_segment_scale_compensate(self, enabled: bool) -> None:
        """Enable or disable segmentScaleCompensate on selected joints."""
        from nlol.core.standalone import small_functions

        reload(small_functions)
        small_functions.set_segment_scale_compensate(enabled)


# entry points
def show_tool():
    """Launch and show tool UI window."""
    MultiToolUI().show_tool()


def reload_tool():
    """Force reload the tool."""
    MultiToolUI().reload_tool()
