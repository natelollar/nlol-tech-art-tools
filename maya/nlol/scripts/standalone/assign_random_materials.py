import random

from maya import cmds


def assign_rand_mat():
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
