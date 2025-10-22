import tomllib
from pathlib import Path

from maya import cmds
from nlol.defaults import rig_folder_path

rig_folderpath = rig_folder_path.rig_folderpath
default_rig_data_filepath = rig_folderpath / "rig_object_data.toml"


class CommonBuildFunctions:
    def __init__(self, rig_data_filepath: Path | None = None):
        """Initialize class for common shared rig methods.

        Args:
            rig_data_filepath: Main rig data file from rig folder.

        """
        if rig_data_filepath:
            self.rig_data_filepath = rig_data_filepath
        else:
            self.rig_data_filepath = default_rig_data_filepath

    def get_rig_data(self):
        """Get rig data from "rig_object_data.toml"."""
        with open(self.rig_data_filepath, "rb") as f:
            rig_object_data_file = tomllib.load(f)
            self.rig_name = rig_object_data_file.get("rig_name")

    def top_rig_grouping(self, objects: str | list | None = None):
        """Entry point.

        Args:
            objects: Maya objects to group under top grp.

        """
        self.get_rig_data()
        self.find_create_top_grp()
        if objects:
            cmds.parent(objects, self.main_rig_group)

    def find_create_top_grp(self):
        """Create main top group for rig components."""
        if self.rig_name:
            self.main_rig_group = f"{self.rig_name}_rigGrp"
        else:
            self.main_rig_group = "main_rigGrp"
        if not cmds.objExists(self.main_rig_group):
            self.main_rig_group = cmds.group(empty=True, name=self.main_rig_group)
