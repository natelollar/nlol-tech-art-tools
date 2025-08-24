from maya import cmds
from nlol.scripts.rig_components.clean_constraints import point_constr


def create_attached_ruler(name: str, ruler_start_object: str, ruler_end_object: str):
    """Create distance dimension node and point constrain start and end locators
    between two objects.  Useful for finding joint length for stretching.

    Args:
        name: Ruler name.
        ruler_start_object: First object to contraint ruler to.
        ruler_end_object: Second object to constrain ruler to.

    Returns:
        Ruler shape, transform, locators, and locator constraints.

    """
    # create ruler tool and get shape of distanceDimension node
    ruler_shape = cmds.distanceDimension(startPoint=(0, 0, 0), endPoint=(0, 0, 10))
    ruler_shape = cmds.rename(ruler_shape, f"{name}distanceDimensionShape")
    # get transform of distanceDimesion node
    ruler_transform = cmds.listRelatives(ruler_shape, allParents=True, type="transform")
    ruler_transform = cmds.rename(ruler_transform, f"{name}distanceDimension")
    # get distanceDimension locators
    ruler_locators = cmds.listConnections(ruler_shape, type="locator")
    ruler_loc_01 = cmds.rename(ruler_locators[0], f"{name}01_loc")
    ruler_loc_02 = cmds.rename(ruler_locators[1], f"{name}02_loc")
    # constrain ruler locators to measure between two objects
    ruler_loc_01_const = point_constr(ruler_start_object, ruler_loc_01)
    ruler_loc_02_const = point_constr(ruler_end_object, ruler_loc_02)

    return (
        ruler_shape,
        ruler_transform,
        ruler_loc_01,
        ruler_loc_02,
        ruler_loc_01_const,
        ruler_loc_02_const,
    )
