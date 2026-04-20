from typing import Any

from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


class NlolMayaRegistry:
    """Custom registry class for nLol Tools in Maya. Record data in
    dictionary such as Maya object names. Used for calling data between
    classes, for example, fetching rig control names from previously
    built rig modules while the rig is building.
    """

    def __init__(self) -> None:
        """Initialize registry for tracking data in Maya for current session."""
        self.nlol_objs: dict[str, Any] = {}

    def register_obj(self, key: str, obj_name: Any) -> None:
        """Register a Maya object name under a given key."""
        self.nlol_objs[key] = obj_name

    def get_obj(self, key: str) -> Any:
        """Retrieve Maya object name by key."""
        return self.nlol_objs.get(key)

    def clear_registry(self) -> None:
        """Clear all data from registry."""
        self.nlol_objs.clear()
        logger.info("Registry cleared...")


_registry_instance = None


def get_registry() -> NlolMayaRegistry:
    """Returns:
    Registry instance.
    """
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = NlolMayaRegistry()
    return _registry_instance
