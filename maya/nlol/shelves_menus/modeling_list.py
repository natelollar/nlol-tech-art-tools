"""List of modeling variables to be called by shelf and menu."""

from importlib import reload

from nlol.core.rig_tools import random_generator

reload(random_generator)

random_colors_dull = random_generator.random_colors_dull


def build_modeling_list():
    """Create a dictionary list of modeling menu and shelf buttons, and their attributes."""
    random_clrs = random_colors_dull()

    shelf_separator = {
        "label": "=" * 35,
        "image": "nlol_separator_03_blue.png",
        "annotation": "Separator.",
        "command": 'print("Separator.")',
        "sourceType": "python",
    }

    modeling_list = [
        shelf_separator,
        {
            "label": "Export Materials",
            "image": "pythonFamily.png",
            "annotation": "Export materials for selected mesh objects to nLol rig folder path.",
            "imageOverlayLabel": "ExpMat",
            "backgroundColor": random_clrs[0],
            "command": "from nlol.core.modeling_tools import materials_export_import\n"
            "from importlib import reload\nreload(materials_export_import)\n"
            "materials_export_import.export_materials()",
            "sourceType": "python",
        },
        {
            "label": "Import Materials to Selected (Matching mesh name)",
            "image": "pythonFamily.png",
            "annotation": "Import materials for selected mesh objects from nLol rig folder path. "
            'Example folderpath: "/auto_rig/materials/". '
            "Materials will be applied to selected objects based on matching name components "
            "of selected mesh to exported material.",
            "imageOverlayLabel": "ImpMat",
            "backgroundColor": random_clrs[1],
            "command": "from nlol.core.modeling_tools import materials_export_import\n"
            "from importlib import reload\nreload(materials_export_import)\n"
            "materials_export_import.import_materials_to_selected()",
            "sourceType": "python",
        },
        # {
        #     "label": "Import Materials to Selected (Matching material name)",
        #     "image": "pythonFamily.png",
        #     "annotation": "Import materials for selected mesh objects from nLol rig folder path. "
        #     'Example folderpath: "/auto_rig/materials/" '
        #     "Materials will be applied to selected objects based on matching name components "
        #     "of assigned material to exported material.",
        #     "imageOverlayLabel": "ImpMat",
        #     "backgroundColor": random_clrs[2],
        #     "command": "from nlol.core.modeling_tools import materials_export_import\n"
        #     "from importlib import reload\nreload(materials_export_import)\n"
        #     "materials_export_import.import_materials_to_selected(use_material_name=True)",
        #     "sourceType": "python",
        # },
        {
            "label": "Update Materials (Scene or Selected)",
            "image": "pythonFamily.png",
            "annotation": "Update scene materials that have matching materials already exported. "
            "Materials should already be exported to the nLol rig folder. "
            "Select meshes to only import materials assigned to those meshes. "
            'Example folderpath: "/auto_rig/materials/" ',
            "imageOverlayLabel": "UpMat",
            "backgroundColor": random_clrs[3],
            "command": "from nlol.core.modeling_tools import materials_export_import\n"
            "from importlib import reload\nreload(materials_export_import)\n"
            "materials_export_import.update_scene_materials()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Substance Arnold Material",
            "image": "pythonFamily.png",
            "annotation": "Setup Arnold material based on selection of 3 input textures "
            "(from Marmoset Toolbag or Substance Painter) and an empty Maya shading group. "
            "Use drag and drop to add texture file nodes to Maya. "
            "Required selection: Color map, Mix map, Normal map, Shading Group. "
            '(3 "file" nodes and 1 "shadingEngine" node)',
            "imageOverlayLabel": "SubMat",
            "backgroundColor": random_clrs[4],
            "command": "from nlol.core.modeling_tools import arnold_material_setup\n"
            "from importlib import reload\nreload(arnold_material_setup)\n"
            "arnold_material_setup.ArnoldMaterialSetup().arnold_basic_mat(substance_material=True, "
            "use_arnold_file_nodes=True)",
            "sourceType": "python",
        },
        {
            "label": "Toolbag Arnold Material",
            "image": "pythonFamily.png",
            "annotation": "Setup Arnold material based on selection of 3 input textures "
            "(from Marmoset Toolbag or Substance Painter) and an empty Maya shading group. "
            "Use drag and drop to add texture file nodes to Maya. "
            "Required selection: Color map, Mix map, Normal map, Shading Group. "
            '(3 "file" nodes and 1 "shadingEngine" node)',
            "imageOverlayLabel": "TooMat",
            "backgroundColor": random_clrs[6],
            "command": "from nlol.core.modeling_tools import arnold_material_setup\n"
            "from importlib import reload\nreload(arnold_material_setup)\n"
            "arnold_material_setup.ArnoldMaterialSetup().arnold_basic_mat()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "file to aiImage",
            "image": "pythonFamily.png",
            "annotation": "Convert Maya file node to Arnold aiimage node. "
            'Delete selected "place2dTexture" nodes and old "file" nodes. '
            "Useful if dragging and dropping in images to hypershade.",
            "imageOverlayLabel": "ArnFil",
            "backgroundColor": random_clrs[7],
            "command": "from nlol.core.modeling_tools import arnold_material_setup\n"
            "from importlib import reload\nreload(arnold_material_setup)\n"
            "arnold_material_setup.ArnoldMaterialSetup().convert_file_to_aiimage()",
            "sourceType": "python",
        },
        {
            "label": "file to aiImage (keep old)",
            "image": "pythonFamily.png",
            "annotation": "Convert Maya file node to Arnold aiimage node. "
            'Do not delete old "file" or "place2dTexture" nodes. ',
            "imageOverlayLabel": "ArnDup",
            "backgroundColor": random_clrs[8],
            "command": "from nlol.core.modeling_tools import arnold_material_setup\n"
            "from importlib import reload\nreload(arnold_material_setup)\n"
            "arnold_material_setup.ArnoldMaterialSetup().convert_file_to_aiimage(delete_old=False)",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Grid Layout",
            "image": "pythonFamily.png",
            "annotation": "Lay objects out in a basic grid.",
            "imageOverlayLabel": "GrdLyt",
            "backgroundColor": random_clrs[9],
            "command": "from nlol.core.modeling_tools import basic_layout\n"
            "from importlib import reload\nreload(basic_layout)\n"
            "basic_layout.grid_layout()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Assign Random Proxy Color",
            "image": "pythonFamily.png",
            "annotation": "Assign random color to selected Arnold standin proxy objects.",
            "imageOverlayLabel": "PxyClr",
            "backgroundColor": random_clrs[10],
            "command": "from nlol.core.standalone import assign_random_colors\n"
            "from importlib import reload\nreload(assign_random_colors)\n"
            "assign_random_colors.random_proxy_color()",
            "sourceType": "python",
        },
        {
            "label": "Proxy View Mode (Shaded)",
            "image": "pythonFamily.png",
            "annotation": "Arnold proxy standin view mode. "
            "view_mode: wireframe = 3, shaded polywire = 5, shaded = 6",
            "imageOverlayLabel": "Shaded",
            "backgroundColor": random_clrs[13],
            "command": "from nlol.core.standalone import assign_random_colors\n"
            "from importlib import reload\nreload(assign_random_colors)\n"
            "assign_random_colors.prox_view_mode(view_mode=6)",
            "sourceType": "python",
        },
        {
            "label": "Proxy View Mode (Shaded Polywire)",
            "image": "pythonFamily.png",
            "annotation": "Arnold proxy standin view mode. "
            "view_mode: wireframe = 3, shaded polywire = 5, shaded = 6",
            "imageOverlayLabel": "ShdWir",
            "backgroundColor": random_clrs[12],
            "command": "from nlol.core.standalone import assign_random_colors\n"
            "from importlib import reload\nreload(assign_random_colors)\n"
            "assign_random_colors.prox_view_mode(view_mode=5)",
            "sourceType": "python",
        },
        {
            "label": "Proxy View Mode (Wireframe)",
            "image": "pythonFamily.png",
            "annotation": "Arnold proxy standin view mode. "
            "view_mode: wireframe = 3, shaded polywire = 5, shaded = 6",
            "imageOverlayLabel": "Wire",
            "backgroundColor": random_clrs[11],
            "command": "from nlol.core.standalone import assign_random_colors\n"
            "from importlib import reload\nreload(assign_random_colors)\n"
            "assign_random_colors.prox_view_mode(view_mode=3)",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Scatter Tool",
            "image": "pythonFamily.png",
            "annotation": "Scatter selected objects to last selected object.",
            "imageOverlayLabel": "SctrUI",
            "backgroundColor": random_clrs[34],
            "command": "from nlol.core.ui import scatter_tool_ui\nscatter_tool_ui.reload_tool()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Export Import Tool",
            "image": "pythonFamily.png",
            "annotation": "Export and import multiple selected objects.",
            "imageOverlayLabel": "ExImUI",
            "backgroundColor": random_clrs[36],
            "command": "from nlol.core.ui import export_import_ui\nexport_import_ui.reload_tool()",
            "sourceType": "python",
        },
    ]

    return modeling_list
