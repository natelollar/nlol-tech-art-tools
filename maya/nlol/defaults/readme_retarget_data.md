### Overview: `retarget_data.toml`
```
Retarget keyframe animation data from source ctrl to target ctrls.
Sets keys only on frames and attributes with source ctrl keys. 
Copies in/out tangent types. Optionally, copy tangent weights/angles.

Initially, setup constraints between source and target ctrls.
```
#### Root Level Parameters:
- `source_namespace, target_namespace` (str): Add parent space names if referencing in rigs.  
    Leave parent space names out of "source_ctrls" and "target_ctrls" params. Add here instead.
- `tangent_weights_angles` (bool): Whether to copy keyframe tangent weights/angles from source ctrl
    to target ctrls.  Probably won't be useful unless source and target ctrls position and
    rotation axis are closely aligned at default pose.
    Optional.  Defaults to False.
- `key_translate_rotate_all` (bool): Option to key translate and rotate for all frames  
    with source control keys.  A happy balance between baking keys on all frames and only keying keyed   
    attributes. Helps avoid interpolation issues.  
    Optional.  Defaults to False.

#### [[source_target_data]] Parameters:
- `source_ctrls` (str): Name of source ctrl. The ctrl with keyframe animation data  
    driving the target ctrl.
    Usually just a single ctrl. Multiple for constraint blending.
    First ctrl is primary ctrl for keyframe/tangent data.  
- `target_ctrls` (str): The target ctrls to be driven by source ctrl.  
    Usually just a single ctrl.  Keyframe animation data will be baked onto these ctrls.
- `connection_type` (str): Constraint type to be used for connecting  
    source ctrl to target ctrls.  
    Values: "parent", "point", "orient", "pointOrient"  
    Optional. Defaults to "parent".  
    "parent": changes to "point" if rotate locked. changes to "orient" if translate locked.
- `offset` (bool): Wether to use maintainOffset for constraints  
    connecting source and target ctrls.  
    Optional. Defaults to True. 
- `scale_constraint` (bool): Whether to apply a scale constraint for retargeting.  
    Optional. Defaults to True.  
    Skips if scale locked.
- `scale_source_ctrl` (str): If needing to use a different source ctrl for scaling retarget  
    add the name here.  
    Optional.  Defaults to "" (No).
- `tangent_weights_angles` (bool): Whether to copy keyframe tangent weights/angles from source ctrl
    to target ctrls.  Probably won't be useful unless source and target ctrls position and
    rotation axis are closely aligned at default pose.
    Optional.  Defaults to False.
- `target_translate, target_rotate` (str): Initial target ctrl transform offsets.  
    Written as XYZ string list.  
    Example: "0, 0, 0"
- `mirror` (bool): Add another input mirrored to the other side.  
    Left/Right substrings will be mirrored in "source_ctrl" and "target_ctrls".  
    So "l_" becomes "r_", etc.  
---
*Lists written as "string lists".*

#### Example:
```
source_namespace = "wyvern_rig"
target_namespace = "dragon_rig"
tangent_weights_angles = false  # useful if controls have very similar transforms
key_translate_rotate_all = true  # keyframe translate rotate on all keyed frames

[[source_target_data]]
source_ctrls = "character_global_ctrl"  # blend with multiple ctrls. first is primary
target_ctrls = "global_ctrl"  # source may drive more than one
# connection_type = "parent"  # default.  "parent", "point", "orient", "pointOrient"
# offset = true # default
# scale_constraint = true  # default
# scale_source_ctrl = ""  # default
# tangent_weights_angles = false  # default
# target_translate = [0, 0, 0]  # target ctrl starting transform offsets
# target_rotate =  [0, 0, 0]

[[source_target_data]]
source_ctrls = "spine1_Root_ctrl" 
target_ctrls = "pelvis_ctrl"

[[source_target_data]]
source_ctrls = "spine2_ctrl" 
target_ctrls = "fkSpine_02_ctrl"
```
