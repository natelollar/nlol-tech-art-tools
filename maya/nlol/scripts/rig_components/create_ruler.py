from maya import cmds
from nlol.scripts.rig_components.clean_constraints import point_constr


def create_attached_ruler(
    name: str,
    ruler_start_object: str,
    ruler_end_object: str,
    parent_hide_grp: str | None = None,
    include_stretch_nodes: bool = False,
):
    """Create distance dimension node and point constrain start and end locators
    between two objects.  Useful for finding joint length for stretching.

    Args:
        name: Name string without "_<type>" suffix using nLol naming convention.
            So "<name>_<direction>_<id>" instead of "<name>_<direction>_<id>_<type>".
        ruler_start_object: First object to contraint ruler to.
        ruler_end_object: Second object to constrain ruler to.
        parent_hide_grp: Group to parent and hide ruler transform and locators under.
        include_stretch_nodes: Create stretch node setup with blendColor 0.0-1.0 on/off toggle.
            Requires stretch attribute outside this function to be input to
            "<blendColors>.blender". And the output would be "<blendColors>.outputR",
            a mult ratio, 1 being no change and 2 being 2x stretch, etc.
            In addition, global scale input would be the global scale multiplyDivide node,
            input1X. The top ctrl parent switch groups scaleX often works for this connection.
            stretch toggle input = <blendColors>.blender
            stretch output to joints = <blendColors>.outputR
            global scale input = <globalscale_multiplyDivide>.input1X

    Returns:
        Ruler shape, transform, locators, locator constraints, and blendColors stretch node.

    """
    name = name.removesuffix("_")
    name_component = name.split("_")[0]

    # create ruler tool and get shape of distanceDimension node
    ruler_shape = cmds.distanceDimension(startPoint=(0, 0, 0), endPoint=(0, 0, 10))
    ruler_shape = cmds.rename(ruler_shape, f"{name}_distanceDimensionShape")

    # get transform of distanceDimesion node
    ruler_transform = cmds.listRelatives(ruler_shape, allParents=True, type="transform")
    ruler_transform = cmds.rename(
        ruler_transform,
        f"{name}_distanceDimension",
    )

    # get distanceDimension locators
    ruler_locators = cmds.listConnections(ruler_shape, type="locator")

    ruler_loc_01_name = name.replace(name_component, f"{name_component}Start")
    ruler_loc_01 = cmds.rename(ruler_locators[0], f"{ruler_loc_01_name}_loc")
    ruler_loc_02_name = name.replace(name_component, f"{name_component}End")
    ruler_loc_02 = cmds.rename(ruler_locators[1], f"{ruler_loc_02_name}_loc")

    # constrain ruler locators to measure between two objects
    ruler_loc_01_const = point_constr(ruler_start_object, ruler_loc_01)
    ruler_loc_02_const = point_constr(ruler_end_object, ruler_loc_02)

    if parent_hide_grp:
        for obj in (ruler_transform, ruler_loc_01, ruler_loc_02):
            cmds.parent(obj, parent_hide_grp)
            cmds.setAttr(f"{obj}.visibility", 0)

    # create stretch node setup
    blendcolors_nd = None
    global_scale_nd = None
    if include_stretch_nodes:
        multiplydivide_nd = cmds.createNode("multiplyDivide")
        cmds.setAttr(f"{multiplydivide_nd}.operation", 2)  # divide
        blendcolors_nd = cmds.createNode("blendColors")
        ruler_distance = cmds.getAttr(f"{ruler_shape}.distance")
        cmds.connectAttr(f"{ruler_shape}.distance", f"{multiplydivide_nd}.input1X")
        #cmds.setAttr(f"{multiplydivide_nd}.input2X", ruler_distance)
        cmds.connectAttr(f"{multiplydivide_nd}.outputX", f"{blendcolors_nd}.color1R")
        cmds.setAttr(f"{blendcolors_nd}.color2R", 1.0)
        # global scale
        global_scale_nd = cmds.createNode("multiplyDivide")
        cmds.setAttr(f"{global_scale_nd}.input1X", 1.0)
        cmds.setAttr(f"{global_scale_nd}.input2X", ruler_distance)
        cmds.connectAttr(f"{global_scale_nd}.outputX", f"{multiplydivide_nd}.input2X")

        stretch_nd_name = name.replace(name_component, f"{name_component}Stretch")
        multiplydivide_nd = cmds.rename(multiplydivide_nd, f"{stretch_nd_name}_multiplyDivide")
        blendcolors_nd = cmds.rename(blendcolors_nd, f"{stretch_nd_name}_blendColors")
        global_scale_nd_name = name.replace(name_component, f"{name_component}StretchGlobalScale")
        global_scale_nd = cmds.rename(global_scale_nd, f"{global_scale_nd_name}_multiplyDivide")

    return (
        ruler_shape,
        ruler_transform,
        ruler_loc_01,
        ruler_loc_02,
        ruler_loc_01_const,
        ruler_loc_02_const,
        blendcolors_nd,
        global_scale_nd
    )
