"""mirror_attrs_export_import.py

Save mirror attributes for control curve transforms.
Used for animation mirroring.
Rig build will automatically load "mirror_attributes.json" from rig folder.
"""

import json
from pathlib import Path

from maya import cmds
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

default_filepath = rig_folder_path.rig_folderpath / "mirror_attributes.json"


class MirrorAttrsExportImport:
    def __init__(self, save_filepath: Path | None = None):
        if not save_filepath:
            save_filepath = default_filepath
        self.save_filepath = save_filepath

        self.logger = get_logger()

    def get_mirror_attrs(self, ctrls: str | list | None = None) -> None:
        """Get selected ctrls mirror attribute values.

        Args:
            ctrls: Rig ctrls to mirror attribute data for.

        """
        if not ctrls:
            ctrls = cmds.ls(selection=True)
            if not ctrls:
                msg = "Nothing selected!"
                self.logger.error(msg)
                raise ValueError(msg)

        if not isinstance(ctrls, (list, tuple)):
            ctrls = [ctrls]

        ctrls_mirror_attrs = {}
        for ctrl in ctrls:
            ctrls_mirror_attrs[ctrl] = {}
            for attr_prefix in ["mirrorTranslate", "mirrorRotate"]:
                for axis in "XYZ":
                    attr = f"{attr_prefix}{axis}"
                    value = cmds.getAttr(f"{ctrl}.{attr}")
                    ctrls_mirror_attrs[ctrl][attr] = value

        self.save_mirror_attrs(ctrls_mirror_attrs)

    def save_mirror_attrs(self, data):
        """Save mirror attribute data to json file.

        Args:
            data: Mirror attribute data to save.

        """
        with open(self.save_filepath, "w") as f:
            json.dump(data, f, indent=4)
        self.logger.info(f"File saved to...  {self.save_filepath}")

    def load_mirror_attrs(self) -> dict:
        """Load mirror attribute data json file.

        Returns:
            Mirror attribute dictionary from json file.

        """
        with open(self.save_filepath) as f:
            data = json.load(f)
        self.logger.debug(f"File read from...  {self.save_filepath}")
        return data

    def apply_mirror_attrs(self) -> None:
        """Load in and apply mirror attribute data from json. No selection needed."""
        if not self.save_filepath.is_file():
            msg = (
                '"mirror_attributes.json" not in rig folder. Skipping mirror attributes setup.\n'
                f'File not found: "{self.save_filepath}".'
            )
            self.logger.info(msg)
            return

        ctrls_mirror_attrs = self.load_mirror_attrs()

        for ctrl in ctrls_mirror_attrs:
            for attr, value in ctrls_mirror_attrs[ctrl].items():
                try:
                    cmds.setAttr(f"{ctrl}.{attr}", value)
                except Exception:
                    self.logger.info(f'"{ctrl}.{attr}" failed to set!')

    def show_mirror_attrs(self, ctrls: str | list | None = None, show_attrs: bool = True) -> None:
        """Show mirror attributes in channel box.

        Args:
            ctrls: Ctrl object/s to show or hide mirror attrs for.
            show_attrs: Bool for whether to show or hide mirror attrs.

        """
        if ctrls is None:
            ctrls = cmds.ls(selection=True)

        if not isinstance(ctrls, (list, tuple)):
            ctrls = [ctrls]

        for ctrl in ctrls:
            for attr_prefix in ["mirrorTranslate", "mirrorRotate"]:
                for axis in "XYZ":
                    attr = f"{attr_prefix}{axis}"
                    try:
                        cmds.setAttr(f"{ctrl}.{attr}", channelBox=show_attrs)
                    except Exception:
                        self.logger.info(f"Failed to show/ hide: {ctrl}.{attr}")
