"""Create various nurbs and nurbs curve objects
for rig controls and other needs.
"""

from importlib import reload
from pathlib import Path

from maya import cmds
from nlol.scripts.rig_components import curve_library
from nlol.scripts.rig_tools import show_attributes, load_curves
from nlol.utilities.nlol_maya_logger import get_logger

reload(show_attributes)
reload(load_curves)
ShowAttributes = show_attributes.ShowAttributes
LoadCurves = load_curves.LoadCurves

curve_lib_folderpath = Path(curve_library.__file__).parent


class CreateCurves:
    """Create various shaped nurbs curve objects."""

    def __init__(
        self,
        name: str = "example_curve",
        size: float = 1.0,
        color_rgb: tuple = (1.0, 0.4, 0.0),
        thickness: float = -1.0,
        show_attrs: bool = False,
        use_curve_defaults: bool = False,
        curve_type: str = "",
    ) -> None:
        self.name = name
        self.size = size
        self.color_rgb = color_rgb
        self.thickness = thickness
        self.show_attrs = show_attrs
        self.use_curve_defaults = use_curve_defaults
        self.nurbs_curve = None
        self.logger = get_logger()

        if curve_type:
            match curve_type:
                case "box_curve":
                    self.nurbs_curve = self.box_curve()
                case "circle_curve":
                    self.nurbs_curve = self.circle_curve()
                case "global_curve":
                    self.nurbs_curve = self.global_curve()
                case "pyramid_curve":
                    self.nurbs_curve = self.pyramid_curve()
                case "sphere_curve":
                    self.nurbs_curve = self.sphere_curve()
                case "tri_circle_curve":
                    self.nurbs_curve = self.tri_circle_curve()
                case "locator_curve":
                    self.nurbs_curve = self.locator_curve()
                case "arrow_twist_curve":
                    self.nurbs_curve = self.arrow_twist_curve()
                case "cylinder_curve":
                    self.nurbs_curve = self.cylinder_curve()
                case "four_arrow_curve":
                    self.nurbs_curve = self.four_arrow_curve()
                case _:
                    warning_msg = f"Unkown curve type: {curve_type}"
                    self.logger.warning(warning_msg)

    def show_channel_box_attrs(self, curve_shape: str) -> None:
        """Whether to show useful curve attributes in channel box."""
        if self.show_attrs:
            ShowAttributes(target_objects=curve_shape).show_curve_attrs()

    def box_curve(self) -> str:
        """Create box shaped curve."""
        nurbs_curve = self.curve_generator("box_curve.json")
        return nurbs_curve

    def circle_curve(self) -> str:
        """Create circle curve."""
        nurbs_curve = self.curve_generator("circle_curve.json")
        return nurbs_curve

    def global_curve(self) -> str:
        """Create global curve."""
        nurbs_curve = self.curve_generator("global_curve.json")
        return nurbs_curve

    def pyramid_curve(self) -> str:
        """Create pyramid shaped curve."""
        nurbs_curve = self.curve_generator("pyramid_curve.json")
        return nurbs_curve

    def sphere_curve(self) -> str:
        """Create sphere shaped curve object."""
        nurbs_curve = self.curve_generator("sphere_curve.json")
        return nurbs_curve

    def tri_circle_curve(self) -> str:
        """Create tri circle curve object."""
        nurbs_curve = self.curve_generator("tri_circle_curve.json")
        return nurbs_curve

    def locator_curve(self) -> str:
        """Create a locator shaped curve object."""
        nurbs_curve = self.curve_generator("locator_curve.json")
        return nurbs_curve

    def arrow_twist_curve(self) -> str:
        """Create an arrow twist shaped curve object."""
        nurbs_curve = self.curve_generator("arrow_twist_curve.json")
        return nurbs_curve

    def cylinder_curve(self) -> str:
        """Create a cylinder shaped curve object."""
        nurbs_curve = self.curve_generator("cylinder_curve.json")
        return nurbs_curve

    def four_arrow_curve(self) -> str:
        """Create a curve object with four arrows pointing outward."""
        nurbs_curve = self.curve_generator("four_arrow_curve.json")
        return nurbs_curve

    def square_curve(self) -> str:
        """Create curve object with specified shape."""
        nurbs_curve = self.curve_generator("square_curve.json")
        return nurbs_curve

    def octagon_curve(self) -> str:
        """Create curve object with specified shape."""
        nurbs_curve = self.curve_generator("octagon_curve.json")
        return nurbs_curve

    def dodecagon_curve(self) -> str:
        """Create curve object with specified shape."""
        nurbs_curve = self.curve_generator("dodecagon_curve.json")
        return nurbs_curve

    def hexadecagon_curve(self) -> str:
        """Create curve object with specified shape."""
        nurbs_curve = self.curve_generator("hexadecagon_curve.json")
        return nurbs_curve

    def curve_generator(self, curve_filename) -> str:
        """Generate curve shape from the "curve_library" folder.

        Args:
            curve_filename: The name of the json file in
                "maya/nlol/scripts/rig_components/curve_library/".
                Ex. "octagon_curve.json"

        """
        crv_filepath = curve_lib_folderpath / curve_filename
        nurbs_curve = LoadCurves(crv_filepath).load_curve_attributes()
        nurbs_curve_shapes = cmds.listRelatives(nurbs_curve, shapes=True)

        if not self.use_curve_defaults:
            cmds.setAttr((nurbs_curve + ".scale"), *[self.size] * 3)
            cmds.makeIdentity(nurbs_curve, apply=True)

            for shp in nurbs_curve_shapes:
                cmds.setAttr(f"{shp}.useObjectColor", 2)
                cmds.setAttr(f"{shp}.wireColorRGB", *self.color_rgb)
                cmds.setAttr(f"{shp}.lineWidth", self.thickness)

            nurbs_curve = cmds.rename(nurbs_curve, self.name)
            nurbs_curve_shapes = cmds.listRelatives(nurbs_curve, shapes=True)

        for shp in nurbs_curve_shapes:
            self.show_channel_box_attrs(shp)

        cmds.select(nurbs_curve)
        return nurbs_curve


class CreateNurbs:
    """Create various shaped nurbs objects."""

    def __init__(
        self,
        name: str = "example_nurbs",
        size: float = 1.0,
        color_rgb: list | tuple = (1.0, 0.4, 0.0),
        material_name: str = "nurbs_mat",
    ) -> None:
        self.name = name
        self.size = size
        self.color_rgb = color_rgb
        self.material_name = material_name
        self.logger = get_logger()

    def sphere_nurbs(self) -> str:
        """Create nurbs sphere object."""
        nurbs_object = self.nurbs_generator("sphere")
        return nurbs_object
    
    def cube_nurbs(self) -> str:
        """Create nurbs cube object."""
        nurbs_object = self.nurbs_generator("cube")
        return nurbs_object

    def nurbs_generator(self, nurbs_object_key: str) -> str:
        """Generate a nurbs object.

        Args:
            nurbs_object_key: Keyword string for the nurbs object.

        Returns:
            Nurbs object name.

        """
        match nurbs_object_key:
            case "sphere":
                nurbs_object = cmds.sphere(n=self.name, axis=(0, 1, 0), radius=7, ch=False)[0]
            case "cube":
                nurbs_object = cmds.nurbsCube(n=self.name, width=10, ch=False)[0]
            case _:
                warning_msg = f"Unkown nurbs object: {nurbs_object}"
                self.logger.warning(warning_msg)

        cmds.setAttr(f"{nurbs_object}.scale", *[self.size] * 3)
        cmds.makeIdentity(nurbs_object, apply=True)

        if cmds.objExists(self.material_name):
            cmds.select(nurbs_object)
            cmds.hyperShade(assign=self.material_name)
        else:
            cmds.shadingNode("standardSurface", asShader=True, name=self.material_name)
            cmds.setAttr(f"{self.material_name}.baseColor", *self.color_rgb)
            cmds.select(nurbs_object)
            cmds.hyperShade(assign=self.material_name)

        return nurbs_object
