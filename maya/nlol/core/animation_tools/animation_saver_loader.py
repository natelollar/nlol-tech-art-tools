import json
import re
from pathlib import Path

from maya import cmds
from nlol import defaults
from nlol.utilities.nlol_maya_logger import get_logger

DEFAULT_LOCATION = Path(defaults.__file__).parent
SAVE_LOCATION = DEFAULT_LOCATION / "other_animation_data.json"

logger = get_logger()


class AnimationSaverLoader:
    """Save and load animation data from selected."""

    def __init__(self, save_filepath: Path | None = None) -> None:
        self.save_filepath = save_filepath or SAVE_LOCATION

    def get_animation_data(
        self,
        objects: str | list | None = None,
        remove_namespace: bool | None = None,
    ) -> None:
        """Get selected objects animation data for all frames with keyed attributes.

        Args:
            objects: Object/s to get keyframe data for. Example; ctrl curves.
                Can be list of objects or single string name.

        """
        objects = objects or cmds.ls(selection=True)
        if not isinstance(objects, (list, tuple)):
            objects = [objects]
        if not objects:
            msg = "Nothing selected!"
            logger.error(msg)
            raise ValueError(msg)

        frame_data = {}
        for obj in objects:
            try:
                key_times = cmds.keyframe(obj, query=True, timeChange=True) or []
                key_times = sorted(set(key_times))
                logger.debug(f"{obj = }")
                logger.debug(f"{key_times = }")
            except Exception as e:
                msg = f"keyframe query failed: {obj}\n{e}"
                logger.info(msg)
                continue

            for frame in key_times:
                keyed_attrs = cmds.keyframe(
                    obj,
                    time=(frame, frame),
                    query=True,
                    name=True,
                )
                keyed_attrs = [
                    cmds.listConnections(attr, plugs=True)[0].split(".")[-1] for attr in keyed_attrs
                ]

                for keyed_attr in keyed_attrs:
                    try:
                        keyed_value = cmds.getAttr(f"{obj}.{keyed_attr}", time=frame)
                    except Exception as e:
                        msg = f"getAttr failed: {frame}; {obj}.{keyed_attr}\n{e}"
                        logger.debug(msg)
                        continue

                    keyed_intangenttype = cmds.keyTangent(
                        f"{obj}.{keyed_attr}",
                        time=(frame, frame),
                        query=True,
                        inTangentType=True,
                    )[0]
                    keyed_outtangenttype = cmds.keyTangent(
                        f"{obj}.{keyed_attr}",
                        time=(frame, frame),
                        query=True,
                        outTangentType=True,
                    )[0]
                    weighted_tangents = cmds.keyTangent(
                        obj,
                        attribute=keyed_attr,
                        query=True,
                        weightedTangents=True,
                    )[0]
                    keyed_locked = cmds.keyTangent(
                        f"{obj}.{keyed_attr}",
                        time=(frame, frame),
                        query=True,
                        lock=True,
                    )[0]

                    keyed_inweight = cmds.keyTangent(
                        f"{obj}.{keyed_attr}",
                        time=(frame, frame),
                        query=True,
                        inWeight=True,
                    )[0]
                    keyed_outweight = cmds.keyTangent(
                        f"{obj}.{keyed_attr}",
                        time=(frame, frame),
                        query=True,
                        outWeight=True,
                    )[0]
                    keyed_inangle = cmds.keyTangent(
                        f"{obj}.{keyed_attr}",
                        time=(frame, frame),
                        query=True,
                        inAngle=True,
                    )[0]
                    keyed_outangle = cmds.keyTangent(
                        f"{obj}.{keyed_attr}",
                        time=(frame, frame),
                        query=True,
                        outAngle=True,
                    )[0]

                    obj_ns = obj
                    if remove_namespace:
                        obj_ns = obj.split(":")[-1]
                    frame_data.setdefault(obj_ns, {})
                    frame_data[obj_ns].setdefault(frame, {})
                    frame_data[obj_ns][frame].setdefault(keyed_attr, {})
                    frame_data[obj_ns][frame][keyed_attr]["keyed_value"] = keyed_value
                    frame_data[obj_ns][frame][keyed_attr]["keyed_intangenttype"] = (
                        keyed_intangenttype
                    )
                    frame_data[obj_ns][frame][keyed_attr]["keyed_outtangenttype"] = (
                        keyed_outtangenttype
                    )
                    frame_data[obj_ns][frame][keyed_attr]["weighted_tangents"] = weighted_tangents
                    frame_data[obj_ns][frame][keyed_attr]["keyed_locked"] = keyed_locked

                    frame_data[obj_ns][frame][keyed_attr]["keyed_inweight"] = keyed_inweight
                    frame_data[obj_ns][frame][keyed_attr]["keyed_outweight"] = keyed_outweight
                    frame_data[obj_ns][frame][keyed_attr]["keyed_inangle"] = keyed_inangle
                    frame_data[obj_ns][frame][keyed_attr]["keyed_outangle"] = keyed_outangle

        self.save_animation_data(frame_data)

    def save_animation_data(self, data) -> None:
        """Save animation data to json file.

        Args:
            data: Keyframe/tangent data to save.

        """
        with open(self.save_filepath, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"File saved to...  {self.save_filepath}")

    def load_animation_data(self) -> None:
        """Read animation data json file."""
        with open(self.save_filepath) as f:
            data = json.load(f)
        logger.info(f"File read from...  {self.save_filepath}")
        return data

    def apply_animation_data(self, namespace: str = ""):
        """Load in and apply animation data from json
        to saved objects.
        """
        logger.info("Applying keyframe data to SAVED objects.")

        frame_data = self.load_animation_data()

        for obj, frames in frame_data.items():
            if namespace:
                namespace = re.sub(r":+$", r"", namespace)
                obj = obj.split(":")[-1]
                obj = f"{namespace}:{obj}"

            for frame, keyed_attrs in frames.items():
                for keyed_attr, keyed_attr_data in keyed_attrs.items():
                    try:
                        cmds.setKeyframe(
                            f"{obj}.{keyed_attr}",
                            time=frame,
                            value=keyed_attr_data["keyed_value"],
                        )
                    except Exception as e:
                        msg = f"setKeyframe failed: {frame}; {obj}.{keyed_attr}\n{e}"
                        logger.info(msg)

                    try:
                        # set tangent type preset.  auto, linear, stepped, etc
                        cmds.keyTangent(
                            f"{obj}.{keyed_attr}",
                            time=(frame, frame),
                            inTangentType=keyed_attr_data["keyed_intangenttype"],
                            outTangentType=keyed_attr_data["keyed_outtangenttype"],
                        )

                        # set tangent angles/weights
                        if (
                            keyed_attr_data["keyed_intangenttype"] == "fixed"
                            or keyed_attr_data["keyed_outtangenttype"] == "fixed"
                        ):
                            cmds.keyTangent(
                                f"{obj}.{keyed_attr}",
                                time=(frame, frame),
                                weightedTangents=keyed_attr_data["weighted_tangents"],
                            )  # weighted/non-weighted tangents
                            cmds.keyTangent(
                                f"{obj}.{keyed_attr}",
                                time=(frame, frame),
                                lock=keyed_attr_data["keyed_locked"],
                            )  # unify/break tangents
                            cmds.keyTangent(
                                f"{obj}.{keyed_attr}",
                                time=(frame, frame),
                                inWeight=keyed_attr_data["keyed_inweight"],
                                outWeight=keyed_attr_data["keyed_outweight"],
                            )
                            cmds.keyTangent(
                                f"{obj}.{keyed_attr}",
                                time=(frame, frame),
                                inAngle=keyed_attr_data["keyed_inangle"],
                                outAngle=keyed_attr_data["keyed_outangle"],
                            )
                    except Exception as e:
                        msg = f"keyTangent failed: {frame}; {obj}.{keyed_attr}\n{e}"
                        logger.debug(msg)
