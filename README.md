# nLol Tech Art Tools
- Includes a rigging framework and other Maya tools. WIP.
- Easily build same rig on multiple versions of a character.
- Easily adjust joints and rebuild the rig.
- Set up rig modules via `rig_object_data.toml`.
- Set up parent spaces via `rig_parent_spaces.toml`.
- Set up display layers via `rig_display_layers.toml`.
- Easily edit adapt rig build script to custom rigs. 
  - `rig_build.py`
- Run rig build via menu/shelf button.
- Example rig setup in `maya/nlol/defaults/rig_unreal`.

----------
- Tested in Maya 2025.3, Windows 11.

----------
- Drag an drop maya_install.py into Maya viewport.
  - Will create Maya menu and shelves.
  - Updates Maya.env with a MAYA_MODULE_PATH.
    - The path will specify the `maya/` folder in this folder.
    - This allows nLol Tools to find `nlol_env.mod`.
