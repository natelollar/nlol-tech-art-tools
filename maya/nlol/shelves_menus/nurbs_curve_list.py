"""List of nurbs curve variables to be called by shelf and menu."""

from importlib import reload

from nlol.core.rig_tools import random_generator

reload(random_generator)

random_colors_dull = random_generator.random_colors_dull


def build_curve_list():
    """Create a dictionary list of curve shelves and their attributes."""
    random_clrs = random_colors_dull()
    random_clrs_other = random_colors_dull(seed_string_prefix="other")
    random_clrs_nurbs = random_colors_dull(seed_string_prefix="nurbs")

    shelf_separator = {
        "label": "=" * 35,
        "image": "",
        "annotation": "Shelf separator.",
        "imageOverlayLabel": "",
        "flexibleWidthType": 2,  # custom width
        "flexibleWidthValue": 16,  # custom width pixels
        "backgroundColor": (0.4, 0.4, 0.4),
        "highlightColor": (0.4, 0.4, 0.4),
        "command": "print('Shelf separator.')",
        "sourceType": "python",
    }

    curve_list = [   
        {
            "label": "Nurbs Sphere",
            "image": "pythonFamily.png",
            "annotation": "Create nurbs sphere object.",
            "imageOverlayLabel": "SphNb",
            "backgroundColor": random_clrs_nurbs[0],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateNurbs(name='sphere_nrb').sphere_nurbs()",
            "sourceType": "python",
        },
        {
            "label": "Nurbs Cube",
            "image": "pythonFamily.png",
            "annotation": "Create nurbs cube object.",
            "imageOverlayLabel": "SphNb",
            "backgroundColor": random_clrs_nurbs[1],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateNurbs(name='cube_nrb').cube_nurbs()",
            "sourceType": "python",
        },
        shelf_separator,
        {
            "label": "Box Curve",
            "image": "pythonFamily.png",
            "annotation": "Create box curve object.",
            "imageOverlayLabel": "Box",
            "backgroundColor": random_clrs_other[0],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).box_curve()",
            "sourceType": "python",
        },
        {
            "label": "Circle Curve",
            "image": "pythonFamily.png",
            "annotation": "Create circle curve object.",
            "imageOverlayLabel": "Crcl",
            "backgroundColor": random_clrs_other[1],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).circle_curve()",
            "sourceType": "python",
        },
        {
            "label": "Global Curve",
            "image": "pythonFamily.png",
            "annotation": "Create global curve object.",
            "imageOverlayLabel": "Globl",
            "backgroundColor": random_clrs_other[2],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).global_curve()",
            "sourceType": "python",
        },
        {
            "label": "Pyramid Curve",
            "image": "pythonFamily.png",
            "annotation": "Create pyramid curve object.",
            "imageOverlayLabel": "Pyrmd",
            "backgroundColor": random_clrs_other[3],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).pyramid_curve()",
            "sourceType": "python",
        },
        {
            "label": "Sphere Curve",
            "image": "pythonFamily.png",
            "annotation": "Create sphere curve object.",
            "imageOverlayLabel": "Sphr",
            "backgroundColor": random_clrs_other[4],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).sphere_curve()",
            "sourceType": "python",
        },
        {
            "label": "Tri Circle Curve",
            "image": "pythonFamily.png",
            "annotation": "Create sphere curve object.",
            "imageOverlayLabel": "TriCrc",
            "backgroundColor": random_clrs_other[5],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).tri_circle_curve()",
            "sourceType": "python",
        },
        {
            "label": "Locator Curve",
            "image": "pythonFamily.png",
            "annotation": "Create locator curve object.",
            "imageOverlayLabel": "Loctr",
            "backgroundColor": random_clrs_other[6],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).locator_curve()",
            "sourceType": "python",
        },
        {
            "label": "Arrow Twist Curve",
            "image": "pythonFamily.png",
            "annotation": "Create arrow twist curve object.",
            "imageOverlayLabel": "ArTwst",
            "backgroundColor": random_clrs[0],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).arrow_twist_curve()",
            "sourceType": "python",
        },
        {
            "label": "Cylinder Curve",
            "image": "pythonFamily.png",
            "annotation": "Create cylinder curve object.",
            "imageOverlayLabel": "Cylndr",
            "backgroundColor": random_clrs[1],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).cylinder_curve()",
            "sourceType": "python",
        },
        {
            "label": "Four Arrow Curve",
            "image": "pythonFamily.png",
            "annotation": "Create four arrow curve object.",
            "imageOverlayLabel": "4Arw",
            "backgroundColor": random_clrs[2],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).four_arrow_curve()",
            "sourceType": "python",
        },
        {
            "label": "Square Curve",
            "image": "pythonFamily.png",
            "annotation": "Create square curve object.",
            "imageOverlayLabel": "Sqr",
            "backgroundColor": random_clrs[3],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).square_curve()",
            "sourceType": "python",
        },
        {
            "label": "Octagon Curve",
            "image": "pythonFamily.png",
            "annotation": "Create octagon curve object.",
            "imageOverlayLabel": "Octgn",
            "backgroundColor": random_clrs[4],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).octagon_curve()",
            "sourceType": "python",
        },
        {
            "label": "Dodecagon Curve",
            "image": "pythonFamily.png",
            "annotation": "Create dodecagon curve object.",
            "imageOverlayLabel": "12Crcl",
            "backgroundColor": random_clrs[5],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).dodecagon_curve()",
            "sourceType": "python",
        },
        {
            "label": "Hexadecagon Curve",
            "image": "pythonFamily.png",
            "annotation": "Create hexadecagon curve object.",
            "imageOverlayLabel": "16Crcl",
            "backgroundColor": random_clrs[6],
            "command": "from nlol.core.rig_components import create_nurbs_curves\n"
            "from importlib import reload\nreload(create_nurbs_curves)\n"
            "create_nurbs_curves.CreateCurves(use_curve_defaults=True, "
            "show_attrs=True).hexadecagon_curve()",
            "sourceType": "python",
        },
    ]

    return curve_list
