import os
import shutil
from pathlib import Path

from maya import cmds


def copy_if_newer(src: str | os.PathLike, dst: str | os.PathLike) -> None:
    """Copy function for shutil.copytree().

    Args:
        src: Copy source filepath
        dst: Copy destination filepath.

    """
    src, dst = Path(src), Path(dst)
    if not dst.exists():
        shutil.copy2(src, dst)
    else:
        src_stat = src.stat()
        dst_stat = dst.stat()
        if src_stat.st_mtime > dst_stat.st_mtime or src_stat.st_size != dst_stat.st_size:
            shutil.copy2(src, dst)


def move_megascans_scene_folders(library_folderpath: Path | str | None = None) -> None:
    """Copy scene Megascans asset folders to new location.
    Queries file nodes for folder paths.
    Currently setup for "Megascans Library/Downloaded/3d/" folders and
    "Megascans Library/Downloaded/surface/" and
    "Megascans Library/Downloaded/3dplant/../../Atlas" folders.

    Args:
        library_folderpath: Megascans library folderpath to copy asset too.
            From one library folder location to another.

    """
    file_nds = cmds.ls(type="file")

    folders_to_copy = set()
    for file_nd in file_nds:
        file_nd_filepath = Path(cmds.getAttr(f"{file_nd}.fileTextureName"))
        asset_folderpath = file_nd_filepath.parent
        folderpath_name = asset_folderpath.name
        if folderpath_name.lower() == "atlas":
            copy_folderpath = file_nd_filepath.parents[2]
            copy_parent_folderpath = copy_folderpath.parent
        else:
            copy_folderpath = file_nd_filepath.parent
            copy_parent_folderpath = copy_folderpath.parent

        print("\n")
        print(f"{file_nd_filepath = !s}")
        print(f"{copy_folderpath = !s}")
        print(f"{copy_parent_folderpath = !s}")

        if library_folderpath:
            new_copy_location = None
            if copy_parent_folderpath.name in {
                "3d",
                "3dplant",
                "surface",
            } and "Megascans Library" in str(copy_parent_folderpath):
                new_copy_location = (
                    Path(library_folderpath)
                    / "Downloaded"
                    / copy_parent_folderpath.name
                    / copy_folderpath.name
                )
                print(f"{new_copy_location = !s}")

                folders_to_copy.add((copy_folderpath, new_copy_location))

    if not library_folderpath:
        print('\nRequires "Megascans Library" folder path to copy files.')
        return

    for copy_folderpath, new_copy_location in folders_to_copy:
        print(f"\nCopying...\nSource: {copy_folderpath}\nDestination: {new_copy_location}")
        shutil.copytree(
            copy_folderpath,
            new_copy_location,
            dirs_exist_ok=True,
            copy_function=copy_if_newer,
        )

    print("\nFinished.")


if __name__ == "__main__":
    move_megascans_scene_folders()  # Run in Maya to query Megascans files to copy.
    # Example:
    # move_megascans_scene_folders(
    #     "c:/project_data/libraries/Megascans Library/",
    # )
