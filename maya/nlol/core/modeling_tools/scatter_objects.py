import random

from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


class ScatterObjects:
    """Scatter objects to surface and other tools."""

    def __init__(self) -> None:
        pass

    def scatter_to_verts(
        self,
        normal_orient: bool = True,
        move_up_down: float = 0,
        normal_orient_rand: bool = True,
        rand_rot: bool = False,
        super_rand_rot: bool = False,
    ) -> None:
        """Scatter selected objects to last selected object vertices.
        Uses Maya rivets to attach and orient objects to vertices of last selected
        scatter object.

        Args:
            normal_orient: Orient scattered objects to surface normals.
                If True, super_rand_rot should be False, vice versa.
            move_up_down: Default vertical offset.  Only effects if normal_orient is true.
            normal_orient_rand: Randomly offset normal orient tilt.
            rand_rot: Randomly rotate scattered objects.
            super_rand_rot: Randomly rotate scattered objects again.

        """
        selected = cmds.ls(selection=True)
        if not selected:
            logger.info("Select objects...")
            return

        scatter_objs = selected[0:-1]  # selection without last object
        scatter_objs_len = len(scatter_objs)  # number of scatter objects

        scatter_surface = selected[-1]  # vertex placement object
        vert_indices = cmds.getAttr(f"{scatter_surface}.vrts", multiIndices=True)  # vert index list
        # vert index list random sample
        if scatter_objs_len <= len(vert_indices):
            vert_indices_sample = random.sample(vert_indices, scatter_objs_len)
        else:
            logger.info("Not enough verts to scatter. Select last object with more verts...")
            return

        rivets = []
        for vert_id in vert_indices_sample:  # get scatter surface vert positions
            cmds.select(f"{scatter_surface}.pnts[{vert_id!s}]")
            cmds.Rivet()
            rivet = cmds.ls(selection=True, type="transform")
            rivets.append(rivet)

        for scatter_obj, rivet in zip(scatter_objs, rivets, strict=False):
            cmds.parent(scatter_obj, rivet)  # scatter object to vert and aim in normals direction
            cmds.setAttr(f"{scatter_obj}.translate", 0, 0, 0)  # zero out position under rivet vert

            if normal_orient:  # orient to normals
                cmds.setAttr(f"{scatter_obj}.rotate", 0, 0, 0)
                # point up and push down
                cmds.setAttr(f"{scatter_obj}.rotateZ", -90)  # point up
                if move_up_down:
                    cmds.setAttr(f"{scatter_obj}.translateX", move_up_down)  # push down
                if normal_orient_rand:  # randomly adjust scatter obj tilt
                    cmds.rotate(
                        random.randrange(-20, 20, 1),
                        random.randrange(-360, 360, 1),
                        random.randrange(-20, 20, 1),
                        relative=True,
                        objectSpace=True,
                        forceOrderXYZ=True,
                    )

            if rand_rot:
                cmds.select(scatter_obj)
                cmds.rotate(
                    random.randrange(-360, 360, 1),
                    random.randrange(-360, 360, 1),
                    random.randrange(-360, 360, 1),
                    relative=True,
                    objectSpace=True,
                    forceOrderXYZ=True,
                )
            if super_rand_rot:
                cmds.setAttr(
                    f"{scatter_obj}.rotate",
                    random.randrange(-360, 360, 1),
                    random.randrange(-360, 360, 1),
                    random.randrange(-360, 360, 1),
                )

            # --------------------------------------------------
            cmds.Unparent(scatter_obj)  # unparent from rivet
            cmds.delete(rivet)  # delete rivet

        cmds.select(selected)

    def boundingbox_scatter(self, normal_orient: bool = True, scatter_2d: bool = True) -> None:
        """Scatter selected objects to last selected object based on bounding box
        of last selected object. Then closest surface.

        Args:
            normal_orient: Orient scattered objects based on surface normals.
                Object "y" up.
            scatter_2d: Whether to snap objects to 2D surface after scattering in 3D space.

        """
        selected = cmds.ls(selection=True)
        if not selected:
            logger.info("Select objects...")
            return

        scatter_objs = selected[0:-1]  # selection without last object
        scatter_surface = selected[-1]  # vertex placement object

        # get bounding box points of scatter surface (order: xmin ymin zmin xmax ymax zmax)
        root_selection_box_bb = cmds.xform(scatter_surface, ws=True, bb=True, q=True)
        bb_x_min, bb_y_min, bb_z_min, bb_x_max, bb_y_max, bb_z_max = root_selection_box_bb

        for scatter_obj in scatter_objs:
            # position to closest geo surface of last selected
            cmds.setAttr(f"{scatter_obj}.tx", random.triangular(bb_x_min, bb_x_max))
            cmds.setAttr(f"{scatter_obj}.ty", random.triangular(bb_y_min, bb_y_max))
            cmds.setAttr(f"{scatter_obj}.tz", random.triangular(bb_z_min, bb_z_max))

            if scatter_2d:
                geo_const = cmds.geometryConstraint(scatter_surface, scatter_obj)
                # note: look at 'point on poly' too, for maintain offset
                cmds.delete(geo_const)

                if normal_orient:  # orient in normal direction
                    nrml_const = cmds.normalConstraint(
                        scatter_surface,
                        scatter_obj,
                        aimVector=(0, 1, 0),
                    )
                    cmds.delete(nrml_const)

        # reselect to scatter multiple times
        cmds.select(scatter_objs)
        cmds.select(scatter_surface, add=True)

    def random_rotate(
        self,
        x_rot_low: float = -360,
        x_rot_high: float = 360,
        y_rot_low: float = -360,
        y_rot_high: float = 360,
        z_rot_low: float = -360,
        z_rot_high: float = 360,
    ) -> None:
        """Randomly rotate selected objects.

        Args:
            x_rot_low, x_rot_high, y_rot_low, y_rot_high, z_rot_low, z_rot_high:
            Low and high values for random rotation.

        """
        selected = cmds.ls(selection=True)
        if not selected:
            logger.info("Select objects...")
            return

        for obj in selected:
            cmds.select(obj)
            cmds.rotate(
                random.triangular(x_rot_low, x_rot_high),
                random.triangular(y_rot_low, y_rot_high),
                random.triangular(z_rot_low, z_rot_high),
                relative=True,
                objectSpace=True,
                forceOrderXYZ=True,
            )

        cmds.select(selected)

    def random_scale(
        self,
        scale_low: float = 0.5,
        scale_high: float = 3,
        scale_stretch: float = 2,
    ) -> None:
        """Randomly scale selected objects uniformly.

        Args:
            scale_low, scale_high: Low and high values for random scale.
            scale_stretch: Stretch multiplier for the scale "y" attr.

        """
        selected = cmds.ls(selection=True)
        if not selected:
            logger.info("Select objects...")
            return

        for obj in selected:
            rand_scale = random.triangular(scale_low, scale_high, 1)
            cmds.setAttr(f"{obj}.scale", rand_scale, rand_scale * scale_stretch, rand_scale)

        cmds.select(selected)

    def simple_move(
        self,
        x_trans_amnt: float = 0,
        y_trans_amnt: float = 0,
        z_trans_amnt: float = 0,
    ) -> None:
        """Move the selected objects with simple tranformation values.
        Useful to push objects up or down. Helpful after scattering.

        Args:
            x_trans_amnt, y_trans_amnt, z_trans_amnt: Transform amounts to move the selected.

        """
        selected = cmds.ls(selection=True)
        if not selected:
            logger.info("Select objects...")
            return

        for obj in selected:
            cmds.select(obj)
            cmds.move(
                x_trans_amnt,
                y_trans_amnt,
                z_trans_amnt,
                relative=True,
                objectSpace=True,
                worldSpaceDistance=True,
            )

        cmds.select(selected)

    def reset_transforms(
        self,
        translate: bool = False,
        rotate: bool = False,
        scale: bool = False,
    ) -> None:
        """Reset selected objects transforms.

        Args:
            translate, rotate, scale: Attributes to reset.

        """
        transform_attrs = []
        reset_vals = []
        if translate:
            transform_attrs.append("translate")
            reset_vals.append(0)
        if rotate:
            transform_attrs.append("rotate")
            reset_vals.append(0)
        if scale:
            transform_attrs.append("scale")
            reset_vals.append(1)

        for val, attr in zip(reset_vals, transform_attrs, strict=False):
            selected = cmds.ls(selection=True)

            for obj in selected:
                obj_locked_attr = cmds.listAttr(obj, locked=True)
                if obj_locked_attr:  # skip if locked attribute
                    # zero out individual unlocked values
                    if f"{attr}X" not in obj_locked_attr:
                        cmds.setAttr(f"{obj}.{attr}X", val)
                    if f"{attr}Y" not in obj_locked_attr:
                        cmds.setAttr(f"{obj}.{attr}Y", val)
                    if f"{attr}Z" not in obj_locked_attr:
                        cmds.setAttr(f"{obj}.{attr}Z", val)
                else:  # else zero out all
                    cmds.setAttr(f"{obj}.{attr}", val, val, val)

    def random_3d_scatter(
        self,
        trans_amnt: float = 300,
        rot_amnt: float = 360,
        scale_amnt: float = 3,
    ) -> None:
        """Scatter selected objects randomly in 3D space.

        Args:
            trans_amnt, rot_amnt: Value for high and low bounds to randomly scatter.
            scale_amnt: Goal value for random uniform scale.

        """
        selected = cmds.ls(selection=True)
        if not selected:
            logger.info("Select objects...")
            return

        for obj in selected:
            # translate
            cmds.setAttr((f"{obj}.tx"), random.uniform(-trans_amnt, trans_amnt))
            cmds.setAttr((f"{obj}.ty"), random.uniform(-trans_amnt, trans_amnt))
            cmds.setAttr((f"{obj}.tz"), random.uniform(-trans_amnt, trans_amnt))
            # rotate
            cmds.setAttr((f"{obj}.rx"), random.uniform(-rot_amnt, rot_amnt))
            cmds.setAttr((f"{obj}.ry"), random.uniform(-rot_amnt, rot_amnt))
            cmds.setAttr((f"{obj}.rz"), random.uniform(-rot_amnt, rot_amnt))
            # scale
            scale_rand = random.uniform(0.3, scale_amnt)  # for uniform scale
            cmds.setAttr((f"{obj}.sx"), scale_rand)
            cmds.setAttr((f"{obj}.sy"), scale_rand)
            cmds.setAttr((f"{obj}.sz"), scale_rand)

    def create_random_objs(
        self,
        count: int = 10,
        position_range: float = 200.0,
        radius_range: tuple = (5, 25),
        height_range: tuple = (5, 100),
        scale_range: tuple = (1, 2),
        scale_stretch: float = 2,
    ) -> None:
        """Create random polygon objects.

        Args:
            position_range: How spread out objects will be.
            count: How many sets of sphere, cube, cylinder, polyCone to create.
            radius_range: Object radius random range for creation.
            height_range: Object height random range for creation.
            scale_range: Range for random uniform scale post object spawn.
            scale_stretch: Additional stretch scalar for vertical "y" scale attr.

        """

        def rand(a, b):
            return random.uniform(a, b)

        def move_random(obj):
            cmds.move(
                rand(-position_range, position_range),
                rand(-position_range, position_range),
                rand(-position_range, position_range),
                obj,
                relative=True,
                objectSpace=True,
            )

        def rotate_random(obj):
            cmds.rotate(
                rand(-360, 360),
                rand(-360, 360),
                rand(-360, 360),
                obj,
                relative=True,
                objectSpace=True,
            )

        for _ in range(count):
            # sphere
            sphere = cmds.polySphere(radius=rand(*radius_range), constructionHistory=False)
            move_random(sphere)
            sphere_scale = rand(*scale_range)
            cmds.scale(
                sphere_scale,
                sphere_scale * scale_stretch,
                sphere_scale,
                sphere,
                relative=True,
                objectSpace=True,
            )
            rotate_random(sphere)

            # cube
            cube_size = rand(*radius_range)
            cube = cmds.polyCube(
                width=cube_size,
                height=rand(*height_range),
                depth=cube_size,
                constructionHistory=False,
            )
            move_random(cube)
            cube_scale = rand(*scale_range)
            cmds.scale(
                cube_scale,
                cube_scale * scale_stretch,
                cube_scale,
                cube,
                relative=True,
                objectSpace=True,
            )
            rotate_random(cube)

            # cylinder
            cylinder = cmds.polyCylinder(
                radius=rand(*radius_range),
                height=rand(*height_range),
                subdivisionsHeight=1,
                constructionHistory=False,
            )
            move_random(cylinder)
            cylinder_scale = rand(*scale_range)
            cmds.scale(
                cylinder_scale,
                cylinder_scale * scale_stretch,
                cylinder_scale,
                cylinder,
                relative=True,
                objectSpace=True,
            )
            rotate_random(cylinder)

            # polycone
            polycone = cmds.polyCone(
                radius=rand(*radius_range),
                height=rand(*height_range),
                subdivisionsHeight=1,
                constructionHistory=False,
            )
            move_random(polycone)
            polycone_scale = rand(*scale_range)
            cmds.scale(
                polycone_scale,
                polycone_scale * scale_stretch,
                polycone_scale,
                polycone,
                relative=True,
                objectSpace=True,
            )
            rotate_random(polycone)

        cmds.select(clear=True)
        cmds.setFocus("MayaWindow")
