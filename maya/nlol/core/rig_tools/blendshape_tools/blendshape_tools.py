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
