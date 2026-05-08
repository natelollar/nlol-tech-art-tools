import shutil
from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

reload(rig_folder_path)
rig_folderpath = rig_folder_path.rig_folderpath
logger = get_logger()


def copy_3d_paint_iff() -> None:
    """Copy iff texture from 3d Paint Tool to xgen folder for mask backup."""
    logger.info("\n")
    logger.info(f"rig_folderpath = {rig_folderpath!s}")

    # get 3d paint tool iff folder path
    # get custom xgen folder path
    maya_project_dir = cmds.workspace(query=True, rootDirectory=True)
    paint_dir = cmds.workspace(fileRuleEntry="3dPaintTextures")
    scene_name = (
        cmds.file(query=True, sceneName=True, shortName=True).replace(".ma", "").replace(".mb", "")
    )
    character_dir = Path(rig_folderpath).parents[1]
    collections_dir = character_dir / "xgen" / "collections"
    logger.info(f"character_dir = {character_dir!s}")
    logger.info(f"paint_dir = {paint_dir}")
    logger.info(f"scene_name = {scene_name}")
    logger.info(f"collections_dir = {collections_dir}")

    # get all iff files in the maya project paint folder
    iff_dir = Path(maya_project_dir) / paint_dir / scene_name
    logger.info(f"iff_dir = {iff_dir}")
    if not iff_dir.exists():
        logger.warning(f"{iff_dir = }")
        return
    iff_filepaths = list(iff_dir.glob("*.iff"))
    logger.info(f"Found {len(iff_filepaths)} IFF files")
    logger.info("\n")

    # find matching collection/description folders for iff mask files
    # copy to folder
    for iff_filepath in iff_filepaths:
        iff_filename = iff_filepath.name
        iff_filename_stem = iff_filepath.stem
        logger.info(f"iff_filename = {iff_filename}")

        matching_dir = None  # description folder matching iff file
        for collection_dir in collections_dir.iterdir():
            # search collection folders  matching iff filename
            if not collection_dir.is_dir() or collection_dir.name not in iff_filename_stem:
                continue
            # search description folders matching iff filename
            for desc_dir in collection_dir.iterdir():
                if not desc_dir.is_dir() or desc_dir.name not in iff_filename_stem:
                    continue

                # get mask type for folder
                mask_type = iff_filename_stem.split(f"{desc_dir.name}_")[-1]
                final_dir = desc_dir / "paintmaps" / mask_type
                logger.info(f"final_dir = {final_dir}")

                if final_dir.exists():
                    matching_dir = final_dir
                    break

        if not matching_dir:
            logger.warning(f"No matching xgen folder found for:\n{iff_filepath}")
            continue

        filepath_dest = matching_dir / iff_filepath.name
        shutil.copy2(iff_filepath, filepath_dest)
        logger.info(f"Copied... \n{iff_filepath} ->->->->-> \n{filepath_dest}")


def bake_ptex(
    mesh: str = "",
    paintmaps_folderpath: str | Path = "",
    image_filepath: str | Path = "",
    texels_per_unit: int = 10,
) -> None:
    """Bake xgen map to ptex."""
    tmp_file_nd = cmds.shadingNode(
        "file",
        name="ptexTmpBake_file",
        asTexture=True,
        isColorManaged=True,
    )

    cmds.setAttr(f"{tmp_file_nd}.fileTextureName", image_filepath, type="string")

    cmds.ptexBake(
        inMesh=mesh,  # "bodyHairShell_lowGeo". mesh with xgen
        # "${DESC}/paintmaps/uv_test" or "$bear_description/paintmaps/uv_test"
        outPtex=paintmaps_folderpath,
        bakeTexture=tmp_file_nd,  # maya file node with texture to convert
        tpu=texels_per_unit,
    )

    cmds.delete(tmp_file_nd)

    # Example:
    # cmds.ptexBake(
    # inMesh="bodyHairShell_lowGeo",
    # outPtex="${DESC}/paintmaps/uv_test",
    # bakeTexture="bodyHairShell_lowGeo_1",
    # tpu=10)