"""List of rigging variables to be called by shelf and menu."""

from importlib import reload

from nlol.scripts.rig_tools import random_generator

reload(random_generator)

random_colors_dull = random_generator.random_colors_dull


def build_rigging_list():
    """Create a dictionary list of rigging men and shelf buttons, and their attributes."""
    random_clrs = random_colors_dull()

    shelf_separator = {
        "label": "=" * 35,
        "image": "nlol_separator_03_blue.png",
        "annotation": "Separator.",
        "command": 'print("Separator.")',
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
            "label": "Locator Constrain Joints",
            "image": "pythonFamily.png",
            "annotation": "Snap locators to objects, then constrain those objects to locators. "
            "Double click to delete locators.",
            "imageOverlayLabel": "LocCons",
            "backgroundColor": (0.3, 0.2, 0.0),
            "command": "from nlol.scripts.rig_components import create_locators\n"
            "from importlib import reload\nreload(create_locators)\n"
            "create_locators.locator_constrain_joints(group_locator=True)",
            "doubleClickCommand": "from nlol.scripts.rig_components import create_locators\n"
            "from importlib import reload\nreload(create_locators)\n"
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
            "label": "Interactive playback",
            "image": "interactivePlayback.png",
            "annotation": "Start Interactive playback.",
            "imageOverlayLabel": "",
            "command": "InteractivePlayback",
            "sourceType": "mel",
        },
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
        {
            "label": "Print Object Type",
            "image": "pythonFamily.png",
            "annotation": "Print Maya Object type for selected.",
            "imageOverlayLabel": "ObjTyp",
            "backgroundColor": random_clrs[6],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.get_selection_type()",
            "sourceType": "python",
        },
        {
            "label": "Print Selected List",
            "image": "pythonFamily.png",
            "annotation": "Print Python list of selected Maya objects.",
            "imageOverlayLabel": "PrnLst",
            "backgroundColor": random_clrs[5],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.print_selected_list()",
            "sourceType": "python",
        },
        {
            "label": "Print Selected String List",
            "image": "pythonFamily.png",
            "annotation": "Print string list of selected Maya objects.",
            "imageOverlayLabel": "StrLst",
            "backgroundColor": random_clrs[4],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.print_selected_list(string_format=True)",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Build Skeletal Mesh Only",
            "image": "pythonFamily.png",
            "annotation": 'Build only skeletal mesh from "maya/nlol/defaults/...".  '
            'To change rig setup, change folder path in "rig_folder_path.py".',
            "imageOverlayLabel": "SklMsh",
            "backgroundColor": random_clrs[6],
            "command": "from nlol.scripts.rig_setup import rig_build_mesh_skeleton\n"
            "from importlib import reload\nreload(rig_build_mesh_skeleton)\n"
            "rig_build_mesh_skeleton.run_mesh_skeleton_build()",
            "sourceType": "python",
        },
        {
            "label": "Build Rig",
            "image": "pythonFamily.png",
            "annotation": 'Build rig files from "maya/nlol/defaults/...".  '
            'Change folder path in "rig_folder_path.py" to change rig setup.',
            "imageOverlayLabel": "BRig",
            "backgroundColor": random_clrs[7],
            "command": "from nlol.scripts.rig_setup import rig_build\n"
            "from importlib import reload\nreload(rig_build)\n"
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
            "from importlib import reload\nreload(save_control_curves)\n"
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
        # {
        #     "label": "Test Function",
        #     "image": "pythonFamily.png",
        #     "annotation": "Run test code from here. Add your code to this python function.",
        #     "imageOverlayLabel": "Tst",
        #     "backgroundColor": random_clrs[10],
        #     "command": "from nlol.scripts.standalone import run_test\n"
        #     "from importlib import reload\n"
        #     "reload(run_test)\n"
        #     "run_test.test()",
        #     "sourceType": "python",
        # },
        {
            "label": "Setup nCloth Rig Components",
            "image": "pythonFamily.png",
            "annotation": "Setup nCloth rig components. Reads data from cloth_data folder.",
            "imageOverlayLabel": "ClthRg",
            "backgroundColor": random_clrs[10],
            "command": "from nlol.scripts.rig_components import flexi_to_cloth\n"
            "from importlib import reload\n"
            "reload(flexi_to_cloth)\n"
            "flexi_to_cloth.FlexiToCloth().build()",
            "sourceType": "python",
        },
        {
            "label": "Save Attach Verts and Object",
            "image": "pythonFamily.png",
            "annotation": "Select vertices from cloth mesh and attach object. "
            "Cloth mesh should not be initialized yet. "
            "This just saves selection to json in cloth_data folder.",
            "imageOverlayLabel": "SvClth",
            "backgroundColor": random_clrs[11],
            "command": "from nlol.scripts.rig_components import flexi_to_cloth\n"
            "from importlib import reload\n"
            "reload(flexi_to_cloth)\n"
            "flexi_to_cloth.FlexiToCloth().save_vertex_ids()",
            "sourceType": "python",
        },
        {
            "label": "Save Collision Meshes",
            "image": "pythonFamily.png",
            "annotation": "Save selected collision mesh names to cloth_data folder.",
            "imageOverlayLabel": "SvColl",
            "backgroundColor": random_clrs[12],
            "command": "from nlol.scripts.rig_components import flexi_to_cloth\n"
            "from importlib import reload\n"
            "reload(flexi_to_cloth)\n"
            "flexi_to_cloth.FlexiToCloth().save_collision_meshes()",
            "sourceType": "python",
        },
        {
            "label": "Save nCloth Settings",
            "image": "pythonFamily.png",
            "annotation": "Save settings for selected nCloth objects.",
            "imageOverlayLabel": "SvSet",
            "backgroundColor": random_clrs[13],
            "command": "from nlol.scripts.rig_components import flexi_to_cloth\n"
            "from importlib import reload\n"
            "reload(flexi_to_cloth)\n"
            "flexi_to_cloth.FlexiToCloth().save_ncloth_settings()",
            "sourceType": "python",
        },
        {
            "label": "Apply nCloth Settings",
            "image": "pythonFamily.png",
            "annotation": "Apply saved nCloth settings from cloth_data folder.",
            "imageOverlayLabel": "AplySet",
            "backgroundColor": random_clrs[14],
            "command": "from nlol.scripts.rig_components import flexi_to_cloth\n"
            "from importlib import reload\n"
            "reload(flexi_to_cloth)\n"
            "flexi_to_cloth.FlexiToCloth().apply_ncloth_settings()",
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
            'Defaults to the "_rigGrp" if nothing selected.',
            "imageOverlayLabel": "SlCtrl",
            "backgroundColor": random_clrs[14],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.select_all_ctrls()",
            "sourceType": "python",
        },
        {
            "label": "Reset All Controls",
            "image": "pythonFamily.png",
            "annotation": "Resets selected ctrls and their descendents or "
            'all ctrls under groups containing string "_rigGrp" if nothing selected. '
            "Resets translate, rotate, and scale.",
            "imageOverlayLabel": "RstCtrl",
            "backgroundColor": random_clrs[11],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.reset_all_ctrls()",
            "sourceType": "python",
        },
        {
            "label": "Reset All Controls (Keyable Attrs)",
            "image": "pythonFamily.png",
            "annotation": 'Same as "Reset All Controls" except resets all keyable attributes '
            "instead of just the smaller list of specified attributes in the function.",
            "imageOverlayLabel": "RstKybl",
            "backgroundColor": random_clrs[12],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.reset_all_ctrls(all_keyable=True)",
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
        {
            "label": "Create Follicle At Surface",
            "image": "pythonFamily.png",
            "annotation": 'Create and attach follicle at nearest "example_surface" point '
            'to "example joint". Surface may be a regular polygonal mesh or nurbs surface.',
            "imageOverlayLabel": "JntFol",
            "backgroundColor": random_clrs[16],
            "command": "from nlol.scripts.rig_components import follicle_at_surface\n"
            "from importlib import reload\nreload(follicle_at_surface)\n"
            "follicle_at_surface.create_joint_follicle()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Export Skin Clusters",
            "image": "pythonFamily.png",
            "annotation": "Select one or more skinned meshes and export their skin clusters to xml."
            " Uses the index method. Exports to current nLol rig folder.",
            "imageOverlayLabel": "ExpSkn",
            "backgroundColor": random_clrs[12],
            "command": "from nlol.scripts.rig_tools import skin_export_import\n"
            "from importlib import reload\nreload(skin_export_import)\n"
            "skin_export_import.export_skin_weights()",
            "sourceType": "python",
        },
        {
            "label": "Import Skin Clusters",
            "image": "pythonFamily.png",
            "annotation": "Import xml skinCluster files from nLol rig folderpath and apply them. "
            "No mesh selection required. "
            "Mesh (shape) names and vertex order should be same as exported.",
            "imageOverlayLabel": "ImpSkn",
            "backgroundColor": random_clrs[13],
            "command": "from nlol.scripts.rig_tools import skin_export_import\n"
            "from importlib import reload\nreload(skin_export_import)\n"
            "skin_export_import.import_skin_weights()",
            "sourceType": "python",
        },
        {
            "label": "Import Skin Selected Only",
            "image": "pythonFamily.png",
            "annotation": "For selected geometry only. "
            "Import xml skinCluster files from nLol rig folderpath and apply them. "
            "Mesh (shape) names and vertex order should be same as exported.",
            "imageOverlayLabel": "ISknSl",
            "backgroundColor": random_clrs[14],
            "command": "from nlol.scripts.rig_tools import skin_export_import\n"
            "from importlib import reload\nreload(skin_export_import)\n"
            "skin_export_import.import_skin_weights(selected_only=True)",
            "sourceType": "python",
        },
        {
            "label": "Select Skinned Joints",
            "image": "pythonFamily.png",
            "annotation": "Select skinned joints from first selected mesh object.",
            "imageOverlayLabel": "SkdJts",
            "backgroundColor": random_clrs[15],
            "command": "from nlol.scripts.standalone import small_functions\n"
            "from importlib import reload\nreload(small_functions)\n"
            "small_functions.query_skinned_joints()",
            "sourceType": "python",
        },
    ]

    return rigging_list
