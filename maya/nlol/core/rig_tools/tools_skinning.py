from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def select_skinned_joints() -> None:
    """Select joints skinned to selected object."""
    my_sel = cmds.ls(selection=True)
    skin_cluster_joints = cmds.skinCluster(my_sel[0], query=True, influence=True)
    cmds.select(skin_cluster_joints)
    logger.info(skin_cluster_joints)


def get_skin_clusters() -> None:
    """Get selected skin cluster name."""
    my_sel = cmds.ls(selection=True)
    history = cmds.listHistory(my_sel[0])
    skin_clusters = cmds.ls(history, type="skinCluster")
    logger.info(skin_clusters)


def duplicate_copy_skin_weights(object: str, name: str = "") -> str:
    """Duplicate object then copy skin weights.
    End up with new skin cluster on duplicated object.

    Args:
        object: Maya object to duplicate and copy skin weights from.
        name: Name of duplicated object.

    Returns:
        Name of duplicate object.

    """
    if not name:
        name = f"{object}1"
    duplicate_object = cmds.duplicate(object, name=name)[0]
    bind_copy_skin_weights(object, duplicate_object)

    return duplicate_object


def bind_copy_skin_weights(source: str, target: str) -> str:
    """Bind target with same joints as source.
    Then apply all skin to one joint to avoid interactive bind errors.
    Then apply copy skin weights from source to target.

    Args:
        source: Original Maya object with skinning. Example: Mesh or curve.
        target: Object to copy skin weights to.

    Returns:
        New target skin cluster name.

    """
    bind_joints = cmds.skinCluster(source, query=True, influence=True)
    source_history = cmds.listHistory(source)
    source_skincluster = cmds.ls(source_history, type="skinCluster")[0]
    # ----- create new skin cluster -----
    # cmds.select(clear=True)
    target_skincluster = cmds.skinCluster(
        bind_joints,
        target,
        name=f"{target}SkinCluster",
        toSelectedBones=True,
        obeyMaxInfluences=False,
        removeUnusedInfluence=False,
    )[0]
    # skin all to single joint first, for clean slate to reapply weights
    cmds.skinPercent(
        target_skincluster,
        target,
        transformValue=(bind_joints[0], 1.0),
    )

    cmds.copySkinWeights(
        sourceSkin=source_skincluster,
        destinationSkin=target_skincluster,
        noMirror=True,
        surfaceAssociation="closestPoint",
        influenceAssociation=["oneToOne", "name", "closestJoint"],
    )

    return target_skincluster
