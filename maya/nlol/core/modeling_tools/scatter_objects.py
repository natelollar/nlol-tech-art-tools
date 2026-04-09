import bisect  # High-performance list searching
import random

from maya.api import OpenMaya as om
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

    def boundingbox_scatter(
        self,
        scatter_objs: list = [],
        scatter_surface: str = "",
        normal_orient: bool = True,
        scatter_2d: bool = True,
    ) -> None:
        """Scatter selected objects to last selected object based on bounding box
        of last selected object. Then closest surface.

        Args:
            normal_orient: Orient scattered objects based on surface normals.
                Object "y" up.
            scatter_2d: Whether to snap objects to 2D surface after scattering in 3D space.

        """
        reselect = False
        if not scatter_objs:
            selected = cmds.ls(selection=True)
            if not selected:
                logger.info("Select objects...")
                return
            scatter_objs = selected[0:-1]  # selection without last object
            scatter_surface = selected[-1]  # vertex placement object
            reselect = True

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

        if reselect:
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

    # ----------------------------------------------------------
    # -------------------- REALTIME SCATTER --------------------
    # ----------------------------------------------------------
    def enable_realtime_scatter(
        self,
        normal_orient: bool = True,
        scatter_2d: bool = True,
    ) -> None:
        """Enable realtime scatter.

        Select your objects to scatter + the poly plane (or any surface) LAST,
        then call this once.

        As you drag/extrude/scale/vertex-push the surface (e.g. growing a river),
        it will automatically re-run universal_weighted_scatter or boundingbox_scatter
        with new random positions every time you RELEASE the mouse and
        the surface area changes.

        Super simple, uses Maya's idleEvent (no tick/currentFrame needed).
        Only triggers on actual size growth so it doesn't spam while you work.

        Args:
            normal_orient: Whether to orient scatter objects to normals of the surface.
            scatter_2d: Whether to snap the scatter objects to the surface using
                "universal_weighted_scatter" or leave as a bounding box volume scatter.

        """
        self.disable_realtime_scatter()  # kill any old jobs

        logger.info("----- Realtime Scatter ENABLED -----")

        selected = cmds.ls(selection=True)
        if len(selected) < 2:
            logger.info("Select scatter objects + surface last...")
            return

        self.realtime_scatter_objs = selected[:-1]
        self.realtime_surface = selected[-1]
        self.realtime_normal_orient = normal_orient
        self.realtime_scatter_2d = scatter_2d

        # kill any old job
        if hasattr(self, "realtime_scatter_job") and self.realtime_scatter_job is not None:
            try:
                cmds.scriptJob(kill=self.realtime_scatter_job, force=True)
            except Exception:
                pass

        self.realtime_scatter_job = cmds.scriptJob(
            idleEvent=self.realtime_scatter_callback,
            killWithScene=True,
        )

        logger.info(f"Realtime scatter ENABLED on surface: {self.realtime_surface}")
        logger.info("-> Drag/extrude the surface -> release mouse = new random scatter")

    def force_realtime_scatter(self) -> None:
        """Force update for realtime scatter."""
        self.force_scatter_update = True

    def disable_realtime_scatter(self) -> None:
        """Stop the realtime job."""
        # kill by the stored ID if it exists
        if hasattr(self, "realtime_scatter_job") and self.realtime_scatter_job is not None:
            try:
                cmds.scriptJob(kill=self.realtime_scatter_job, force=True)
            except Exception:
                pass
            self.realtime_scatter_job = None

        # cleanup: search and kill any "zombie" jobs by function name
        # this catches jobs that stayed alive after UI reloads
        search_string = "realtime_scatter_callback"
        all_jobs = cmds.scriptJob(listJobs=True)
        for job in all_jobs:
            if search_string in job:
                try:
                    job_id = int(job.split(":")[0])
                    cmds.scriptJob(kill=job_id, force=True)
                    logger.info(f"Cleaned up zombie scriptJob: {job_id}")
                except Exception:
                    continue

        self.realtime_scatter_objs = None
        self.realtime_surface = None
        logger.info("----- Realtime Scatter DISABLED -----")

    def realtime_scatter_callback(self) -> None:
        """Internal idle callback using surface area checks."""
        if (
            not hasattr(self, "realtime_surface")
            or not self.realtime_surface
            or not cmds.objExists(self.realtime_surface)
        ):
            return

        try:
            # check surface area (precise - catches internal vertex moves/extrusions)
            current_area = self.get_surface_area(self.realtime_surface)
            area_changed = False
            if hasattr(self, "last_area") and self.last_area is not None:
                # use a small epsilon for float comparison
                if abs(current_area - self.last_area) > 0.001:
                    area_changed = True
            else:
                area_changed = True

            if area_changed or self.force_scatter_update:
                try:
                    if self.realtime_scatter_2d:
                        self.universal_weighted_scatter(
                            self.realtime_scatter_objs,
                            self.realtime_surface,
                            normal_orient=self.realtime_normal_orient,
                        )
                    else:
                        self.boundingbox_scatter(
                            self.realtime_scatter_objs,
                            self.realtime_surface,
                            normal_orient=self.realtime_normal_orient,
                            scatter_2d=False,
                        )
                except Exception as e:
                    logger.error(f"Realtime scatter failed: {e}")

                self.last_area = current_area
                self.force_scatter_update = False

        except Exception:
            return

    def get_surface_area(self, node_name: str) -> float:
        """Returns the world-space surface area for poly or nurbs.
        Used for detecting a change in surface area.

        Args:
            node_name: Name of Maya node. In this case a polygonal or nurbs transform.

        """
        if not cmds.objExists(node_name):
            return 0.0

        # get the shape node
        shapes = cmds.listRelatives(node_name, shapes=True, fullPath=True) or [node_name]
        shape = shapes[0]
        node_type = cmds.nodeType(shape)

        try:
            if node_type == "mesh":
                area = cmds.polyEvaluate(shape, worldArea=True)
                return area

            if node_type == "nurbsSurface":
                sel = om.MSelectionList()
                sel.add(shape)
                dag_path = sel.getDagPath(0)
                nurbs_fn = om.MFnNurbsSurface(dag_path)
                return nurbs_fn.area()

        except Exception as e:
            logger.warning(f"Could not calculate area for {node_name}: {e}")

        return 0.0

    def universal_weighted_scatter(
        self,
        scatter_objs: list = [],
        scatter_surface: str = "",
        normal_orient: bool = True,
    ) -> None:
        """Scatters objects evenly across any surface, regardless of face size or UVs.
        Works for both poly and nurbs.

        Args:
            scatter_objs: Maya objects to scatter.
            scatter_surface: What about to scatter on.
            normal_orient: Whether to orient scatter objects to surface normals.

        """
        if not scatter_objs:
            selected = cmds.ls(selection=True)
            if not selected:
                logger.info("Select objects...")
                return
            scatter_objs = selected[:-1]
            scatter_surface = selected[-1]

        shape = cmds.listRelatives(scatter_surface, shapes=True, fullPath=True)[0]
        node_type = cmds.nodeType(shape)

        # --- PRE-PROCESS PHASE (Calculate Weights) ---
        face_weights = []
        total_area = 0.0

        if node_type == "mesh":
            # get the total number of faces on the mesh to iterate through them
            num_faces = cmds.polyEvaluate(shape, face=True)
            for i in range(num_faces):
                # calculate the area manually because polyEvaluate returns 0 on some meshes
                # get the vertex indices for the current face (returns a string like 'FACE 0: 1 2 5 4')
                info = cmds.polyInfo(f"{shape}.f[{i}]", faceToVertex=True)[0]
                # parse the string to extract only the integer IDs of the vertices
                v_indices = [int(v) for v in info.split(":")[1].split() if v.strip().isdigit()]
                # get the world-space [x, y, z] position for every vertex in this face
                pts = [
                    cmds.xform(f"{shape}.vtx[{v}]", query=True, worldSpace=True, translation=True)
                    for v in v_indices
                ]

                f_area = 0.0
                # use a "triangle fan" to calculate area: anchor at pts[0] and create triangles
                # from subsequent pairs of vertices. works for triangles, quads, and N-gons
                for j in range(len(pts) - 2):
                    # define the three corners of the current triangle slice
                    p0, p1, p2 = pts[0], pts[j + 1], pts[j + 2]
                    # create two vectors (edges) sharing the common point p0
                    v1 = [p1[k] - p0[k] for k in range(3)]
                    v2 = [p2[k] - p0[k] for k in range(3)]
                    # calculate the cross product of v1 and v2
                    # the resulting vectors magnitude equals the area of a parallelogram
                    cp = [
                        v1[1] * v2[2] - v1[2] * v2[1],
                        v1[2] * v2[0] - v1[0] * v2[2],
                        v1[0] * v2[1] - v1[1] * v2[0],
                    ]
                    # area of triangle = 0.5 * magnitude of cross product
                    # magnitude is sqrt(x^2 + y^2 + z^2)
                    f_area += 0.5 * (sum(x**2 for x in cp) ** 0.5)
                # accumulate the total area of the mesh
                total_area += f_area
                # store the "running total" area. this is used later for importance sampling
                # (randomly picking a face weighted by its size)
                face_weights.append(total_area)

        # --- SCATTER PHASE ---
        for obj in scatter_objs:
            pos = [0, 0, 0]

            if node_type == "mesh" and total_area > 0:
                # pick a face:
                # Generate a random number between 0 and the total surface area
                r = random.uniform(0, total_area)
                # use binary search (bisect) to find which face corresponds to that 'r' value
                # this ensures larger faces have a higher statistical chance of being picked
                face_idx = bisect.bisect_left(face_weights, r)

                # get face geometry:
                # retrieve the vertices and their world positions for the chosen face
                vtx_str = cmds.polyInfo(f"{shape}.f[{face_idx}]", faceToVertex=True)[0]
                vtx_indices = [int(i) for i in vtx_str.split(":")[1].split() if i.strip().isdigit()]
                pts = [
                    cmds.xform(f"{shape}.vtx[{v}]", q=True, ws=True, t=True) for v in vtx_indices
                ]

                # triangulate the face (operates inside a single face):
                # if the face is a quad or N-gon, we must pick a specific triangle within it
                sub_tris, sub_weights, sub_total = [], [], 0.0
                for i in range(len(pts) - 2):
                    p0, p1, p2 = pts[0], pts[i + 1], pts[i + 2]
                    v1, v2 = [p1[k] - p0[k] for k in range(3)], [p2[k] - p0[k] for k in range(3)]
                    cp = [
                        v1[1] * v2[2] - v1[2] * v2[1],
                        v1[2] * v2[0] - v1[0] * v2[2],
                        v1[0] * v2[1] - v1[1] * v2[0],
                    ]
                    # calculate sub-triangle area to keep the distribution uniform
                    tri_a = 0.5 * (sum(x**2 for x in cp) ** 0.5)
                    sub_total += tri_a
                    sub_weights.append(sub_total)
                    sub_tris.append((p0, p1, p2))

                # pick a triangle:
                # if the face was an N-gon, pick one of its triangle "slices" based on area
                if sub_total > 0:
                    tr = random.uniform(0, sub_total)
                    tri_idx = bisect.bisect_left(sub_weights, tr)
                    tp0, tp1, tp2 = sub_tris[tri_idx]
                    # barycentric sampling:
                    # pick a random point inside the chosen triangle
                    u, v = random.random(), random.random()
                    # if u + v > 1, the point is in the "other half" of the parallelogram
                    # 'mirror' it back into the triangle
                    if u + v > 1:
                        u, v = 1 - u, 1 - v
                    # w is the third weight (all three must add up to 1.0)
                    w = 1 - u - v
                    # calculate the final 3D position by mixing the positions of the 3 vertices
                    pos = [(u * tp0[i] + v * tp1[i] + w * tp2[i]) for i in range(3)]

            elif node_type == "nurbsSurface":
                # nurbs are mathematically "smooth", so we use parametric (UV)
                u_range = [
                    cmds.getAttr(f"{shape}.minMaxRangeU.minValueU"),
                    cmds.getAttr(f"{shape}.minMaxRangeU.maxValueU"),
                ]
                v_range = [
                    cmds.getAttr(f"{shape}.minMaxRangeV.minValueV"),
                    cmds.getAttr(f"{shape}.minMaxRangeV.maxValueV"),
                ]

                rand_u = random.uniform(u_range[0], u_range[1])
                rand_v = random.uniform(v_range[0], v_range[1])
                pos = cmds.pointOnSurface(shape, u=rand_u, v=rand_v, top=True, p=True)

            # apply position
            cmds.xform(obj, worldSpace=True, translation=pos)

            # apply orientation
            if normal_orient:
                tmp = cmds.normalConstraint(
                    scatter_surface,
                    obj,
                    aimVector=(0, 1, 0),
                    # worldUpType=0,
                )
                cmds.delete(tmp)
