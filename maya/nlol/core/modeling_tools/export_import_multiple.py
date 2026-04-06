from pathlib import Path

from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


class ExportImportMultiple:
    """Export or import multiple objects at the same time.
    Reimport and refresh Arnold standin nodes.
    """

    def check_load_plugin(self, plugin_name):
        """Check if loaded and if not load Maya plugin."""
        if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
            logger.info(f'Loading plugin: "{plugin_name}".  Consider auto loading plugin.')
            cmds.loadPlugin(plugin_name)

    def export_multiple(
        self,
        folderpath: Path | str,
        object_type: str,
        objects: list[str] | None = None,
    ):
        """Export multiple objects. Defaults to selected objects.
        Export to OBJ, FBX, MA, MB or ASS.

        Args:
            folderpath: Where to save exported objects to.
            object_type: Specific object type to export as.
            objects: A list of objects to export.
                Or leave blank to export selected.

        """
        if not objects:
            objects = cmds.ls(selection=True)

        if not Path(folderpath).exists():
            msg = f"Folder path does not exist: {folderpath}"
            logger.error(msg)
            raise ValueError(msg)

        match object_type:
            case "OBJexport":
                export_options = "groups=1;ptgroups=0;materials=0;smoothing=1;normals=1"
                self.check_load_plugin("objExport")
            case "FBX export":
                export_options = "v=0;"
                self.check_load_plugin("fbxmaya")
            case "mayaAscii":
                export_options = "v=0;"
            case "mayaBinary":
                export_options = "v=0;"
            case "ASS Export":
                export_options = "-boundingBox;-mask 14591;-lightLinks 1;-shadowLinks 1;-fullPath"
                self.check_load_plugin("mtoa")
            case _:
                msg = f"Unknown object type: {object_type}"
                logger.error(msg)
                raise ValueError(msg)

        for obj in objects:
            cmds.select(clear=True)
            cmds.select(obj)
            cmds.file(
                Path(folderpath) / obj,
                force=True,
                options=export_options,
                type=object_type,
                preserveReferences=True,
                exportSelected=True,
            )

    def import_multiple(
        self,
        filepaths: list[Path] | list[str],
        auto_remove_ns: bool = False,
    ):
        """Import multiple objects. Works with OBJ, FBX, MA, MB or ASS.

        Args:
            filepaths: A list of object filepaths.
            auto_remove_ns: Automatically remove the added "importedNs" namespace.

        """
        filepaths = [Path(filepath) for filepath in filepaths]
        for i, filepath in enumerate(filepaths):
            object_ext = filepath.suffix
            object_name = filepath.stem

            match object_ext:
                case ".obj":
                    import_options = "mo=1;lo=0"
                    self.check_load_plugin("objExport")
                case ".fbx":
                    import_options = ""
                    self.check_load_plugin("fbxmaya")
                case ".ma":
                    import_options = "v=0;"
                case ".mb":
                    import_options = "v=0;"
                case ".ass":
                    import_options = ""
                    self.check_load_plugin("mtoa")
                case _:
                    msg = f"Unknown object extension: {object_ext}"
                    logger.error(msg)
                    raise ValueError(msg)

            if object_ext in [".obj", ".fbx", ".ma", ".mb"]:
                if not cmds.namespace(exists="importedNs"):
                    cmds.namespace(add="importedNs")
                if object_ext == ".fbx":  # set namespace to avoid maya quirks
                    cmds.namespace(setNamespace="importedNs")
                else:
                    cmds.namespace(setNamespace=":")
                # import filepath
                cmds.file(
                    filepath,
                    i=True,  # import
                    ignoreVersion=True,
                    mergeNamespacesOnClash=True,
                    # renameAll=True,
                    namespace="importedNs",
                    force=True,
                    preserveReferences=True,
                    importTimeRange="keep",
                    options=import_options,
                )
                cmds.namespace(setNamespace=":")  # set namespace back to root

            elif object_ext == ".ass":  # import arnold proxy files differently
                standin_name = f"{object_name}AiStandIn"
                if cmds.objExists(standin_name):
                    logger.info(f'Already exists: "{standin_name}". Reloading filepath...')
                    standin_shape = cmds.listRelatives(standin_name, shapes=True)[0]
                    cmds.setAttr(f"{standin_shape}.dso", filepath, type="string")
                    cmds.dgdirty(standin_shape)  # refresh node
                    if i == len(filepaths) - 1:
                        logger.info("Refreshing scene...")
                        cmds.refresh(force=True)
                else:
                    standin_shape = cmds.createNode(
                        "aiStandIn",
                        name=f"{standin_name}Shape",
                    )
                    standin_transform = cmds.listRelatives(standin_shape, parent=True)[0]
                    cmds.rename(standin_transform, f"{standin_name}")
                    cmds.setAttr(f"{standin_shape}.dso", filepath, type="string")
                    cmds.setAttr(f"{standin_shape}.mode", 3)

        if auto_remove_ns:
            try:
                cmds.namespace(removeNamespace="importedNs", mergeNamespaceWithRoot=True)
            except Exception:
                logger.info('Namespace already removed: "importedNs"')
