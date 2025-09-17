"""Load in json curve shape data.
Build a new control curve.
"""

import ast
import json
from pathlib import Path

from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger


class LoadCurves:
    """Load curves from curve library."""

    def __init__(self, filepath: str | Path):
        self.filepath = filepath
        self.logger = get_logger()

    def read_curve_attributes(self):
        """Read curve shape attributes from json file."""
        with open(self.filepath) as f:
            curve_attributes = json.load(f)
            # self.logger.debug(f'Control shapes read: "{self.filepath}"')
            return curve_attributes

    def load_curve_attributes(self):
        """Iterate through curve shape attribute data in json file.
        Apply data to curve shapes. Build new curve.
        """
        transform_node = ""
        curve_attributes = self.read_curve_attributes()
        for i, attr_list in enumerate(curve_attributes.values()):
            # query curve attributes from json file
            curve = attr_list["curve"]
            use_object_color = attr_list["useObjectColor"]
            object_color = attr_list["objectColor"]
            wire_color_rgb = ast.literal_eval(attr_list["wireColorRGB"])
            line_width = attr_list["lineWidth"]

            curve_degree = attr_list["curve_degree"]
            curve_spans = attr_list["curve_spans"]
            curve_form = attr_list["curve_form"]
            cv_positions = ast.literal_eval(attr_list["cv_positions"])

            if cmds.objExists(transform_node):
                transform_node = transform_node
            else:
                transform_node = cmds.group(em=True, name=curve)

            # create new curve shapes
            if curve_form == 0 or curve_form == 1:
                new_curve_transform = cmds.curve(point=cv_positions, degree=curve_degree)
                new_curve_shape = cmds.listRelatives(new_curve_transform, shapes=True)

            if curve_form == 2 and curve_degree == 1:  # closed curve and degree is linear
                # last cv position to first to form a closed curve
                last_element = cv_positions.pop()

                cv_positions.insert(0, last_element)
                new_curve_transform = cmds.curve(point=cv_positions, degree=curve_degree)
                new_curve_shape = cmds.listRelatives(new_curve_transform, shapes=True)

            if curve_form == 2 and curve_degree != 1:
                new_curve_transform = cmds.circle(
                    sections=curve_spans,
                    degree=curve_degree,
                    constructionHistory=False,
                )
                new_curve_shape = cmds.listRelatives(new_curve_transform, shapes=True)[0]
                for i, pos in enumerate(cv_positions):
                    cv_identifier = f"{new_curve_shape}.cv[{i}]"
                    cmds.xform(cv_identifier, translation=pos)

            # parent curve shape to control transform node
            cmds.parent(new_curve_shape, transform_node, relative=True, shape=True)

            new_curve_shape = cmds.rename(new_curve_shape, f"{transform_node}Shape")

            cmds.delete(new_curve_transform)

            # ----- color and width attrs -----
            cmds.setAttr(f"{new_curve_shape}.useObjectColor", use_object_color)
            cmds.setAttr(f"{new_curve_shape}.objectColor", object_color)
            cmds.setAttr(f"{new_curve_shape}.wireColorRGB", *wire_color_rgb)
            cmds.setAttr(f"{new_curve_shape}.lineWidth", line_width)

        return transform_node
