from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger


def set_camera_pivot_to_selected():
    """Set camera tumble pivot to selected object pivot without the camera jumping to object.
    For example, useful when rotating around a specific joint in a joint chain.
    Meant to work with tumble tool settings set to tumble pivot.
    Set these settings with "tumble_tool_settings" shelf button.
    """
    logger = get_logger()

    selection = cmds.ls(sl=True)[0]
    viewport = cmds.getPanel(withFocus=True)
    logger.debug(f"Viewport = {viewport}")

    if "modelPanel" in viewport:
        current_cam_query = cmds.modelEditor(viewport, query=True, activeView=True, camera=True)
        current_cam = current_cam_query.split("|")[-1]
        logger.debug(f"Current Camera: {current_cam}")

        if selection:
            # ----- tumble pibot -----
            sel_pivot_pos = cmds.xform(
                selection,
                query=True,
                worldSpace=True,
                rotatePivot=True,
            )  # get selected obejct rotate pivot world space position
            logger.debug(f"Current Camera Pivot Position: {sel_pivot_pos}")
            cmds.setAttr((f"{current_cam}.tumblePivot"), *sel_pivot_pos)

            # ------ center of interest--------#
            # get distance between camera and rotate pivot of object
            # to set center of interest distance
            cam_pos = cmds.xform(current_cam, query=True, worldSpace=True, translation=True)

            # ------ distance between 2 points in 3d space equation ------
            cam_x, cam_y, cam_z = cam_pos
            # xyz position of intersection
            obj_x, obj_y, obj_z = sel_pivot_pos

            # part of following equation.  seperated for readability
            equation_x = (obj_x - cam_x) ** 2  # squared
            equation_y = (obj_y - cam_y) ** 2
            equation_z = (obj_z - cam_z) ** 2

            # distance between two 3d points standard math equation
            dist_between = (equation_x + equation_y + equation_z) ** 0.5  # **0.5 is square root

            # set to absolute so distance is not negative
            dist_between_abs = abs(dist_between)
            logger.debug(f"Camera distance to object pivot: {dist_between_abs}")
            # set center of interest for current camera
            cmds.setAttr(f"{current_cam}.centerOfInterest", dist_between_abs)

            # -------------------------------#
            # ----- Set locator position ----#
            if cmds.objExists("cam_pivot_loc"):
                connected_cam = cmds.listConnections("cam_pivot_loc.translate")[0]
                logger.debug(f"Current camera connected to locator: {connected_cam}")

                same_cam = current_cam == connected_cam
                logger.debug(f"Same Camera: {same_cam}")

                if not same_cam:
                    cmds.connectAttr(
                        f"{current_cam}.tumblePivot",
                        "cam_pivot_loc.translate",
                        force=True,
                    )

                new_connected_cam = cmds.listConnections("cam_pivot_loc.translate")[0]
                logger.debug(f"New camera connected to locator: {new_connected_cam}")
            else:
                logger.debug('No "cam_pivot_loc" in scene.')
        else:
            logger.debug("Nothing selected for pivot.")
    else:
        logger.debug("Not in viewport.")
