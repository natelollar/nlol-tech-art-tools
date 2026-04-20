from importlib import reload

from maya import cmds, mel
from nlol.core.rig_setup import common_build_components
from nlol.core.rig_tools import tools_skinning
from nlol.utilities import nlol_maya_logger, nlol_maya_registry

reload(common_build_components)
reload(tools_skinning)

registry = nlol_maya_registry.get_registry()
logger = nlol_maya_logger.get_logger()


class CurveDynamics:
    """General curve dynamics setup using Maya's nHair system."""

    def __init__(self) -> None:
        """Initialize class."""

    def build(self, curves: list[str] | str, hair_system: str = "") -> None:
        """Entry point. Run this method.
        --------------------------------------------------
        """
        # run main methods
        cmds.undoInfo(openChunk=True)
        try:
            self.CommonBuildComponents = common_build_components.CommonBuildComponents()
            self.CommonBuildComponents.build_top_dynamics_grps()
            self.CommonBuildComponents.build_dynamics_aux_ctrl()
            self.build_dynamics_on_crvs(curves, hair_system)
        finally:
            cmds.undoInfo(closeChunk=True)

    def build_dynamics_on_crvs(
        self,
        curves: list[str] | str,
        hair_system: str = "",
        create_restpose_curves: bool = True,
    ) -> None:
        """Apply dynamics to curves via nHair system and blendshape. With attributes via
        dynamics aux ctrl.

        Args:
            curves: Curve/s to apply dynamics too.
            hair_system: Maya nHair system node.
            create_restpose_curves: Whether to duplicate curve and copy skin weights
                to avoid cycle warning from blendshape.

        """
        if isinstance(curves, str):
            curves = [curves]

        for crv in curves:
            self.build_dynamics_on_crv(
                curve=crv,
                create_restpose_curve=create_restpose_curves,
                hair_system=hair_system,
            )

    def build_dynamics_on_crv(
        self,
        curve: str,
        create_restpose_curve: bool = True,
        hair_system: str = "",
    ) -> None:
        """Applying curve dynamics to single curve.
        Duplicate curve first if needed for separate rest pose curve.
        Copy skin weights from original curve if needed.
        Apply final dynamic curve to original curve as blendshape.
        Add attributes to global dynamics ctrl for rig.

        Args:
            curve: Main curve which will end up with the blendshape
                connected to the dynamics curve.
            create_restpose_curve: Whether to duplicate the main curve.
                This new curve would be the restpose curve with same skin weights.
                This helps avoid cycle error when connecting the dynamics curve as
                a blendshape back to the original.

        """
        nucleus_nd = registry.get_obj("dynamics_nucleus_nd")
        dynamics_components_grp = registry.get_obj("dynamics_components_grp")

        restpose_crv = None
        curve_nm_split = curve.split("_")
        curve_nm_first = curve.split("_")[0]  # first name component
        curve_nm_ending = "_".join(curve_nm_split[1:])
        if create_restpose_curve:
            restpose_crv_nm_start = f"{curve_nm_first}RestPose"
            restpose_crv_nm = f"{restpose_crv_nm_start}_{curve_nm_ending}"
            restpose_crv = tools_skinning.duplicate_copy_skin_weights(curve, name=restpose_crv_nm)
        else:
            restpose_crv = curve

        cmds.select(restpose_crv)  # select curve to create dynamic curve from
        if hair_system:
            cmds.select(hair_system, add=True)  # will use same hair system
        if nucleus_nd:
            cmds.select(nucleus_nd, add=True)  # will use same nucleus node

        # nHair < Make Selected Curves Dynamic. Options: NURBS curves. Exact shape match.
        mel.eval('makeCurvesDynamic 2 { "0", "0", "1", "1", "0"};')

        # ----- find, rename, set settings and parent dynamic components -----
        # hair follicle
        world_origin_follicle = cmds.listRelatives(restpose_crv, parent=True)[0]
        world_origin_follicle = cmds.rename(
            world_origin_follicle,
            f"{restpose_crv}Follicle",
        )
        follicle_shp = cmds.listRelatives(world_origin_follicle, shapes=True)[0]
        cmds.setAttr(f"{world_origin_follicle}.pointLock", 1)  # Base. So tip not attached.
        cmds.parent(world_origin_follicle, dynamics_components_grp)
        # hair system
        if not hair_system:
            hair_system = cmds.listConnections(
                follicle_shp,
                source=False,
                destination=True,
                type="hairSystem",
            )[0]
            hair_system = cmds.rename(hair_system, f"{restpose_crv}HairSystem")
            cmds.setAttr(f"{hair_system}.drag", 0.1)  # slows overall movement slightly
            cmds.setAttr(f"{hair_system}.damp", 0.3)  # kills bounce
            cmds.setAttr(f"{hair_system}.stretchDamp", 0.5)  # damping along the length
            cmds.parent(hair_system, dynamics_components_grp)
        hair_system_shp = cmds.listRelatives(hair_system, shapes=True)[0]
        # dynamic curve
        dynamic_crv = cmds.listConnections(
            follicle_shp,
            source=False,
            destination=True,
            type="nurbsCurve",
        )[0]
        dynamic_crv_nm_start = f"{curve_nm_first}Dynamic"
        dynamic_crv_nm = f"{dynamic_crv_nm_start}_{curve_nm_ending}"
        dynamic_crv = cmds.rename(dynamic_crv, dynamic_crv_nm)
        dynamic_crv_grp = cmds.listRelatives(dynamic_crv, parent=True)[0]
        dynamic_crv_grp = cmds.rename(dynamic_crv_grp, f"{dynamic_crv_nm}Grp")
        cmds.parent(dynamic_crv_grp, dynamics_components_grp)
        # nucleus node
        if not nucleus_nd:
            nucleus_nd = cmds.listConnections(
                hair_system_shp,
                source=False,
                destination=True,
                type="nucleus",
            )[0]
            nucleus_nd = cmds.rename(nucleus_nd, "main_nucleus")
            cmds.parent(nucleus_nd, dynamics_components_grp)
            cmds.setAttr(f"{nucleus_nd}.spaceScale", 0.01)
            # nucleus name to data registry
            registry.register_obj("dynamics_nucleus_nd", nucleus_nd)
            # add nucleus attrs to dynamics aux ctrl
            self.CommonBuildComponents.aux_ctrl_nucleus_attrs(nucleus_nd)

        # connect dynamic curve to original main curve via blendshape
        blendshape_nd = f"{curve}BlendShape"
        cmds.blendShape(dynamic_crv, curve, name=blendshape_nd)

        # dynamic curve attributes
        self.aux_ctrl_nhair_attrs(hair_system_shp, blendshape_nd, dynamic_crv)

    def aux_ctrl_nhair_attrs(self, hair_system_shp, blendshape_nd, dynamic_crv) -> None:
        """Set up auxiliary ctrl attributes for curve dynamics.

        Args:
            hair_system_shape: nHair system shape node.
            blendshape_nd: Blendshape node being used for nHair curve dynamics.
            dynamic_crv: Curve being simulated with hair system used for final blendshape.

        """
        aux_ctrl = registry.get_obj("dynamics_aux_ctrl")

        divider_attr_nm = hair_system_shp
        if not cmds.objExists(f"{aux_ctrl}.{divider_attr_nm}"):
            # ---------- divider attr ----------
            cmds.addAttr(
                aux_ctrl,
                longName=divider_attr_nm,
                niceName=divider_attr_nm,
                attributeType="enum",
                enumName=divider_attr_nm,
            )
            cmds.setAttr(f"{aux_ctrl}.{divider_attr_nm}", channelBox=True)

            # ---------- active/simulationMethod attrs ----------
            active_attr_nm = f"{hair_system_shp}__active"
            cmds.addAttr(
                aux_ctrl,
                longName=active_attr_nm,
                niceName=active_attr_nm,
                attributeType="bool",
                defaultValue=False,
                keyable=True,
            )
            cmds.connectAttr(
                f"{aux_ctrl}.{active_attr_nm}",
                f"{hair_system_shp}.active",
            )

            # use condition node so Active can set enum attr (Off or All Follicles)
            condition_nd = cmds.createNode("condition", name=f"{active_attr_nm}Condition")
            cmds.setAttr(f"{condition_nd}.secondTerm", 0.5)
            cmds.setAttr(f"{condition_nd}.operation", 2)  # Greater Than
            cmds.setAttr(f"{condition_nd}.colorIfTrueR", 3.0)
            cmds.setAttr(f"{condition_nd}.colorIfFalseR", 0.0)
            cmds.connectAttr(
                f"{aux_ctrl}.{active_attr_nm}",
                f"{condition_nd}.firstTerm",
            )
            cmds.connectAttr(
                f"{condition_nd}.outColorR",
                f"{hair_system_shp}.simulationMethod",
            )

            # ---------- startCurveAttract attr ----------
            curveattract_attr_nm = f"{hair_system_shp}__startCurveAttract"
            cmds.addAttr(
                aux_ctrl,
                longName=curveattract_attr_nm,
                niceName=curveattract_attr_nm,
                attributeType="double",
                defaultValue=0.30,
                keyable=True,
            )
            cmds.connectAttr(
                f"{aux_ctrl}.{curveattract_attr_nm}",
                f"{hair_system_shp}.startCurveAttract",
            )
        else:
            # ---------- divider attr ----------
            # create divider just for blendshape attr if hair system attr already exist
            divider_attr_nm = dynamic_crv
            cmds.addAttr(
                aux_ctrl,
                longName=divider_attr_nm,
                niceName=divider_attr_nm,
                attributeType="enum",
                enumName=divider_attr_nm,
            )
            cmds.setAttr(f"{aux_ctrl}.{divider_attr_nm}", channelBox=True)

        # ---------- blendshape attr ----------
        blendshape_attr_nm = f"{dynamic_crv}__blendShape"
        cmds.addAttr(
            aux_ctrl,
            longName=blendshape_attr_nm,
            niceName=blendshape_attr_nm,
            attributeType="double",
            defaultValue=0,
            minValue=0,
            maxValue=1,
            keyable=True,
        )
        cmds.connectAttr(
            f"{aux_ctrl}.{blendshape_attr_nm}",
            f"{blendshape_nd}.{dynamic_crv}",
        )
