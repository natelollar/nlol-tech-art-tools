"""List of rigging variables to be called by shelf and menu."""

from importlib import reload

from nlol.scripts.rig_tools import random_generator

reload(random_generator)

random_colors_dull = random_generator.random_colors_dull


def build_rigging_list():
    """Create a dictionary list of rigging shelves and their attributes."""
    random_clrs = random_colors_dull()

    shelf_separator = {
        "label": "=" * 35,
        "annotation": "Shelf separator.",
        "imageOverlayLabel": "",
        "flexibleWidthType": 2,  # custom width
        "flexibleWidthValue": 16,  # custom width pixels
        "backgroundColor": (0.4, 0.4, 0.4),
        "highlightColor": (0.4, 0.4, 0.4),
        "command": "print('Shelf separator.')",
        "sourceType": "python",
    }

    rigging_list = [
        shelf_separator,
        {
            "label": "Create joint",
            "image": "pythonFamily.png",
            "annotation": "Create single joint.",
            "imageOverlayLabel": "JNT",
            "backgroundColor": (0.4, 0.3, 0.0),
            "command": "from nlol.scripts.rig_components import create_joint\n"
            "from importlib import reload\n"
            "reload(create_joint)\n"
            "create_joint.single_joint()",
            "sourceType": "python",
        },
        {
            "label": "Joint Axis Locator",
            "image": "pythonFamily.png",
            "annotation": "Create locator at joints for manual axis alignment.  "
            "Double click to delete locators.",
            "imageOverlayLabel": "JntLoc",
            "backgroundColor": (0.5, 0.2, 0.0),
            "command": "from nlol.scripts.rig_components import create_locators\n"
            "from importlib import reload\n"
            "reload(create_locators)\n"
            "create_locators.axis_locator()",
            "doubleClickCommand": "from nlol.scripts.rig_components import create_locators\n"
            "from importlib import reload\n"
            "reload(create_locators)\n"
            "create_locators.axis_locator_del()",
            "sourceType": "python",
            "menuItem": [
                (
                    "Delete Locators",
                    "from nlol.scripts.rig_components import create_locators\n"
                    "from importlib import reload\n"
                    "reload(create_locators)\n"
                    "create_locators.axis_locator_del()",
                ),
            ],
            "menuItemPython": (0,),
        },
        {
            "label": "Locator Snap Parent",
            "image": "pythonFamily.png",
            "annotation": "Create and snap locators to selected joints or objects. "
            "Then apply parent and scale constraint with object as parent."
            "Double click to delete locators.",
            "imageOverlayLabel": "LocSnp",
            "backgroundColor": (0.4, 0.2, 0.0),
            "command": "from nlol.scripts.rig_components import create_locators\n"
            "from importlib import reload\n"
            "reload(create_locators)\n"
            "create_locators.locator_snap_parent()",
            "doubleClickCommand": "from nlol.scripts.rig_components import create_locators\n"
            "from importlib import reload\n"
            "reload(create_locators)\n"
            "create_locators.axis_locator_del()",
            "sourceType": "python",
        },
        {
            "label": "Show Joint Attributes",
            "image": "pythonFamily.png",
            "annotation": "Show useful joint attributes in channel box. Double click to remove.",
            "imageOverlayLabel": "JntAtr",
            "backgroundColor": (0.4, 0.0, 0.9),
            "command": "from nlol.scripts.rig_tools import show_attributes\n"
            "from importlib import reload\n"
            "reload(show_attributes)\n"
            "show_attributes.ShowAttributes().show_joint_attrs()",
            "doubleClickCommand": "from nlol.scripts.rig_tools import show_attributes\n"
            "from importlib import reload\n"
            "reload(show_attributes)\n"
            "show_attributes.ShowAttributes(show_attrs=False).show_joint_attrs()",
            "sourceType": "python",
        },
        {
            "label": "Snap to Closest Axis",
            "image": "pythonFamily.png",
            "annotation": "Snap first selected (child objects) to last selected (parent object)"
            " closest pointing axis. Zeros out all values except translate of closest pointing axis.",
            "imageOverlayLabel": "SnpAx",
            "backgroundColor": random_clrs[0],
            "command": "from nlol.scripts.rig_tools import get_aligned_axis\n"
            "from importlib import reload\n"
            "reload(get_aligned_axis)\n"
            "get_aligned_axis.snap_to_closest_axis()",
            "sourceType": "python",
        },
        {
            "label": "Snap to Closest Axis (Translate Only)",
            "image": "pythonFamily.png",
            "annotation": "Snap first selected (child objects) to last selected (parent object)"
            " closest pointing axis. Zeros out all values except translate of closest pointing axis."
            " This version only zeros out translate values, not rotate.",
            "imageOverlayLabel": "SnpAxT",
            "backgroundColor": random_clrs[1],
            "command": "from nlol.scripts.rig_tools import get_aligned_axis\n"
            "from importlib import reload\n"
            "reload(get_aligned_axis)\n"
            "get_aligned_axis.snap_to_closest_axis(translate_only=True)",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Save Control Curves",
            "image": "pythonFamily.png",
            "annotation": 'Save control curve shape attributes to "maya/nlol/default" folder location.',
            "imageOverlayLabel": "SvCrvs",
            "backgroundColor": random_clrs[2],
            "command": "from nlol.scripts.rig_setup import save_control_curves\n"
            "from importlib import reload\n"
            "reload(save_control_curves)\n"
            "save_control_curves.SaveControlCurves(use_generic_filepath=True).write_curve_attributes()",
            "sourceType": "python",
        },
        {
            "label": "Load Control Curves",
            "image": "pythonFamily.png",
            "annotation": 'Apply curve shape attributes from "maya/nlol/default" folder location.',
            "imageOverlayLabel": "LdCrvs",
            "backgroundColor": random_clrs[3],
            "command": "from nlol.scripts.rig_setup import save_control_curves\n"
            "from importlib import reload\n"
            "reload(save_control_curves)\n"
            "save_control_curves.SaveControlCurves(use_generic_filepath=True).apply_curve_attributes()",
            "sourceType": "python",
        },
        {
            "label": "Replace Curve Shape",
            "image": "pythonFamily.png",
            "annotation": "Replace last selected curves with first selected curve."
            " This will replace the curve shapes underneath each curve transform.",
            "imageOverlayLabel": "RpCrv",
            "backgroundColor": random_clrs[4],
            "command": "from nlol.scripts.rig_tools import replace_curves\n"
            "from importlib import reload\n"
            "reload(replace_curves)\n"
            "replace_curves.replace_crv_shps()",
            "sourceType": "python",
        },
        {
            "label": "Mirror Control Curves",
            "image": "pythonFamily.png",
            "annotation": "Mirror selected control curve shapes to opposite side. "
            '"left" or "right" across X axis. ',
            "imageOverlayLabel": "MrrCrv",
            "backgroundColor": random_clrs[6],
            "command": "from nlol.scripts.rig_tools import mirror_curve_shapes\n"
            "from importlib import reload\n"
            "reload(mirror_curve_shapes)\n"
            "mirror_curve_shapes.mirror_curves()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Hierarchy",
            "image": "menuIconSelect.png",
            "annotation": "Select hierarchy",
            "imageOverlayLabel": "Hier",
            "command": "SelectHierarchy",
            "sourceType": "mel",
        },
        {
            "label": "Backface Culling",
            "image": "menuIconDisplay.png",
            "annotation": "Toggle geometry backface visibility",
            "imageOverlayLabel": "BC",
            "command": "ToggleBackfaceGeometry",
            "sourceType": "mel",
        },
        {
            "label": "Go to Bind Pose",
            "image": "goToBindPose.png",
            "annotation": "Returns the skeleton to the position where its bind pose was set",
            "imageOverlayLabel": "",
            "command": "GoToBindPose",
            "sourceType": "mel",
        },
        shelf_separator,
        {
            "label": "Build Rig",
            "image": "pythonFamily.png",
            "annotation": 'Build rig files from "maya/nlol/defaults/rig_folder_path.py"'
            'Change folder path in "rig_folder_path.py" to change rig setup.',
            "imageOverlayLabel": "HRig",
            "backgroundColor": random_clrs[7],
            "command": "from nlol.scripts.rig_setup import rig_build\n"
            "from importlib import reload\n"
            "reload(rig_build)\n"
            "rig_build.run_rig_build()",
            "sourceType": "python",
        },
        {
            "label": "Save Control Curves",
            "image": "pythonFamily.png",
            "annotation": "Save control curve shape attributes to load back in when building the rig.",
            "imageOverlayLabel": "SvCrvs",
            "backgroundColor": random_clrs[8],
            "command": "from nlol.scripts.rig_setup import save_control_curves\n"
            "from importlib import reload\n"
            "reload(save_control_curves)\n"
            "save_control_curves.SaveControlCurves().write_curve_attributes()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Delete Rig",
            "image": "pythonFamily.png",
            "annotation": "Delete current nLol rig in scene, "
            "but leave the skeletal mesh. Reset bind pose.",
            "imageOverlayLabel": "DlRig",
            "backgroundColor": random_clrs[9],
            "command": "from nlol.scripts.rig_tools import rig_delete\n"
            "from importlib import reload\n"
            "reload(rig_delete)\n"
            "rig_delete.remove_nlol_rig()",
            "sourceType": "python",
        },
        {
            "label": "Test Function",
            "image": "pythonFamily.png",
            "annotation": "Run test code from here. Add your code to this python function.",
            "imageOverlayLabel": "Tst",
            "backgroundColor": random_clrs[10],
            "command": "from nlol.scripts.standalone import run_test\n"
            "from importlib import reload\n"
            "reload(run_test)\n"
            "run_test.test()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Select Object Shapes",
            "image": "pythonFamily.png",
            "annotation": "Select object (curves) first, "
            "then this function selects those objects shapes.",
            "imageOverlayLabel": "SlShps",
            "backgroundColor": random_clrs[11],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.select_shapes()",
            "sourceType": "python",
        },
        {
            "label": "Show Curve Attributes",
            "image": "pythonFamily.png",
            "annotation": "Show useful curve attributes in channel box. Double click to remove.",
            "imageOverlayLabel": "CrvAtr",
            "backgroundColor": random_clrs[13],
            "command": "from nlol.scripts.rig_tools import show_attributes\n"
            "from importlib import reload\n"
            "reload(show_attributes)\n"
            "show_attributes.ShowAttributes().show_curve_attrs()",
            "doubleClickCommand": "from nlol.scripts.rig_tools import show_attributes\n"
            "from importlib import reload\nreload(show_attributes)\n"
            "show_attributes.ShowAttributes(show_attrs=False).show_curve_attrs()",
            "sourceType": "python",
        },
        {
            "label": "Select Shapes Show Attributes",
            "image": "pythonFamily.png",
            "annotation": "Select curves first then this function selects those objects shapes "
            "and shows useful attributes.",
            "imageOverlayLabel": "SlShw",
            "backgroundColor": random_clrs[12],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.select_shapes_show_attrs()",
            "sourceType": "python",
        },
        {
            "label": "Select All Controls",
            "image": "pythonFamily.png",
            "annotation": "Select all controls under rig group. "
            'Defaults to "rig_allGrp" if nothing selected.',
            "imageOverlayLabel": "SlCtrl",
            "backgroundColor": random_clrs[14],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.select_all_controls()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Assign Random Material",
            "image": "pythonFamily.png",
            "annotation": "Assign standard surface material with random color to selected objects.",
            "imageOverlayLabel": "RndMat",
            "backgroundColor": random_clrs[15],
            "command": "from nlol.scripts.standalone import assign_random_materials\n"
            "from importlib import reload\nreload(assign_random_materials)\n"
            "assign_random_materials.assign_rand_mat()",
            "sourceType": "python",
        },
    ]

    return rigging_list
