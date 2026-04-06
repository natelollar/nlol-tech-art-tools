import random

from maya import cmds


def assign_rand_mat() -> None:
    """Assign standard surface material with random color to selected objects.
    Name materials after the objects.
    Useful for visualizing multiple of blockout shapes.
    """
    selection = cmds.ls(sl=True)

    for obj in selection:
        # create material name
        if "_" in obj:
            mat_name = obj.replace(obj.split("_")[-1], "mat")
        else:
            mat_name = "example_mat"
        # create material
        standard_mat = cmds.shadingNode("standardSurface", name=mat_name, asShader=True)
        # create shader group
        standard_mat_SG = cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=f"{standard_mat}SG",
        )
        # connect material to shader group
        cmds.connectAttr(f"{standard_mat}.outColor", f"{standard_mat_SG}.surfaceShader", force=True)

        # assign material to selected
        cmds.select(obj)
        cmds.hyperShade(assign=standard_mat)

        # create random colors
        clr_r = random.triangular(0, 1)
        clr_g = random.triangular(0, 1)
        clr_b = random.triangular(0, 1)

        # assign random colors
        cmds.setAttr(f"{standard_mat}.baseColor", clr_r, clr_g, clr_b)


def random_proxy_color(shaded_polywire: bool = False) -> None:
    """Assign random color to selected Arnold standIn proxy ".ass" files.

    Args:
        shaded_polywire: Whether to use shaded polywire on proxy,
            or else just use shaded.

    """
    selected_proxies = cmds.ls(selection=True)

    for proxy in selected_proxies:
        shapes = cmds.listRelatives(proxy, shapes=True, type="aiStandIn")
        for shape in shapes:
            if shaded_polywire:
                cmds.setAttr(f"{shape}.mode", 5)  # Shaded Polywire
            else:
                pass
            cmds.setAttr(f"{shape}.overrideEnabled", 1)
            cmds.setAttr(f"{shape}.overrideRGBColors", 1)
            random_values = [random.random() for _ in range(3)]
            cmds.setAttr(f"{shape}.overrideColorRGB", *random_values)


def prox_view_mode(view_mode: int = 5) -> None:
    """Assign random color to selected Arnold standIn proxy ".ass" files.

    Args:
        view_mode: wireframe = 3, shaded polywire = 5, shaded = 6

    """
    selected_proxies = cmds.ls(selection=True)

    for proxy in selected_proxies:
        shapes = cmds.listRelatives(proxy, shapes=True, type="aiStandIn")
        for shape in shapes:
            cmds.setAttr(f"{shape}.mode", view_mode)
