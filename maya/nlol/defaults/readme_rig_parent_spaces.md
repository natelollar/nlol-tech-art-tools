### Overview: `rig_parent_spaces.toml`
```
Setup custom rig parent spaces for rig modules. 
Also, set up base parent or single parent space when no parent spaces needed.
Constrain child ctrls to parent ctrls or objects.
Entering the ctrl name will automatically find the parent switch group.
```

#### [[control]] Parameters:
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
    - See "swap_side_str()" function.  
- `use_point_constraint` (bool): Use point constraint instead of parent translate constraint. Requires "base_parent/s". 
- `skip_translate, skip_rotate, skip_scale` (bool): Skip translate (or point), rotate or scale parent switch setup. 
    - Requires "separate_transforms" and "base_parent/s". 
    - False value is the same as not including the parameter, so the transform won't be skipped.
    - Skip only works for translate and rotate if separate_transforms is on.
    - Skip scale does work for regular "parents" if "base_parent/s" value is also given.
---
*Lists written as "string lists".*
<br/> 
<br/> 

### *Example `rig_parent_spaces.toml`*:
```
# ---------- base ----------
[[control]]
control = "global_ctrl"
parents = "world_ctrl"

[[control]]
control = "root_ctrl"
parents = "global_ctrl"

[[control]]
control = "cog_ctrl"
parents = "root_ctrl"

[[control]]
control = "pelvis_ctrl"
parents = "cog_ctrl, root_ctrl, global_ctrl, world_ctrl"

# ---------- neck ----------
[[control]]
control = "fkNeck_01_ctrl, ikNeckStart_ctrl"
parents = "spine_05_jnt, pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true

# ---------- spine ----------
[[control]]
control = "fkSpine_01_ctrl, ikSpineStart_ctrl"
parents = "pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true

# ---------- shoulder/clavicle ----------
[[control]]
control = "fkShoulder_left_01_ctrl"
parents = "spine_05_jnt, pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true
mirror_right = true

[[control]]
control = "ikShoulderStart_left_ctrl"
parents = "spine_05_jnt"
mirror_right = true

# ---------- arms/wings ----------
[[control]]
control = "ikUpperArm_left_ctrl"
parents = "offsetShoulder_left_02_jnt"
mirror_right = true

[[control]]
control = "fkUpperArm_left_ctrl"
parents = "offsetShoulder_left_02_jnt, spine_05_jnt, pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true
mirror_right = true

[[control]]
control = "ikEndArm_left_ctrl"
parents = "cog_ctrl, root_ctrl, global_ctrl, world_ctrl, spine_05_jnt, pelvis_ctrl"
mirror_right = true

[[control]]
control = "ikArmPoleVector_left_ctrl"
parents = "cog_ctrl, root_ctrl, global_ctrl, world_ctrl, ikEndArm_left_ctrl, spine_05_jnt, pelvis_ctrl"
mirror_right = true

# ---------- fingers ----------
[[control]]
control = """
wingFinger_a01_left_ctrl, 
wingFinger_b01_left_ctrl, 
wingFinger_c01_left_ctrl,
wingFinger_d01_left_ctrl,
wingFinger_e01_left_ctrl
"""
parents = "wrist_left_jnt"
mirror_right = true

[[control]]
control = "wingFinger_c02_left_ctrl"
parents = "wingFinger_c01_left_ctrl"
mirror_right = true

# ---------- leg ----------
[[control]]
control = "fkUpperLeg_left_ctrl"
parents = "pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl" 
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true
mirror_right = true

[[control]]
control = "ikUpperLeg_left_ctrl"
parents = "pelvis_ctrl"
mirror_right = true

[[control]]
control = "ikLegUpperPoleVector_left_ctrl"
parents = "cog_ctrl, root_ctrl, global_ctrl, world_ctrl, ikAnkleLeg_left_ctrl, pelvis_ctrl"
separate_transforms = true
skip_rotate = true
skip_scale = true
use_point_constraint = true
base_parent = true
mirror_right = true

[[control]]
control = "ikLegLowerPoleVector_left_ctrl"
parents = "cog_ctrl, root_ctrl, global_ctrl, world_ctrl, ikAnkleLeg_left_ctrl, pelvis_ctrl"
separate_transforms = true
skip_rotate = true
skip_scale = true
use_point_constraint = true
base_parent = true
mirror_right = true

[[control]]
control = "ikAnkleLeg_left_ctrl"
parents = "cog_ctrl, root_ctrl, global_ctrl, world_ctrl, ikUpperLeg_left_ctrl, pelvis_ctrl"
mirror_right = true

# ---------- tail ----------
[[control]]
control = "fkTail_01_ctrl"
parents = "pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true
mirror_right = true

[[control]]
control = "fkTail_02_ctrl"
parents = "fkTail_01_ctrl, pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true
mirror_right = true

[[control]]
control = "flexiTail_01_ctrl"
parents = "pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_scale = true
base_parent = true
mirror_right = true

[[control]]
control = "flexiTail_02_ctrl"
parents = "pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl, flexiTail_01_ctrl"
mirror_right = true

[[control]]
control = "flexiTail_03_ctrl"
parents = "pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl, flexiTail_01_ctrl, flexiTail_02_ctrl"
mirror_right = true

# ---------- face ----------
# lower face
[[control]]
control = "lip_botLeft_01_ctrl, lip_botLeft_02_ctrl"
parents = "jaw_ctrl"
mirror_right = true

[[control]]
control = "lip_botCenter_ctrl, tongue_01_ctrl"
parents = "jaw_ctrl"

# upper face
[[control]]
control = """
lip_topLeft_01_ctrl, 
lip_topLeft_02_ctrl, 
eyeLid_topLeft_ctrl, 
eyeLid_botLeft_ctrl, 
horn_left_ctrl,
eye_left_ctrl
"""
parents = "head_jnt"
mirror_right = true

[[control]]
control = "lip_topCenter_ctrl, nose_ctrl, jaw_ctrl"
parents = "head_jnt"

# ---------- chin tentacles ----------
[[control]]
control = "fkChinTentacle_left_01_ctrl"
parents = "jaw_ctrl, head_jnt, spine_05_jnt, pelvis_ctrl, cog_ctrl, root_ctrl, global_ctrl, world_ctrl"
separate_transforms = true
skip_translate = true
skip_scale = true
base_parent = true
mirror_right = true

[[control]]
control = "flexiChinTentacle_left_01_ctrl"
parents = "jaw_ctrl"
mirror_right = true

[[control]]
control = "flexiChinTentacle_left_02_ctrl"
parents = "jaw_ctrl, flexiChinTentacle_left_01_ctrl"
mirror_right = true

[[control]]
control = "flexiChinTentacle_left_03_ctrl"
parents = "jaw_ctrl, flexiChinTentacle_left_01_ctrl, flexiChinTentacle_left_02_ctrl"
mirror_right = true

# ---------- switch/attr ctrls ----------
[[control]]
control = "legSwch_left_ctrl, shoulderSwch_left_ctrl, armSwch_left_ctrl, chinTentacleSwch_left_ctrl"
parents = "global_ctrl, root_ctrl, cog_ctrl, pelvis_ctrl, world_ctrl"
mirror_right = true

[[control]]
control = "nClothAux_ctrl, tailSwch_ctrl, spineSwch_ctrl, neckSwch_ctrl"
parents = "global_ctrl, root_ctrl, cog_ctrl, pelvis_ctrl, world_ctrl"

```
