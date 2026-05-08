import re
from pathlib import Path

from nlol.core.general_utils import cap
from nlol.core.rig_tools.name_components import NlolNameComponents
from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

nlol_name_components = NlolNameComponents()
join_nm_comps = nlol_name_components.join_nm_comps
find_name_comps = nlol_name_components.find_name_comps
logger = get_logger()


class ArnoldMaterialSetup:
    def arnold_basic_mat(
        self,
        substance_material: bool = False,
        megascans_material: bool = False,
        use_arnold_file_nodes: bool = False,
    ) -> None:
        """Setup Arnold material based on selection of 3 input textures (from Marmoset Toolbag
        or Substance Painter) and an empty Maya shading group. Use drag and drop to add texture
        file nodes to Maya. Required selection: Color map, Mix map, Normal map, Shading Group.
        (3 "file" nodes and 1 "shadingEngine" node)

        Args:
            substance_material: Use Substance Painter - Unreal 4 (Packed) text naming,
                to identify selected texture file nodes.
            megascans_material: Assume Megascans environment asset files;
                Albedo, Roughness, and Normal.
            use_arnold_file_nodes: Use Arnold aiiamge nodes instead of regular Maya file nodes,
                when connecting to Arnold material.  Still drag and drop,
                    and select file nodes before running method.

        """
        self.substance_material = substance_material
        self.megascans_material = megascans_material

        # ----------------------------------------------------------------------
        selected = cmds.ls(selection=True)  # 3 image file nodes, 1 shading group node
        shading_nds = [obj for obj in selected if cmds.objectType(obj) == "shadingEngine"]
        shading_nd = shading_nds[0]  # shading group node
        file_nds = [obj for obj in selected if cmds.objectType(obj) == "file"]

        # ----------------------------------------------------------------------
        # error checking
        if len(file_nds) != 3:
            msg = "Select exactly 3 file nodes. Albedo, mixmap, and normal."
            logger.error(msg)
            raise ValueError(msg)
        if len(shading_nds) != 1:
            msg = "Select 1 empty shading group node."
            logger.error(msg)
            raise ValueError(msg)

        # ----------------------------------------------------------------------
        # map suffixes
        if self.substance_material:
            albedo_str = "BaseColor"
            mixmap_str = "OcclusionRoughnessMetallic"
            normal_str = "Normal"
        elif self.megascans_material:
            albedo_str = "Albedo"
            mixmap_str = "Roughness"
            normal_str = "Normal"
        else:
            albedo_str = "albedo"
            mixmap_str = "mixmap"
            normal_str = "normal"

        albedo_file_nd = [obj for obj in selected if albedo_str.lower() in obj.lower()][0]
        mixmap_file_nd = [obj for obj in selected if mixmap_str.lower() in obj.lower()][0]
        normal_file_nd = [obj for obj in selected if normal_str.lower() in obj.lower()][0]

        udims_fild_nds = []
        for file_nd in file_nds:
            texture_name = Path(cmds.getAttr(f"{file_nd}.fileTextureName")).name
            if "100" in texture_name:
                udims_fild_nds.append(file_nd)

        # get name comp
        file_nd_1 = file_nds[0]  # first file node
        file_nd_1_filepath = Path(cmds.getAttr(f"{file_nd_1}.fileTextureName"))
        if self.megascans_material:
            name_comp = file_nd_1_filepath.parent.name
            if name_comp.lower() == "atlas":
                name_comp = file_nd_1_filepath.parents[2].name

            name_comp_no_wspace = re.sub(r"\s+", "", name_comp)
            name_comp_split = name_comp_no_wspace.split("_")
            name_comp_split = [cap(txt) for txt in name_comp_split]
            name_comp = "".join(name_comp_split)
        else:
            name_comp = file_nd_1.split("_")[0]
        # get lod str
        normal_file_nd_filepath = Path(cmds.getAttr(f"{normal_file_nd}.fileTextureName"))
        lod_str = re.search(r"_LOD(\d)", normal_file_nd_filepath.stem)
        if lod_str:
            lod_str = lod_str.group(0).strip("_")
            lod_str = lod_str + "_"
        else:
            lod_str = ""

        # ----------------------------------------------------------------------
        # create shading nodes
        stnd_surface_nd = cmds.shadingNode(
            "standardSurface",
            asShader=True,
            name=f"{name_comp}_{lod_str}mat",
        )
        open_pbr_nd = cmds.shadingNode(
            "openPBRSurface",
            asShader=True,
            name=f"{name_comp}_{lod_str}matArnold",
        )
        bump_nd = cmds.shadingNode(
            "bump2d",
            asUtility=True,
            name=f"{name_comp}Normal_{lod_str}bump2d",
        )
        normal_arnold_nd = cmds.shadingNode(
            "aiNormalMap",
            asUtility=True,
            name=f"{name_comp}Normal_{lod_str}aiNormalMap",
        )
        if self.megascans_material:
            ao_ramp_nd = None
            rough_ramp_nd = cmds.shadingNode(
                "ramp",
                asTexture=True,
                name=f"{name_comp}Roughness_{lod_str}ramp",
            )
            metal_ramp_nd = None
        else:
            ao_ramp_nd = cmds.shadingNode("ramp", asTexture=True, name=f"{name_comp}Occlusion_ramp")
            rough_ramp_nd = cmds.shadingNode(
                "ramp",
                asTexture=True,
                name=f"{name_comp}Roughness_{lod_str}ramp",
            )
            metal_ramp_nd = cmds.shadingNode(
                "ramp",
                asTexture=True,
                name=f"{name_comp}Metalness_{lod_str}ramp",
            )

        # ----------------------------------------------------------------------
        # connect nodes
        # shading group connections
        cmds.connectAttr(f"{stnd_surface_nd}.outColor", f"{shading_nd}.surfaceShader")
        cmds.connectAttr(f"{open_pbr_nd}.outColor", f"{shading_nd}.aiSurfaceShader")
        # ----- standard surface connections -----
        cmds.connectAttr(f"{albedo_file_nd}.outColor", f"{stnd_surface_nd}.baseColor")
        cmds.connectAttr(f"{normal_file_nd}.outAlpha", f"{bump_nd}.bumpValue")
        cmds.connectAttr(f"{bump_nd}.outNormal", f"{stnd_surface_nd}.normalCamera")

        if self.megascans_material:
            cmds.connectAttr(f"{mixmap_file_nd}.outColorG", f"{stnd_surface_nd}.specularRoughness")
        else:
            cmds.connectAttr(f"{mixmap_file_nd}.outColorR", f"{stnd_surface_nd}.base")
            cmds.connectAttr(f"{mixmap_file_nd}.outColorG", f"{stnd_surface_nd}.specularRoughness")
            cmds.connectAttr(f"{mixmap_file_nd}.outColorB", f"{stnd_surface_nd}.metalness")

        # ----- open pbr connections -----
        if self.megascans_material:
            self.mixmap_r_plug = None
            self.mixmap_g_plug = f"{rough_ramp_nd}.vCoord"
            self.mixmap_b_plug = None
            cmds.connectAttr(f"{mixmap_file_nd}.outColorG", self.mixmap_g_plug)
            cmds.connectAttr(f"{rough_ramp_nd}.outAlpha", f"{open_pbr_nd}.specularRoughness")
        else:
            self.mixmap_r_plug = f"{ao_ramp_nd}.vCoord"
            self.mixmap_g_plug = f"{rough_ramp_nd}.vCoord"
            self.mixmap_b_plug = f"{metal_ramp_nd}.vCoord"
            cmds.connectAttr(f"{mixmap_file_nd}.outColorR", self.mixmap_r_plug)
            cmds.connectAttr(f"{mixmap_file_nd}.outColorG", self.mixmap_g_plug)
            cmds.connectAttr(f"{mixmap_file_nd}.outColorB", self.mixmap_b_plug)
            cmds.connectAttr(f"{ao_ramp_nd}.outAlpha", f"{open_pbr_nd}.baseWeight")
            cmds.connectAttr(f"{rough_ramp_nd}.outAlpha", f"{open_pbr_nd}.specularRoughness")
            cmds.connectAttr(f"{metal_ramp_nd}.outAlpha", f"{open_pbr_nd}.baseMetalness")

        self.albedo_plug = f"{open_pbr_nd}.baseColor"
        self.normal_plug = f"{normal_arnold_nd}.input"
        cmds.connectAttr(f"{albedo_file_nd}.outColor", self.albedo_plug)
        cmds.connectAttr(f"{normal_file_nd}.outColor", self.normal_plug)
        cmds.connectAttr(f"{normal_arnold_nd}.outValue", f"{open_pbr_nd}.normalCamera")

        # ----------------------------------------------------------------------
        # adjust node settings
        cmds.setAttr(f"{bump_nd}.bumpInterp", 1)  # tangent space normals
        cmds.setAttr(f"{albedo_file_nd}.ignoreColorSpaceFileRules", 1)
        cmds.setAttr(f"{mixmap_file_nd}.ignoreColorSpaceFileRules", 1)
        cmds.setAttr(f"{mixmap_file_nd}.colorSpace", "Raw", type="string")
        cmds.setAttr(f"{normal_file_nd}.ignoreColorSpaceFileRules", 1)
        cmds.setAttr(f"{normal_file_nd}.colorSpace", "Raw", type="string")
        # enable udim tiling mode
        for file_nd in udims_fild_nds:
            cmds.setAttr(f"{file_nd}.uvTilingMode", 3)
            cmds.setAttr(f"{file_nd}.uvTileProxyQuality", 1)  # 1k preview
        # other settings
        if not self.megascans_material:
            cmds.setAttr(f"{ao_ramp_nd}.colorEntryList[0].color", 0.50, 0.50, 0.50)
            cmds.setAttr(f"{ao_ramp_nd}.colorEntryList[1].color", 1.0, 1.0, 1.0)
            cmds.setAttr(f"{ao_ramp_nd}.colorEntryList[1].position", 1.0)

        if self.substance_material:  # account for inverted G/Y normal
            # invert arnold normal node G/Y
            cmds.setAttr(f"{normal_arnold_nd}.invertY", 1)
            # invert G/Y normal for viewport 2.0 bump2D setup
            normalvp2_file_nd = cmds.duplicate(normal_file_nd)[0]
            plusminus_gain_nd = cmds.shadingNode(
                "plusMinusAverage",
                asUtility=True,
                name=f"{name_comp}NormalVp2Gain_plusMinusAverage",
            )
            cmds.setAttr(f"{plusminus_gain_nd}.input3D[0]", 1.0, -1.0, 1.0)
            cmds.connectAttr(f"{plusminus_gain_nd}.output3D", f"{normalvp2_file_nd}.colorGain")
            plusminus_offset_nd = cmds.shadingNode(
                "plusMinusAverage",
                asUtility=True,
                name=f"{name_comp}NormalVp2Offset_plusMinusAverage",
            )
            cmds.setAttr(f"{plusminus_offset_nd}.input3D[0]", 0.0, 1.0, 0.0)
            cmds.connectAttr(f"{plusminus_offset_nd}.output3D", f"{normalvp2_file_nd}.colorOffset")

            cmds.connectAttr(
                f"{normalvp2_file_nd}.outAlpha",
                f"{bump_nd}.bumpValue",
                force=True,
            )

            file_nds.append(normalvp2_file_nd)

        # ----------------------------------------------------------------------
        # connect single place2dTexture node to all image file nodes
        place2d_nd = cmds.shadingNode(
            "place2dTexture",
            asUtility=True,
            name=f"{name_comp}_{lod_str}place2dTexture",
        )
        # connect new place2dTexture node to image file nodes
        self.connect_place2d_nd(place2d_nd, file_nds)

        # ----------------------------------------------------------------------
        # rename nodes
        albedo_file_nd = cmds.rename(albedo_file_nd, f"{name_comp}{cap(albedo_str)}_{lod_str}file")
        mixmap_file_nd = cmds.rename(mixmap_file_nd, f"{name_comp}{cap(mixmap_str)}_{lod_str}file")
        normal_file_nd = cmds.rename(normal_file_nd, f"{name_comp}{cap(normal_str)}_{lod_str}file")
        if self.substance_material:
            cmds.rename(normalvp2_file_nd, f"{name_comp}{cap(normal_str)}Vp2_{lod_str}file")
        shading_nd = cmds.rename(shading_nd, f"{name_comp}_{lod_str}matSG")

        # ----------------------------------------------------------------------
        msg = (
            f'---------- Material Created!: "{open_pbr_nd}", "{stnd_surface_nd}", '
            f'"{shading_nd}" ----------\n'
            'Ignore any ".ignoreColorSpaceFileRules" and ".uvTilingMode" deferred errors...'
        )
        logger.info(msg)

        # ----------------------------------------------------------------------
        self.name_comp = name_comp
        self.lod_str = lod_str
        self.albedo_file_nd = albedo_file_nd
        self.mixmap_file_nd = mixmap_file_nd
        self.normal_file_nd = normal_file_nd
        self.albedo_str = albedo_str
        self.mixmap_str = mixmap_str
        self.normal_str = normal_str

        # ----------------------------------------------------------------------
        if use_arnold_file_nodes:
            self.setup_arnold_image_nodes()

    def setup_arnold_image_nodes(self) -> None:
        """Use Arnold file nodes (aiImage) instead of regular Maya file nodes (file)
        for Arnold material.
        """
        albedo_aiimage = cmds.shadingNode(
            "aiImage",
            asTexture=True,
            name=f"{self.name_comp}{cap(self.albedo_str)}_{self.lod_str}aiImage",
        )
        mixmap_aiimage = cmds.shadingNode(
            "aiImage",
            asTexture=True,
            name=f"{self.name_comp}{cap(self.mixmap_str)}_{self.lod_str}aiImage",
        )
        normal_aiimage = cmds.shadingNode(
            "aiImage",
            asTexture=True,
            name=f"{self.name_comp}{cap(self.normal_str)}_{self.lod_str}aiImage",
        )
        albedo_filepath = Path(cmds.getAttr(f"{self.albedo_file_nd}.fileTextureName")).as_posix()
        mixmap_filepath = Path(cmds.getAttr(f"{self.mixmap_file_nd}.fileTextureName")).as_posix()
        normal_filepath = Path(cmds.getAttr(f"{self.normal_file_nd}.fileTextureName")).as_posix()
        updated_filepaths = []
        for filepath in [albedo_filepath, mixmap_filepath, normal_filepath]:
            if re.search(r"(\.)(\d{4})(\.)", filepath):  # replace .1001. with <UDIM>
                filepath = re.sub(r"(\.)(\d{4})(\.)", r".<UDIM>.", filepath)
            updated_filepaths.append(filepath)
        albedo_filepath, mixmap_filepath, normal_filepath = updated_filepaths

        cmds.setAttr(f"{albedo_aiimage}.filename", albedo_filepath, type="string")
        cmds.setAttr(f"{mixmap_aiimage}.filename", mixmap_filepath, type="string")
        cmds.setAttr(f"{normal_aiimage}.filename", normal_filepath, type="string")
        cmds.setAttr(f"{albedo_aiimage}.ignoreColorSpaceFileRules", 1)
        cmds.setAttr(f"{mixmap_aiimage}.ignoreColorSpaceFileRules", 1)
        cmds.setAttr(f"{normal_aiimage}.ignoreColorSpaceFileRules", 1)
        cmds.setAttr(f"{mixmap_aiimage}.colorSpace", "Raw", type="string")
        cmds.setAttr(f"{normal_aiimage}.colorSpace", "Raw", type="string")

        cmds.connectAttr(f"{albedo_aiimage}.outColor", self.albedo_plug, force=True)
        cmds.connectAttr(f"{normal_aiimage}.outColor", self.normal_plug, force=True)
        if self.megascans_material:
            cmds.connectAttr(f"{mixmap_aiimage}.outColorG", self.mixmap_g_plug, force=True)
        else:
            cmds.connectAttr(f"{mixmap_aiimage}.outColorR", self.mixmap_r_plug, force=True)
            cmds.connectAttr(f"{mixmap_aiimage}.outColorG", self.mixmap_g_plug, force=True)
            cmds.connectAttr(f"{mixmap_aiimage}.outColorB", self.mixmap_b_plug, force=True)

        if self.substance_material:
            cmds.delete(self.normal_file_nd)

    def connect_place2d_nd(self, place2d_nd: str, file_nds: list[str]) -> None:
        """Connect a single place2dTexture node to multiple image file nodes.
        Delete old place2dTexture node if exist.

        Args:
            place2d_nd: The place2dTexture to be connected to the image file nodes.
            file_nds: The list of file nodes to be connected to the single place2dTexture node.

        """
        if not isinstance(file_nds, (list, tuple)):
            file_nds = [file_nds]

        for file_nd in file_nds:
            # delete old place2dTexture nodes
            old_place2d_nd = cmds.listConnections(file_nd, type="place2dTexture")
            if old_place2d_nd:
                old_place2d_nd = list(set(old_place2d_nd))[0]
                cmds.delete(old_place2d_nd)

            # connect new place2d node to file node
            cmds.connectAttr(f"{place2d_nd}.outUV", f"{file_nd}.uvCoord", force=True)
            cmds.connectAttr(f"{place2d_nd}.outUvFilterSize", f"{file_nd}.uvFilterSize", force=True)
            cmds.connectAttr(f"{place2d_nd}.coverage", f"{file_nd}.coverage", force=True)
            cmds.connectAttr(
                f"{place2d_nd}.translateFrame",
                f"{file_nd}.translateFrame",
                force=True,
            )
            cmds.connectAttr(f"{place2d_nd}.rotateFrame", f"{file_nd}.rotateFrame", force=True)
            cmds.connectAttr(f"{place2d_nd}.mirrorU", f"{file_nd}.mirrorU", force=True)
            cmds.connectAttr(f"{place2d_nd}.mirrorV", f"{file_nd}.mirrorV", force=True)
            cmds.connectAttr(f"{place2d_nd}.stagger", f"{file_nd}.stagger", force=True)
            cmds.connectAttr(f"{place2d_nd}.wrapU", f"{file_nd}.wrapU", force=True)
            cmds.connectAttr(f"{place2d_nd}.wrapV", f"{file_nd}.wrapV", force=True)
            cmds.connectAttr(f"{place2d_nd}.repeatUV", f"{file_nd}.repeatUV", force=True)
            cmds.connectAttr(f"{place2d_nd}.vertexUvOne", f"{file_nd}.vertexUvOne", force=True)
            cmds.connectAttr(f"{place2d_nd}.vertexUvTwo", f"{file_nd}.vertexUvTwo", force=True)
            cmds.connectAttr(f"{place2d_nd}.vertexUvThree", f"{file_nd}.vertexUvThree", force=True)
            cmds.connectAttr(
                f"{place2d_nd}.vertexCameraOne",
                f"{file_nd}.vertexCameraOne",
                force=True,
            )
            cmds.connectAttr(f"{place2d_nd}.noiseUV", f"{file_nd}.noiseUV", force=True)
            cmds.connectAttr(f"{place2d_nd}.offset", f"{file_nd}.offset", force=True)
            cmds.connectAttr(f"{place2d_nd}.rotateUV", f"{file_nd}.rotateUV", force=True)

    def convert_file_to_aiimage(self, delete_old: bool = True) -> None:
        """Convert Maya file node to Arnold aiimage node.
        And delete selected "place2dTexture" nodes.
        Useful if dragging and dropping in images to hypershade.

        Args:
            delete_old: Delete old file node.

        """
        selected = cmds.ls(selection=True)
        if delete_old:
            place2d_nds = [nd for nd in selected if cmds.objectType(nd) == "place2dTexture"]
            cmds.delete(place2d_nds)
            for nd in place2d_nds:
                selected.remove(nd)
        selected = [nd for nd in selected if cmds.objectType(nd) == "file"]

        for file_nd in selected:
            # name components
            name_comp = file_nd.split("_")[0]
            descriptors = [
                "BaseColor",
                "OcclusionRoughnessMetallic",
                "Roughness",
                "Normal",
                "albedo",
                "mixmap",
            ]
            matched_descriptor = next(
                (d for d in descriptors if d.lower() in file_nd.lower()),
                None,
            )
            if matched_descriptor:
                name_comp = name_comp.replace(matched_descriptor, "")  # avoid duplicate
                aiimage_name = f"{name_comp}{cap(matched_descriptor)}"
            else:
                aiimage_name = file_nd.replace("_file", "_aiImage")

            # create arnold file node
            aiimage_nd = cmds.shadingNode(
                "aiImage",
                asTexture=True,
                name=f"{aiimage_name}_aiImage",
            )

            # copy over filepath string
            filepath = Path(cmds.getAttr(f"{file_nd}.fileTextureName")).as_posix()
            if re.search(r"(\.)(\d{4})(\.)", filepath):  # replace .1001. with <UDIM>
                filepath = re.sub(r"(\.)(\d{4})(\.)", r".<UDIM>.", filepath)
            cmds.setAttr(f"{aiimage_nd}.filename", filepath, type="string")

            # copy over other settings
            aiimage_nd_ignorecolorspace = cmds.getAttr(f"{file_nd}.ignoreColorSpaceFileRules")
            cmds.setAttr(f"{aiimage_nd}.ignoreColorSpaceFileRules", aiimage_nd_ignorecolorspace)
            aiimage_nd_colorspace = cmds.getAttr(f"{file_nd}.colorSpace")
            cmds.setAttr(f"{aiimage_nd}.colorSpace", aiimage_nd_colorspace, type="string")

            # remove old file node
            if delete_old:
                cmds.delete(file_nd)

            # copy over other settings
            logger.info(f"Node created: ----- {aiimage_nd} -----")

    def rename_megascans_obj(self, megascans_objs: list | str = "") -> None:
        """Rename selected or input megascans object.

        Args:
            megascans_objs: Megascan environment object/s to rename.

        """
        if not megascans_objs:
            megascans_objs = cmds.ls(selection=True)
            if megascans_objs:
                megascans_objs = [
                    obj
                    for obj in megascans_objs
                    if cmds.objectType(cmds.listRelatives(obj, shapes=True)[0]) == "mesh"
                ][0]
            else:
                logger.info("Select Megascans object to rename...")
                return

        if not isinstance(megascans_objs, (list, tuple)):
            megascans_objs = [megascans_objs]

        for obj in megascans_objs:
            obj_shp = cmds.listRelatives(obj, shapes=True)[0]
            obj_shading_grp = cmds.listConnections(obj_shp, destination=True, type="shadingEngine")[
                0
            ]
            megascans_obj_nm = obj_shading_grp.split("_")
            megascans_obj_nm = "_".join(megascans_obj_nm[:-1])
            megascans_obj_nm = megascans_obj_nm + "_geo"

            cmds.rename(obj, megascans_obj_nm)

            logger.info(f"Renamed: {megascans_obj_nm}")


class OpenPBRSetup:
    """Connect selected file nodes to "openPBRSurface" material in Maya hypershade window.
    Or select shading group if no pbr surface yet.  Naming of material nodes will be based off
    pbr surface name or shading group name if no material yet.

    Uses nLol naming convention: "<name>_<direction>_<id>_<type>"
    """

    def create(self, rename_after_geo: bool = False, rename_after_folder: bool = False) -> None:
        """Class entry point. Run this with file nodes and "openPBRSurface"
        or shading group selected.

        Args:
            rename_after_geo: Rename material and shading group after connected geo.
                Geo objects nLol naming components will be used.
            rename_after_folder: Rename material and shading group after
                parent folder of first image file. Useful for Megascans assets.

        """
        selected = cmds.ls(selection=True)
        shading_nds = [obj for obj in selected if cmds.objectType(obj) == "shadingEngine"]
        shading_nd = shading_nds[0] if shading_nds else ""
        openpbr_nds = [obj for obj in selected if cmds.objectType(obj) == "openPBRSurface"]
        openpbr_nd = openpbr_nds[0] if openpbr_nds else ""
        file_nds = [obj for obj in selected if cmds.objectType(obj) == "file"]

        if not openpbr_nd:
            if not shading_nd:
                msg = 'OpenPBRSetup requires "openPBRSurface" or shading group selection.'
                logger.error(msg)
                raise ValueError(msg)
            name_comp, side_dir, obj_id, _ = find_name_comps(shading_nd)

            openpbr_nd_nm = join_nm_comps(name_comp, side_dir, obj_id, "matArnold")
            openpbr_nd = cmds.shadingNode(
                "openPBRSurface",
                asShader=True,
                name=openpbr_nd_nm,
            )
            cmds.connectAttr(f"{openpbr_nd}.outColor", f"{shading_nd}.surfaceShader")
        else:
            name_comp, side_dir, obj_id, _ = find_name_comps(openpbr_nd)

        if rename_after_geo:
            shading_nd_geo = cmds.listConnections(shading_nd, type="mesh")[0]
            name_comp, side_dir, obj_id, _ = find_name_comps(shading_nd_geo)
        if rename_after_folder:
            file_nd_1 = file_nds[0]  # first file node
            file_nd_1_filepath = Path(cmds.getAttr(f"{file_nd_1}.fileTextureName"))

            name_comp = file_nd_1_filepath.parent.name
            if name_comp.lower() == "atlas":
                name_comp = file_nd_1_filepath.parents[2].name

            name_comp_no_wspace = re.sub(r"\s+", "", name_comp)
            name_comp_split = name_comp_no_wspace.split("_")
            name_comp_split = [cap(txt) for txt in name_comp_split]
            name_comp = "".join(name_comp_split)

        texture_stings_dict = {
            "baseColor": {
                "keywords": {"baseColor", "diffuse", "albedo", "color"},
                "file_nd_output": "outColor",
                "material_input": "baseColor",
            },
            "ambientOcclusion": {
                "keywords": {"ambientOcclusion", "ao"},
                "file_nd_output": "outColorR",
                "material_input": "baseWeight",
                "colorSpace": "Raw",
            },
            "roughness": {
                "keywords": {"roughness", "rough"},
                "file_nd_output": "outColor",
                "material_input": "specularRoughness",
                "colorSpace": "Raw",
            },
            "gloss": {
                "keywords": {"glossiness", "gloss"},
                "file_nd_output": "outAlpha",
                "material_input": "specularRoughness",
                "colorSpace": "Raw",
                "alphaIsLuminance": True,
                "inbetween_type": "reverse",
                "inbetween_input": "inputX",
                "inbetween_output": "outputX",
            },
            "normal": {
                "keywords": {"normal"},
                "file_nd_output": "outColor",
                "material_input": "normalCamera",
                "colorSpace": "Raw",
                "inbetween_type": "aiNormalMap",
                "inbetween_input": "input",
                "inbetween_output": "outValue",
                "invert_normal": False,
            },
            "opacity": {
                "keywords": {"opacity"},
                "file_nd_output": "outAlpha",
                "material_input": "geometryOpacity",
                "colorSpace": "Raw",
                "alphaIsLuminance": True,
            },
            "mixmap": {
                "keywords": {"OcclusionRoughnessMetallic", "mixmap"},
                "file_nd_output": ("outColorR", "outColorG", "outColorB"),
                "material_input": ("baseWeight", "specularRoughness", "baseMetalness"),
                "colorSpace": "Raw",
            },
        }

        renamed_file_nds = []
        for texture_type, texture_data in texture_stings_dict.items():
            # find matching file node w/ texture keyword
            texture_keywords = texture_data["keywords"]
            texture_file_nds = [
                nd for nd in file_nds if any(txt.lower() in nd.lower() for txt in texture_keywords)
            ]
            # connect file node to material
            texture_file_nd = texture_file_nds[0] if texture_file_nds else ""

            if texture_file_nd:
                texture_file_nd_nm = join_nm_comps(
                    f"{name_comp}{cap(texture_type)}",
                    side_dir,
                    obj_id,
                    "file",
                )
                texture_file_nd = cmds.rename(texture_file_nd, texture_file_nd_nm)

                file_nd_output = texture_data["file_nd_output"]
                material_input = texture_data["material_input"]
                colorspace = texture_data.get("colorSpace", "")
                alphaisluminance = texture_data.get("alphaIsLuminance", False)
                inbetween_type = texture_data.get("inbetween_type", "")
                inbetween_input = texture_data.get("inbetween_input", "")
                inbetween_output = texture_data.get("inbetween_output", "")
                invert_normal = texture_data.get("invert_normal", False)

                inbetween_nd = ""
                if inbetween_type:
                    inbetween_nd_nm = join_nm_comps(
                        f"{name_comp}{cap(texture_type)}",
                        side_dir,
                        obj_id,
                        inbetween_type,
                    )
                    inbetween_nd = cmds.shadingNode(
                        inbetween_type,
                        asUtility=True,
                        name=inbetween_nd_nm,
                    )

                self.connect_material_file_nodes(
                    texture_file_nd=texture_file_nd,
                    material_nd=openpbr_nd,
                    material_input=material_input,
                    file_nd_output=file_nd_output,
                    colorspace=colorspace,
                    alphaisluminance=alphaisluminance,
                    inbetween_nd=inbetween_nd,
                    inbetween_input=inbetween_input,
                    inbetween_output=inbetween_output,
                    invert_normal=invert_normal,
                )

                renamed_file_nds.append(texture_file_nd)

        # connect single place2dTexture node to all image file nodes
        place2d_nd_nm = join_nm_comps(name_comp, side_dir, obj_id, "place2dTexture")
        place2d_nd = cmds.shadingNode(
            "place2dTexture",
            asUtility=True,
            name=place2d_nd_nm,
        )
        ArnoldMaterialSetup().connect_place2d_nd(place2d_nd, renamed_file_nds)

        # --------------------
        msg = (
            f'---------- Material Created!: "{openpbr_nd}", "{shading_nd}" ----------\n'
            'Ignore any ".ignoreColorSpaceFileRules" and ".uvTilingMode" deferred errors...'
        )
        logger.info(msg)

    def connect_material_file_nodes(
        self,
        texture_file_nd: str,
        file_nd_output: str | tuple[str, str, str],
        material_nd: str,
        material_input: str | tuple[str, str, str],
        colorspace: str = "",
        alphaisluminance: int | bool = False,
        inbetween_nd: str = "",
        inbetween_input: str = "",
        inbetween_output: str = "",
        invert_normal: bool = False,
    ) -> None:
        """Connect an image file node to the correct material plug and set node settings.

        Args:
            texture_type: Type of texture map. Example: "color", "roughness", "mixmap".
            texture_file_nd: Image file node make connections from. If is Python type "list/tuple",
                then the 3 values will be outputs for file nodes "color"; "r", "g", and "b".
            file_nd_output: Output for image file node.
            material_nd: Material node to connect to.
            material_input: Input attribute for material node. If is Python type "list/tuple",
                then the 3 values will be inputs for file nodes "color"; "r", "g", and "b".
            colorspace, alphaisluminance: Various node settings to apply.
            inbetween_nd: Node inbetween file node and material.
                Example would be an "aiNormalMap", "reverse", or "ramp" node.
            inbetween_input, inbetween_output: Input and output for inbetween node.
            invert_normal: Invert Y for "aiNormalMap".

        """
        # file node to material node connection
        if isinstance(file_nd_output, (list, tuple)) and isinstance(material_input, (list, tuple)):
            if len(file_nd_output) != 3 or len(material_input) != 3:
                msg = (
                    'Must have 3 values for rgb if using list with "file_nd_output" '
                    'and "material_input".'
                )
                logger.error(msg)
                raise ValueError(msg)
            cmds.connectAttr(
                f"{texture_file_nd}.{file_nd_output[0]}",
                f"{material_nd}.{material_input[0]}",
                force=True,
            )
            cmds.connectAttr(
                f"{texture_file_nd}.{file_nd_output[1]}",
                f"{material_nd}.{material_input[1]}",
                force=True,
            )
            cmds.connectAttr(
                f"{texture_file_nd}.{file_nd_output[2]}",
                f"{material_nd}.{material_input[2]}",
                force=True,
            )
        else:
            cmds.connectAttr(
                f"{texture_file_nd}.{file_nd_output}",
                f"{material_nd}.{material_input}",
                force=True,
            )
        # inbetween node connections
        if inbetween_nd:
            cmds.connectAttr(
                f"{texture_file_nd}.{file_nd_output}",
                f"{inbetween_nd}.{inbetween_input}",
                force=True,
            )
            cmds.connectAttr(
                f"{inbetween_nd}.{inbetween_output}",
                f"{material_nd}.{material_input}",
                force=True,
            )

        # node settings
        cmds.setAttr(f"{texture_file_nd}.ignoreColorSpaceFileRules", True)
        if colorspace:
            cmds.setAttr(f"{texture_file_nd}.colorSpace", colorspace, type="string")
        if alphaisluminance:
            cmds.setAttr(f"{texture_file_nd}.alphaIsLuminance", True)
        if invert_normal:  # assumes inbetween node is "aiNormalMap"
            cmds.setAttr(f"{inbetween_nd}.invertY", True)
        # udim file setting
        texture_name = Path(cmds.getAttr(f"{texture_file_nd}.fileTextureName")).name
        if "100" in texture_name:
            cmds.setAttr(f"{texture_file_nd}.uvTilingMode", 3)
            cmds.setAttr(f"{texture_file_nd}.uvTileProxyQuality", 1)  # 1k preview
