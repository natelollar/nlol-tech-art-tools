import re
import tomllib
from pathlib import Path

from maya import cmds
from nlol import defaults
from nlol.core.general_utils import swap_side_str
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

RIG_DATA_LOCATION = rig_folder_path.rig_folderpath
RIG_RETARGET_LOCATION = RIG_DATA_LOCATION / "retarget_data.toml"
DEFAULT_LOCATION = default_folderpath = Path(defaults.__file__).parent
DEFAULT_RETARGET_LOCATION = DEFAULT_LOCATION / "retarget_data.toml"

logger = get_logger()


class RetargetAnimation:
    """Retarget keyframe animation data from one set of character ctrls to another.
    Import toml data to connect equivalent ctrls. Then keyframe target ctrls
    on same keyframes as source ctrls. Optionally, keep same tangent weights/angles.
    See "nlol/defaults/readme_retarget_data.md" for more details.
    """

    def __init__(self, retarget_data_filepath: str | Path | None = None) -> None:
        """Initialize class.

        Args:
            retarget_data_filepath: Filepath to "retarget_data.toml".

        """
        self.retarget_data_filepath = (
            retarget_data_filepath or RIG_RETARGET_LOCATION or DEFAULT_RETARGET_LOCATION
        )

        self.read_retarget_data()
        self.mirror_retarget_data()

    def apply_ctrl_connections(self) -> None:
        """Use source target ctrl data from toml file and apply constraints
        accordingly. Connections to later be used for animation retargeting.
        """
        for data in self.retarget_data:
            source_ctrls = data["source_ctrls"].split(",")
            source_ctrls = [txt.strip() for txt in source_ctrls if txt.strip()]
            if self.source_namespace:
                source_ctrls = [f"{self.source_namespace}:{txt}" for txt in source_ctrls]
            target_ctrls = data["target_ctrls"].split(",")
            target_ctrls = [txt.strip() for txt in target_ctrls if txt.strip()]
            if self.target_namespace:
                target_ctrls = [f"{self.target_namespace}:{txt}" for txt in target_ctrls]

            connection_type = data.get("connection_type", "parent")
            offset = data.get("offset", True)
            scale_constraint = data.get("scale_constraint", True)
            scale_source_ctrl = data.get("scale_source_ctrl", "")
            if self.source_namespace and scale_source_ctrl:
                scale_source_ctrl = f"{self.source_namespace}:{scale_source_ctrl}"

            target_translate = data.get("target_translate", "0, 0, 0").split(",")
            target_translate = [int(txt.strip()) for txt in target_translate if txt.strip()]
            target_rotate = data.get("target_rotate", "0, 0, 0").split(",")
            target_rotate = [int(txt.strip()) for txt in target_rotate if txt.strip()]

            for ctrl in target_ctrls:  # bind target ctrls to source ctrl
                if not target_translate == [0, 0, 0]:
                    cmds.setAttr(f"{ctrl}.translate", *target_translate)
                if not target_rotate == [0, 0, 0]:
                    cmds.setAttr(f"{ctrl}.rotate", *target_rotate)

                translate_locked = cmds.getAttr(f"{ctrl}.translateX", lock=True)
                rotate_locked = cmds.getAttr(f"{ctrl}.rotateX", lock=True)
                scale_locked = cmds.getAttr(f"{ctrl}.scaleX", lock=True)

                for source_ctrl in source_ctrls:  # if blending target ctrl between multiple
                    match connection_type.lower():
                        case "parent":
                            if translate_locked:
                                self.orient_constr(source_ctrl, ctrl, offset)
                            elif rotate_locked:
                                self.point_constr(source_ctrl, ctrl, offset)
                            else:
                                self.parent_constr(source_ctrl, ctrl, offset)
                        case "point":
                            self.point_constr(source_ctrl, ctrl, offset)
                        case "orient":
                            self.orient_constr(source_ctrl, ctrl, offset)
                        case "pointorient":
                            self.point_constr(source_ctrl, ctrl, offset)
                            self.orient_constr(source_ctrl, ctrl, offset)
                        case _:
                            logger.warning(f"Unknown connection_type: {connection_type}")

                    if scale_constraint:
                        scale_source_ctrl = scale_source_ctrl or source_ctrl
                        if not scale_locked:
                            self.scale_constr(scale_source_ctrl, ctrl, offset)

    def parent_constr(self, source_ctrl: str, target_ctrl: str, offset: bool) -> None:
        """Apply custom parent constraint.

        Args:
            source_ctrl: Driver ctrl.
            target_ctrl: Driven ctrl.
            offset: Maintain offset.

        """
        cmds.parentConstraint(
            source_ctrl,
            target_ctrl,
            name=f"{target_ctrl}RetargetParentConstraint",
            weight=1.0,
            maintainOffset=offset,
        )

    def point_constr(self, source_ctrl: str, target_ctrl: str, offset: bool) -> None:
        """Apply custom point constraint.

        Args:
            Same as parent_constr().

        """
        cmds.pointConstraint(
            source_ctrl,
            target_ctrl,
            name=f"{target_ctrl}RetargetPointConstraint",
            weight=1.0,
            maintainOffset=offset,
        )

    def orient_constr(self, source_ctrl: str, target_ctrl: str, offset: bool) -> None:
        """Apply custom orient constraint.

        Args:
            Same as parent_constr().

        """
        cmds.orientConstraint(
            source_ctrl,
            target_ctrl,
            name=f"{target_ctrl}RetargetOrientConstraint",
            weight=1.0,
            maintainOffset=offset,
        )

    def scale_constr(self, source_ctrl: str, target_ctrl: str, offset: bool) -> None:
        """Apply custom scale constraint.

        Args:
            Same as parent_constr().

        """
        cmds.scaleConstraint(
            source_ctrl,
            target_ctrl,
            name=f"{target_ctrl}RetargetScaleConstraint",
            weight=1.0,
            maintainOffset=offset,
        )

    def delete_ctrl_connections(self) -> None:
        """Delete all scene constraints containing the "Retarget...Constraint" substring."""
        parent_constraints = cmds.ls(type="parentConstraint")
        point_constraints = cmds.ls(type="pointConstraint")
        orient_constraints = cmds.ls(type="orientConstraint")
        scale_constraints = cmds.ls(type="scaleConstraint")

        constraints = (
            parent_constraints + point_constraints + orient_constraints + scale_constraints
        )

        retarget_constraints = [cn for cn in constraints if re.search(r"Retarget\w+Constraint", cn)]

        cmds.delete(retarget_constraints)

    def read_retarget_data(self) -> None:
        """Import retarget data from toml. Defaults to "retarget_data.toml" in nLol rig folder
        or defaults folder.
        """
        with open(self.retarget_data_filepath, "rb") as f:
            retarget_data_file = tomllib.load(f)
            self.source_namespace = retarget_data_file.get("source_namespace", "")
            self.source_namespace = re.sub(r":+", r"", self.source_namespace)
            self.target_namespace = retarget_data_file.get("target_namespace", "")
            self.target_namespace = re.sub(r":+", r"", self.target_namespace)
            self.tangent_weights_angles = retarget_data_file.get("tangent_weights_angles", False)
            self.key_translate_rotate_all = retarget_data_file.get(
                "key_translate_rotate_all",
                False,
            )
            self.retarget_data = retarget_data_file["source_target_data"]

    def mirror_retarget_data(self) -> None:
        """Mirror retarget data that has the mirror parameter."""
        mirrored_inputs = []
        for data in self.retarget_data:
            mirror = data.get("mirror", False)
            if mirror:
                source_ctrls = swap_side_str(data["source_ctrls"])
                target_ctrls = swap_side_str(data["target_ctrls"])
                scale_source_ctrl = swap_side_str(data.get("scale_source_ctrl", ""))

                mirrored_input = data.copy()
                mirrored_input["source_ctrls"] = source_ctrls
                mirrored_input["target_ctrls"] = target_ctrls
                mirrored_input["scale_source_ctrl"] = scale_source_ctrl

                mirrored_inputs.append(mirrored_input)
        self.retarget_data.extend(mirrored_inputs)

    def copy_keyframes(self) -> None:
        """Keyframe the target ctrls on same frames as source ctrls.
        Transfer in/out tangent types; auto, linear, stepped, etc.
        Optionally, transfer tangent angles/weights too.
        """
        for data in self.retarget_data:
            source_ctrls = data["source_ctrls"].split(",")
            source_ctrls = [txt.strip() for txt in source_ctrls if txt.strip()]
            if self.source_namespace:
                source_ctrls = [f"{self.source_namespace}:{txt}" for txt in source_ctrls]
            source_ctrl = source_ctrls[0]  # only use first for keyframe/tangent data, etc
            target_ctrls = data["target_ctrls"].split(",")
            target_ctrls = [txt.strip() for txt in target_ctrls if txt.strip()]
            if self.target_namespace:
                target_ctrls = [f"{self.target_namespace}:{txt}" for txt in target_ctrls]

            key_times = cmds.keyframe(source_ctrl, query=True, timeChange=True) or []
            key_times = sorted(set(key_times))
            logger.debug(f"{key_times = }")

            maintain_attrs_trans_rot = {
                "translateX",
                "translateY",
                "translateZ",
                "rotateX",
                "rotateY",
                "rotateZ",
            }
            maintain_attrs_scale = {
                "scaleX",
                "scaleY",
                "scaleZ",
            }
            maintain_attrs = maintain_attrs_trans_rot | maintain_attrs_scale

            for ctrl in target_ctrls:
                frame_data = {}
                for frame in key_times:
                    keyed_attrs = cmds.keyframe(
                        source_ctrl,
                        time=(frame, frame),
                        query=True,
                        name=True,
                    )
                    keyed_attrs = [
                        cmds.listConnections(attr, plugs=True)[0].split(".")[-1]
                        for attr in keyed_attrs
                    ]
                    if self.key_translate_rotate_all:  # add translate rotate
                        keyed_attrs = list(set(keyed_attrs) | maintain_attrs_trans_rot)

                    for keyed_attr in keyed_attrs:
                        if keyed_attr in maintain_attrs:
                            keyed_value = cmds.getAttr(f"{ctrl}.{keyed_attr}", time=frame)
                        else:
                            try:
                                keyed_value = cmds.getAttr(
                                    f"{source_ctrl}.{keyed_attr}",
                                    time=frame,
                                )
                            except Exception as e:
                                msg = f"getAttr failed: {frame}; {source_ctrl}.{keyed_attr}\n{e}"
                                logger.debug(msg)
                                continue

                        keyed_intangenttype = (
                            cmds.keyTangent(
                                f"{source_ctrl}.{keyed_attr}",
                                time=(frame, frame),
                                query=True,
                                inTangentType=True,
                            )
                            or [None]
                        )[0]
                        keyed_outtangenttype = (
                            cmds.keyTangent(
                                f"{source_ctrl}.{keyed_attr}",
                                time=(frame, frame),
                                query=True,
                                outTangentType=True,
                            )
                            or [None]
                        )[0]
                        weighted_tangents = (
                            cmds.keyTangent(
                                source_ctrl,
                                attribute=keyed_attr,
                                query=True,
                                weightedTangents=True,
                            )
                            or [None]
                        )[0]
                        keyed_locked = (
                            cmds.keyTangent(
                                f"{source_ctrl}.{keyed_attr}",
                                time=(frame, frame),
                                query=True,
                                lock=True,
                            )
                            or [None]
                        )[0]

                        keyed_inweight = (
                            cmds.keyTangent(
                                f"{source_ctrl}.{keyed_attr}",
                                time=(frame, frame),
                                query=True,
                                inWeight=True,
                            )
                            or [None]
                        )[0]
                        keyed_outweight = (
                            cmds.keyTangent(
                                f"{source_ctrl}.{keyed_attr}",
                                time=(frame, frame),
                                query=True,
                                outWeight=True,
                            )
                            or [None]
                        )[0]
                        keyed_inangle = (
                            cmds.keyTangent(
                                f"{source_ctrl}.{keyed_attr}",
                                time=(frame, frame),
                                query=True,
                                inAngle=True,
                            )
                            or [None]
                        )[0]
                        keyed_outangle = (
                            cmds.keyTangent(
                                f"{source_ctrl}.{keyed_attr}",
                                time=(frame, frame),
                                query=True,
                                outAngle=True,
                            )
                            or [None]
                        )[0]

                        frame_data.setdefault(frame, {})
                        frame_data[frame].setdefault(keyed_attr, {})
                        frame_data[frame][keyed_attr]["keyed_value"] = keyed_value

                        frame_data[frame][keyed_attr]["keyed_intangenttype"] = keyed_intangenttype
                        frame_data[frame][keyed_attr]["keyed_outtangenttype"] = keyed_outtangenttype
                        frame_data[frame][keyed_attr]["weighted_tangents"] = weighted_tangents
                        frame_data[frame][keyed_attr]["keyed_locked"] = keyed_locked

                        frame_data[frame][keyed_attr]["keyed_inweight"] = keyed_inweight
                        frame_data[frame][keyed_attr]["keyed_outweight"] = keyed_outweight
                        frame_data[frame][keyed_attr]["keyed_inangle"] = keyed_inangle
                        frame_data[frame][keyed_attr]["keyed_outangle"] = keyed_outangle

                        logger.debug(f"{frame = }")
                        logger.debug(f"{keyed_attr = }")
                        logger.debug(f"{keyed_intangenttype = }")
                        logger.debug(f"{keyed_outtangenttype = }")

                for frame, keyed_attrs in frame_data.items():
                    for keyed_attr, keyed_attr_data in keyed_attrs.items():
                        try:
                            # set keyframe
                            cmds.setKeyframe(
                                f"{ctrl}.{keyed_attr}",
                                time=frame,
                                value=keyed_attr_data["keyed_value"],
                            )
                        except Exception as e:
                            msg = f"setKeyframe failed: {frame}; {ctrl}.{keyed_attr}\n{e}"
                            logger.debug(msg)

                        try:
                            # set tangent type preset.  auto, linear, stepped, etc
                            if (
                                keyed_attr_data["keyed_intangenttype"]
                                and keyed_attr_data["keyed_outtangenttype"]
                            ):
                                cmds.keyTangent(
                                    f"{ctrl}.{keyed_attr}",
                                    time=(frame, frame),
                                    inTangentType=keyed_attr_data["keyed_intangenttype"],
                                    outTangentType=keyed_attr_data["keyed_outtangenttype"],
                                )

                            if not self.tangent_weights_angles:
                                continue

                            # set tangent angles/weights
                            if (
                                keyed_attr_data["keyed_intangenttype"] == "fixed"
                                or keyed_attr_data["keyed_outtangenttype"] == "fixed"
                            ):
                                if keyed_attr_data["weighted_tangents"]:
                                    cmds.keyTangent(
                                        f"{ctrl}.{keyed_attr}",
                                        time=(frame, frame),
                                        weightedTangents=keyed_attr_data["weighted_tangents"],
                                    )  # weighted/non-weighted tangents
                                if keyed_attr_data["keyed_locked"]:
                                    cmds.keyTangent(
                                        f"{ctrl}.{keyed_attr}",
                                        time=(frame, frame),
                                        lock=keyed_attr_data["keyed_locked"],
                                    )  # unify/break tangents
                                if (
                                    keyed_attr_data["keyed_inweight"]
                                    and keyed_attr_data["keyed_outweight"]
                                ):
                                    cmds.keyTangent(
                                        f"{ctrl}.{keyed_attr}",
                                        time=(frame, frame),
                                        inWeight=keyed_attr_data["keyed_inweight"],
                                        outWeight=keyed_attr_data["keyed_outweight"],
                                    )
                                if (
                                    keyed_attr_data["keyed_inangle"]
                                    and keyed_attr_data["keyed_outangle"]
                                ):
                                    cmds.keyTangent(
                                        f"{ctrl}.{keyed_attr}",
                                        time=(frame, frame),
                                        inAngle=keyed_attr_data["keyed_inangle"],
                                        outAngle=keyed_attr_data["keyed_outangle"],
                                    )
                        except Exception as e:
                            msg = f"keyTangent failed: {frame}; {ctrl}.{keyed_attr}\n{e}"
                            logger.debug(msg)
