from pathlib import Path

from maya import cmds
from nlol.defaults.rig_folder_path import rig_folderpath
from nlol.utilities.nlol_maya_logger import get_logger
from nlol.utilities.nlol_maya_registry import get_registry

logger = get_logger()
registry = get_registry()


class ImportRigModule:
    """Import custom rig files. These would be rig modules built previous to running rig build,
    and would live in a "*_rig" Maya file. They could also be manually built rig parts.
    Custom rig files will be imported during the rig module phase so parent spacing
    and control shapes still apply.

    Default location for the "custom_rig.ma" file will be the parent folder
    of the main nLol auto rig folder. For instance, ".../character/rig/custom_rig.ma",
    alongside ".../character/rig/auto_rig/rig_object_data.toml".

    When importing, materials and display layers will be combined if already existing in scene.
    """

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str,
        locators: list[str] = [],
        controls: list[str] = [],
        remove_namespace: bool = False,
        strip_namespace_from_materials: bool = True,
        reference: bool = False,
        custom_rig_filepath: Path | str = "",
        custom_rig_folderpath: Path | str = "",
        custom_rig_filename: str = "",
    ) -> None:
        """Initialize class.

        Args:
            rig_module_name: Custom name for the rig module.
            mirror_direction: Extra string describing mirror side. Ex. "left", "right".
            main_joints: The main skinned joints.
            locators: Where to position rig controls. Must match number of controls.
                Locator list index will match control index, so locator index 1
                will be position for control index 1. Locators should be added
                in "rig_helpers.ma" file, located in the rig folder.
                If no locators, controls will be left at imported position.
            controls: Controls to be positioned at locators. If no controls
                rig will be left at imported position.
            remove_namespace: Remove added namespace after importing.
            strip_namespace_from_materials: Will strip namespace from newly imported material nodes.
            reference: Whether to reference the rig file in.
            custom_rig_filepath: Full path to file, including filename and extension.
            custom_rig_folderpath: Full folder path for rig file. File name not included.
                Defaults to main nLol rig folder parent path.
            custom_rig_filename: Maya file name only, including extension. ".ma" or ".mb"

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.locators = locators
        self.controls = controls
        self.remove_namespace = remove_namespace
        self.strip_namespace_from_materials = strip_namespace_from_materials
        self.reference = reference

        self.import_rig_filepath = custom_rig_filepath
        if not self.import_rig_filepath:
            rig_folderpath_main = rig_folderpath()
            rig_folderpath_parent = custom_rig_folderpath or Path(rig_folderpath_main).parent
            rig_filename = custom_rig_filename or "custom_rig.ma"
            self.import_rig_filepath = Path(rig_folderpath_parent) / Path(rig_filename)

        logger.debug(f"Imported rig file: {self.import_rig_filepath}")

    def build(self) -> str:
        """Entry point. Run method to import and setup custom rig file.
        --------------------------------------------------

        Returns:
            Top rig group for custom rig file.

        """
        import_rig_grp = self.build_main()

        return import_rig_grp

    def build_main(self) -> str:
        """Import custom rig file to main rig scene. Add namespace.

        Returns:
            Top rig group for custom rig file.

        """
        # -----
        import_namespace = f"{self.mod_name}{self.mirr_side}rig"
        if self.reference:
            imported_nodes = cmds.file(
                str(self.import_rig_filepath),
                reference=True,
                returnNewNodes=True,
                namespace=import_namespace,
            )
        else:
            imported_nodes = cmds.file(
                str(self.import_rig_filepath),
                i=True,
                returnNewNodes=True,
                namespace=import_namespace,
            )

        # -----
        # leave at imported position if locators/controls not listed
        if self.locators and self.controls:
            if len(self.locators) == len(self.controls):
                # ----- get ctrl top parent grps
                ctrl_parent_grps = []
                for ctrl in self.controls:
                    top_ctrl_grp = f"{import_namespace}:{ctrl}Grp"
                    if cmds.objExists(top_ctrl_grp):
                        ctrl_parent_grps.append(f"{ctrl}Grp")
                if len(ctrl_parent_grps) == len(self.controls):
                    self.controls = ctrl_parent_grps
                # position ctrls/grps at locators
                for loc, ctrl in zip(self.locators, self.controls, strict=False):
                    cmds.matchTransform(
                        f"{import_namespace}:{ctrl}",
                        loc,
                        position=True,
                        rotation=True,
                    )
                    loc_scale = cmds.getAttr(f"{loc}.scale")[0]
                    cmds.setAttr(f"{import_namespace}:{ctrl}.scale", *loc_scale)
            else:
                msg = (
                    "Number of locators and controls must be same for import_rig_mod:  "
                    f"{self.mod_name}{self.mirr_side}rig"
                )
                logger.error(msg)
                raise ValueError(msg)

        # ----- group parenting
        top_nodes = cmds.ls(assemblies=True)
        import_top_nodes = [node for node in top_nodes if import_namespace in node]
        import_rig_grp = [node for node in import_top_nodes if "_rigGrp" in node]
        import_rig_grp = import_rig_grp[0] if import_rig_grp else ""
        import_skeletalmesh_grp = [node for node in import_top_nodes if "_skeletalMeshGrp" in node]
        import_skeletalmesh_grp = import_skeletalmesh_grp[0] if import_skeletalmesh_grp else ""

        main_rig_grp = registry.get_obj("main_rig_grp")
        if import_rig_grp and cmds.listRelatives(import_rig_grp, parent=True) != [main_rig_grp]:
            cmds.parent(import_rig_grp, main_rig_grp)
        main_skeletalmesh_grp = registry.get_obj("main_skeletalmesh_grp")
        if import_skeletalmesh_grp and cmds.listRelatives(import_skeletalmesh_grp, parent=True) != [
            main_skeletalmesh_grp,
        ]:
            cmds.parent(import_skeletalmesh_grp, main_skeletalmesh_grp)

        # ----- consolidate materials and display layers
        if not self.reference:
            # ----- assign materials if already exist. delete duplicate materials.
            scene_sgs = cmds.ls(type="shadingEngine")  # sgs == shader groups
            import_sgs = cmds.ls(imported_nodes, type="shadingEngine")

            previous_scene_sgs = [sg for sg in scene_sgs if sg not in import_sgs]
            previous_scene_sgs_dict = {sg.split(":")[-1]: sg for sg in previous_scene_sgs}
            for import_sg in import_sgs:
                import_sg_base_name = import_sg.split(":")[-1]
                existing_sg = previous_scene_sgs_dict.get(import_sg_base_name)

                import_sg_nodes = cmds.listHistory(
                    import_sg,
                    pruneDagObjects=True,
                )
                import_sg_nodes = [nd for nd in import_sg_nodes if "groupId" not in nd]

                if existing_sg:
                    objs_with_sg = cmds.sets(import_sg, query=True)
                    # assign existing material
                    cmds.sets(objs_with_sg, edit=True, forceElement=existing_sg)
                    # remove old material nodes
                    for node in import_sg_nodes:
                        if cmds.objExists(node):
                            cmds.delete(node)
                            logger.debug(f"Deleted: {node}")
                elif self.strip_namespace_from_materials:  # if first time material imported
                    for node in import_sg_nodes:
                        node_no_ns = node.replace(f"{import_namespace}:", "")
                        cmds.rename(node, node_no_ns)

            # ----- use existing display layers if exist. delete duplicate layers.
            scene_lyrs = cmds.ls(type="displayLayer")
            import_lyrs = cmds.ls(imported_nodes, type="displayLayer")
            previous_scene_lyrs = [lyr for lyr in scene_lyrs if lyr not in import_lyrs]
            previous_scene_lyrs_dict = {lyr.split(":")[-1]: lyr for lyr in previous_scene_lyrs}
            for import_lyr in import_lyrs:
                import_lyr_base_name = import_lyr.split(":")[-1]
                existing_lyr = previous_scene_lyrs_dict.get(import_lyr_base_name)
                if existing_lyr:
                    import_lyr_objs = cmds.editDisplayLayerMembers(import_lyr, query=True)
                    if import_lyr_objs:
                        cmds.editDisplayLayerMembers(existing_lyr, import_lyr_objs, noRecurse=True)
                    cmds.delete(import_lyr)
                    logger.debug(f'Replaced "{import_lyr}" with "{existing_lyr}".')
        else:
            msg = 'Imported rig is "referenced". Skipping material and display layer consolidation.'
            logger.debug(msg)

        # ----- delete locators
        for loc in self.locators:
            if cmds.objExists(loc):
                cmds.delete(loc)

        # ----- remove namespace
        if self.remove_namespace:
            cmds.namespace(removeNamespace=import_namespace, mergeNamespaceWithRoot=True)
            import_rig_grp = import_rig_grp.replace(f"{import_namespace}:", "")
            return import_rig_grp

        return import_rig_grp
