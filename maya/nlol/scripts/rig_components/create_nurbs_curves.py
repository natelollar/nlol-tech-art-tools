"""Create various nurbs and nurbs curve objects
for rig controls and other needs.
"""

from importlib import reload

from maya import cmds
from nlol.scripts.rig_tools import show_attributes
from nlol.utilities.nlol_maya_logger import get_logger

reload(show_attributes)
ShowAttributes = show_attributes.ShowAttributes


class CreateCurves:
    """Create various shaped nurbs curve objects."""

    def __init__(
        self,
        name: str = "example_curve",
        size: float = 1.0,
        color_rgb: tuple = (1.0, 0.4, 0.0),
        thickness: float = -1.0,
        show_attrs: bool = False,
        curve_type: str = "",
    ) -> None:
        self.name = name
        self.size = size
        self.color_rgb = color_rgb
        self.thickness = thickness
        self.show_attrs = show_attrs
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
                case _:
                    warning_msg = f"Unkown curve type: {curve_type}"
                    self.logger.warning(warning_msg)
    def show_channel_box_attrs(self, curve_shape: str) -> None:
        """Whether to show useful curve attributes in channel box."""
        if self.show_attrs:
            ShowAttributes(target_objects=curve_shape).show_curve_attrs()

    def box_curve(self) -> str:
        """Create box shaped curve."""
        # create curve. set curve point locations in world space.
        nurbs_curve = cmds.curve(
            degree=1,
            point=[
                (-1, 1, 1),
                (-1, 1, -1),
                (1, 1, -1),
                (1, 1, 1),
                (-1, 1, 1),
                (-1, -1, 1),
                (-1, -1, -1),
                (1, -1, -1),
                (1, -1, 1),
                (-1, -1, 1),
                (-1, 1, 1),
                (1, 1, 1),
                (1, -1, 1),
                (1, -1, -1),
                (1, 1, -1),
                (-1, 1, -1),
                (-1, -1, -1),
            ],
        )
        # adjust scale
        cmds.setAttr(f"{nurbs_curve}.scale", *[self.size] * 3)
        # freeze transforms
        cmds.makeIdentity(nurbs_curve, apply=True)
        # access nurbs curve shape
        nurbs_curve_shape = cmds.listRelatives(nurbs_curve, shapes=True)[0]
        # enable wire color
        cmds.setAttr(f"{nurbs_curve_shape}.useObjectColor", 2)
        # change wire color
        cmds.setAttr(
            f"{nurbs_curve_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        # adjust visible curve thickness
        cmds.setAttr(f"{nurbs_curve_shape}.lineWidth", self.thickness)
        # show useful curve attrs
        self.show_channel_box_attrs(nurbs_curve_shape)
        # name shape
        nurbs_curve = cmds.rename(nurbs_curve, self.name)
        # return curve name string
        return nurbs_curve

    def circle_curve(
        self,
        normal: tuple[float, float, float] = (0, 1, 0),
    ) -> str:
        """Create circle curve."""
        nurbs_curve = cmds.circle(
            constructionHistory=False,
            radius=10,
            normal=normal,
        )[0]
        cmds.setAttr(f"{nurbs_curve}.scale", *[self.size] * 3)
        cmds.makeIdentity(nurbs_curve, apply=True)
        nurbs_curve_shape = cmds.listRelatives(nurbs_curve, shapes=True)[0]
        cmds.setAttr(f"{nurbs_curve_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{nurbs_curve_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{nurbs_curve_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(nurbs_curve_shape)
        nurbs_curve = cmds.rename(nurbs_curve, self.name)

        return nurbs_curve

    def global_curve(self) -> str:
        """Create global curve."""
        nurbs_curve = cmds.curve(
            degree=1,
            point=[
                (5.0, 0.0, 110.0),
                (75.0, 0.0, 45.0),
                (85.0, 0.0, 15.0),
                (80.0, 0.0, -30.0),
                (60.0, 0.0, -50.0),
                (-60.0, 0.0, -50.0),
                (-80.0, 0.0, -30.0),
                (-85.0, 0.0, 15.0),
                (-75.0, 0.0, 45.0),
                (-5.0, 0.0, 110.0),
                (5.0, 0.0, 110.0),
            ],
        )
        cmds.setAttr((nurbs_curve + ".scale"), *[self.size] * 3)
        cmds.makeIdentity(nurbs_curve, apply=True)

        nurbs_curve_shape = cmds.listRelatives(nurbs_curve, shapes=True)[0]
        cmds.setAttr(f"{nurbs_curve_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{nurbs_curve_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{nurbs_curve_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(nurbs_curve_shape)
        nurbs_curve = cmds.rename(nurbs_curve, self.name)

        return nurbs_curve

    def pyramid_curve(self) -> str:
        """Create pyramid shaped curve."""
        nurbs_curve = cmds.curve(
            degree=1,
            point=[
                (0, 5, -5),
                (-5, 0, -5),
                (0, -5, -5),
                (5, 0, -5),
                (0, 5, -5),
                (0, 0, 5),
                (5, 0, -5),
                (0, -5, -5),
                (0, 0, 5),
                (-5, 0, -5),
            ],
        )
        cmds.setAttr((nurbs_curve + ".scale"), *[self.size] * 3)
        cmds.makeIdentity(nurbs_curve, apply=True)

        nurbs_curve_shape = cmds.listRelatives(nurbs_curve, shapes=True)[0]
        cmds.setAttr(f"{nurbs_curve_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{nurbs_curve_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{nurbs_curve_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(nurbs_curve_shape)
        nurbs_curve = cmds.rename(nurbs_curve, self.name)

        return nurbs_curve

    def sphere_curve(self) -> str:
        """Create sphere shaped curve object."""
        # circle curve a
        curve_a = cmds.circle(
            constructionHistory=False,
            radius=3,
            normal=(0, 1, 0),
        )[0]
        curve_a_shape = cmds.listRelatives(curve_a, s=True)[0]
        cmds.setAttr(f"{curve_a_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{curve_a_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{curve_a_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(curve_a_shape)

        # circle curve b
        curve_b = cmds.circle(constructionHistory=False, radius=3, normal=(0, 0, 0))[0]
        curve_b_shape = cmds.listRelatives(curve_b, shapes=True)[0]
        cmds.setAttr(f"{curve_b_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{curve_b_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{curve_b_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(curve_b_shape)
        # parent shape to main transform
        cmds.parent(curve_b_shape, curve_a, relative=True, shape=True)
        # delete circle curve b transform
        cmds.delete(curve_b)

        # create 3rd nurbs circle
        curve_c = cmds.circle(constructionHistory=False, radius=3, normal=(1, 0, 0))[0]
        curve_c_shape = cmds.listRelatives(curve_c, shapes=True)[0]
        cmds.setAttr(f"{curve_c_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{curve_c_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{curve_c_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(curve_c_shape)
        # parent shape to main transform
        cmds.parent(curve_c_shape, curve_a, relative=True, shape=True)
        # delete circle curve c transform
        cmds.delete(curve_c)

        # renaming curve transform renames all its shapes
        curve_main = cmds.rename(curve_a, self.name)
        # rename shapes cleanup.
        shape_list = cmds.listRelatives(curve_main, shapes=True)
        cmds.rename(shape_list[0], f"{curve_main}_aShape")
        cmds.rename(shape_list[1], f"{curve_main}_bShape")
        cmds.rename(shape_list[2], f"{curve_main}_cShape")
        # user scale
        cmds.setAttr(f"{curve_main}.scale", *[self.size] * 3)
        cmds.makeIdentity(curve_main, apply=True)
        # select curve to replace shape selection
        cmds.select(curve_main)

        return curve_main

    def tri_circle_curve(self) -> str:
        """Create tri circle curve object."""
        # create circle a
        curve_a = cmds.circle(constructionHistory=False, radius=3, normal=(0, 1, 0))[0]
        curve_a_shape = cmds.listRelatives(curve_a, shapes=True)[0]
        cmds.setAttr(f"{curve_a_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{curve_a_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{curve_a_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(curve_a_shape)

        # circle curve b
        curve_b = cmds.circle(constructionHistory=False, radius=3, normal=(0, 1, 0))[0]
        cmds.move(0, 5, 0, curve_b, relative=True)
        cmds.makeIdentity(curve_b, apply=True)
        curve_b_shape = cmds.listRelatives(curve_b, shapes=True)[0]
        cmds.setAttr(f"{curve_b_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{curve_b_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{curve_b_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(curve_b_shape)
        # parent shape to main transform
        cmds.parent(curve_b_shape, curve_a, relative=True, shape=True)
        # delete circle curve b transform
        cmds.delete(curve_b)

        # create 3rd nurbs circle
        curve_c = cmds.circle(constructionHistory=False, radius=3, normal=(0, 1, 0))[0]
        curve_c_shape = cmds.listRelatives(curve_c, shapes=True)[0]
        cmds.move(0, -5, 0, curve_c, relative=True)
        cmds.makeIdentity(curve_c, apply=True)
        cmds.setAttr(f"{curve_c_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{curve_c_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{curve_c_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(curve_c_shape)
        # parent shape to main transform
        cmds.parent(curve_c_shape, curve_a, relative=True, shape=True)
        # delete circle curve c transform
        cmds.delete(curve_c)

        # renaming curve transform renames all its shapes
        curve_main = cmds.rename(curve_a, self.name)
        # rename shapes cleanup.
        shape_list = cmds.listRelatives(curve_main, shapes=True)
        cmds.rename(shape_list[0], f"{curve_main}_aShape")
        cmds.rename(shape_list[1], f"{curve_main}_bShape")
        cmds.rename(shape_list[2], f"{curve_main}_cShape")
        # scale to reshape points
        cmds.scale(2.5, 1, 2.5, curve_main, relative=True)
        cmds.makeIdentity(curve_main, apply=True)
        # user scale
        cmds.setAttr(f"{curve_main}.scale", *[self.size] * 3)
        cmds.makeIdentity(curve_main, apply=True)
        # select curve to replace shape selection
        cmds.select(curve_main)

        return curve_main

    def locator_curve(self) -> str:
        """Create a locator shaped curve object."""
        nurbs_curve = cmds.curve(
            degree=1,
            point=[
                (0.0, 0.0, 5.0),
                (0.0, 0.0, -5.0),
                (0.0, 0.0, 0.0),
                (-5.0, 0.0, 0.0),
                (5.0, 0.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, 5.0, 0.0),
                (0.0, 0.0, 0.0),
                (0.0, -5.0, 0.0),
            ],
        )
        cmds.setAttr((nurbs_curve + ".scale"), *[self.size] * 3)
        cmds.makeIdentity(nurbs_curve, apply=True)

        nurbs_curve_shape = cmds.listRelatives(nurbs_curve, shapes=True)[0]
        cmds.setAttr(f"{nurbs_curve_shape}.useObjectColor", 2)
        cmds.setAttr(
            f"{nurbs_curve_shape}.wireColorRGB",
            self.color_rgb[0],
            self.color_rgb[1],
            self.color_rgb[2],
        )
        cmds.setAttr(f"{nurbs_curve_shape}.lineWidth", self.thickness)
        self.show_channel_box_attrs(nurbs_curve_shape)
        nurbs_curve = cmds.rename(nurbs_curve, self.name)

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

    def sphere_nurbs(self) -> str:
        """Create nurbs sphere object."""
        nurbs_sphere = cmds.sphere(n=self.name, axis=(0, 1, 0), radius=1, ch=False)[0]
        cmds.setAttr(f"{nurbs_sphere}.scale", *[self.size] * 3)
        cmds.makeIdentity(nurbs_sphere, apply=True)
        if cmds.objExists(self.material_name):
            cmds.select(nurbs_sphere)
            cmds.hyperShade(assign=self.material_name)
        else:
            cmds.shadingNode("standardSurface", asShader=True, name=self.material_name)
            cmds.setAttr(
                f"{self.material_name}.baseColor",
                self.color_rgb[0],
                self.color_rgb[1],
                self.color_rgb[2],
            )
            cmds.select(nurbs_sphere)
            cmds.hyperShade(assign=self.material_name)

        return nurbs_sphere
