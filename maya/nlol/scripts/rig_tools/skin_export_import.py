import xml.etree.ElementTree as ET
from importlib import reload

from maya import cmds, mel
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_folder_path)

skinweights_folderpath = rig_folder_path.rig_folderpath / "skin_weights"
logger = get_logger()


def export_skin_weights():
    """Export index values of multiple skin clusters to xml."""
    mesh_selection = cmds.ls(selection=True)

    for mesh in mesh_selection:
        mesh_history = cmds.listHistory(mesh)
        skin_cluster = cmds.ls(mesh_history, type="skinCluster")[0]
        logger.info(f"mesh: {mesh}")
        logger.info(f"skin_cluster: {skin_cluster}")

        cmds.deformerWeights(
            f"{skin_cluster}.xml",
            export=True,
            deformer=skin_cluster,
            format="XML",
            path=skinweights_folderpath,
        )


def import_skin_weights(selected_only: bool = False):
    """Import xml skinCluster files from nLol rig folderpath and apply them.
    Mesh (shape) names and vertex order should be same as exported.
    No mesh selection required.
    Applies new skin cluster first, then applies skin weights index from xml file.

    Args:
        selected_only: Only import and apply skin for selected geometry.

    """
    if selected_only:
        my_sel = cmds.ls(selection=True)  # current selection
        selection = [obj for obj in my_sel if cmds.listRelatives(obj, shapes=True, type="mesh")]
        if not selection:
            logger.warning(f"Nothing selected for skin import: {my_sel}")
            return

    skincluster_filepaths = list(skinweights_folderpath.glob("*.xml"))
    if not list(skincluster_filepaths):
        error_msg = (
            f'No xml skin cluster filepaths in: "{skinweights_folderpath}" '
            'Use nLol "Export Skin Clusters" shelf button or "Deform < Export Weights...".'
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    for skincluster_filepath in skincluster_filepaths:
        logger.debug(f"skincluster_filepath: {skincluster_filepath}")
        # ---------- get skinCluster variables from xml ----------
        xml_tree = ET.parse(skincluster_filepath)
        xml_root = xml_tree.getroot()

        shape_element = xml_root.find("shape")
        mesh_shape = shape_element.get("name")
        logger.debug(f"mesh_shape: {mesh_shape}")

        weights_element = xml_root.find("weights")
        skincluster_name = weights_element.get("deformer")
        logger.debug(f"skincluster: {skincluster_name}")

        weights_elements = xml_root.findall("weights")
        bind_joints = [weights.get("source") for weights in weights_elements]
        logger.debug(f"bind_joints: {bind_joints}")

        # ---------- apply skin weights ----------
        # unbind old skin weights
        mesh = cmds.listRelatives(mesh_shape, parent=True)[0]
        if selected_only:
            if mesh not in selection:  # skip if not selected
                logger.debug(f"Skipping skin weights for: {mesh}")
                continue
        logger.debug(f"mesh: {mesh}")
        mesh_history = cmds.listHistory(mesh)
        old_skincluster = cmds.ls(mesh_history, type="skinCluster")
        logger.debug(f"old_skincluster: {old_skincluster}")
        if old_skincluster:
            cmds.select(mesh)
            # going to bindPose first is good, 
            # unless joints have been intentionally moved or reparented
            #mel.eval("gotoBindPose; DetachSkin;")
            mel.eval("DetachSkin;")
            cmds.select(clear=True)

        # ----- create new skin cluster -----
        new_skincluster = cmds.skinCluster(
            bind_joints,
            mesh,
            name=skincluster_name,
            toSelectedBones=True,
            obeyMaxInfluences=False,
            removeUnusedInfluence=False,
        )
        # skin all to single joint first, for clean slate to reapply weights
        cmds.skinPercent(
            new_skincluster[0],
            mesh,
            transformValue=(bind_joints[0], 1.0),
        )

        # ----- import and apply user pre-saved weights -----
        cmds.deformerWeights(
            skincluster_filepath.name,
            im=True,
            method="index",
            deformer=new_skincluster[0],
            path=skincluster_filepath.parent,
        )

        # apply normalize weights (default for "Import Weights...")
        cmds.skinCluster(new_skincluster, edit=True, forceNormalizeWeights=True)
