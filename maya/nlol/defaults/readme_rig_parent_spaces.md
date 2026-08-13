### Overview: `rig_parent_spaces.toml`
```
Setup custom rig parent spaces for rig modules. 
Also, set up base parent or single parent space when no parent spaces needed.
Constrain child ctrls to parent ctrls or objects.
Entering the ctrl name will automatically find the parent switch group.
```

#### [[control]] Parameters:
##### Shared:
- `control` (str): Child control to set up parent spaces for.  May contain single ctrl or multiple in a string list.
    - May want to list multiple ctrls for certain cases where all other parameter values are the same.
- `parents` (str): Parent objects. Usually other ctrls but may be any Maya transform. 
    Optional if "base_parents" is used.
- `mirror_right` (bool): Use left control data for the right side. 
    - Currently works with "left" in the control name.
    - See "swap_side_str()" function.  
    Optional.
##### Base Parent:
- `base_parents` (str): Parent and scale constrain the base parent group, above the parent switch group. 
    - May be used instead of a single "parents" object for a regular parent relationship. 
    - Also, used when a point constraint needs full rotate parent constraint above, like for "use_point_constraint".
    - Also, helpful if only enabling rotation switching.
    - May add multiple base_parents values.
- `base_parent` (bool): Used instead of "base_parents" string list. Copies and uses "parents" values in place of "base_parents".
    Do not use both "base_parent" and "base_parents".
##### Separate Transforms:
- `separate_transforms` (bool): Create separate attributes for translate, rotate, and scale.
- `use_point_constraint` (bool): Use point constraint instead of parent translate constraint. Requires "separate_transforms" and "base_parent/s". 
- `skip_translate, skip_rotate, skip_scale` (bool): Skip translate (or point), rotate or scale parent switch setup. 
    - Requires "separate_transforms" and "base_parent/s". 
    - False value is the same as not including the parameter, so the transform won't be skipped.
    - Skip only works for translate and rotate if separate_transforms is on.
    - Skip scale does work for regular "parents" if "base_parent/s" value is also given.
---
*Lists written as "string lists".*
<br/> 
<br/> 

### *Examples `rig_parent_spaces.toml`*:

#### `control`
Required: `control`. `parents` and/or `base_parents`.  
Optional: `mirror_right`, `base_parents`, `base_parent`, `separate_transforms`, `use_point_constraint`, `skip_translate`, `skip_rotate`, `skip_scale`.  
Notes:  
`control` — the child ctrl. Can list more than one if they use the same parents.  
`parents` — what it parents to. One name = always parented there. Several names = a switch.  
`mirror_right` — also set up the right side. Control name needs "left".  
`base_parent` — also parent the group above the switch, using the same "parents" list. Use this when skipping a transform or using a point constraint.  
`base_parents` — same idea, but you pick the objects. Do not use with "base_parent".  
`separate_transforms` — make separate switches for translate, rotate, and scale.  
`use_point_constraint` — follow parent position only. Needs "separate_transforms" and "base_parent".  
`skip_translate` / `skip_rotate` / `skip_scale` — leave that transform off the switch.  

Parent switch.
```toml
[[control]]
control = "ikAnkleLeg_left_ctrl"
parents = "cog_ctrl, root_ctrl, global_ctrl, world_ctrl, ikUpperLeg_left_ctrl, pelvis_ctrl"
mirror_right = true
#separate_transforms = true
#base_parent = true
#base_parents = "pelvis_ctrl"
#use_point_constraint = true
#skip_translate = true
#skip_rotate = true
#skip_scale = true
```

Rotate switch. Translate and scale stay with base_parent/s.
```toml
[[control]]
control = "fkUpperArm_left_ctrl"
parents = "offsetShoulder_left_02_jnt, spine_05_jnt, pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true
mirror_right = true
```

Point constraint. Rotate and scale stay with base_parent/s.
```toml
[[control]]
control = "ikLegPoleVector_left_ctrl"
parents = "cog_ctrl, root_ctrl, global_ctrl, world_ctrl, ikAnkleLeg_left_ctrl, pelvis_ctrl"
separate_transforms = true
skip_rotate = true
skip_scale = true
use_point_constraint = true
base_parent = true
mirror_right = true
```
