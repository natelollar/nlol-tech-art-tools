import json
from pathlib import Path

from maya import cmds
from nlol import defaults
from nlol.defaults.rig_folder_path import rig_folderpath
from nlol.utilities.nlol_maya_logger import get_logger


class MirrorAttrsExportImport:
    """Export and import mirror attributes for animation.
    Also, add mirror attributes to generic objects.

    Mainly for saving/loading mirror attributes for ctrl curves, later used for animation mirroring.
    Rig build will automatically load "mirror_attributes.json" from rig folder.
    """

    def __init__(self, save_filepath: Path | None = None, use_generic_filepath: bool = False):
        """Initialize class.

        Args:
            save_filepath: Rig filepath for specific character.
            use_generic_filepath: Generic nlol defaults filepath.
                Example: "nlol/core/defaults/other_mirror_attributes.json"

        """
        rig_filepath = rig_folderpath() / "mirror_attributes.json"

        defaults_folderpath = Path(defaults.__file__).parent
        generic_filepath = defaults_folderpath / "other_mirror_attributes.json"

        if not save_filepath:
            if use_generic_filepath:
                save_filepath = generic_filepath
            else:
                save_filepath = rig_filepath

        self.save_filepath = save_filepath

        self.logger = get_logger()

    def get_save_mirror_attrs(self, ctrls: str | list | None = None) -> None:
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
                    if cmds.objExists(f"{ctrl}.{attr}"):
                        value = cmds.getAttr(f"{ctrl}.{attr}")
                        ctrls_mirror_attrs[ctrl][attr] = value

        self.save_mirror_attrs(ctrls_mirror_attrs)

    def save_mirror_attrs(self, data) -> None:
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
        self.logger.info(f"File read from...  {self.save_filepath}")
        return data

    def apply_mirror_attrs(self) -> None:
        """Load in and apply mirror attribute data from json. No selection needed."""
        if not self.save_filepath.is_file():
            msg = '"mirror_attributes.json" not in rig folder. Skipping mirror attrs setup...\n'
            self.logger.info(msg)
            msg = f'File not found: "{self.save_filepath}".'
            self.logger.debug(msg)
            return

        ctrls_mirror_attrs = self.load_mirror_attrs()

        for ctrl in ctrls_mirror_attrs:
            for attr, value in ctrls_mirror_attrs[ctrl].items():
                try:
                    cmds.setAttr(f"{ctrl}.{attr}", value)
                except Exception:
                    self.logger.debug(f'"{ctrl}.{attr}" failed to set!')

    def show_hide_mirror_attrs(
        self,
        ctrls: str | list | None = None,
        show_attrs: bool = True,
    ) -> None:
        """Show or hide mirror attributes in channel box.

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

    def add_mirror_attrs(self, show_attrs: bool = True) -> None:
        """Add mirror attributes to selected objects. Example: ".mirrorTranslateX"

        Args:
            show_attrs: Show added mirror attributes in channel box.

        """
        selected = cmds.ls(selection=True)

        for obj in selected:
            for attr_prefix in ["mirrorTranslate", "mirrorRotate"]:
                for axis in "XYZ":
                    attr = f"{attr_prefix}{axis}"
                    if not cmds.objExists(f"{obj}.{attr}"):
                        cmds.addAttr(
                            obj,
                            longName=f"{attr}",
                            attributeType="long",
                            defaultValue=0,
                            minValue=-1,
                            maxValue=1,
                        )
                    try:
                        cmds.setAttr(f"{obj}.{attr}", channelBox=show_attrs)
                    except Exception:
                        self.logger.info(f"Failed to show/ hide: {obj}.{attr}")

    def remove_mirror_attrs(self, ctrls: str | list | None = None) -> None:
        """Remove mirror attributes from selected (or given) objects.

        Args:
            ctrls: Ctrl object/s to remove mirror attrs from.
                Defaults to selection.

        """
        if ctrls is None:
            ctrls = cmds.ls(selection=True)
        if not isinstance(ctrls, (list, tuple)):
            ctrls = [ctrls]
        for ctrl in ctrls:
            for attr_prefix in ["mirrorTranslate", "mirrorRotate"]:
                for axis in "XYZ":
                    attr = f"{attr_prefix}{axis}"
                    if cmds.attributeQuery(attr, node=ctrl, exists=True):
                        try:
                            cmds.deleteAttr(f"{ctrl}.{attr}")
                        except Exception:
                            self.logger.info(f"Failed to remove: {ctrl}.{attr}")

    def paste_first_mirror_attrs_to_selected(self) -> None:
        """Paste the first saved ctrl's mirror attributes onto all selected ctrls.

        Save can still store many ctrls. Paste uses only the first one.
        """
        if not self.save_filepath.is_file():
            cmds.warning(f"File not found: {self.save_filepath}")
            return

        with open(self.save_filepath, encoding="utf-8") as f:
            data = json.load(f)

        if not data:
            cmds.warning(f"No mirror attributes in: {self.save_filepath}")
            return

        selected = cmds.ls(selection=True)
        if not selected:
            cmds.warning("Nothing selected! Select controls to paste onto.")
            return

        saved_name = next(iter(data))
        saved_attrs = data[saved_name]
        if not saved_attrs:
            cmds.warning(f'"{saved_name}" has no mirror attributes to paste.')
            return

        for obj in selected:
            for attr, value in saved_attrs.items():
                try:
                    cmds.setAttr(f"{obj}.{attr}", value)
                except Exception as e:
                    self.logger.debug(f"Failed to set {obj}.{attr}: {e}")

        self.logger.info(
            f"Pasted mirror attributes from {saved_name} onto: {', '.join(selected)}",
        )
