# nLol Tech Art Tools

> Modular rigging system and tech art pipeline tools for Maya.

![Maya 2026.3](https://img.shields.io/badge/Maya-2026.3-1f6feb?style=flat-square&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Windows 11](https://img.shields.io/badge/Windows-11-0078D4?style=flat-square&logo=windows&logoColor=white)
![PySide](https://img.shields.io/badge/UI-PySide-41CD52?style=flat-square)

**Quick links:** [Overview](#overview) · [Installation](#installation) · [Auto Rigger](#modular-auto-rigger) · [Animation](#animation-shelf--menu) · [Modeling](#modeling-shelf--menu) · [Nurbs Curves](#nurbs-curves-shelf--menu) · [Rigging](#rigging-shelf--menu) · [Utils](#utils-shelf--menu) · [Naming](#nlol-naming-convention)

---

## Overview
- Build the same rig across multiple character versions with ease.
- Adjust joints and rebuild without starting over.
- Easily edit and adapt rig build setup to custom rigs.
- Add any number of rig modules to a character.
- Config-driven setup via TOML files.
  - Set up rig modules via `rig_object_data.toml`.
  - Set up parent spaces via `rig_parent_spaces.toml`.
  - Set up display layers via `rig_display_layers.toml`.
  - Set up blendshape set driven keys via `blendshape_setdrivenkeys.toml`.
- Rig build entry point: `.../nlol-tech-art-tools/maya/nlol/core/rig_setup/rig_build.py`
- Launch rig build via menu/shelf button: `nLol Rigging < Build Rig`
- Switch the active rig folder via `Rig Context UI` (or `/defaults/rig_context.json`).
- Build and save the active rig, or batch-build all auto-rig folders under a character.
- Example rig setup: `maya/nlol/defaults/unrealRigExample/`
- Additional tools include animation retargeting, anim picker, control mirroring, asset scattering, and more.
- Also, saving/loading of skin weights, control shapes, materials, animations, and  
  cloth and curve dynamics settings is supported.

### Installation
- Drag and drop `maya_install.py` into the Maya viewport.
  - Creates Maya menu and shelves automatically.  
    - Updates `Maya.env` with `MAYA_MODULE_PATH` pointing to `.../nlol-tech-art-tools/maya/`.  
  - Points to wherever user has placed folder.  
  - Allows nLol Tools in Maya to locate `nlol_env.mod`.  
- To uninstall, drag and drop `maya_uninstall.py` into Maya viewport.
  - Removes shelves/menus and folder path from `Maya.env`.
  - Restart Maya.

### Locations
- Generic save location for json files is the `/defaults` folder.
  - `.../nlol-tech-art-tools/maya/nlol/defaults/`.
  - The defaults folder also contains readmes for certain config files.
- Active **rig folder path** is defined in `/defaults/rig_context.json`  
  which is read by `/defaults/rig_folder_path.py` to resolve the path dynamically.
  - Must be adjusted to user custom rig folder.
  - Can also be switched in-session with `Rig Context UI`.
  - Example: `D:/projects/fantasy_world/characters/dragon/rig/auto_rig/`
- "Custom rig folder", "auto-rig folder", and "rig folder" are used interchangeably.
  - This is the folder containing `rig_object_data.toml` and the other build files.

## Modular Auto Rigger
- For rig building example, see custom rig folder `/defaults/unrealRigExample/`.
  - Set custom rig folder here to test rig building.
  - Or set to custom rig folders in `/defaults/otherRigExamples/` for additional testing.
- Readmes to aid in creating the toml configs can be found in the `/defaults` folder.
  - Example: `.../nlol-tech-art-tools/maya/nlol/defaults/readme_rig_object_data.md`
### Basic Steps
1. Add custom rig folder path to `/defaults/rig_context.json` using the `folderpath` parameter.
   - Current rig folder is the `active` one, which can be changed while Maya is open.
   - Easiest via `nLol Utils < Rig Context UI` (also available under Rigging).
2. Create character model/s and save as `model.ma` in `/custom_rig_folder`.
3. Create a skeleton for the model/s and save as `skeleton.ma` in `/custom_rig_folder`.
4. Skin skeleton to model/s. Export weights to `/custom_rig_folder/skin_weights/`.
   - Rename model skin clusters to "meshBaseName_skinCluster" before exporting.
     - Easily rename with `nLol Rigging < Rename Skin Cluster`.
   - Export in one click via `nLol Rigging < Export Skin Cluster`.
     - Or manually export weights with Maya `Modeling < Deform < Export Weights...` as XML.
5. Now test that the skeletal mesh builds via `nLol Rigging < Build Skeletal Mesh Only`.
6. Next, set up rigging data in `rig_object_data.toml`.
   - Manually create this toml file in `/custom_rig_folder`.
   - This toml file contains a list of rig module names and the joints they will be applied to.
7. If needed, add extra rig objects to `rig_helpers.ma`.
   - For instance, reverse foot control locators or COG control locator. 
8. Test that everything builds so far via `nLol Rigging < Build Rig`.
9. Once rig is building successfully, adjust rig control curve shapes.
   - Save to `rig_control_curves.json` via `nLol Rigging < Save Rig Control Curves`.
10. Next, set up parent spaces with `rig_parent_spaces.toml`.
    - Manually create toml in rig folder.
    - User sets up parents for rig controls in this file.
11. Optionally, set up display layers next with `rig_display_layers.toml`.
12. Then add any final python code to `finalize_script.py`.
13. Build the rig again and make sure everything works. 
    - Save the rig file now. Reference in for animation.
    - Or use `nLol Rigging < Build Rig, Update Materials, and Save Files` to build, update materials, and save in one step.
      - Saves `{name}_skeletalMesh.ma` and `{name}_rig.ma` next to the auto-rig folder.
#### Rig Materials
- Materials should be manually updated in `model.ma` or via "Build Save Active/All" rig feature.
  - In the model file materials can be updated via `nLol Modeling < Update Materials`.
  - Make sure materials have been previously exported to `/custom_rig_folder/materials`.
- Export materials from raw working file with `nLol Modeling < Export Materials`.
#### Rig Mirror Attributes
- Set up mirror attributes for rig controls. 
  - Add attributes to controls first if needed. `nLol Animation < Add Mirror Attributes`
  - Then save to rig folder with `nLol Animation < Save Mirror Attributes`.
    - Saves as `mirror_attributes.json` in rig folder.
- Mirror attributes will be automatically added to controls when rig is built.
  - Or manually apply to controls with `nLol Animation < Load Mirror Attributes`.
- This allows rig controls to be mirrored across local X axis when animating.
#### Rig Cloth Setup
- Cloth data saves to `/custom_rig_folder/dynamics_data/`.
- Use `nLol Rigging < Save Attach Verts and Object` to export cloth data.
  - Select verts of cloth mesh and attach object, then run.
  - Saves to file with suffix `*DynamicConstraint.json`.
- Use `nLol Rigging < Save Collision Meshes` to export collision mesh names.
  - Saves to `collision_meshes.json`.
  - Save actual collision meshes manually in `rig_helpers.ma`.
- Use `nLol Rigging < Save nCloth Settings` to save cloth settings.
  - Settings are applied when rig is built.
  - An nCloth object must be selected when saving out the settings.
  - Easiest to adjust cloth settings with rig built. Then export and rebuild rig.
- Save cloth geometry in `rig_helpers.ma`.
  - Or if cloth is part of final model its okay to save in `model.ma`.
- Cloth setup will be applied when rig is built.
  - A cloth auxiliary control will be added to the rig, with scene cloth attributes.
#### Rig Curve Dynamics Setup
- Curve dynamics data also saves to `/custom_rig_folder/dynamics_data/`.
- Use `nLol Rigging < Save hairSystem/follicle/nucleus Settings` to export settings.
  - Select hairSystem, follicle, and/or nucleus nodes, then run.
  - Saves to files with suffix `*HairSystemShapeSettings.json`, `*FollicleShapeSettings.json`, or `*nucleusSettings.json`.
- Settings auto-load when the rig is built (for example via `fk_ik_spline_chain_mod`).
- Or apply manually with `nLol Rigging < Apply hairSystem/follicle/nucleus Settings`.
#### Rig Blendshape Setup
- Save blendshapes to `/custom_rig_folder/blendshapes.ma`.
- Blendshapes should be on a single mesh. 
  - Mesh should be same name as original except with string "BlendShapes".
    - So all "head_geo" blendshapes should be on "headBlendShapes_geo", etc...
- Add rig controls for blendshapes to `rig_helpers.ma`.
- Configure setup for blendshapes and controls in `/custom_rig_folder/blendshape_setdrivenkeys.toml`.
  - This config file needs to be manually created.
  - Contains data for connecting rig controls to blendshapes via set driven keys.
- See `/defaults/readme_blendshape_setdrivenkeys.md` for more details on toml setup.

## Animation Shelf / Menu
*Transforms, keyframes, mirroring, retargeting, and animation UIs.*

- **Select All Controls**
  - Select all controls under rig group. Defaults to the "_rigGrp" if nothing selected.
- **Reset All Controls**
  - Resets selected ctrls and their descendants, or all ctrls under groups containing string "_rigGrp" if nothing selected.
  - Resets translate, rotate, and scale.

- **Save/Load Transforms for Selected**
  - Saves "translate", "rotate", "scale" for selected objects.
  - Saves to `/defaults/other_control_transforms.json`.
  - Load applies to the saved object names (no selection required).
- **Paste Transforms to Selected**
  - Load transforms onto selected objects in the same selection order as saved.
  - Useful as a copy/paste transforms function.
- **Select Hierarchy Transform Nodes**
  - Select hierarchy; transform nodes only. Leaves out the initial selection (usually a group).

- **Save/Load Keyframe for Selected**
  - Saves current keyframe data for selected objects.
  - Saves to `/defaults/other_control_keyframes.json`.
  - Load to saved objects, or load to currently selected objects.
- **Save/Load All Keyframes**
  - Saves all keyframes within current playback range for selected objects.
  - Saves to `/defaults/other_control_keyframes.json`.

- **Mirror Opposite Ctrl, Mirror Selected Ctrl**
  - Mirror selected controls "left to right" or "right to left".
  - Mirror to opposite side controls or mirror opposite to selected.
  - Requires mirror attributes.  Mirrors across X axis in rig local space. 
- **Add Mirror Attributes**
  - Add mirror attributes to rig controls via `nLol Animation < Add Mirror Attributes`.
  - Example: ".mirrorTranslateX", ".mirrorRotateX"
- **Remove Mirror Attributes**
  - Remove mirror attributes from selected controls.
- **Save/Load Mirror Attributes**
  - Save mirror attributes for selected controls.
  - Loads in mirror data to saved control names. No selection required for loading.
  - Saves to `/defaults/other_mirror_attributes.json` (generic),  
    or to `/custom_rig_folder/mirror_attributes.json` (rig folder).    
- **Show/Hide Mirror Attributes**
  - Show and hide rig control mirror attributes in channel box.

- **Temp Locator**
  - Create temporary locator at world origin.
  - Useful for creating a temp pivot with multi parent constraint.
- **Multi Parent Constraint**
  - Useful for constraining multiple ctrls to locator for temp pivot.
  - Constrains to last selected object.

- **Animation Retargeting**
  - **Source Target Connect**
    - Source/target control connections via retarget data config file. 
    - Supports namespaces.
    - Various types of constraint connections supported.
  - **Delete Connections**
    - Easily delete connections.
  - **Copy Keyframes**
    - Copy/bake keyframes between source/target controls.
    - Keys target on same frames and attributes as source.
    - Supports copying in/out tangent types (auto, linear, stepped, etc).
    - Supports copying tangent weights and angles.
    - Useful if trying to preserve animation data instead of baking every keyframe.
  - Loads data from `/custom_rig_folder/retarget_data.toml`.  
  - See `/defaults/readme_retarget_data.md` for more detail.  

- **Animation Save Load UI**
  - Supports namespaces.
  - Supports in/out tangent types and tangent weights/angles.
  - Choose custom save location or saves to `/defaults/other_animation_data.json`.
  - Select controls and click save.
- **nLol Anim Picker**
  - Open the nLol animation picker UI for selecting and working with rig controls.
  - Saves to and loads from `/custom_rig_folder/anim_picker/anim_picker.json`.
  - Add jpg/png files to `anim_picker` folder for use.
- **Parent Space Match UI**
  - UI for space switch matching. Keeps ctrl transforms when switching parent spaces.

## Modeling Shelf / Menu
*Materials, layout, proxies, scattering, and mesh utilities.*

- **Export Materials**
  - Exports materials to `/custom_rig_folder/materials/`.
  - Select objects with materials connected via hypershade and click export.
  - Example material name: "characterProp_mat"
  - Materials saved to MA files named after materials.
- **Import Materials to Selected**
  - Import materials for selected mesh objects from `/materials` folder.
  - Mesh should have same base name as material.
- **Update Materials**
  - Updates all materials in scene based off whats in the `/materials` folder.
  - Or update materials of only selected objects.
  - Scene materials will be updated if they have same name as a saved material.

- **Substance Arnold Material**
  - Drag and drop "BaseColor", "OcclusionRoughnessMetallic", and "Normal" map into hypershade window.
  - Select the three file nodes and a shading group node, then click the button to create material.
  - Uses "openPBRSurface".
- **Toolbag Arnold Material**
  - Same as Substance material except drop in "albedo", "mixmap", and "normal" map to hypershade.
- **Megascans Arnold Material**
  - Same workflow for Megascans environment assets.
  - Required maps: Albedo, Roughness, Normal, plus a shading group.
- **Rename Megascans Object**
  - Rename selected Megascans objects based off assigned material shading group.
  - Replaces "_suffix" with "_geo".
- **Connect Files to OpenPBR**
  - Select file nodes and an openPBR material (or shading group), then connect.
  - Megascans variant also renames after the texture path parent folder.
- **File to aiImage**
  - Switches file node to aiImage node.
  - Option to keep old file node.

- **Reset Object Transforms**
  - Reset selected object transforms.
- **Grid Layout**
  - Spread out selected objects in ZX 2d grid.  
- **Duplicate Replace**
  - Replace selected objects with the first selected, while keeping target transforms.
  - Variants: instanced, instanced with source as first, or regular (no instance).
- **Instance to Regular**
  - Duplicate and replace instanced objects with regular objects.

- **Assign Random Proxy Color**
  - Assigns random viewport color to selected Arnold proxies (.ass).
- **Proxy View Mode**
  - Switch Arnold proxies between shaded, shaded polywire, and wireframe in viewport.

- **Scatter Tool UI**
  - Scatter objects on surface of last selected based on vertices, bounding box, or surface area.
  - Apply random transform values to selected objects.
  - Orient scattered objects to surface normals, with random variation if needed.
  - Scatter objects in volume of last selected object based off bounding box.
  - Create random objects for test scattering.
  - Scatter objects in realtime to any area of a mesh or nurbsSurface.
- **Export Import Tool UI**
  - Export multiple objects to custom folder. Supports OBJ, FBX, MA, MB, and ASS.
  - Each object saved to its own file named after object.
  - Import multiple files as well.

- **Copy IFF Mask to Xgen Folder**
  - Backup Xgen Core IFF mask from the 3d Paint Tool to a bespoke xgen paintmaps folder.
- **Vert Snapper**
  - Snap first selected object's verts to closest verts on the second selected object.
- **Hard Edge UV Seams**
  - Create UV seams along hard edges.

## Nurbs Curves Shelf / Menu
*Ready-to-use control curve and nurbs shapes.*

- Create different ready to go curve shapes with the click of a button.
  - Useful when creating rig controls.
- Includes nurbs primitives (sphere, cube) plus common control shapes:
  - Box, Circle, Global, Pyramid, Sphere, Tri Circle, Locator, Arrow Twist, Cylinder,
    Four Arrow, Square, Octagon, Dodecagon, Hexadecagon.

## Rigging Shelf / Menu
*Joint helpers, rig build/save, dynamics, skins, and blendshapes.*

- **Create Joint**
  - Creates joint at world origin.
- **Joint Axis Locator**
  - Create locator parented under joint for visualizing axis.
- **Locator Snap Parent**
  - Parent constrain locator to joint for visualizing axis.
- **Locator Constrain Joints**
  - Create locator as parent of selected via parent constraint, for a quick and dirty joint control. 
- **Show Joint Attributes**
  - Show useful joint attributes like wireColor, rotateAxis, jointOrient, etc.
- **Snap to Closest Axis**
  - Snap select objects to closest axis of last selected object.
    - If the axis were lines drawn out from the last selected object.
  - Option to only translate objects without aligning rotation.
- **Object Aim X, Snap Align X**
  - Aim first selected object's X axis at second selected object via aim constraint.
- **Joint Orient X**
  - Aim first selected joints X axis at second selected joint via "Orient Joint".
--------------------  
- **Save/Load Control Curves**
  - Select rig control curves and run.
  - Saves to and loads from `/defaults/other_control_curves.json`.  
  - No selection needed to load shapes in.
- **Replace Curve Shapes**
  - Replace rig control curves shapes with first selected curve.
- **Mirror Control Curves**
  - Mirror selected control curves shapes to opposite side controls, across world space X.

- **Interactive Playback / Hierarchy / Backface Culling / Go to Bind Pose**
  - Quick Maya convenience buttons for common viewport and skinning workflow actions.
- **Print Object Type / Print Selected List / Print Selected String List**
  - Print selected object type, or a Python/string list of selected objects.
- **Print Name Components (nLol)**
  - Print selected name components using the nLol naming convention.
- **Hide Rig Clutter**
  - Hide rig clutter after showing the entire hierarchy.
- **Replace Node Connections**
  - Replace old node connections with new node connections.
  - First selected is the new node, second selected is the old node.
--------------------  
- **Build Skeletal Mesh Only**
  - Build rig up to the skeletal mesh, then stop.
  - This includes importing model, skeleton and applying skin weights. 
- **Build Rig**
  - Build entire rig from `/custom_rig_folder/rig_object_data.toml`.
    - Saves rig module data, including what rig modules build on what joints.
    - See `/defaults/readme_rig_object_data.md` for more detail.  
  - Other config files, scripts, and Maya files that help build the rig include:
    - These files are placed in the root `/custom_rig_folder`. Not all are required.
    - `rig_parent_spaces.toml` 
      - Set up parent spaces for the rig.
      - See `readme_rig_parent_spaces.md`.
    - `rig_display_layers.toml`.
      - Set up additional display layers for the rig.
      - See `readme_rig_display_layers.md`.
    - `blendshape_setdrivenkeys.toml`. 
      - Set up blendshape connections to rig controls with set driven keys.
      - See `readme_blendshape_setdrivenkeys.md`.
    - `rig_control_curves.json`
      - Saves control curve shapes for the rig.
    - `mirror_attributes.json`
      - Saves mirror attribute data for rig controls. Used for mirroring during animation.
    - `finalize_script.py`
      - A final python script to run at the end of the rig build.
    - `model.ma`
      - Contains the model geometry for the rig.
    - `skeleton.ma` 
      - Contains skeleton for the rig.
    - `rig_helpers.ma`
      - Contains extra Maya objects for the rig, such as locators or cloth attach objects.
    - `blendshapes.ma`
      - Contains blendshapes weighted to single models.
  - Additional folders inside `/custom_rig_folder` include:
    - `/skin_weights`
      - Contains skin weights for the rig.
    - `/materials`
      - Contains materials for the rig. Not required.
    - `/dynamics_data` 
      - Contains cloth and curve dynamics data for the rig. Not required.
  - See example rig setup in `/defaults/unrealRigExample/`.
- **Build Rig, Update Materials, and Save Files**
  - Build the active auto-rig folder, update materials, and save out files.
  - Updates materials in `model.ma` and re-saves it.
  - Saves `{name}_skeletalMesh.ma` and `{name}_rig.ma` next to the auto-rig folder.
    - `{name}` is the `name` from `rig_context.json`.
  - Change active folder via `rig_context.json` or `Rig Context UI`.
- **Build All Rigs in Character Folder**
  - Build all auto-rig folders under the character (parent of the active rig folder).
  - Updates materials and saves `{name}_skeletalMesh.ma` and `{name}_rig.ma` for each.
  - Main rig folder should contain string `autorig`, `auto-rig`, or `auto_rig`, case-insensitive.
- **Rig Context UI**
  - Set/switch the active rig folder.
- **Save Rig Control Curves**
  - Save control curve shapes to `/custom_rig_folder/rig_control_curves.json`.
- **Delete Rig**
  - Remove rig from scene and clean up constraints, leaving only skeleton and mesh.
--------------------  
- **Setup nCloth Rig Components**
  - Sets up nCloth for rig. Make sure rig nCloth settings are saved first.
  - Usually run through rig build.
  - Rig nCloth data in `/custom_rig_folder/dynamics_data`.
- **Save Attach Verts and Object**
  - Saves selected verts and selected object names to file with suffix `*DynamicConstraint.json`.
  - Selected verts will identify cloth mesh and what verts to attach.
  - Selected object will identify the attach object.
  - Cloth mesh should not be initialized yet.
- **Save Collision Meshes**
  - Saves selected collision mesh names to `collision_meshes.json`.
- **Save nCloth Settings**
  - Save settings for selected nCloth objects to files with suffix `*NClothShapeSettings.json`.
  - Supports having ramp attached to `inputAttractMap` attribute.
  - Auto applies when rig built.
- **Apply nCloth Settings**
  - Apply saved nCloth settings from `dynamics_data/` folder.   
--------------------  
- **Save hairSystem/follicle/nucleus Settings**
  - Save settings for selected hairSystem, follicle, or nucleus objects to `dynamics_data/` folder.   
    - Saves to files with suffix `*HairSystemShapeSettings.json`, `*FollicleShapeSettings.json`, or `*nucleusSettings.json`.   
  - Used for saving curve dynamics data.   
    - For example, when curve dynamics are applied via the "fk_ik_spline_chain_mod" rig module.   
  - Auto loads settings when rig is built.   
- **Apply hairSystem/follicle/nucleus Settings**
  - Apply saved hairSystem, follicle, or nucleus settings from `dynamics_data/` folder.   
--------------------  
- **Select Object Shapes**
  - Select all transforms shapes. Useful for curve shape settings.
- **Show Curve Attributes**
  - Show useful curve attributes in channel box. Double click to remove.
- **Select Shapes Show Attributes**
  - Selects transform shapes then shows useful curve attributes.
- **Select All Controls**
  - Select all controls under rig group. Defaults to the "_rigGrp" if nothing selected.
- **Reset All Controls**
  - Resets all ctrls under groups containing string "_rigGrp" if nothing selected.
    - Or resets selected ctrls and their descendants. 
  - Resets transforms and other basic attributes.
- **Reset All Controls (Keyable Attrs)**
  - Same as "Reset All Controls" except resets all keyable attributes.
--------------------  
- **Assign Random Material**
  - Assign a standard surface material with random color to selected objects.
- **Create Follicle At Surface**
  - Create and attach follicle at nearest "example_surface" point to "example joint".
  - Surface may be a regular polygonal mesh or nurbs surface.
--------------------  
- **Rename Skin Cluster**
  - Rename selected mesh's skin cluster using nLol naming convention.
- **Export Skin Clusters**
  - Select one or more skinned meshes and export their skin clusters to xml.
  - Uses the index method. Exports to `/custom_rig_folder/skin_weights`.
  - Skin cluster base name should be same as mesh.
- **Import Skin Clusters**
  - Import xml skinCluster files from `/skin_weights` folder and apply them.
  - No mesh selection required.
  - Mesh (shape) names and vertex order should be same as when exported.
- **Import Skin Selected Only**
  - Same as "Import Skin Clusters" but only imports skin weights for selected.
- **Select Skinned Joints**
  - Gets skinned joints from selected mesh transform.
 --------------------  
 - **Duplicate Out Blendshapes**
   - For selected meshes, create duplicate for each blendshape weight.
 - **Copy Blendshapes**
   - Copy blendshapes from first selected mesh to second.
 - **Duplicate Arkit Blendshapes**
   - Duplicate selected mesh for each keyframed blendshape pose listed in `arkit_blendshapes.toml`. 
   - Frame 1-52.
 - **Connect Blendshapes**
   - Connect blendshapes to control setup. 
   - Rig controls connect to set driven keys which drive the blendshapes.
   - Runs when rig is built.
   - Connection data saved in `/custom_rig_folder/blendshape_setdrivenkeys.toml`.
   - See `/defaults/readme_blendshape_setdrivenkeys.md` for more detail. 
 - **Copy Blendshapes (No Selection)**
   - Copy BlendShapes from source to target mesh. Deletes source mesh.
   - Source mesh name is same as target except contains string "BlendShapes".
   - No selection needed.

## Utils Shelf / Menu
*Viewport navigation, debugger helpers, and nLol UIs.*

- **New Display Layer**
  - Create a display layer without the "makeCurrent" flag.
- **Collapse Display Layers**
  - Clear empty Layer Editor id slots (Maya 2026). Save and re-open if New Layer still fails.
- **Maya Debugger**
  - Start python debugger for Maya.
  - Assumes "debugpy" folder already setup in Maya "scripts" folder.
  - See `maya/nlol/core/standalone/maya_debug.py` for a bit more info.
- **Port Connection**
  - Connect Maya to port 7001.

- **Set Hotkey for "Camera Pivot to Mouse"**
  - Sets hotkey to "alt+f".
  - When pressed camera tumble pivot set to first raycast intersecting a polygon from mouse point.
  - Makes viewport camera rotation very predictable.
  - Hotkey can be managed in Maya hotkey editor.
  - May need to create custom "Hotkey Set" first, before running this.
- **Set Hotkey for "Camera Pivot to Selected"**
  - Sets hotkey to "shift+f".
  - When pressed camera tumble pivot set to selected object's pivot.  
  - Much more predictable when selecting joints. 
    - Pivot set to selected joint pivot, instead of joints bounding box center.  
  - Also, doesn't zoom in automatically like default hotkey "f".  
- **Create Camera Pivot Locator**
  - To help confirm whether "Camera Pivot" hotkeys are working.
  - Small locator variant also available.
- **Set Camera Tumble Tool Settings**
  - Sets the camera pivot settings to work with "Camera Pivot" hotkeys.
  - View < Camera Tools < Tumble Tool
- **Reset Tumble Tool Settings**
  - Resets camera pivot settings to Maya default.

- **Center All Windows**
  - Centers all Maya windows to primary monitor, including custom PySide windows.
  - Useful if windows lost from adjusting multi-monitor display.

- **nLol Main UI**
  - Opens nLol dockable UI that contains all nLol buttons.
  - An alternative to the shelf or menu. 
- **Rig Context UI**
  - Set/switch the active rig folder.
- **nLol Multi-tool UI**
  - PySide UI with useful tools laid out in tabs.
- **nLol Anim Picker**
  - Open the nLol animation picker.
  - Saves to and loads from `/custom_rig_folder/anim_picker/anim_picker.json`.
  - Add jpg/png files to `anim_picker` folder for use.
- **Renamer Tool UI**
  - Helpful tool for quickly renaming objects in Maya. 
- **Check / Clear Registry Data**
  - Check or clear nLol registry data (global dictionary for Maya objects).

## Reload Shelf
*Refresh shelves and menus after editing `*_list.py` button definitions.*

- **Reload nLol Shelves**
  - Helpful when adding new shelf buttons via `/shelves_menus/*_list.py` files.
- **Reload nLol Menus**

## nLol Naming Convention
- Pattern:
  ```
  <name>_<direction>_<id>_<type>
  ```
  - `<name>` - base name of an object
  - `<direction>` - `"left"` or `"right"`
  - `<id>` - `"01"` or `"a01"`
  - `<type>` - `"geo"`, `"grp"`, `"ctrl"`, etc.
- Hybrid snake_case with camelCase components.
- Not all components required.
- See more detail in `maya/nlol/core/rig_setup/README.md`.
- Examples: `head_geo`, `arm_left_01_ctrl`, `eyeLid_right_ctrlGrp`, `tail_02_jnt`, `global_ctrl`
