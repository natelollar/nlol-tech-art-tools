"""List of rigging variables to be called by shelf and menu."""

from nlol.scripts.rig_tools import random_generator as rg

rig_build_rgb = rg.random_color(seed_string="rig_build_rgb")
snap_to_axis_01_rgb = rg.random_color(seed_string="snap_to_axis_01")
snap_to_axis_02_rgb = rg.random_color(seed_string="snap_to_axis_02")
create_fk_ctrl = rg.random_color(seed_string="create_fk_ctrl")
create_root_ctrl = rg.random_color(seed_string="create_root_ctrl")
test_function_rgb = rg.random_color(seed_string="test_function")
remove_nlol_rig_rgb = rg.random_color(seed_string="remove_nlol_rig_rgb")

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

RIGGING_LIST = [
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
        "annotation": "Show useful joint attributes in Channel Box. Double click to remove.",
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
        "backgroundColor": snap_to_axis_01_rgb[1],
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
        "backgroundColor": snap_to_axis_02_rgb[1],
        "command": "from nlol.scripts.rig_tools import get_aligned_axis\n"
        "from importlib import reload\n"
        "reload(get_aligned_axis)\n"
        "get_aligned_axis.snap_to_closest_axis(translate_only=True)",
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
        "label": "Rig Human",
        "image": "pythonFamily.png",
        "annotation": "Build default human rig.  "
        'Check "./maya/nlol/defaults/rig_human/" for details',
        "imageOverlayLabel": "HRig",
        "backgroundColor": rig_build_rgb[1],
        "command": "from nlol.defaults.rig_human import rig_build\n"
        "from importlib import reload\n"
        "reload(rig_build)\n"
        "rig_build.run_rig_build()",
        "sourceType": "python",
    },
    shelf_separator,
    {
        "label": "Delete Rig",
        "image": "pythonFamily.png",
        "annotation": "Delete current nLol rig in scene, "
        "but leave the skeletal mesh. Reset bind pose.",
        "imageOverlayLabel": "DlRig",
        "backgroundColor": remove_nlol_rig_rgb[1],
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
        "backgroundColor": test_function_rgb[1],
        "command": "from nlol.scripts.standalone import run_test\n"
        "from importlib import reload\n"
        "reload(run_test)\n"
        "run_test.test()",
        "sourceType": "python",
    },
]
