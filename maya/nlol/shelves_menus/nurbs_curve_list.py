"""List of nurbs curve variables to be called by shelf and menu."""

from nlol.scripts.rig_tools import random_generator as rg

box_curve_rgb = rg.random_color(seed_string="box_curve_rgb")
box_curve_name = '"box_crv"'
circle_curve_rgb = rg.random_color(seed_string="circle_curve_rgb")
circle_curve_name = '"circle_crv"'
global_curve_rgb = rg.random_color(seed_string="global_curve_rgb")
global_curve_name = '"global_curve_crv"'
pyramid_curve_rgb = rg.random_color(seed_string="pyramid_curve_rgb0")
pyramid_curve_name = '"pyramid_crv"'
sphere_curve_rgb = rg.random_color(seed_string="sphere_curve_rgb")
sphere_curve_name = '"sphere_crv"'
tri_circle_curve_rgb = rg.random_color(seed_string="tri_circle_curve_rgb")
tri_circle_curve_name = '"tri_circle_crv"'
locator_curve_rgb = rg.random_color(seed_string="locator_curve_rgb")
locator_curve_name = '"locator_crv"'
sphere_nurbs_rgb = rg.random_color(seed_string="sphere_nurbs_rgb")
sphere_nurbs_name = '"sphere_nrb"'

NURBS_CURVE_LIST = [
    {
        "label": "Box Curve",
        "image": "pythonFamily.png",
        "annotation": "Create box curve object.",
        "imageOverlayLabel": "BxCv",
        "backgroundColor": box_curve_rgb[1],
        "command": "from nlol.scripts.rig_components import create_nurbs_curves\n"
        "from importlib import reload\n"
        "reload(create_nurbs_curves)\n"
        f"create_nurbs_curves.CreateCurves(name={box_curve_name},"
        f"color_rgb={box_curve_rgb[0]}, show_attrs=True).box_curve()",
        "sourceType": "python",
    },
    {
        "label": "Circle Curve",
        "image": "pythonFamily.png",
        "annotation": "Create circle curve object.",
        "imageOverlayLabel": "CrlCv",
        "backgroundColor": circle_curve_rgb[1],
        "command": "from nlol.scripts.rig_components import create_nurbs_curves\n"
        "from importlib import reload\n"
        "reload(create_nurbs_curves)\n"
        f"create_nurbs_curves.CreateCurves(name={circle_curve_name},"
        f"color_rgb={circle_curve_rgb[0]}, show_attrs=True).circle_curve()",
        "sourceType": "python",
    },
    {
        "label": "Global Curve",
        "image": "pythonFamily.png",
        "annotation": "Create global curve object.",
        "imageOverlayLabel": "GlbCv",
        "backgroundColor": global_curve_rgb[1],
        "command": "from nlol.scripts.rig_components import create_nurbs_curves\n"
        "from importlib import reload\n"
        "reload(create_nurbs_curves)\n"
        f"create_nurbs_curves.CreateCurves(name={global_curve_name},"
        f"color_rgb={global_curve_rgb[0]}, show_attrs=True).global_curve()",
        "sourceType": "python",
    },
    {
        "label": "Pyramid Curve",
        "image": "pythonFamily.png",
        "annotation": "Create pyramid curve object.",
        "imageOverlayLabel": "PyrCv",
        "backgroundColor": pyramid_curve_rgb[1],
        "command": "from nlol.scripts.rig_components import create_nurbs_curves\n"
        "from importlib import reload\n"
        "reload(create_nurbs_curves)\n"
        f"create_nurbs_curves.CreateCurves(name={pyramid_curve_name},"
        f"color_rgb={pyramid_curve_rgb[0]}, show_attrs=True).pyramid_curve()",
        "sourceType": "python",
    },
    {
        "label": "Sphere Curve",
        "image": "pythonFamily.png",
        "annotation": "Create sphere curve object.",
        "imageOverlayLabel": "SprCv",
        "backgroundColor": sphere_curve_rgb[1],
        "command": "from nlol.scripts.rig_components import create_nurbs_curves\n"
        "from importlib import reload\n"
        "reload(create_nurbs_curves)\n"
        f"create_nurbs_curves.CreateCurves(name={sphere_curve_name},"
        f"color_rgb={sphere_curve_rgb[0]}, show_attrs=True).sphere_curve()",
        "sourceType": "python",
    },
    {
        "label": "Tri Circle Curve",
        "image": "pythonFamily.png",
        "annotation": "Create sphere curve object.",
        "imageOverlayLabel": "TriCv",
        "backgroundColor": tri_circle_curve_rgb[1],
        "command": "from nlol.scripts.rig_components import create_nurbs_curves\n"
        "from importlib import reload\n"
        "reload(create_nurbs_curves)\n"
        f"create_nurbs_curves.CreateCurves(name={tri_circle_curve_name},"
        f"color_rgb={tri_circle_curve_rgb[0]}, show_attrs=True).tri_circle_curve()",
        "sourceType": "python",
    },
    {
        "label": "Locator Curve",
        "image": "pythonFamily.png",
        "annotation": "Create locator curve object.",
        "imageOverlayLabel": "LocCv",
        "backgroundColor": locator_curve_rgb[1],
        "command": "from nlol.scripts.rig_components import create_nurbs_curves\n"
        "from importlib import reload\n"
        "reload(create_nurbs_curves)\n"
        f"create_nurbs_curves.CreateCurves(name={locator_curve_name},"
        f"color_rgb={locator_curve_rgb[0]}, show_attrs=True).locator_curve()",
        "sourceType": "python",
    },
    {
        "label": "Nurbs Sphere",
        "image": "pythonFamily.png",
        "annotation": "Create nurbs sphere object.",
        "imageOverlayLabel": "SphNb",
        "backgroundColor": sphere_nurbs_rgb[1],
        "command": "from nlol.scripts.rig_components import create_nurbs_curves\n"
        "from importlib import reload\n"
        "reload(create_nurbs_curves)\n"
        f"create_nurbs_curves.CreateNurbs(name={sphere_nurbs_name},"
        f"color_rgb={sphere_nurbs_rgb[0]}).sphere_nurbs()",
        "sourceType": "python",
    },
]
