### Overview: `rig_parent_spaces.toml`
```
Setup custom rig parent spaces for rig modules. 
Also, set up base parent or single parent space when no parent spaces needed.
Constrain child ctrls to parent ctrls or objects.
Entering the ctrl name will automatically find the parent switch group.
```

#### Parameters:
- `control` (str): Child contrl to set up parent spaces for.  May contain single ctrl or multiple in a string list.
    - May want to list multiple ctrls for certain cases where all other parameter values are the same.
- `parents` (str): Parent objects. Usually other ctrls but may be any Maya transform. 
- `separate_transforms` (bool): Create seperate attributes for translate, rotate, and scale.
- `base_parents` (str): Parent and scale constrain the base parent group, above the parent switch group. 
    - May be used instead of a single "parents" object for a regular parent relationship. 
    - Also, used when a point constraint needs full rotate parent constraint above, like for "use_point_constraint".
    - Also, helpful if only enabling rotation switching.
    - May add multiple base_parents values.
- `base_parent` (bool): Used instead of "base_parents" string list. Copies and uses "parents" values in place of "base_parents".
- `mirror_right` (str): Use left control data for the right side. 
    - Currently works with any "left" or parents with suffix "_l".
    - See "left_to_right_str()" function.  
- `use_point_constraint` (bool): Use point constraint instead of parent translate constraint. Requires "base_parent/s". 
- `skip_translate, skip_rotate, skip_scale` (bool): Skip translate (or point), rotate or scale parent switch setup. 
    - Requires "separate_transforms" and "base_parent/s". 
    - False value is the same as not including the parameter, so the transform won't be skipped.
    - Skip only works for translate and rotate if separate_transforms is on.
    - Skip scale does work for regular "parents" if "base_parent/s" value is also given.
---
*Lists written as "string lists".*

#### Example:
```
[[control]]
control = "ikLegPoleVector_left_ctrl"
parents = "root_ctrl, pelvis_ctrl, ikAnkle_left_ctrl"
separate_transforms = true
skip_translate = false
skip_rotate = true
skip_scale = true
use_point_constraint = true
base_parent = "root_ctrl"
mirror_right = true
```
