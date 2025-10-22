import tomllib
from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.core import general_utils
from nlol.core.rig_components import create_display_layers
from nlol.utilities.nlol_maya_logger import get_logger

reload(create_display_layers)

left_to_right_str = general_utils.left_to_right_str
objects_display_lyr = create_display_layers.objects_display_lyr


class BuildDisplayLayers:
    """Set up display layers for the rig."""

    def __init__(self, display_lyrs_filepath: str | Path):
        """Args:
        rig_ps_filepath: The "rig_display_layers.toml" file to import.
        """
        self.display_lyrs_filepath = display_lyrs_filepath

        self.logger = get_logger()

    def build(self):
        """Build process entry point for BuildDisplayLayers class.
        --------------------------------------------------
        Get data from "rig_display_layers.toml" first.  Then create display layers.
        """
        if not Path(self.display_lyrs_filepath).is_file():
            msg = (
                '"display_lyrs_filepath.toml" not in rig folder. Skipping display layers setup.\n'
                f'File not found: "{self.display_lyrs_filepath}".'
            )
            self.logger.info(msg)
            return

        # query rig display layer data
        with open(self.display_lyrs_filepath, "rb") as f:
            display_lyr_data = tomllib.load(f)["display_layer"]

        # ----- add right dicts -----
        right_display_lyrs = []
        for lyr_dict in display_lyr_data:
            mirror_right = lyr_dict.get("mirror_right")
            if mirror_right:
                objects = left_to_right_str(lyr_dict["objects"])
                base_name = left_to_right_str(lyr_dict.get("base_name", ""))
                display_layer = left_to_right_str(lyr_dict.get("display_layer", ""))

                right_dict = {
                    "objects": objects,
                    "base_name": base_name,
                    "display_layer": display_layer,
                    "reference": lyr_dict.get("reference"),
                    "hide": lyr_dict.get("hide"),
                }
                right_display_lyrs.append(right_dict)
        display_lyr_data.extend(right_display_lyrs)

        # ----- create new display layers -----
        for lyr_dict in display_lyr_data:
            objects = [  # string list to regular list.  exclude empty strings.
                stripped for txt in lyr_dict["objects"].split(",") if (stripped := txt.strip())
            ]
            base_name = lyr_dict.get("base_name", "")
            display_layer = lyr_dict.get("display_layer", "")
            reference = lyr_dict.get("reference")
            hide = lyr_dict.get("hide")

            objects_display_lyr(
                objects=objects,
                base_name=base_name,
                display_layer=display_layer,
                reference=reference,
                hide=hide,
            )

        # ----- sort all scene display layers -----
        # query scene display layers first
        scene_display_lyrs = [lyr for lyr in cmds.ls(type="displayLayer") if lyr != "defaultLayer"]
        scene_lyr_data_sorted = []
        for lyr in scene_display_lyrs:
            objects = cmds.editDisplayLayerMembers(lyr, query=True)

            reference = True if cmds.getAttr(f"{lyr}.displayType") == 2 else False
            hide = True if cmds.getAttr(f"{lyr}.visibility") == 0 else False

            scene_lyr_data_sorted.append(
                {
                    "objects": objects,
                    "display_layer": lyr,
                    "reference": reference,
                    "hide": hide,
                },
            )
            # delete scene display layer
            cmds.delete(lyr)
        # sorty layers alphabetically
        scene_lyr_data_sorted.sort(key=lambda lyr_dict: lyr_dict["display_layer"], reverse=True)

        # ----- recreate scene display layers -----
        for lyr_dict in scene_lyr_data_sorted:
            objects = lyr_dict["objects"]
            display_layer = lyr_dict["display_layer"]
            reference = lyr_dict.get("reference")
            hide = lyr_dict.get("hide")

            objects_display_lyr(
                objects=objects,
                display_layer=display_layer,
                reference=reference,
                hide=hide,
            )
