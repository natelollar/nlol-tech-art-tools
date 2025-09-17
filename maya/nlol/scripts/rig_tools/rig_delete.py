from maya import cmds, mel
from nlol.utilities.nlol_maya_logger import get_logger


def remove_nlol_rig(
    rig_group_string: str = "_rigGrp",
    skeletalmesh_group_string: str = "_skeletalMeshGrp",
) -> None:
    """Delete current nLol rig in scene, but leave the skeletal mesh.  Reset bind pose.

    Args:
        skinned_mesh: Character mesh in scene to reset bind pose for.
        delete_objects: Extra rig objects to delete.
        rig_group_string: Either main rig group name or
            string within main rig group identifying it.
        rig_group_string: Either main skeletal mesh group name or
            string within main skeletal mesh group identifying it.

    """
    logger = get_logger()

    cmds.undoInfo(openChunk=True)
    try:
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

        # ---------- delete top rig group/s ----------
        top_nodes = cmds.ls(assemblies=True)
        top_rig_groups = [node for node in top_nodes if rig_group_string in node]
        for grp in top_rig_groups:
            if cmds.objExists(grp):
                cmds.delete(grp)

        # ---------- delete unused nodes ----------
        mel.eval("MLdeleteUnused;")

        # ---------- reset bind poses ----------
        # for meshes in skeletal mesh group/s
        skeletalmesh_groups = [node for node in top_nodes if skeletalmesh_group_string in node]
        for grp in skeletalmesh_groups:
            grp_children = cmds.listRelatives(grp, allDescendents=True)
            mesh_shapes = cmds.listRelatives(grp_children, shapes=True, type="mesh")
            meshes = cmds.listRelatives(mesh_shapes, parent=True)
            meshes = list(set(meshes))  # remove duplicates

            for mesh in meshes:
                logger.debug(f"mesh: {mesh}")
                try:
                    # query joints scale compensate
                    skinned_jnts = cmds.skinCluster(mesh, query=True, influence=True)
                    logger.debug(f"skinned_jnts: {skinned_jnts}")
                    scale_compensate_attr_query = []
                    for jnt in skinned_jnts:
                        scale_compensate_attr = cmds.getAttr(f"{jnt}.segmentScaleCompensate")
                        scale_compensate_attr_query.append(scale_compensate_attr)

                    # ----- reset bind pose -----
                    mesh_history = cmds.listHistory(mesh)
                    skincluster = cmds.ls(mesh_history, type="skinCluster")
                    if skincluster:
                        dag_pose_nodes = cmds.listConnections(
                            f"{skincluster[0]}.bindPose",
                            type="dagPose",
                        )
                        cmds.dagPose(dag_pose_nodes, restore=True, g=True)
                    else:
                        logger.warning(f'Likely "{mesh}" not skinned, skipping reset bindpose.')

                    # set scale compensate to value from before restore bind pose
                    for attr_query, jnt in zip(
                        scale_compensate_attr_query,
                        skinned_jnts,
                        strict=False,
                    ):
                        cmds.setAttr(f"{jnt}.segmentScaleCompensate", attr_query)

                except Exception:
                    raise

    finally:
        cmds.undoInfo(closeChunk=True)
