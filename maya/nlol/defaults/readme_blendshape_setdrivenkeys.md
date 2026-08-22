### Overview: `blendshape_setdrivenkeys.toml`
```
Connect blendshapes or other object attributes to transform ctrls via set driven keys.
For a face ctrl setup, for example, include the ctrls in "rig_helpers.ma".
Include the blendshapes weighted to single meshes in "blendshapes.ma".
```
- Set driven key connections live in "../autoRig/blendshape_setdrivenkeys.toml".  
- Blendshape models live in "../autoRig/blendshapes.ma".
    - Blendshapes weighted to single models.  
        - "headBlendShapes_geo" should be a single model with blendshapes already added.  
    - Model names should have the string "blendshape/s" added.  
        - "headBlendShapes_geo" original file would have been "head_geo".  
- Extra ctrls go in "../autoRig/rig_helpers.ma".  
- Build Rig imports the blendshapes Maya file, then connects from the toml.  

#### Root Level Parameters:
- `start_in_tangent_type, start_out_tangent_type` (str): Set driven key's "in/out tangent type"  
    for animation curve start keyframe. Defaults to "linear".  
    Optional.
- `mid_in_tangent_type, mid_out_tangent_type` (str): Set driven key's "in/out tangent type"  
    for animation curve mid keyframe. Defaults to "auto".  
    Optional.
- `end_in_tangent_type, end_out_tangent_type` (str): Set driven key's "in/out tangent type"  
    for animation curve end keyframe. Defaults to "linear".  
    Optional.

#### [[setdrivenkeys]] Parameters:
##### Driver:
- `transform_crv` (str): The name of the curve to drive the set driven key.
- `crv_attr` (str): The name of the curve's attribute that drives the set driven key.  
    As in "translateX" or "rotateY".
- `transform_crv_attr` (str): Alternative to using "transform_crv" and "crv_attr".  
    Driver curve for set driven key with attribute. 
    Example: "clawOpenClose_ctrl.translateY"
    Do not use with "transform_crv" / "crv_attr".
##### Driven:
- `blendshape_attr` (str): The name of the blendshape attribute as in "noseSneerLeft".  
    Does not include the blendshape node name.
- `object_attr` (str): Full object plus attribute name as in "my_ctrl.my_attribute".  
    Used instead of "blendshape_attr", but not both.  
    Useful for connecting eye roll joints instead of blendshape.
##### Keys:
- `blendshape_start, blendshape_mid, blendshape_end` (float): The start/middle/end blendshape value to be keyed.  
    For the driven attribute; not necessarily a blendshape.  
    Optional.  Defaults to 0.0, None, and 1.0. 
- `object_start, object_mid, object_end` (float): Use instead of "blendshape_start/mid/end". 
    Same but with different names. Useful if no blendshapes and just creating set driven keys. 
    Do not use with "blendshape_start/end".
- `crv_start, crv_mid, crv_end` (float): The start/middle, end transform curve value to be keyed. 
    The driver attribute values. 
    Optional.  Defaults to 0.0, None, and 1.0.
##### Mirror:
- `mirror_right` (bool): Mirror the parameters to the other side as well.
    Optional.
- `mirror_right_invert` (bool): Inverts just the "crv_end" parameter. As in, -1.0 to 1.0.
    Optional.
##### Corrective:
- `blendshape_fix_attrs` (str): A string or string list.  The name of the corrective blendshapes  
    that the "transform_crv" and "crv_attr" drive.  A corrective blendshape should be listed for  
    multiple "setdrivenkeys" values in the list.  So if "ctrl.ty" and "ctrl.tx" both drive the  
    corrective blendshape weight, it should be listed in both "blendshape_fix_attrs" keys.  
    Example: blendshape_fix_attrs = "mouthCornerUpOut_left_fixTarget, mouthCornerDownOut_left_fixTarget"  
---
*Lists written as "string lists".*
<br/> 
<br/> 

### *Examples `blendshape_setdrivenkeys.toml`*:

#### Root
Optional: `start_in_tangent_type`, `start_out_tangent_type`, `mid_in_tangent_type`, `mid_out_tangent_type`, `end_in_tangent_type`, `end_out_tangent_type`.  
Notes:  
`start_*` / `mid_*` / `end_*` — in/out tangent types for the start, mid, and end driven keys.  

```toml
start_in_tangent_type = "linear"
start_out_tangent_type = "linear"
#mid_in_tangent_type = "auto"
#mid_out_tangent_type = "auto"
end_in_tangent_type = "linear"
end_out_tangent_type = "linear"
```

#### `setdrivenkeys`
Required: `blendshape_attr` or `object_attr`. Driver: `transform_crv` + `crv_attr`, or `transform_crv_attr`.  
Optional: `blendshape_start`, `blendshape_mid`, `blendshape_end`, `object_start`, `object_mid`, `object_end`, `crv_start`, `crv_mid`, `crv_end`, `mirror_right`, `mirror_right_invert`, `blendshape_fix_attrs`.  
Notes:  
`blendshape_attr` — blendshape target name only, not the node.  
`object_attr` — "object.attribute" instead of a blendshape. Do not use with "blendshape_attr".  
`transform_crv` / `crv_attr` — driver ctrl and attribute.  
`transform_crv_attr` — same thing as one string, "ctrl.attribute". Do not use with "transform_crv" / "crv_attr".  
`blendshape_start` / `mid` / `end` — driven values. Defaults 0, none, 1.  
`object_start` / `mid` / `end` — same values, other names. Do not use with "blendshape_start/end".  
`crv_start` / `mid` / `end` — driver values. Defaults 0, none, 1.  
`mirror_right` — also set up the right side.  
`mirror_right_invert` — flip "crv_end" on the right side only.  
`blendshape_fix_attrs` — corrective targets this driver also feeds. List the same corrective on every driver that should affect it.  

Blendshape + mirror:
```toml
[[setdrivenkeys]]
blendshape_attr = "noseSneerLeft"
transform_crv_attr = "noseSneerLeft_ctrl.translateY"
#transform_crv = "noseSneerLeft_ctrl"
#crv_attr = "translateY"
mirror_right = true
#blendshape_start = 0.0
#blendshape_end = 1.0
#crv_start = 0.0
#crv_end = 1.0
#mirror_right_invert = true
```

Other direction. Same ctrl, negative driver and driven values:
```toml
[[setdrivenkeys]]
blendshape_attr = "noseSneerLeft"
transform_crv_attr = "noseSneerLeft_ctrl.translateY"
#transform_crv = "noseSneerLeft_ctrl"
#crv_attr = "translateY"
blendshape_end = -1.0
crv_end = -1.0
mirror_right = true
```

Invert the driver on the right side:
```toml
[[setdrivenkeys]]
blendshape_attr = "eyeLookOutLeft"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateX"
mirror_right = true
mirror_right_invert = true
```

Corrective blendshapes. List the same fix target on every driver that should affect it:
```toml
[[setdrivenkeys]]
blendshape_attr = "mouthCornerOut_left_target"
transform_crv = "mouthCorner_left_ctrl"
crv_attr = "translateX"
crv_end = 2.0
mirror_right = true
mirror_right_invert = true
blendshape_fix_attrs = "mouthCornerUpOut_left_fixTarget, mouthCornerDownOut_left_fixTarget"
```

Drive a transform instead of a blendshape:
```toml
[[setdrivenkeys]]
transform_crv_attr = "clawOpenClose_ctrl.translateZ"
object_attr = "clawFinger_a01_ctrlAuxOffsetGrp.rotateZ"
crv_start = 0.0
crv_end = 60.0
object_start = 0.0
object_end = 90
```
