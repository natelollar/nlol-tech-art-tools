from maya import cmds, mel

current_rig = "body_original_low"
current_delete_objects = ["rig_allGrp"]


def remove_nlol_rig(skinned_mesh: str | None = None, delete_objects: tuple | None = None) -> None:
    """Delete current nLol rig in scene, but leave the skeletal mesh.  Reset bind pose.

    Args:
        skinned_mesh: Character mesh in scene to reset bind pose for.
        delete_objects: Extra rig objects to delete.

    """
    cmds.undoInfo(openChunk=True)
    try:
        if not skinned_mesh:
            skinned_mesh = current_rig
        if not delete_objects:
            delete_objects = current_delete_objects

        # ---------- delete rig objects ----------
        all_parentConstraint = cmds.ls(type="parentConstraint")
        all_scaleConstraint = cmds.ls(type="scaleConstraint")
        all_ikEffector = cmds.ls(type="ikEffector")
        all_blendColors = cmds.ls(type="blendColors")
        all_locators = cmds.ls(type="locator")
        all_locators = [cmds.listRelatives(loc, parent=True)[0] for loc in all_locators]
        rig_helper_nodes = cmds.ls("*rig_helpers*")

        cmds.select(cl=True)
        cmds.select(
            all_parentConstraint,
            all_scaleConstraint,
            all_ikEffector,
            all_blendColors,
            all_locators,
            rig_helper_nodes,
            add=True,
        )
        cmds.delete()

        for obj in delete_objects:
            if cmds.objExists(obj):
                cmds.delete(obj)

        # ---------- delete unused nodes ----------
        mel.eval("MLdeleteUnused;")

        # ---------- reset bind pose ----------
        # query joints scale compensate
        skinned_jnts = cmds.skinCluster(skinned_mesh, query=True, influence=True)
        scale_compensate_attr_query = []
        for jnt in skinned_jnts:
            scale_compensate_attr = cmds.getAttr(f"{jnt}.segmentScaleCompensate")
            scale_compensate_attr_query.append(scale_compensate_attr)

        cmds.dagPose(skinned_mesh, restore=True, g=True, bindPose=True)

        # set scale compensate to value from before restore bind pose
        for attr_query, jnt in zip(scale_compensate_attr_query, skinned_jnts):
            cmds.setAttr(f"{jnt}.segmentScaleCompensate", attr_query)
    finally:
        cmds.undoInfo(closeChunk=True)
