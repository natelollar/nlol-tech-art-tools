# nLol Tech Art Tools
- Includes a rigging framework and other Maya tools. WIP.
- Easily build same rig on multiple versions of a character.
- Easily adjust joints and rebuild the rig.
- Setup rig modules via custom toml file.
  - `rig_object_data.toml`
- Setup parent spaces via custom toml file.
  - `rig_parent_spaces.toml`
- Easily edit adapt rig build script to custom rigs. 
  - `rig_build.py`

----------
- Tested in Maya 2025.3, Windows 11.

----------
- Drag an drop maya_install.py into Maya viewport.
  - Will create Maya menu and shelves.
  - Updates Maya.env with a MAYA_MODULE_PATH.
    - The path will specify the `maya/` folder in this folder.
    - This allows nLol Tools to find `nlol_env.mod`.
