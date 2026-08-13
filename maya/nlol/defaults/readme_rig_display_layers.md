### Overview: `rig_display_layers.toml`
```
Set up specific Maya object display layers via "rig_display_layers.toml". 
Or, add per rig module display layers with "display_layer" in "rig_object_data.toml". 

Uses first object name for display_layer name. "Lyr" suffix added when built.
Or use either base_name or display_layer keys, but not both.
```
#### [[display_layer]] Parameters:
##### Shared:
- `objects` (str): Maya objects.
    - Works as display layer name too if no base_name or display_layer parameters.
- `mirror_right` (bool): Duplicate parameters and replace left with right strings.
    - If not left string in display_layer or base_name, will parent under same display layer.
    Optional.
##### Name:
- `base_name` (str): camelCase name component for the layer. Do not include "_lyr".
    - As in nLol rig naming convention, `<name>_<type>`.
    - Example: A rig_module_name string from "rig_object_data.toml".
    - Layer name becomes "<base_name>_lyr".
- `display_layer` (str): Full display layer name.  
    - Used instead of base_name or first object name.
    Do not use both "base_name" and "display_layer".
##### State:
- `reference` (bool): Reference the display layer by default.
    Optional.
- `hide` (bool): Hide the display layer by default.
    Optional.
---
*Lists written as "string lists".*
<br/> 
<br/> 

### *Examples `rig_display_layers.toml`*:

#### `display_layer`
Required: `objects`.  
Optional: `base_name`, `display_layer`, `reference`, `hide`, `mirror_right`.  
Notes:  
`objects` — Maya objects to put in the layer. Can list more than one.  
`display_layer` — full layer name. Used instead of "base_name" or the first object name.  
`base_name` — layer name becomes "<base_name>_lyr". Do not include "_lyr". Do not use with "display_layer".  
`mirror_right` — also set up the right side. If the layer name has no "left", both sides go in the same layer.  
`reference` — set the layer to reference by default.  
`hide` — hide the layer by default.  

Named layer + mirror. Both sides share the layer because the name has no "left":
```toml
[[display_layer]]
display_layer = "eyesOffset_ctrlLyr"
objects = "fkEyes_left_ctrl"
mirror_right = true
#base_name = "eyesOffset"
#reference = true
#hide = true
```

Name from first object (`eyeGlass_lowGeoLyr`). Reference + mirror:
```toml
[[display_layer]]
objects = "eyeGlass_lowGeo"
mirror_right = true
reference = true
```

Hide:
```toml
[[display_layer]]
objects = "eyesAimParent_ctrlGrp"
hide = true
```

Same layer name, more objects. Second block mirrors into that layer:
```toml
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
```
