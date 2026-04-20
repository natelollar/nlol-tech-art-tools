from importlib import reload
from pathlib import Path

from nlol.defaults import rig_folder_path
from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds, mel

reload(rig_folder_path)

materials_folderpath = rig_folder_path.rig_folderpath / "materials"
logger = get_logger()


def remove_meshes_namespaces(imported_nodes: list[str], imported_namespace: str = "") -> list[str]:
    """Delete meshes in list and remove list namespace.
    Useful when importing materials and unwanted mesh objects in file.

    Returns:
        List of imported objects without namespace.
        And with imported mesh transforms and shading groups deleted.

    """
    # delete imported mesh transforms and shading group nodes
    imp_delete_nodes = []
    for nd in imported_nodes:
        if cmds.objectType(nd) == "mesh":
            mesh_transform = cmds.listRelatives(nd, parent=True)
            imp_delete_nodes.append(mesh_transform[0])
        if cmds.objectType(nd) == "shadingEngine":  # shading group
            imp_delete_nodes.append(nd)
    imp_delete_nodes = list(set(imp_delete_nodes))  # remove duplicates
    if imp_delete_nodes:
        cmds.delete(imp_delete_nodes)

    # remove objects from imported list that not longer exist
    imported_nodes = [nd for nd in imported_nodes if cmds.objExists(nd)]

    # remove namespace
    if imported_namespace:
        cmds.namespace(removeNamespace=imported_namespace, mergeNamespaceWithRoot=True)
        imported_nodes = [nd.replace(f"{imported_namespace}:", "") for nd in imported_nodes]

    return imported_nodes


def export_materials() -> None:
    """Export materials for selected mesh transforms to individual ".ma" files.
    Exports to "materials" folder in nLol rig folder. Ex: "/auto_rig/materials/".
    """
    selected = cmds.ls(selection=True)
    mesh_selection = [obj for obj in selected if cmds.listRelatives(obj, shapes=True, type="mesh")]
    if not mesh_selection:
        cmds.warning("Nothing selected. Select mesh transforms with assigned materials to export.")
        return

    materials_folderpath.mkdir(exist_ok=True)

    for mesh in mesh_selection:
        shape = cmds.listRelatives(mesh, shapes=True)[0]
        shading_groups = cmds.listConnections(shape, type="shadingEngine")
        shading_groups = list(set(shading_groups))
        for shading_group in shading_groups:  # incase mesh has multiple materials on faces
            material = cmds.listConnections(f"{shading_group}.surfaceShader")
            material = material[0] if material else None
            arnold_material = cmds.listConnections(f"{shading_group}.aiSurfaceShader")
            arnold_material = arnold_material[0] if arnold_material else None
            logger.debug(f"{mesh = }")
            logger.debug(f"{shading_group = }")
            logger.debug(f"{material = }")
            logger.debug(f"{arnold_material = }")

            cmds.select(clear=True)
            if material:
                cmds.select(material, add=True)
            if arnold_material:
                cmds.select(arnold_material, add=True)
            if material or arnold_material:
                material_filename = material or f"{mesh.split('_')[0]}_mat"
                cmds.file(
                    materials_folderpath / material_filename,
                    force=True,
                    options="v=0;",
                    type="mayaAscii",
                    preserveReferences=True,
                    exportSelected=True,
                )
                logger.info(f"Exported: {materials_folderpath / material_filename}.ma")


def import_materials_to_selected(
    surface_shader: str = "standardSurface",
    ai_surface_shader: str = "openPBRSurface",
    use_material_name: bool = False,
) -> None:
    """Import Maya material files from nLol rig folderpath and apply them.
    Example folderpath: "/auto_rig/materials/"
    Uses name component to apply material. nLol mesh name component should be same as material.
    nLol naming convention: "<name>_<direction>_<id>_<type>"

    Args:
        surface_shader: Maya node type of material for connecting to shading group's
            ".surfaceShader" input.
        ai_surface_shader: Maya node type of material for connecting to shading group's
            ".aiSurfaceShader" input.
        use_material_name: Use assigned material name component to match exported material,
            instead of mesh name component.

    """
    selected = cmds.ls(selection=True)  # current selection
    mesh_selection = [obj for obj in selected if cmds.listRelatives(obj, shapes=True, type="mesh")]
    if not mesh_selection:
        logger.warning(f"Nothing selected for material import: {selected}")
        return

    # get previously exported material filepaths
    material_filepaths = list(materials_folderpath.glob("*.ma"))
    if not list(material_filepaths) or not Path(materials_folderpath).exists():
        error_msg = (
            f'Missing ".ma" material filepaths from: "{materials_folderpath}". '
            "Use nLol material export button."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    material_file_names = [Path(matpath).name for matpath in material_filepaths]
    material_name_components = [filename.split("_")[0] for filename in material_file_names]

    # main mesh selection iteration
    for mesh in mesh_selection:
        name_comp = mesh.split("_")[0]  # use mesh for name component
        # disconnect and remove old material
        shape = cmds.listRelatives(mesh, shapes=True)[0]
        shading_group = cmds.listConnections(shape, type="shadingEngine")
        shading_group = shading_group[0] if shading_group else None
        if shading_group:  # if no shading group, skip to prevent error
            connected = cmds.listConnections(shading_group, source=True, destination=False)
            connected_materials = [node for node in connected if node in cmds.ls(materials=True)]
            # use material for name component instead
            if use_material_name:  # requires material with matching name already assigned to mesh
                name_comp = connected_materials[0].split("_")[0]

        if use_material_name and not shading_group:
            logger.warning(
                f"Skipping mesh: {mesh}. No material for name component: {shading_group}",
            )
            continue

        if name_comp in material_name_components:
            logger.info(f"Material match found: {name_comp}_")
        else:
            logger.warning(f"Skipping mesh: {mesh}. No material match: {name_comp}_")
            continue

        # delete old materials
        if shading_group:
            for node in connected:
                if node in cmds.ls(materials=True):
                    cmds.delete(node)
            mel.eval("MLdeleteUnused;")
        # create SG, after deleting
        shading_group = cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=f"{name_comp}_matSG",
        )

        # import and find matching materials
        matching_material_filepath = [
            filepath for filepath in material_filepaths if f"{name_comp}_" in str(filepath)
        ][0]
        imported_nodes = cmds.file(
            matching_material_filepath,
            i=True,
            returnNewNodes=True,
            namespace="tempNamespace",
        )
        logger.debug(f"BEFORE: {imported_nodes = }")
        # remove unwanted meshes
        imported_nodes = remove_meshes_namespaces(imported_nodes, "tempNamespace")
        logger.debug(f"AFTER: {imported_nodes = }")

        matching_materials = [
            node for node in imported_nodes if node in cmds.ls(materials=True)
        ] or []
        if len(matching_materials) > 2:
            logger.warning(f"More than 2 materials matching mesh name: {matching_materials}")
        elif len(matching_materials) == 0:
            msg = f"No materials matching mesh name: {matching_materials}"
            logger.error(msg)
            raise ValueError(msg)

        # connect materials to shading group
        for matching_material in matching_materials:
            if cmds.objectType(matching_material) == surface_shader:
                cmds.connectAttr(f"{matching_material}.outColor", f"{shading_group}.surfaceShader")
            elif cmds.objectType(matching_material) == ai_surface_shader:
                cmds.connectAttr(
                    f"{matching_material}.outColor",
                    f"{shading_group}.aiSurfaceShader",
                )
        # assign material to mesh transform
        cmds.select(mesh)
        cmds.hyperShade(assign=matching_material)


def update_scene_materials(
    surface_shader: str = "standardSurface",
    ai_surface_shader: str = "openPBRSurface",
) -> None:
    """Update scene materials with same names as exported materials.
    If no selection, updates for all exported materials in scene, otherwise,
    will only update materials assigned to selected meshes.

    Args:
        surface_shader: Maya node type of material for connecting to shading group's
            ".surfaceShader" input.
        ai_surface_shader: Maya node type of material for connecting to shading group's
            ".aiSurfaceShader" input.

    """
    selected = cmds.ls(selection=True)
    mesh_selection = [obj for obj in selected if cmds.listRelatives(obj, shapes=True, type="mesh")]

    # get previously exported material filepaths
    material_filepaths = list(materials_folderpath.glob("*.ma"))
    if not list(material_filepaths) or not Path(materials_folderpath).exists():
        error_msg = (
            f'Missing ".ma" material filepaths from: "{materials_folderpath}". '
            "Use nLol material export shelf button to export materials."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)
    material_names = [Path(matpath).stem for matpath in material_filepaths]
    # check if materials exist in scene
    materials = [mat for mat in material_names if mat in cmds.ls(materials=True)]

    if mesh_selection:  # limit materials to those assigned to selected meshes
        connected_materials = set()
        for mesh in mesh_selection:
            shape = cmds.listRelatives(mesh, shapes=True)[0]
            shading_group = cmds.listConnections(shape, type="shadingEngine")
            connected_nodes = cmds.listConnections(shading_group, source=True, destination=False)
            connected_nodes = [node for node in connected_nodes if node in cmds.ls(materials=True)]
            connected_materials.update(connected_nodes)
        # check for materials assigned but not exported
        materials_leftout = [node for node in connected_materials if node not in material_names]
        materials_leftout = [
            node for node in materials_leftout if cmds.objectType(node) != ai_surface_shader
        ]
        if materials_leftout:
            logger.warning(f"Assigned materials not yet exported: {materials_leftout}")
        # limit to exported materials
        materials = [node for node in connected_materials if node in materials]

    logger.debug(f"{materials = }")

    # iterate exported materials
    for material in materials:
        shading_group = cmds.listConnections(material, type="shadingEngine")  # get SG
        # get nodes connected to shading group
        connected = cmds.listConnections(shading_group, source=True, destination=False)
        # get faces assigned to materials
        face_sets = cmds.sets(shading_group, query=True, nodesOnly=False)
        logger.debug(f"Faces: {face_sets}")

        # delete old materials
        for obj in connected:
            if obj in cmds.ls(materials=True):
                cmds.delete(obj)
        mel.eval("MLdeleteUnused;")
        # create SG, after deleting
        name_without_end = material.split("_")[:-1]
        name_comp = "_".join(name_without_end)
        shading_group = cmds.sets(
            renderable=True,
            noSurfaceShader=True,
            empty=True,
            name=f"{name_comp}_matSG",
        )

        # import and find matching materials
        matching_material_filepath = [
            filepath for filepath in material_filepaths if f"{name_comp}_" in str(filepath)
        ][0]
        imported_nodes = cmds.file(
            matching_material_filepath,
            i=True,
            returnNewNodes=True,
            namespace="tempNamespace",
        )
        imported_nodes = remove_meshes_namespaces(imported_nodes, "tempNamespace")
        matching_materials = [node for node in imported_nodes if node in cmds.ls(materials=True)]

        # connect materials to shading group
        for matching_material in matching_materials:
            if cmds.objectType(matching_material) == surface_shader:
                cmds.connectAttr(f"{matching_material}.outColor", f"{shading_group}.surfaceShader")
            elif cmds.objectType(matching_material) == ai_surface_shader:
                cmds.connectAttr(
                    f"{matching_material}.outColor",
                    f"{shading_group}.aiSurfaceShader",
                )

        # assign material to mesh transform
        for face_set in face_sets:
            cmds.select(face_set)
            logger.debug(f"{face_set = }")
            logger.debug(f"{matching_material = }")
            cmds.hyperShade(assign=matching_material)

        cmds.select(clear=True)
