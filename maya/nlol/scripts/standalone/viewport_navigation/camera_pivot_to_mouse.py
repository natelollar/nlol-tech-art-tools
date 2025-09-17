"""Set perspective camera Tumble pivot, no mouse click needed.
Sets point upon hotkey click.
Select the raycast intersection with mesh shape thats closest to camera.
Set to prefered hotkey, maybe 'alt + f'.
"""

from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget
from shiboken6 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger


def viewport_mouse_position() -> tuple[int, int]:
    """Get viewport mouse 2D XY position.
    Finds mouse position in 2d space without using "cmds.draggerContext".

    Returns:
        Viewport window X and Y mouse position.

    """
    # get active viewport
    active_view = omui.M3dView.active3dView()
    # get cursor position
    global_pos = QCursor.pos()
    view_widget = wrapInstance(int(active_view.widget()), QWidget)
    # get cursor x y screenspace position
    mouse_pos = view_widget.mapFromGlobal(global_pos)
    flipped_y = view_widget.height() - mouse_pos.y()  # Y is fipped, up is down and down is up.
    flipped_y = flipped_y - 1  # flip causes it to be one off compared to cmds.draggerContext

    return mouse_pos.x(), flipped_y


def pivot_to_mouse():
    """Set camera tumble pivot to first mesh shape intersection in front of mouse raycast
    for current camera in current Maya viewport.
    Meant to work with tumble tool settings set to tumble pivot.
    Set these settings with "tumble_tool_settings" shelf button.
    """
    logger = get_logger()

    vp_x, vp_y = viewport_mouse_position()

    position = om.MPoint()
    direction = om.MVector()
    hitpoint = om.MFloatPoint()

    active_view = omui.M3dView.active3dView()
    active_view.viewToWorld(int(vp_x), int(vp_y), position, direction)

    # get viewport panel to query correct isolate selected set
    # and later, get current camera
    viewport = cmds.getPanel(withFocus=True)

    # -------- get shapes in 'isolate selected' set --------
    isolated_shapes = []
    if cmds.isolateSelect(viewport, query=True, state=True):
        view_set = cmds.isolateSelect(viewport, query=True, viewObjects=True)
        if view_set:
            isolated_objs = cmds.sets(view_set, query=True, nodesOnly=True) or []
            isolated_objs = cmds.ls(isolated_objs, transforms=True, allPaths=True) or []
            logger.debug(f"----- isolated_objs: {isolated_objs} -----")
            # get shapes via transorm hierarchy
            for transform in isolated_objs:
                transform_hierarchy = cmds.listRelatives(
                    transform,
                    allDescendents=True,
                    type="transform",
                    fullPath=True,
                ) or []
                transform_hierarchy.extend([transform])
                # for each transform in hierarchy find mesh shapes
                # avoids shape instances outside of transforms
                for trans in transform_hierarchy:
                    trans_shp = (
                        cmds.listRelatives(
                            trans,
                            type="mesh",
                            shapes=True,
                            fullPath=True,
                            allDescendents=True,
                        )
                        or []
                    )
                    isolated_shapes.extend(trans_shp)
    logger.debug(f"----- isolated_shapes: {isolated_shapes} -----")

    # --------- get mesh shapes for raycast intersection ---------
    # only visible shapes. and use allPaths to avoid mesh instance name conflicts
    # ignore skinned intermediate meshes by checking if ends with 'Orig'
    intersect_mesh_shps = cmds.ls(type="mesh", visible=True, allPaths=True)
    intersect_mesh_shps = [shp for shp in intersect_mesh_shps if not shp.endswith("Orig")]
    logger.debug(f"----- intersect_mesh_shps: {intersect_mesh_shps} -----")

    # filter out objects not in isolate selected set
    if isolated_shapes:
        # search for intersect shape allPath in isolated shape fullPath
        intersect_mesh_shps = [
            shp
            for shp in intersect_mesh_shps
            if any(shp in iso_shp for iso_shp in isolated_shapes)
        ]
        logger.debug(f"----- intersect_mesh_shps: {intersect_mesh_shps} -----")

    # -------------- find intersections --------------
    intersections = []
    intersection_meshes = []
    for obj in intersect_mesh_shps:
        selections = om.MSelectionList()
        selections.add(obj)
        dagPath = om.MDagPath()
        selections.getDagPath(0, dagPath)

        fnMesh = om.MFnMesh(dagPath)
        intersection = fnMesh.closestIntersection(
            om.MFloatPoint(position),
            om.MFloatVector(direction),
            None,
            None,
            False,
            om.MSpace.kWorld,
            99999,
            False,
            None,
            hitpoint,
            None,
            None,
            None,
            None,
            None,
        )

        if intersection:
            x, y, z = hitpoint.x, hitpoint.y, hitpoint.z
            intersections.append([x, y, z])
            intersection_meshes.append(obj)

    # ----------------------------------------
    if intersections:
        # use current camera
        current_cam_query = cmds.modelEditor(viewport, query=True, activeView=True, camera=True)
        current_cam = current_cam_query.split("|")[-1]
        cam_position = cmds.xform(current_cam, query=True, worldSpace=True, translation=True)

        # find distance to camera of each position
        distances_to_shapes = []
        for inter in intersections:
            # xyz pos of camera
            x1 = cam_position[0]
            y1 = cam_position[1]
            z1 = cam_position[2]
            # xyz position of intersection
            x2 = inter[0]
            y2 = inter[1]
            z2 = inter[2]

            # part of following equation.  seperated for readability
            equation_x = (x2 - x1) ** 2  # squared
            equation_y = (y2 - y1) ** 2
            equation_z = (z2 - z1) ** 2

            # distance between two 3d points standard math equation
            dist_between = (equation_x + equation_y + equation_z) ** 0.5  # **0.5 is square root

            # mouse raycast generates multiple intersections
            # if there are multiple meshes in mouse line of site
            # add the distances between camera and intersection to list
            distances_to_shapes.append(
                abs(dist_between),
            )  # set to absolute so distance is not negative

        # get closest intersecting distance (smallest distance between cam and intersection)
        closest_inters_dist = min(distances_to_shapes)
        # get list index of closest distance
        closest_inters_index = distances_to_shapes.index(min(distances_to_shapes))
        # apply that index to original intersection position list
        closest_inters_pos = intersections[closest_inters_index]

        # set camera tumble pivot to closest intersection point
        cmds.setAttr(f"{current_cam}.tumblePivot", *closest_inters_pos)
        # set center of interest for current camera (affects zooming in and out)
        cmds.setAttr(f"{current_cam}.centerOfInterest", closest_inters_dist)

        # ----------------------------------------
        # set locator position to current camera tumble pivot
        if cmds.objExists("cam_pivot_loc"):
            connected_cam = cmds.listConnections("cam_pivot_loc.translate")[0]
            if not current_cam == connected_cam:
                cmds.connectAttr(
                    f"{current_cam}.tumblePivot",
                    "cam_pivot_loc.translate",
                    force=True,
                )
        else:
            logger.debug("No 'cam_pivot_loc' in scene.")

        # get intersected mesh for debugging
        closest_inters_mesh = intersection_meshes[closest_inters_index]
        logger.debug(
            f'---------- Intersected with "{closest_inters_mesh}": {closest_inters_pos} ----------',
        )
