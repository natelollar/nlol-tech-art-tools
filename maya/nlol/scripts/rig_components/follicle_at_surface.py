from maya import cmds
from nlol.scripts.rig_components import create_nurbs_curves


def create_joint_follicle(
    flexi_surface: str = "flexiSurface_geo",
    joint: str = "example_joint",
    name: str = "example",
    create_locator_curve: bool = True,
) -> tuple[str, str, str]:
    """Create follicle at position where joint is closest to flexi surface.

    Args:
        flexi_surface: Mesh surface to detect closest joint position for follicle creation.
        joint: Joint for detecing closest mesh position.
        name: Overall core name for created objects.
        create_locator_curve: Locator shaped curve helpful for viewing follicle position.

    Returns:
        Follicle transform, shape, and curve.

    """
    # ----- create and setup nodes -----
    suffix = "1" if name == "example" else ""  # add suffix when testing
    follicle_transform = cmds.createNode("transform", name=f"{name}_follicle{suffix}")
    follicle_shape = cmds.createNode("follicle", parent=follicle_transform)

    flexi_surface_shape = cmds.listRelatives(flexi_surface, shapes=True)[0]
    flexi_surface_type = cmds.objectType(flexi_surface_shape)

    if flexi_surface_type == "nurbsSurface":
        cmds.connectAttr(f"{flexi_surface_shape}.local", f"{follicle_shape}.inputSurface")
        closestpointonmesh_nd = cmds.createNode("closestPointOnSurface")
        cmds.connectAttr(f"{flexi_surface_shape}.local", f"{closestpointonmesh_nd}.inputSurface")
    else:
        cmds.connectAttr(f"{flexi_surface_shape}.outMesh", f"{follicle_shape}.inputMesh")
        closestpointonmesh_nd = cmds.createNode("closestPointOnMesh")
        cmds.connectAttr(f"{flexi_surface_shape}.outMesh", f"{closestpointonmesh_nd}.inMesh")

    cmds.connectAttr(f"{flexi_surface_shape}.worldMatrix[0]", f"{follicle_shape}.inputWorldMatrix")
    joint_position = cmds.xform(joint, query=True, worldSpace=True, translation=True)
    cmds.setAttr(f"{closestpointonmesh_nd}.inPosition", *joint_position)

    # ----- query position and uv data -----
    surface_position = cmds.getAttr(f"{closestpointonmesh_nd}.position")[0]
    u_pos = cmds.getAttr(f"{closestpointonmesh_nd}.parameterU")
    v_pos = cmds.getAttr(f"{closestpointonmesh_nd}.parameterV")
    # normalize nurbs surface UVs
    if flexi_surface_type == "nurbsSurface":
        u_min, u_max = cmds.getAttr(f"{flexi_surface}.minMaxRangeU")[0]
        v_min, v_max = cmds.getAttr(f"{flexi_surface}.minMaxRangeV")[0]
        u_pos = (u_pos - u_min) / (u_max - u_min)
        v_pos = (v_pos - v_min) / (v_max - v_min)

    # ----- attach follicle to surface -----
    # must set translate and uv parameters before connecting outTranslate and outRotate
    cmds.setAttr(f"{follicle_transform}.translate", *surface_position)
    cmds.setAttr(f"{follicle_shape}.parameterU", u_pos)
    cmds.setAttr(f"{follicle_shape}.parameterV", v_pos)

    cmds.connectAttr(f"{follicle_shape}.outTranslate", f"{follicle_transform}.translate")
    cmds.connectAttr(f"{follicle_shape}.outRotate", f"{follicle_transform}.rotate")

    # ----- create curve under follicle -----
    # helps for viewing follicle
    # parent curve under follicle
    if create_locator_curve:
        locator_curve = create_nurbs_curves.CreateCurves(
            name=f"{follicle_transform}Crv",
            color_rgb=(0.6, 0.0, 0.3),
            line_width=1.5,
        ).locator_curve()
        cmds.parent(locator_curve, follicle_transform, relative=True)

    # ----- cleanup -----
    cmds.delete(closestpointonmesh_nd)
    for axis in "XYZ":
        cmds.setAttr(f"{follicle_transform}.translate{axis}", lock=True)
        cmds.setAttr(f"{follicle_transform}.rotate{axis}", lock=True)
        if create_locator_curve:
            cmds.setAttr(f"{locator_curve}.translate{axis}", lock=True)
            cmds.setAttr(f"{locator_curve}.rotate{axis}", lock=True)
            cmds.setAttr(f"{locator_curve}.scale{axis}", lock=True)

    return follicle_transform, follicle_shape, locator_curve
