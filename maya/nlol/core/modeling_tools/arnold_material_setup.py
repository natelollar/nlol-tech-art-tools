import re
from pathlib import Path

from nlol.core.general_utils import cap
from nlol.utilities.nlol_maya_logger import get_logger

from maya import cmds

logger = get_logger()


class ArnoldMaterialSetup:
    def arnold_basic_mat(
        self,
        substance_material: bool = False,
        use_arnold_file_nodes: bool = False,
    ) -> None:
        """Setup Arnold material based on selection of 3 input textures (from Marmoset Toolbag
        or Substance Painter) and an empty Maya shading group. Use drag and drop to add texture
        file nodes to Maya. Required selection: Color map, Mix map, Normal map, Shading Group.
        (3 "file" nodes and 1 "shadingEngine" node)

        Args:
            substance_material: Use Substance Painter - Unreal 4 (Packed) text naming,
                to identify selected texture file nodes.
            use_arnold_file_nodes: Use Arnold aiiamge nodes instead of regular Maya file nodes,
                when connecting to Arnold material.  Still drag and drop,
                    and select file nodes before running method.

        """
        # ----------------------------------------------------------------------
        selected = cmds.ls(selection=True)  # 3 image file nodes, 1 shading group node
        file_nds = [obj for obj in selected if cmds.objectType(obj) == "file"]
        shading_nds = [obj for obj in selected if cmds.objectType(obj) == "shadingEngine"]

        # ----------------------------------------------------------------------
        # error checking
        if len(file_nds) != 3:
            msg = "Select exactly 3 file nodes. Albedo, mixmap, and normal."
            logger.warning(msg)
            raise ValueError(msg)
        if len(shading_nds) != 1:
            msg = "Select 1 empty shading group node."
            logger.warning(msg)
            raise ValueError(msg)

        # ----------------------------------------------------------------------
        # map suffixes
        if substance_material:
            albedo_str = "BaseColor"
            mixmap_str = "OcclusionRoughnessMetallic"
            normal_str = "Normal"
        else:
            albedo_str = "albedo"
            mixmap_str = "mixmap"
            normal_str = "normal"

        albedo_file_nd = [obj for obj in selected if albedo_str.lower() in obj.lower()][0]
        mixmap_file_nd = [obj for obj in selected if mixmap_str.lower() in obj.lower()][0]
        normal_file_nd = [obj for obj in selected if normal_str.lower() in obj.lower()][0]
        udims_fild_nds = []
        for file_nd in selected:
            try:
                texture_name = Path(cmds.getAttr(f"{file_nd}.fileTextureName")).name
                if "100" in texture_name:
                    udims_fild_nds.append(file_nd)
            except Exception:
                pass
        # shading group node
        shading_nd = [obj for obj in selected if cmds.objectType(obj) == "shadingEngine"][0]
        # get nLol name component from selected file node
        file_obj = [obj for obj in selected if cmds.objectType(obj) == "file"][0]
        name_comp = file_obj.split("_")[0]

        # ----------------------------------------------------------------------
        # create shading nodes
        stnd_surface_nd = cmds.shadingNode(
            "standardSurface",
            asShader=True,
            name=f"{name_comp}_mat",
        )
        open_pbr_nd = cmds.shadingNode(
            "openPBRSurface",
            asShader=True,
            name=f"{name_comp}_matArnold",
        )
        bump_nd = cmds.shadingNode("bump2d", asUtility=True, name=f"{name_comp}Normal_bump2d")
        normal_arnold_nd = cmds.shadingNode(
            "aiNormalMap",
            asUtility=True,
            name=f"{name_comp}Normal_aiNormalMap",
        )
        ao_ramp_nd = cmds.shadingNode("ramp", asTexture=True, name=f"{name_comp}Occlusion_ramp")
        rough_ramp_nd = cmds.shadingNode("ramp", asTexture=True, name=f"{name_comp}Roughness_ramp")
        metal_ramp_nd = cmds.shadingNode("ramp", asTexture=True, name=f"{name_comp}Metalness_ramp")

        # ----------------------------------------------------------------------
        # connect nodes
        # shading group connections
        cmds.connectAttr(f"{stnd_surface_nd}.outColor", f"{shading_nd}.surfaceShader")
        cmds.connectAttr(f"{open_pbr_nd}.outColor", f"{shading_nd}.aiSurfaceShader")
        # standard surface connections
        cmds.connectAttr(f"{albedo_file_nd}.outColor", f"{stnd_surface_nd}.baseColor")
        cmds.connectAttr(f"{mixmap_file_nd}.outColorR", f"{stnd_surface_nd}.base")
        cmds.connectAttr(f"{mixmap_file_nd}.outColorG", f"{stnd_surface_nd}.specularRoughness")
        cmds.connectAttr(f"{mixmap_file_nd}.outColorB", f"{stnd_surface_nd}.metalness")
        cmds.connectAttr(f"{normal_file_nd}.outAlpha", f"{bump_nd}.bumpValue")
        cmds.connectAttr(f"{bump_nd}.outNormal", f"{stnd_surface_nd}.normalCamera")
        # open pbr connections
        self.albedo_plug = f"{open_pbr_nd}.baseColor"
        self.mixmap_r_plug = f"{ao_ramp_nd}.vCoord"
        self.mixmap_g_plug = f"{rough_ramp_nd}.vCoord"
        self.mixmap_b_plug = f"{metal_ramp_nd}.vCoord"
        self.normal_plug = f"{normal_arnold_nd}.input"
        cmds.connectAttr(f"{albedo_file_nd}.outColor", self.albedo_plug)
        cmds.connectAttr(f"{mixmap_file_nd}.outColorR", self.mixmap_r_plug)
        cmds.connectAttr(f"{mixmap_file_nd}.outColorG", self.mixmap_g_plug)
        cmds.connectAttr(f"{mixmap_file_nd}.outColorB", self.mixmap_b_plug)
        cmds.connectAttr(f"{ao_ramp_nd}.outAlpha", f"{open_pbr_nd}.baseWeight")
        cmds.connectAttr(f"{rough_ramp_nd}.outAlpha", f"{open_pbr_nd}.specularRoughness")
        cmds.connectAttr(f"{metal_ramp_nd}.outAlpha", f"{open_pbr_nd}.baseMetalness")
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
        cmds.setAttr(f"{ao_ramp_nd}.colorEntryList[0].color", 0.50, 0.50, 0.50)
        cmds.setAttr(f"{ao_ramp_nd}.colorEntryList[1].color", 1.0, 1.0, 1.0)
        cmds.setAttr(f"{ao_ramp_nd}.colorEntryList[1].position", 1.0)

        if substance_material:  # account for inverted G/Y normal
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
            name=f"{name_comp}_place2dTexture",
        )
        # delete old place2dTexture nodes
        for file_nd in file_nds:
            old_place2d_nd = cmds.listConnections(file_nd, type="place2dTexture")
            if old_place2d_nd:
                old_place2d_nd = list(set(old_place2d_nd))[0]
                cmds.delete(old_place2d_nd)
        # connect new place2dTexture node to image file nodes
        self.connect_place2d_nd(place2d_nd, file_nds)

        # ----------------------------------------------------------------------
        # rename nodes
        albedo_file_nd = cmds.rename(albedo_file_nd, f"{name_comp}{cap(albedo_str)}_file")
        mixmap_file_nd = cmds.rename(mixmap_file_nd, f"{name_comp}{cap(mixmap_str)}_file")
        normal_file_nd = cmds.rename(normal_file_nd, f"{name_comp}{cap(normal_str)}_file")
        if substance_material:
            cmds.rename(normalvp2_file_nd, f"{name_comp}{cap(normal_str)}Vp2_file")
        shading_nd = cmds.rename(shading_nd, f"{name_comp}_matSG")

        # ----------------------------------------------------------------------
        logger.info(
            f"---------- Material Created!: {open_pbr_nd, stnd_surface_nd, shading_nd} ----------\n"
            'Ignore any ".ignoreColorSpaceFileRules" and ".uvTilingMode" deferred errors...',
        )

        # ----------------------------------------------------------------------
        self.name_comp = name_comp
        self.albedo_file_nd = albedo_file_nd
        self.mixmap_file_nd = mixmap_file_nd
        self.normal_file_nd = normal_file_nd
        self.albedo_str = albedo_str
        self.mixmap_str = mixmap_str
        self.normal_str = normal_str

        # ----------------------------------------------------------------------
        if use_arnold_file_nodes:
            self.setup_arnold_image_nodes(substance_material)

    def setup_arnold_image_nodes(self, substance_material: bool = False) -> None:
        """Use Arnold file nodes (aiImage) instead of regular Maya file nodes (file)
        for Arnold material.

        Args:
            substance_material: See "arnold_basic_mat()".

        """
        albedo_aiimage = cmds.shadingNode(
            "aiImage",
            asTexture=True,
            name=f"{self.name_comp}{cap(self.albedo_str)}_aiImage",
        )
        mixmap_aiimage = cmds.shadingNode(
            "aiImage",
            asTexture=True,
            name=f"{self.name_comp}{cap(self.mixmap_str)}_aiImage",
        )
        normal_aiimage = cmds.shadingNode(
            "aiImage",
            asTexture=True,
            name=f"{self.name_comp}{cap(self.normal_str)}_aiImage",
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
        cmds.connectAttr(f"{mixmap_aiimage}.outColorR", self.mixmap_r_plug, force=True)
        cmds.connectAttr(f"{mixmap_aiimage}.outColorG", self.mixmap_g_plug, force=True)
        cmds.connectAttr(f"{mixmap_aiimage}.outColorB", self.mixmap_b_plug, force=True)
        cmds.connectAttr(f"{normal_aiimage}.outColor", self.normal_plug, force=True)

        if substance_material:
            cmds.delete(self.normal_file_nd)

    def connect_place2d_nd(self, place2d_nd: str, file_nds: list[str]) -> None:
        """Connect a single place2dTexture node to multiple image file nodes.

        Args:
            place2d_nd: The place2dTexture to be connected to the image file nodes.
            file_nds: The list of file nodes to be connected to the single place2dTexture node.

        """
        for file_nd in file_nds:
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
            descriptors = ["BaseColor", "OcclusionRoughnessMetallic", "Normal", "albedo", "mixmap"]
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
