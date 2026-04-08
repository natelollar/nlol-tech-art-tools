### Overview: `display_layers.toml`
```
Set up specific Maya object display layers via "display_layers.toml". 
Or, add per rig module display layers in "rig_object_data.py". 

Uses first object name for display_layer name. "Lyr" suffix added when built.
Or use either base_name or display_layer keys, but not both.
```
#### [[display_layer]] Parameters:
- `objects` (str): Maya objects.
    - Works as display layer name too if no base_name or display_layer parameters.
- `base_name` (str): camelCase name component for the layer. Do not include "_lyr".
    - As in nLol rig naming convention, `<name>_<type>`.
    - Example: A rig_module_name string from "rig_object_data.toml".
- `display_layer` (str): Full display layer name.  
    - Used instead of base_name or first object name.
- `reference` (bool): Reference the display layer by default.
- `hide` (bool): Hide the display layer by default.
- `mirror_right` (bool): Duplicate parameters and replace left with right strings.
    - If not left string in display_layer or base_name, will parent under same display layer.
---
*Lists written as "string lists".*
<br/> 
<br/> 

### *Example `display_layers.toml`*:
```
[[display_layer]]
display_layer = "eyesOffset_ctrlLyr"
objects = "fkEyes_left_ctrl" 
mirror_right = true

[[display_layer]]
objects = "eyeGlass_lowGeo" 
mirror_right = true
reference = true

[[display_layer]]
display_layer = "ezorLeatherStrip_ctrlLyr"
objects = "fkEzorLeatherStripMain_left_ctrlGrp" 
mirror_right = true

[[display_layer]]
objects = "eyesAimParent_ctrlGrp" 
hide = true

[[display_layer]]
display_layer = "worldRootAux_ctrlLyr"
objects = "root_ctrl, global_ctrl, spineSwch_ctrl, neckSwch_ctrl"

[[display_layer]]
display_layer = "worldRootAux_ctrlLyr"
objects = """
ezorLeatherStripAttr_left_ctrl, 
shoulderSwch_left_ctrl, 
armSwch_left_ctrl, 
legSwch_left_ctrl
"""
mirror_right = true

[[display_layer]]
display_layer = "sling_ctrlGrpLyr"
objects = """
slingMain_grp,
slingLoop_grp,
slingParent_ctrlGrp,
slingParentOffset_ctrlGrp
"""

[[display_layer]]
objects = "sling_lowGeo"
reference = true

[[display_layer]]
objects = "slingRock_lowGeo"
reference = true

[[display_layer]]
objects = "sword_lowGeo"
reference = true

[[display_layer]]
objects = "rockBag_lowGeo"
reference = true

[[display_layer]]
display_layer = "blendshapeFace_ctrlLyr"
objects = "headBlendShape_ctrlGrp"
#hide = true

[[display_layer]]
objects = "squishyFaceBlendShapeMain_grp"

```