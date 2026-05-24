"""OBJ Mesh Cleanup Script
Place this script in the folder containing the OBJ sequence with "clean_liquigen_objs.cmd".
Double click the cmd script to launch the cleanup session.

Scans each OBJ for NaN/Inf vertices, deletes any degenerate faces found,
and exports the cleaned OBJ back to the same file path.

Removes normals from OBJ to save space (all OBJ export options turned off.)
"""

import os
import math
from pathlib import Path

from maya import cmds
from maya.api import OpenMaya as om

# output folder path defaults to the location of this python script
try:
    current_folderpath = Path(__file__).resolve().parent
except NameError:
    current_folderpath = Path(os.getcwd())

# ----------
obj_export_options = "groups=0;ptgroups=0;materials=0;smoothing=0;normals=0"


# --------------------------------------------------
def get_mesh_transform() -> str | None:
    """Return the first mesh transform in the scene."""
    shapes = cmds.ls(type="mesh", noIntermediate=True)
    if not shapes:
        return None
    return cmds.listRelatives(shapes[0], parent=True, fullPath=False)[0]


def strip_namespaces() -> None:
    """Remove all namespaces from the scene."""
    namespaces = [
        ns for ns in cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
        if ns not in ("UI", "shared")
    ]
    for ns in sorted(namespaces, reverse=True):  # deepest first
        try:
            cmds.namespace(removeNamespace=ns, mergeNamespaceWithRoot=True)
        except Exception:
            pass


def cleanup_mesh(mesh: str) -> int:
    """Check mesh for NaN/Inf verts and delete bad faces. Returns face count deleted."""
    sel = om.MSelectionList()
    sel.add(mesh)
    dag = sel.getDagPath(0)
    dag.extendToShape()
    fn = om.MFnMesh(dag)
    points = fn.getPoints(om.MSpace.kWorld)

    bad_indices = [
        i for i, p in enumerate(points)
        if any(math.isnan(v) or math.isinf(v) for v in (p.x, p.y, p.z))
    ]

    if not bad_indices:
        return 0

    bad_verts = [f"{mesh}.vtx[{i}]" for i in bad_indices]
    bad_faces = cmds.polyListComponentConversion(bad_verts, fromVertex=True, toFace=True)
    bad_faces = cmds.ls(bad_faces, fl=True)
    cmds.delete(bad_faces)
    return len(bad_faces)


def run_cleanup() -> None:
    cmds.loadPlugin("objExport", quiet=True)
    #if not cmds.pluginInfo("objExport.mll", query=True, loaded=True):
    #        cmds.loadPlugin("objExport.mll")

    obj_files = sorted(current_folderpath.glob("*.obj"))
    if not obj_files:
        print(f"No OBJ files found in: {current_folderpath}")
        return

    print(f"--- STARTING CLEANUP: {len(obj_files)} files ---")

    for obj_path in obj_files:
        print(f"========== {obj_path.name} ==========")
        # clear scene for next frame
        cmds.file(new=True, force=True)

        try:
            # import
            cmds.file(
                obj_path.as_posix(),
                i=True,
                type="OBJ",
                ignoreVersion=True,
                mergeNamespacesOnClash=True,
                namespace=":",
            )

            strip_namespaces()

            mesh = get_mesh_transform()
            if not mesh:
                print(f"SKIP (no mesh): {obj_path.name}")
                continue

            face_count = cleanup_mesh(mesh)

            if face_count:
                print(f"---> FIXED {face_count} faces.")
            else:
                print("---> OK")
 
            # export back to same path
            cmds.select(mesh, replace=True)
            cmds.file(
                obj_path.as_posix(),
                exportSelected=True,
                type="OBJexport",
                options=obj_export_options,
                force=True,
            )
        except Exception as e:
            print(f"FAILED: {obj_path.name}")
            print(e)

    print("--- CLEANUP COMPLETE ---")


if __name__ == "__main__":
    import maya.standalone
    maya.standalone.initialize(name="python")

    cmds.scriptEditorInfo(
        suppressErrors=True,
        #suppressWarnings=True,
        suppressInfo=True,
    )

    try:
        run_cleanup()
    finally:
        maya.standalone.uninitialize()