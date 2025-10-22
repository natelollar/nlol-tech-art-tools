from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def objects_display_lyr(
    objects: str | list[str],
    base_name: str | None = None,
    display_layer: str | None = None,
    reference: bool = False,
    hide: bool = False,
    name_only: bool = False,
) -> str:
    """Add objects to Maya display layer.
    Uses first objects name for display_layer name, with "Lyr" suffix.
    Or use either base_name or display_layer string, but not both.

    Args:
        objects: Maya objects. String, string list or regular list of objects.
        base_name: camelCase name component for the layer. Do not include "_lyr".
            nLol rig naming convention. "<name>_<type>".
            Example would be a rig_module_name string from "rig_object_data.toml".
        display_layer: Full display layer name.  Used instead of base_name arg.
        reference: Reference the display layer by default.
        hide: Hide the display layer by default.
        name_only: Get display layer name only.  Don't create layer.
            Maybe useful if need to sort alphabetically before creating.

    Returns:
        Display layer name string.

    """
    if not isinstance(objects, list):
        objects = [  # single string or string list to regular list
            stripped for txt in objects.split(",") if (stripped := txt.strip())
        ]

    if base_name and display_layer:
        msg = (
            "Cannot use both base_name and display_layer for name string. "
            f'base_name: "{base_name}", display_layer: "{display_layer}")'
        )
        logger.error(msg)
        raise ValueError(msg)

    if not display_layer:
        if base_name:
            display_layer = f"{base_name}_lyr"
        else:
            display_layer = f"{objects[0]}Lyr"

    if not name_only:
        if not cmds.objExists(display_layer):
            cmds.select(clear=True)  # clear selection to be safe
            cmds.createDisplayLayer(name=display_layer, empty=True)

        objects = [obj for obj in objects if obj]  # remove empty strings
        if objects:
            cmds.editDisplayLayerMembers(display_layer, objects, noRecurse=True)

        if reference:
            cmds.setAttr(f"{display_layer}.displayType", 2)
        if hide:
            cmds.setAttr(f"{display_layer}.visibility", 0)

    return display_layer
