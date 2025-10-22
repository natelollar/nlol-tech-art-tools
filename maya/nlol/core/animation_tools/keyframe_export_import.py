"""keyframe_export_import.py

Select animation ctrls keyframe data.
"""

import json
from pathlib import Path

from nlol import defaults
from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

default_folderpath = Path(defaults.__file__).parent
save_filepath = default_folderpath / "other_control_keyframes.json"


class KeyframeExportImport:
    def __init__(self, save_filepath: Path = save_filepath):
        self.save_filepath = save_filepath

        self.logger = get_logger()

    def get_keyframe_data(
        self,
        objects: str | list | None = None,
        key_frame: int | None = None,
    ) -> None:
        """Get selected objects keyframe data for current frame.

        Args:
            objects: Object/s to get keyframe data for. Example; ctrl curves.
                Can be list of objects or single string name.
            key_frame: Frame in the timeline to get keyframe data for.

        """
        if not objects:
            objects = cmds.ls(selection=True)
            if not objects:
                msg = "Nothing selected!"
                self.logger.error(msg)
                raise ValueError(msg)
        if not key_frame:
            key_frame = cmds.currentTime(query=True)

        if not isinstance(objects, (list, tuple)):
            objects = [objects]

        objects_keyframe_data = {}
        for obj in objects:
            keyed_attrs = cmds.keyframe(
                obj,
                time=(key_frame, key_frame),
                query=True,
                name=True,
            )
            if not keyed_attrs:
                continue
            keyed_attrs = [attr.split("_")[-1] for attr in keyed_attrs]

            objects_keyframe_data[obj] = {}
            for attr in keyed_attrs:
                objects_keyframe_data[obj][attr] = cmds.getAttr(f"{obj}.{attr}")

        self.save_keyframe_data(objects_keyframe_data)

    def get_keyframe_data_all(
        self,
        objects: str | list | None = None,
        animation_range: tuple[int, int] | None = None,
    ) -> None:
        """Get selected objects keyframe data for all frames in animation range.

        Args:
            objects: Object/s to get keyframe data for. Example; ctrl curves.
                Can be list of objects or single string name.
            animation_range: Animation range or custom range to save keyframes for.

        """
        if not objects:
            objects = cmds.ls(selection=True)
            if not objects:
                msg = "Nothing selected!"
                self.logger.error(msg)
                raise ValueError(msg)
        if not animation_range:
            start_frame = cmds.playbackOptions(query=True, animationStartTime=True)
            end_frame = cmds.playbackOptions(query=True, animationEndTime=True)
        else:
            start_frame = animation_range[0]
            end_frame = animation_range[1]

        if not isinstance(objects, (list, tuple)):
            objects = [objects]

        objects_keyframe_data = {}
        for key_frame in range(int(start_frame), int(end_frame) + 1):
            cmds.currentTime(key_frame)
            objects_keyframe_data[key_frame] = {}
            for obj in objects:
                keyed_attrs = cmds.keyframe(
                    obj,
                    time=(key_frame, key_frame),
                    query=True,
                    name=True,
                )
                if not keyed_attrs:
                    continue
                keyed_attrs = [attr.split("_")[-1] for attr in keyed_attrs]

                objects_keyframe_data[key_frame][obj] = {}
                for attr in keyed_attrs:
                    objects_keyframe_data[key_frame][obj][attr] = cmds.getAttr(f"{obj}.{attr}")

        self.save_keyframe_data(objects_keyframe_data)

    def save_keyframe_data(self, data):
        """Save keyframe data to json file.

        Args:
            data: Keyframe data to save.

        """
        with open(self.save_filepath, "w") as f:
            json.dump(data, f, indent=4)
        self.logger.info(f"File saved to...  {self.save_filepath}")

    def load_keyframe_data(self):
        """Read keyframe data json file."""
        with open(self.save_filepath) as f:
            data = json.load(f)
        self.logger.info(f"File read from...  {self.save_filepath}")
        return data

    def apply_keyframe_data(self, set_key: bool = False) -> None:
        """Load in and apply keyframe data from json.
        Apply to saved objects for current frame.
        No selection needed.

        Args:
            Set_key: Set key for new values on current frame.

        """
        self.logger.info("Applying keyframe data to SAVED objects.")

        objects_keyframe_data = self.load_keyframe_data()

        for obj in objects_keyframe_data:
            for attr, value in objects_keyframe_data[obj].items():
                if not cmds.objExists(f"{obj}.{attr}"):
                    continue
                try:
                    cmds.setAttr(f"{obj}.{attr}", value)
                    if set_key:
                        cmds.setKeyframe(f"{obj}.{attr}")
                except Exception:
                    self.logger.info(f'"{obj}.{attr}" failed to set!')

    def apply_keyframe_data_to_selected(self, set_key: bool = False) -> None:
        """Load in and apply keyframe data from json.
        Apply to selected objects for current frame
        in the same order previous objects were selected when saved.

        Args:
            Set_key: Set key for new values on current frame.

        """
        self.logger.info("Applying keyframe data to SELECTED objects.")

        objects_keyframe_data = self.load_keyframe_data()
        selected = cmds.ls(selection=True)

        for key_obj, sel_obj in zip(objects_keyframe_data, selected, strict=False):
            for attr, value in objects_keyframe_data[key_obj].items():
                if not cmds.objExists(f"{sel_obj}.{attr}"):
                    continue
                try:
                    cmds.setAttr(f"{sel_obj}.{attr}", value)
                    if set_key:
                        cmds.setKeyframe(f"{sel_obj}.{attr}")
                except Exception:
                    self.logger.info(f'"{sel_obj}.{attr}" failed to set!')

    def apply_keyframe_data_all(self):
        """Load in and apply keyframe data from json.
        Apply to saved objects for all frames in saved animaiton range.
        """
        self.logger.info("Applying keyframe data to SAVED objects.")

        objects_keyframe_data = self.load_keyframe_data()

        for key_frame in objects_keyframe_data:
            cmds.currentTime(key_frame)
            for obj in objects_keyframe_data[key_frame]:
                for attr, value in objects_keyframe_data[key_frame][obj].items():
                    if not cmds.objExists(f"{obj}.{attr}"):
                        continue
                    try:
                        cmds.setAttr(f"{obj}.{attr}", value)
                        cmds.setKeyframe(f"{obj}.{attr}")
                    except Exception:
                        self.logger.info(f'"{obj}.{attr}" failed to set!')
