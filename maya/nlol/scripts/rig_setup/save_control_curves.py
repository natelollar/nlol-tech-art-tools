"""Save control curve shape attributes.
Select curves and save.
Saves to "maya/nlol/defaults/".
Execute to load in. No selection needed.
"""

import ast
import json
from pathlib import Path

from nlol import defaults
from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

rig_folderpath = rig_folder_path.rig_folderpath
rig_ctrl_crvs_filepath = rig_folderpath / "rig_control_curves.json"

default_folderpath = Path(defaults.__file__).parent
generic_filepath = default_folderpath / "other_control_curves.json"


class SaveControlCurves:
    """Select curves and use write_curve_attributes() to save out curve shape attributes to json.
    Use apply_curve_attributes() to load back in curve attributes via json. No selection required.
    Saves out curve shape wire color, line width, and cv shape.
    Works with regular cv curves and circles.
    """

    def __init__(
        self,
        filepath: str | Path = rig_ctrl_crvs_filepath,
        use_generic_filepath: bool = False,
    ):
        if use_generic_filepath:
            self.filepath = generic_filepath
        else:
            self.filepath = filepath

        self.logger = get_logger()

    def get_curve_attributes(self):
        """Get curve shape attributes. Query control curves from current selection.
        Use ".wireColorRGB" as main color attribute. Also, allows wire color index.
        """
        selection = cmds.ls(selection=True)

        curve_attributes = {}
        for curve in selection:
            curve_shapes = cmds.listRelatives(curve, shapes=True)

            for shape in curve_shapes:
                if cmds.objectType(shape) == "nurbsCurve":
                    use_object_color = cmds.getAttr(f"{shape}.useObjectColor")
                    object_color = cmds.getAttr(f"{shape}.objectColor")
                    wire_color_rgb = cmds.getAttr(f"{shape}.wireColorRGB")[0]
                    line_width = cmds.getAttr(f"{shape}.lineWidth")

                    curve_degree = cmds.getAttr(f"{shape}.degree")
                    curve_spans = cmds.getAttr(f"{shape}.spans")
                    curve_form = cmds.getAttr(f"{shape}.form")

                    cv_positions = cmds.getAttr(f"{shape}.cv[*]")

                    curve_attributes[shape] = {
                        "curve": curve,
                        "useObjectColor": use_object_color,
                        "objectColor": object_color,
                        "wireColorRGB": str(wire_color_rgb),
                        "lineWidth": line_width,
                        "curve_degree": curve_degree,
                        "curve_spans": curve_spans,
                        "curve_form": curve_form,
                        "cv_positions": str(cv_positions),
                    }

        return curve_attributes

    def write_curve_attributes(self):
        """Write curve shape attributes to json file."""
        curve_attributes = self.get_curve_attributes()
        if not curve_attributes:
            self.logger.warning("No curves selected to save.")
            return
        with open(self.filepath, "w") as f:
            json.dump(curve_attributes, f, indent=4)
            self.logger.info(f'Control shapes saved: "{self.filepath}"')

    def read_curve_attributes(self):
        """Read curve shape attributes from json file."""
        with open(self.filepath) as f:
            curve_attributes = json.load(f)
            self.logger.debug(f'Control shapes read: "{self.filepath}"')
            return curve_attributes

    def apply_curve_attributes(self):
        """Iterate through curve shape attribute data in json file. Apply data to control curves.
        Replace current control or create new ones if curve shape transforms don't exist.
        """
        old_curve_shapes = []
        curves = []
        for shape, attr_list in self.read_curve_attributes().items():
            curve = attr_list["curve"]

            old_curve_shapes.append(shape)  # use to delete leftover shapes from previous version
            curves.append(curve)

            # query curve attributes from json file
            # convert string back to regular data with ast.literal_eval()
            use_object_color = attr_list["useObjectColor"]
            object_color = attr_list["objectColor"]
            wire_color_rgb = ast.literal_eval(attr_list["wireColorRGB"])
            line_width = attr_list["lineWidth"]

            curve_degree = attr_list["curve_degree"]
            curve_spans = attr_list["curve_spans"]
            curve_form = attr_list["curve_form"]
            cv_positions = ast.literal_eval(attr_list["cv_positions"])

            if cmds.objExists(curve):
                transform_node = curve
            else:
                transform_node = cmds.group(em=True, name=curve)
            # empty shape so transform group acts as a 'shape transform' and not a 'group'.
            cmds.createNode("nurbsCurve", name=f"{shape}_empty_shape", parent=transform_node)

            # delete and replace old shapes incase shape has entirely changed
            if cmds.objExists(shape):
                cmds.delete(shape)

            # create new curve shapes
            # account for different forms of curve shapes including circles
            # generally this is a regular control curve drawn out with cv curve tool
            if curve_form == 0 or curve_form == 1:
                new_curve_transform = cmds.curve(point=cv_positions, degree=curve_degree)
                new_curve_shape = cmds.listRelatives(new_curve_transform, shapes=True)
            # generally this is a blocky circle with straight sharp edges
            # like a regular curve but starts out as a closed shape
            # can be built with cmds.circle(degree=1)
            # delete history off circles or will not work
            if curve_form == 2 and curve_degree == 1:  # closed curve and degree is linear
                # last cv position to first to form a closed curve
                last_element = cv_positions.pop()

                cv_positions.insert(0, last_element)
                new_curve_transform = cmds.curve(point=cv_positions, degree=curve_degree)
                new_curve_shape = cmds.listRelatives(new_curve_transform, shapes=True)
            # generally a regular smooth circle
            # closed periodic curve shape and degree is cubic (smooth)
            if curve_form == 2 and curve_degree != 1:
                new_curve_transform = cmds.circle(
                    sections=curve_spans,
                    degree=curve_degree,
                    constructionHistory=False,
                )  # spans should be same as sections
                new_curve_shape = cmds.listRelatives(new_curve_transform, shapes=True)[0]
                # cmds.curve() does not work with smooth circle
                for i, pos in enumerate(cv_positions):
                    cv_identifier = f"{new_curve_shape}.cv[{i}]"
                    cmds.xform(cv_identifier, translation=pos)

            # parent curve shape to control transform node
            cmds.parent(new_curve_shape, transform_node, relative=True, shape=True)
            cmds.rename(new_curve_shape, shape)
            cmds.delete(new_curve_transform)

            # ----- color and width attrs -----
            if cmds.objExists(shape):
                cmds.setAttr(f"{shape}.useObjectColor", use_object_color)
                cmds.setAttr(f"{shape}.objectColor", object_color)
                cmds.setAttr(f"{shape}.wireColorRGB", *wire_color_rgb)
                cmds.setAttr(f"{shape}.lineWidth", line_width)
            else:
                self.logger.warning(f"{shape}: Shape does not exist. Cannot apply color.")

        # remove empty shape and shapes not saved out in json file
        # remove shapes not in new version of controls
        for crv_transform in curves:
            current_shapes = cmds.listRelatives(crv_transform, shapes=True)
            for crv_shp in current_shapes:
                if crv_shp not in old_curve_shapes:
                    cmds.delete(crv_shp)

        # clear last selection
        cmds.select(clear=True)
