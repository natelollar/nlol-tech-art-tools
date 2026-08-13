### Overview: `retarget_data.toml`
```
Retarget keyframe animation data from source ctrl to target ctrls.
Sets keys only on frames and attributes with source ctrl keys. 
Copies in/out tangent types. Optionally, copy tangent weights/angles.

Initially, setup constraints between source and target ctrls.
```
#### Root Level Parameters:
- `source_namespace, target_namespace` (str): Namespace if the rig is referenced.  
    Leave the namespace off "source_ctrls" and "target_ctrls". Add it here instead.
- `tangent_weights_angles` (bool): Whether to copy keyframe tangent weights/angles from source ctrl
    to target ctrls.  Probably won't be useful unless source and target ctrls position and
    rotation axis are closely aligned at default pose.
    Optional.  Defaults to False.
- `key_translate_rotate_all` (bool): Option to key translate and rotate for all frames  
    with source control keys.  A happy balance between baking keys on all frames and only keying keyed   
    attributes. Helps avoid interpolation issues.  
    Optional.  Defaults to False.

#### [[source_target_data]] Parameters:
##### Shared:
- `source_ctrls` (str): Name of source ctrl. The ctrl with keyframe animation data  
    driving the target ctrl.
    Usually just a single ctrl. Multiple for constraint blending.
    First ctrl is primary ctrl for keyframe/tangent data.  
- `target_ctrls` (str): The target ctrls to be driven by source ctrl.  
    Usually just a single ctrl.  Keyframe animation data will be baked onto these ctrls.
- `mirror` (bool): Add another input mirrored to the other side.  
    Left/Right substrings will be mirrored in "source_ctrls" and "target_ctrls".  
    So "l_" becomes "r_", etc.  
##### Constraint:
- `connection_type` (str): Constraint type to be used for connecting  
    source ctrl to target ctrls.  
    Values: "parent", "point", "orient", "pointOrient"  
    Optional. Defaults to "parent".  
    "parent": changes to "point" if rotate locked. changes to "orient" if translate locked.
- `offset` (bool): Whether to use maintainOffset for constraints  
    connecting source and target ctrls.  
    Optional. Defaults to True. 
- `scale_constraint` (bool): Whether to apply a scale constraint for retargeting.  
    Optional. Defaults to True.  
    Skips if scale locked.
- `scale_source_ctrl` (str): If needing to use a different source ctrl for scaling retarget  
    add the name here.  
    Optional.  Defaults to "" (uses "source_ctrls").
##### Pose Offset:
- `target_translate, target_rotate` (str): Initial target ctrl transform offsets.  
    Written as XYZ string list.  
    Example: "0, 0, 0"
---
*Lists written as "string lists".*
<br/> 
<br/> 

### *Examples `retarget_data.toml`*:

#### Root
Optional: `source_namespace`, `target_namespace`, `tangent_weights_angles`, `key_translate_rotate_all`.  
Notes:  
`source_namespace` / `target_namespace` — namespace if a rig is referenced. Leave it off the ctrl names.  
`tangent_weights_angles` — also copy tangent weights and angles. Only useful if source and target align in the default pose.  
`key_translate_rotate_all` — on every source keyframe, also key translate and rotate on the target. Helps fk interpolation.  

```toml
source_namespace = "wyvern_rig"
target_namespace = ""
key_translate_rotate_all = true
#tangent_weights_angles = false
```

#### `source_target_data`
Required: `source_ctrls`, `target_ctrls`.  
Optional: `connection_type`, `offset`, `scale_constraint`, `scale_source_ctrl`, `target_translate`, `target_rotate`, `mirror`.  
Notes:  
`source_ctrls` — the animated ctrl. First name is used for keys and tangents. Extra names blend the constraint.  
`target_ctrls` — ctrls that receive the baked keys. Can list more than one.  
`connection_type` — "parent" (default), "point", "orient", or "pointOrient".  
`mirror` — also set up the other side. Swaps left/right in the ctrl names.  
`target_translate` / `target_rotate` — starting offset on the target before the constraint, as "x, y, z".  

Simple 1:1:
```toml
[[source_target_data]]
source_ctrls = "spine1_Root_ctrl"
target_ctrls = "pelvis_ctrl"
#connection_type = "parent"
#offset = true
#scale_constraint = true
#scale_source_ctrl = ""
#target_translate = "0, 0, 0"
#target_rotate = "0, 0, 0"
#mirror = true
```

Point + mirror:
```toml
[[source_target_data]]
source_ctrls = "l_ikHip_ctrl"
target_ctrls = "ikUpperLeg_left_ctrl"
connection_type = "point"
mirror = true
```

Offset + mirror:
```toml
[[source_target_data]]
source_ctrls = "l_elbow_PV_ctrl"
target_ctrls = "ikArmPoleVector_left_ctrl"
target_translate = "0, 0, -47"
mirror = true
```

Blend sources. First ctrl is primary for keys:
```toml
[[source_target_data]]
source_ctrls = "tail_ik_ctrlB, tail_ik_ctrlA"
target_ctrls = "flexiTail_02_ctrl"
mirror = true
```
