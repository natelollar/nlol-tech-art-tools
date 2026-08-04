"""GUI Batch Render Script
Place this script in the render output folder with "arnold_batch_render_start.cmd".
Double click the cmd script to launch the render session.

This script allows one to add multiple cameras and/or render layers to a render session
and render "overnight" without needing to click render for each new camera.
Different shots can be added as well by tweaking file paths.  Various settings like
camera AA samples can also be adjusted.

Certain layer overrides like AA samples or active AOVs can best be done in
the Maya render layer manager "Render Setup editor".
"""
# TODO: should add confirm start, to avoid mistake start...

import os
import re
from pathlib import Path

from mtoa.cmds import arnoldRender

from maya import cmds

# output folder path defaults to the location of this python script
try:
    current_folderpath = Path(__file__).resolve().parent
except NameError:
    current_folderpath = Path(os.getcwd())
maya_files = sorted(
    scene_file for ext in ("*.ma", "*.mb") for scene_file in current_folderpath.glob(ext)
)
if not maya_files:
    raise FileNotFoundError(f"No .ma/.mb files found: {current_folderpath}")
maya_filepath = maya_files[0].as_posix()

# ----------
scene = "myEpicScene_a1_shot"
res_mult = 1.0  # resolution multiplier
start_f, end_f = 1, 240  # 1, 240
camera = "camera2"
# master render layer is called "defaultRenderLayer"
render_layers = ["defaultRenderLayer", "character_renderLayer", "background_renderLayer"]

render_jobs = [
    {
        "maya_fipath": maya_filepath,
        "cam": camera,
        "start": start_f,
        "end": end_f,
        "layers": render_layers,
    },
    {
        "maya_fipath": maya_filepath,
        "cam": "camera3",
        "start": start_f,
        "end": end_f,
        "layers": render_layers,
    },
    {
        "maya_fipath": maya_filepath,
        "cam": "camera4",
        "start": 60,
        "end": 120,
        "layers": ["character_renderLayer", "background_renderLayer"],
    },
    {
        "maya_fipath": maya_filepath,
        "cam": "camera5",
        "start": 60,
        "end": 120,
    },
]

# ----------
res_w, res_h = 2560, 1168
res_w, res_h = int(res_w * res_mult), int(res_h * res_mult)
render_device = 1  # 1 is GPU, 0 is CPU
bucket_size = 64  # default = 64
filter_type = "gaussian"  # default = "gaussian"; "blackman_harris"; "box"
# samples
aa_samples = 8
aa_samples = int(aa_samples * res_mult)
# lock sampling noise
lock_sampling_noise = True
# adaptive sampling
adaptive_sampling = False  # default = False
aa_samples_max = 8  # default = 20
aa_adaptive_threshold = 0.015  # default = 0.015; lower is slower
# ray depth
ray_depth_total = 10  # default = 10
ray_depth_diffuse = 1  # default = 1
ray_depth_specular = 1  # default = 1
ray_depth_transmission = 8  # default = 8
ray_depth_volume = 0  # default = 0
ray_depth_transparency = 10  # default = 10
# motion blur
motion_blur = False
instantaneous_shutter = False  # enable for motion vector pass
# 32 bit driver
enable_aov32bit_driver = True
enable_painterid_driver = True
aov32bit_driver = "aov32bit_aiAOVDriver"  # custom driver = "aov32bit_aiAOVDriver"
painterid_driver = "painterID_aiAOVDriver"  # custom driver = "substanceID_aiAOVDriver"

# --------------------------------------------------
output_filename = f"{scene}.<Camera>.<RenderLayer>"
output_filepath = Path(current_folderpath / output_filename).as_posix()
output_32bit = f"{scene}.<Camera>.<RenderLayer>.32bit"
output_32bit_filepath = Path(current_folderpath / output_32bit).as_posix()
output_painterid = f"{scene}.<Camera>.<RenderLayer>.painterID"
output_painterid_filepath = Path(current_folderpath / output_painterid).as_posix()


def run_batch() -> None:
    """Batch style render but with render sequence."""
    for job in render_jobs:
        print(f"--- OPENING: {job['maya_fipath']} ---")
        try:
            cmds.file(job["maya_fipath"], open=True, force=True)
        except Exception as e:
            print(f"Warning: Scene opened with errors, but attempting to continue... {e}")

        # apply overrides
        cmds.setAttr("defaultRenderGlobals.startFrame", job["start"])
        cmds.setAttr("defaultRenderGlobals.endFrame", job["end"])
        cmds.setAttr("defaultArnoldRenderOptions.renderDevice", render_device)
        cmds.setAttr("defaultArnoldRenderOptions.bucketSize", bucket_size)
        cmds.setAttr("defaultArnoldFilter.aiTranslator", filter_type, type="string")
        # samples
        cmds.setAttr("defaultArnoldRenderOptions.AASamples", aa_samples)
        # lock sampling noise
        cmds.setAttr("defaultArnoldRenderOptions.lock_sampling_noise", lock_sampling_noise)
        # adaptive sampling
        cmds.setAttr("defaultArnoldRenderOptions.enableAdaptiveSampling", adaptive_sampling)
        cmds.setAttr("defaultArnoldRenderOptions.AASamplesMax", aa_samples_max)
        cmds.setAttr("defaultArnoldRenderOptions.AAAdaptiveThreshold", aa_adaptive_threshold)
        # ray depth
        cmds.setAttr("defaultArnoldRenderOptions.GITotalDepth", ray_depth_total)
        cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseDepth", ray_depth_diffuse)
        cmds.setAttr("defaultArnoldRenderOptions.GISpecularDepth", ray_depth_specular)
        cmds.setAttr("defaultArnoldRenderOptions.GITransmissionDepth", ray_depth_transmission)
        cmds.setAttr("defaultArnoldRenderOptions.GIVolumeDepth", ray_depth_volume)
        cmds.setAttr("defaultArnoldRenderOptions.autoTransparencyDepth", ray_depth_transparency)
        # motion blur
        cmds.setAttr("defaultArnoldRenderOptions.motion_blur_enable", motion_blur)
        cmds.setAttr("defaultArnoldRenderOptions.ignoreMotionBlur", instantaneous_shutter)
        ##
        cmds.setAttr("defaultResolution.width", res_w)
        cmds.setAttr("defaultResolution.height", res_h)
        cmds.setAttr("defaultResolution.pixelAspect", 1.0)
        cmds.setAttr(
            "defaultResolution.deviceAspectRatio",
            res_w / res_h,
        )  # to force exr metadata ratio
        cmds.setAttr("defaultArnoldDriver.multipart", True)
        cmds.setAttr("defaultArnoldDriver.mergeAOVs", True)
        cmds.setAttr("defaultArnoldDriver.halfPrecision", True)  # 16-bit main output
        cmds.setAttr("defaultArnoldDriver.exrCompression", 8)  # 8 = dwaa
        cmds.setAttr("defaultArnoldRenderOptions.log_to_file", True)
        cmds.setAttr("defaultArnoldRenderOptions.log_verbosity", 2)  # 0-6, higher = more detail

        # output folder
        Path(current_folderpath).mkdir(parents=True, exist_ok=True)
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", output_filepath, type="string")
        print(f"--- OUTPUT: {output_filepath} ---")

        # 32-bit driver separate path (P, crypto)
        if enable_aov32bit_driver and cmds.objExists(aov32bit_driver):
            cmds.setAttr(f"{aov32bit_driver}.multipart", True)
            cmds.setAttr(f"{aov32bit_driver}.mergeAOVs", True)
            cmds.setAttr(f"{aov32bit_driver}.halfPrecision", False)  # 32-bit
            cmds.setAttr(f"{aov32bit_driver}.exrCompression", 4)  # 4 = piz
            cmds.setAttr(f"{aov32bit_driver}.prefix", output_32bit_filepath, type="string")
            print(f"--- 32BIT OUTPUT: {output_32bit_filepath} ---")
        # substance painter id pass. use w/ custom filter set to "closest". dwaa caused pixel blending.
        if enable_painterid_driver and cmds.objExists(painterid_driver):
            cmds.setAttr(f"{painterid_driver}.multipart", True)
            cmds.setAttr(f"{painterid_driver}.mergeAOVs", True)
            cmds.setAttr(f"{painterid_driver}.halfPrecision", True)  # 16-bit
            cmds.setAttr(f"{painterid_driver}.exrCompression", 3)  # 3 = zip
            cmds.setAttr(f"{painterid_driver}.prefix", output_painterid_filepath, type="string")
            print(f"--- PAINTER ID OUTPUT: {output_painterid_filepath} ---")

        # render the specific camera
        print(f"--- RENDERING: {job['cam']} (Frames {job['start']}-{job['end']}) ---")
        arnoldRender.arnoldMakeCameraRenderable(job["cam"])

        # get all render layers and render each enabled one
        render_layers = cmds.ls(type="renderLayer")
        custom_layers = job.get("layers", [])

        if custom_layers:
            layers_to_render = [
                lyr
                if lyr == "defaultRenderLayer"
                else lyr
                if re.match(r"^rs_", lyr)
                else f"rs_{lyr}"
                for lyr in custom_layers
            ]  # maya "rs" adds prefix
            missing = [lyr for lyr in layers_to_render if lyr not in render_layers]
            if missing:
                print(f"Custom layers not found in scene, skipping job: {missing}")
                continue  # skip this job, not the whole batch
        else:
            layers_to_render = [
                lyr
                for lyr in render_layers
                if cmds.getAttr(f"{lyr}.renderable")
                and not cmds.referenceQuery(lyr, isNodeReferenced=True)
            ]

        for layer in layers_to_render:
            print(
                f"--- RENDERING: {job['cam']} | LAYER: {layer} (Frames {job['start']}-{job['end']}) ---",
            )
            cmds.editRenderLayerGlobals(currentRenderLayer=layer)

            log_layer_name = layer.removeprefix("rs_")
            log_filename = f"{scene}.{job['cam']}.{log_layer_name}.log"
            log_filepath = Path(current_folderpath / log_filename).as_posix()
            cmds.setAttr("defaultArnoldRenderOptions.log_filename", log_filepath, type="string")

            arnoldRender.arnoldSequenceRender(0, 0, job["cam"], False)

    print("--- ALL JOBS COMPLETE ---")

    # this forces Maya to close when done
    cmds.evalDeferred("cmds.quit(force=True)")


if __name__ == "__main__":
    run_batch()
