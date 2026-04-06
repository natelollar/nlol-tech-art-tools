import tomllib
from pathlib import Path

from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()

arkit_blendshapes_filepath = Path(__file__).parent / "arkit_blendshapes.toml"


class BlendShapeTools:
    def run_extract_arkit_poses(self):
        """Run "extract_poses_from_animation()" with undo chunk.
        Extracts 52 arkit blendshapes using "arkit_blendshapes.toml".
        Keyframe poses first, matching the listed frames, then select and run.
        """
        cmds.undoInfo(openChunk=True)
        try:
            self.extract_arkit_poses()
        finally:
            cmds.undoInfo(closeChunk=True)

    def extract_arkit_poses(self):
        """Duplicate selected mesh for each keyframed blendshape pose.
        Combine back into a new mesh and parent to world.
        """
        with open(arkit_blendshapes_filepath, "rb") as f:
            blendshapes_data = tomllib.load(f)
            keyframe_poses = blendshapes_data["blendshapes"]

        selected = cmds.ls(selection=True)

        for sel in selected:
            blendshapes = []
            for blendshape, frame in keyframe_poses.items():
                cmds.currentTime(frame)
                blendshape_mesh = cmds.duplicate(sel, name=blendshape)
                cmds.parent(blendshape_mesh, world=True)

                blendshapes.append(blendshape_mesh)

            # add blendshape 1-52 to neutral pose frame 0
            cmds.blendShape(*blendshapes[1:], blendshapes[0], name=f"{sel}BlendShape")
            cmds.delete(*blendshapes[1:])

            # rename main geo
            geo_name = f"{sel.split('_')[0]}BlendShapes"
            geo_name = sel.replace(sel.split("_")[0], geo_name)
            cmds.rename(blendshapes[0], geo_name)

    def duplicate_out_blendshapes(self):
        """Enable each blendshape one at a time and duplicate the deformed mesh.
        Creates a separate mesh for each blendshape.
        """
        selected = cmds.ls(selection=True)

        for sel in selected:
            blendshape_nodes = cmds.ls(cmds.listHistory(sel), type="blendShape")
            if not blendshape_nodes:
                logger.warning(f"No blendshape: {sel}")
                continue

            blendshape_node = blendshape_nodes[0]
            blendshapes = cmds.listAttr(f"{blendshape_node}.weight", multi=True)

            # reset all blendshape weights to 0
            for blendshape in blendshapes:
                cmds.setAttr(f"{blendshape_node}.{blendshape}", 0)

            # enable individual blendshapes and duplicate geo
            for blendshape in blendshapes:
                # enable current blendshape
                cmds.setAttr(f"{blendshape_node}.{blendshape}", 1)
                # duplicate deformed mesh
                duplicate = cmds.duplicate(sel, name=blendshape)
                if cmds.listRelatives(duplicate, parent=True) is not None:
                    cmds.parent(duplicate, world=True)
                # disable current blendshape
                cmds.setAttr(f"{blendshape_node}.{blendshape}", 0)

    def copy_blendshapes(self):
        """Copy blendshapes from first selected mesh to second.
        Target mesh may already have a blendshape node, but not required.
        Assumes only one blendshape node max, per mesh.
        """
        selected = cmds.ls(selection=True)
        if len(selected) != 2:
            logger.warning(
                "Select source mesh first and then target mesh, to copy blendshape weights. "
                "Only 2 meshes should be selected.",
            )
            return
        source_mesh = selected[0]
        target_mesh = selected[1]

        # get source blendshape node
        source_blendshape_nd = cmds.ls(cmds.listHistory(source_mesh), type="blendShape")[0]
        source_blendshapes = cmds.listAttr(f"{source_blendshape_nd}.weight", multi=True)

        # get target blendshape node
        target_blendshape_nd = cmds.ls(cmds.listHistory(target_mesh), type="blendShape")
        if target_blendshape_nd:
            target_blendshape_nd = target_blendshape_nd[0]
            # number of blendhsapes on target
            target_blendshapes = cmds.listAttr(f"{target_blendshape_nd}.weight", multi=True)
            target_blendshapes_amount = len(target_blendshapes)
        else:  # or create target blendshape node
            target_blendshape_nd = cmds.blendShape(
                target_mesh,
                frontOfChain=True,
                name=f"{target_mesh}BlendShape",
            )[0]
            target_blendshapes_amount = 0

        # reset source blendshape weights to 0
        for blendshape in source_blendshapes:
            cmds.setAttr(f"{source_blendshape_nd}.{blendshape}", 0)

        # transfer blendshapes
        for i, blendshape in enumerate(source_blendshapes):
            cmds.setAttr(f"{source_blendshape_nd}.{blendshape}", 1)
            blendshape_duplicate = cmds.duplicate(source_mesh, name=blendshape)[0]
            cmds.setAttr(f"{source_blendshape_nd}.{blendshape}", 0)

            cmds.blendShape(
                target_blendshape_nd,
                edit=True,
                target=(target_mesh, (i + target_blendshapes_amount), blendshape_duplicate, 1.0),
            )
            cmds.delete(blendshape_duplicate)
