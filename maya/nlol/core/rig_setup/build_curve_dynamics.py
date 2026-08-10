import json
from importlib import reload
from pathlib import Path

from maya import cmds, mel
from nlol.core.rig_setup import common_build_components
from nlol.core.rig_tools import rigging_functions, tools_skinning
from nlol.defaults.rig_folder_path import rig_folderpath
from nlol.utilities import nlol_maya_logger, nlol_maya_registry

reload(common_build_components)
reload(rigging_functions)
reload(tools_skinning)

registry = nlol_maya_registry.get_registry()
logger = nlol_maya_logger.get_logger()


class CurveDynamics:
    """General curve dynamics setup using Maya's nHair system.
    Useful for tentacles or tubes.
    """

    def __init__(self) -> None:
        """Initialize class."""
        self.dynamics_data_folderpath = rig_folderpath() / "dynamics_data"

    def build(
        self,
        curves: list[str] | str,
        use_existing_hairsystem: bool = False,
        hairsystem_name: str = "",
    ) -> None:
        """Entry point. Run this method.
        --------------------------------------------------

        Args:
            See following methods.

        """
        # run main methods
        cmds.undoInfo(openChunk=True)
        try:
            self.CommonBuildComponents = common_build_components.CommonBuildComponents()
            self.CommonBuildComponents.build_top_dynamics_grps()
            self.CommonBuildComponents.build_dynamics_aux_ctrl()
            self.build_dynamics_on_crvs(
                curves=curves,
                use_existing_hairsystem=use_existing_hairsystem,
                hairsystem_name=hairsystem_name,
            )
            self.apply_hair_settings()
        finally:
            cmds.undoInfo(closeChunk=True)

    def build_dynamics_on_crvs(
        self,
        curves: list[str] | str,
        create_restpose_curves: bool = True,
        use_existing_hairsystem: bool = False,
        hairsystem_name: str = "",
    ) -> None:
        """Apply dynamics to curves via nHair system and blendshape. With attributes via
        dynamics aux ctrl.

        Args:
            curves: Curve/s to apply dynamics too.
            create_restpose_curves: Whether to duplicate curve and copy skin weights
                to avoid cycle warning from blendshape.
            use_existing_hairsystem: Use existing hair system in scene.
                Does not need to be specified.  Still creates initial hair system if needed.
            hairsystem_name: Specify nHair system transform node.
                Use existing or will create first time with this name. Not required.

        """
        if isinstance(curves, str):
            curves = [curves]

        for crv in curves:
            self.build_dynamics_on_crv(
                curve=crv,
                create_restpose_curve=create_restpose_curves,
                use_existing_hairsystem=use_existing_hairsystem,
                hairsystem_name=hairsystem_name,
            )

    def build_dynamics_on_crv(
        self,
        curve: str,
        create_restpose_curve: bool = True,
        use_existing_hairsystem: bool = False,
        hairsystem_name: str = "",
    ) -> None:
        """Applying curve dynamics to single curve.
        Duplicate curve first if needed for separate rest pose curve.
        Copy skin weights from original curve if needed.
        Apply final dynamic curve to original curve as blendshape.
        Add attributes to global dynamics ctrl for rig.

        "use_existing_hairsystem" will use previous hair system in scene.
        Though, still creates hair system first and then deletes/ replaces
        with initial hair system.
        "hairsystem_name" uses specific previous hair system or initially creates
        with name.  Will still create and delete hair systems, though will replace
        with this specific one.

        Args:
            curve: Main curve which will end up with the blendshape
                connected to the dynamics curve.
            create_restpose_curve: Whether to duplicate the main curve.
                This new curve would be the restpose curve with same skin weights.
                This helps avoid cycle error when connecting the dynamics curve as
                a blendshape back to the original.
            use_existing_hairsystem: Use existing hair system in scene.
                Does not need to be specified. Still creates initial hair system if needed.
            hairsystem_name: Maya nHair system node transform to use and create first
                if doesn't exist.

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
        hair_system = cmds.listConnections(
            follicle_shp,
            source=False,
            destination=True,
            type="hairSystem",
        )[0]
        if hairsystem_name and not cmds.objExists(hairsystem_name):
            hair_system = cmds.rename(hair_system, hairsystem_name)
        else:
            hair_system = cmds.rename(hair_system, f"{restpose_crv}HairSystem")
        cmds.setAttr(f"{hair_system}.drag", 0.1)  # slows overall movement slightly
        cmds.setAttr(f"{hair_system}.damp", 0.3)  # kills bounce
        cmds.setAttr(f"{hair_system}.stretchDamp", 0.5)  # damping along the length
        cmds.parent(hair_system, dynamics_components_grp)
        hair_system_shp = cmds.listRelatives(hair_system, shapes=True)[0]

        # ----- reconnect main nucleus.
        # fails to connect with nucleus selection for makeCurvesDynamic.
        current_nucleus_nd = cmds.listConnections(hair_system_shp, type="nucleus")[0]
        if nucleus_nd and current_nucleus_nd != nucleus_nd:
            rigging_functions.replace_node_connections(
                old_node=current_nucleus_nd,
                new_node=nucleus_nd,
                delete_old_node=True,
                increment_input_dest_plug=True,
                increment_output_src_plug=True,
            )

        # -----
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

        # replace current hair system w/ existing hair system
        # or skip and use separate hair system for each curve
        existing_hairsystem_shp = None
        if use_existing_hairsystem:
            hair_systems = cmds.ls(type="hairSystem")
            if hair_systems:
                existing_hairsystem_shp = hair_systems[0]  # hair system shape node
        if hairsystem_name:
            existing_hairsystem_shp = cmds.listRelatives(hairsystem_name, shapes=True)[0]
        if use_existing_hairsystem or hairsystem_name:
            if hair_system_shp != existing_hairsystem_shp:
                rigging_functions.replace_node_connections(
                    old_node=hair_system_shp,
                    new_node=existing_hairsystem_shp,
                    delete_old_node_parent=True,  # delete unused hair system transform
                    increment_input_dest_plug=True,
                    increment_output_src_plug=True,
                    # avoid duplicate connections
                    skipped_output_connections={"inputActive", "inputActiveStart"},
                )

        # dynamic curve attributes
        if existing_hairsystem_shp:
            hair_system_shp = existing_hairsystem_shp
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

    def apply_hair_settings(self) -> None:
        """Apply saved hairSystem, follicle, or nucleus settings from "*Settings.json"
        files in dynamics_data folder. Files must also contain string
        "hairSystem", "follicle", or "nucleus"; not case sensitive.
        """
        hair_settings = self.get_saved_hair_settings()
        for settings in hair_settings:
            # ----- check if hair/dynamics object exists yet
            dynamics_obj = next(iter(settings["main"].keys()), None)
            if not dynamics_obj:  # skip if dict empty
                continue
            dynamics_obj = dynamics_obj.split(".")[0]
            if not cmds.objExists(dynamics_obj):
                continue
            # ----- apply main hair settings -----
            for attr, value in settings["main"].items():
                try:
                    if isinstance(value, list) and any(isinstance(v, (list, tuple)) for v in value):
                        value = value[0]
                        if not value:
                            continue
                        cmds.setAttr(attr, *value)
                    elif attr.split(".")[1] in {"startCurveAttract", "startFrame"}:
                        connections = cmds.listConnections(  # aux ctrl connection
                            attr,
                            source=True,
                            destination=False,
                            plugs=True,
                        )
                        if connections:
                            cmds.setAttr(connections[0], value)
                        else:
                            cmds.setAttr(attr, value)
                    else:
                        cmds.setAttr(attr, value)

                    msg = f"Settings applied: {attr}, {value}"
                    logger.debug(msg)
                except Exception:
                    logger.debug(
                        f"Failed to set hairSystem/follicle/nucleus attr: {attr}, {value}",
                    )

    def get_saved_hair_settings(self) -> list[dict]:
        """Get saved hairSystem, follicle, or nucleus settings.
        These settings will be in "*Settings.json" files in the dynamics_data folder.
        Files must also contain string "hairSystem", "follicle", or "nucleus", not case sensitive.

        Returns:
            A list of saved settings for hairSystem, follicle, or nucleus objects.

        """
        hair_settings_filepaths = list(self.dynamics_data_folderpath.glob("*Settings.json"))
        hair_settings_filepaths = [
            pth
            for pth in hair_settings_filepaths
            if any(
                keyword in Path(pth).stem.lower()
                for keyword in ["hairsystem", "follicle", "nucleus"]
            )
        ]
        if not list(hair_settings_filepaths):
            msg = (
                "No custom hairSystem, follicle, or nucleus "
                f'settings in: "{self.dynamics_data_folderpath}"\n'
                'Try adding "hairSystem", "follicle", "nucleus" or "Settings" string '
                "to file names if string missing. "
            )
            logger.debug(msg)

        hair_settings = []
        for settings_file in hair_settings_filepaths:
            with open(settings_file) as f:
                settings = json.load(f)
                hair_settings.append(settings)

        return hair_settings

    def save_hair_settings(self) -> None:
        """Save nHair, follicle, or nucleus settings to a json file per object."""
        nhair_settings, follicle_settings, nucleus_settings = self.get_selected_hair_settings()
        self.dynamics_data_folderpath.mkdir(exist_ok=True)

        obj_settings = nhair_settings | follicle_settings | nucleus_settings
        if not obj_settings:
            logger.info(
                "Select hairSystems, follicles, and/or nucleus' to save. Missing selection...",
            )

        for obj, settings in obj_settings.items():
            obj_settings_filepath = self.dynamics_data_folderpath / f"{obj}Settings.json"
            with open(obj_settings_filepath, "w") as f:
                json.dump(settings, f, indent=4)
                msg = f"Settings saved: {obj_settings_filepath}"
                logger.info(msg)

    def get_selected_hair_settings(self) -> tuple[dict, dict]:
        """Get hair system settings from selected nHair objects.
        Also, get settings for selected follicles, such as ".pointLock".
        Used for storing dynamic curve settings, contained in both hair systems
        and follicles. In addition, saves selected nucleus settings too.

        Returns:
            Dictionaries with nHair, follicle, and nucleus settings for each selected.

        """
        selected = cmds.ls(selection=True)
        sim_objs = {"hairSystem": [], "follicle": [], "nucleus": []}
        for obj in selected:
            shapes = cmds.listRelatives(obj, shapes=True)
            shape = shapes[0] if shapes else None
            if shape:
                shape_type = cmds.objectType(shape)
                if shape_type in sim_objs:
                    sim_objs[shape_type].append(shape)
            else:
                node_type = cmds.objectType(obj)
                if node_type in sim_objs:
                    sim_objs[node_type].append(obj)

        nhair_objs = sim_objs["hairSystem"]
        follicle_objs = sim_objs["follicle"]
        nucleus_objs = sim_objs["nucleus"]

        nhair_settings = self.get_hair_obj_settings(nhair_objs)
        follicle_settings = self.get_hair_obj_settings(follicle_objs)
        nucleus_settings = self.get_hair_obj_settings(nucleus_objs)

        return nhair_settings, follicle_settings, nucleus_settings

    def get_hair_obj_settings(self, objs: list[str]) -> dict[str, dict]:
        """Get Maya object settings.

        Args:
            objs: hairSystem/follicle transforms (or nucleus) to get attributes and values for.

        """
        hair_ramps = [
            "attractionScale",
            "stiffnessScale",
            "clumpWidthScale",
            "clumpCurl",
            "clumpFlatness",
            "hairWidthScale",
            "displacementScale",
        ]

        settings = {}
        for obj in objs:
            settings[obj] = {"main": {}}
            for attr in cmds.listAttr(obj, keyable=True, settable=True, visible=True) or []:
                try:
                    settings[obj]["main"][f"{obj}.{attr}"] = cmds.getAttr(f"{obj}.{attr}")
                except Exception as e:
                    logger.debug(f"Skipped {obj}.{attr}: {e}")

            for ramp in hair_ramps:
                if not cmds.objExists(f"{obj}.{ramp}"):
                    continue
                for i in range(cmds.getAttr(f"{obj}.{ramp}", size=True)):
                    for sub_attr in ("Position", "FloatValue", "Interp"):
                        key = f"{obj}.{ramp}[{i}].{ramp}_{sub_attr}"
                        settings[obj]["main"][key] = cmds.getAttr(key)

        return settings
