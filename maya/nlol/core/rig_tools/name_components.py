from maya import cmds
from nlol.core.rig_setup.rig_variables import SIDE_DIRECTIONS
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


class NlolNameComponents:
    """Utilities for nLol name components.
    The nLol name components are used for naming Maya objects in a consistent manner
    for the nLol Maya toolset.
    nLol naming convention: "<base_name>_<side_direction>_<obj_id>_<obj_type>"
    In simpler terms: "<name>_<direction>_<id>_<type>"
    These are camelCase name components. Not all components are required.
    At least <name> and <type> are required.
    """

    def find_name_comps(self, object: str) -> tuple[str]:
        """Find nlol name components of Maya object.

        Args:
            object: A single Maya object.

        Returns:
            Set of name components in order.

        """
        obj_split = object.split("_")
        number_comps = len(obj_split)
        base_name = obj_split[0]
        obj_type = obj_split[-1]
        side_direction = ""
        obj_id = ""

        if number_comps >= 3:
            # side_contains_digit = bool(re.search(r"\d+", obj_split[1]))
            directions = SIDE_DIRECTIONS
            side_contains_direction = any(txt for txt in directions if txt in obj_split[1].lower())

        if number_comps == 4:
            if side_contains_direction:
                side_direction = obj_split[1]
                obj_id = obj_split[-2]
            else:
                side_direction = obj_split[-2]
                obj_id = obj_split[1]
        elif number_comps == 3:
            if side_contains_direction:
                side_direction = obj_split[1]
                obj_id = ""
            else:
                side_direction = ""
                obj_id = obj_split[1]

        elif number_comps > 4:
            msg = "Too many nLol name components for Maya object. (More than 4.)"
            logger.error(msg)
            raise ValueError(msg)
        else:
            pass

        return (base_name, side_direction, obj_id, obj_type)

    def print_name_comps(self, objects: list[str] | None = None) -> None:
        """Print selected name components to logger.

        Args:
            objects: A list of Maya objects.

        """
        selected = cmds.ls(selection=True)
        if not objects:
            objects = selected

        if not isinstance(objects, (list, tuple)):
            objects = [objects]

        for object in objects:
            base_name, side_direction, obj_id, obj_type = self.find_name_comps(object)
            logger.info(f"{base_name = }")
            logger.info(f"{side_direction = }")
            logger.info(f"{obj_id = }")
            logger.info(f"{obj_type = }")

    def join_nm_comps(
        self,
        base_name: str,
        side_direction: str = "",
        obj_id: str = "",
        obj_type: str = "",
    ) -> None:
        """Join separated nLol name components with underscores. All name components required,
        but side_direction and obj_id can have empty strings as inputs.

        Args:
             base_name, side_direction, obj_id, obj_type: nLol name components.

        Returns:
            Full object name with nLol naming convention.

        """
        if not base_name:
            msg = "base_name cannot be empty."
            logger.error(msg)
            raise ValueError(msg)
        if not obj_type:
            msg = "obj_type cannot be empty."
            logger.error(msg)
            raise ValueError(msg)

        full_name = "_".join(txt for txt in [base_name, side_direction, obj_id, obj_type] if txt)

        return full_name
