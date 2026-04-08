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
<br/> 
<br/> 

### *Example `retarget_data.toml`*:
```
# ----------------------------------------
source_namespace = "wyvern_rig"
target_namespace = ""
# tangent_weights_angles = false  # default
key_translate_rotate_all = true  # keyframe translate rotate on all keyed frames

# ----------------------------------------
# global
[[source_target_data]]
source_ctrls = "character_global_ctrl"  # blend with multiple ctrls. first is primary
target_ctrls = "global_ctrl"  # source may drive more than one
# connection_type = "parent"  # default.  "parent", "point", "orient", "pointOrient"
# offset = true # default
# scale_constraint = true  # default
# scale_source_ctrl = ""  # default
# target_translate = [0, 0, 0]  # target ctrl starting transform offsets
# target_rotate =  [0, 0, 0]

# ----------------------------------------
# pelvis
[[source_target_data]]
source_ctrls = "spine1_Root_ctrl" 
target_ctrls = "pelvis_ctrl"

# ----------------------------------------
# spine
[[source_target_data]]
source_ctrls = "spine2_ctrl" 
target_ctrls = "fkSpine_02_ctrl"

[[source_target_data]]
source_ctrls = "spine3_ctrl" 
target_ctrls = "fkSpine_03_ctrl"

[[source_target_data]]
source_ctrls = "spine4_ctrl" 
target_ctrls = "fkSpine_04_ctrl"

# ----------------------------------------
# neck
[[source_target_data]]
source_ctrls = "neck1_ctrl" 
target_ctrls = "fkNeck_01_ctrl"

[[source_target_data]]
source_ctrls = "neck2_ctrl" 
target_ctrls = "fkNeck_02_ctrl"

[[source_target_data]]
source_ctrls = "neck3_ctrl" 
target_ctrls = "fkNeck_03_ctrl"

# ----------------------------------------
# ik leg
[[source_target_data]]
source_ctrls = "l_ikHip_ctrl" 
target_ctrls = "ikUpperLeg_left_ctrl"
connection_type = "point"
mirror = true

[[source_target_data]]
source_ctrls = "l_ankle_poleVector_ctrl" 
target_ctrls = "ikLegLowerPoleVector_left_ctrl"
target_translate = "0, 0, -32"
mirror = true

[[source_target_data]]
source_ctrls = "l_knee_poleVector_ctrl" 
target_ctrls = "ikLegUpperPoleVector_left_ctrl"
target_translate = "0, 0, -45"
mirror = true

[[source_target_data]]
source_ctrls = "l_ikFoot_ctrl" 
target_ctrls = "ikAnkleLeg_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_ftCtrl_toe_wiggle" 
target_ctrls = "legFootToeWiggle_left_ctrl"
mirror = true

# ----------------------------------------
# fk leg
[[source_target_data]]
source_ctrls = "fkJnt_l_hip_ctrl" 
target_ctrls = "fkUpperLeg_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "fkJnt_l_knee_ctrl" 
target_ctrls = "fkMiddleLeg_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "fkJnt_l_ankle_ctrl" 
target_ctrls = "fkLowerLeg_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "fkJnt_l_foot1_ctrl" 
target_ctrls = "fkAnkleLeg_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "fkJnt_l_foot2_ctrl" 
target_ctrls = "fkToeLeg_left_ctrl"
mirror = true

# ----------------------------------------
# ik arm
[[source_target_data]]
source_ctrls = "l_ikClav_ctrl" 
target_ctrls = "ikShoulderStart_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_ikShldr_ctrl" 
target_ctrls = "ikShoulder_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_ikWrist_ctrl" 
target_ctrls = "ikEndArm_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_elbow_PV_ctrl" 
target_ctrls = "ikArmPoleVector_left_ctrl"
target_translate = "0, 0, -47"
mirror = true


# ----------------------------------------
# fk arm
[[source_target_data]]
source_ctrls = "fkJnt_l_clavicle_ctrl" 
target_ctrls = "fkShoulder_left_01_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "fkJnt_l_shoulder_ctrl" 
target_ctrls = "fkUpperArm_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "fkJnt_l_elbow_ctrl" 
target_ctrls = "fkLowerArm_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "fkJnt_l_wrist_ctrl" 
target_ctrls = "fkEndArm_left_ctrl"
mirror = true

# ----------------------------------------
# fk wing
[[source_target_data]]
source_ctrls = "l_fingerA1_ctrl" 
target_ctrls = "wingFinger_a01_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_fingerB1_ctrl" 
target_ctrls = "wingFinger_b01_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_wingA1_ctrl" 
target_ctrls = "fkElbow_left_ctrl"
connection_type = "orient"
mirror = true

[[source_target_data]]
source_ctrls = "l_wingB1_ctrl" 
target_ctrls = "wingFinger_e01_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_wingC1_ctrl" 
target_ctrls = "wingFinger_d01_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_wingD1_ctrl" 
target_ctrls = "wingFinger_c01_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_wingD2_ctrl" 
target_ctrls = "wingFinger_c02_left_ctrl"
mirror = true

# ----------------------------------------
# ik tail
[[source_target_data]]
source_ctrls = "tail_ik_ctrlA" 
target_ctrls = "flexiTail_01_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail_ik_ctrlB, tail_ik_ctrlA" 
target_ctrls = "flexiTail_02_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail_ik_ctrlB" 
target_ctrls = "flexiTail_03_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail_offset_ctrl" 
target_ctrls = "fkTailOffset_08_ctrl"
mirror = true

# ----------------------------------------
# fk tail
[[source_target_data]]
source_ctrls = "tail7_fkCtrl" 
target_ctrls = "fkTail_08_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail6_fkCtrl" 
target_ctrls = "fkTail_07_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail5_fkCtrl" 
target_ctrls = "fkTail_06_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail4_fkCtrl" 
target_ctrls = "fkTail_05_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail3_fkCtrl" 
target_ctrls = "fkTail_04_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail2_fkCtrl" 
target_ctrls = "fkTail_03_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tail1_fkCtrl" 
target_ctrls = "fkTail_02_ctrl"
mirror = true

# ----------------------------------------
# head/face
[[source_target_data]]
source_ctrls = "jaw_ctrlB" 
target_ctrls = "jaw_ctrl"

[[source_target_data]]
source_ctrls = "l_horn_ctrl" 
target_ctrls = "horn_left_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_top_lid_ctrl" 
target_ctrls = "eyeLid_topLeft_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_bot_lid_ctrl" 
target_ctrls = "eyeLid_botLeft_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "tongue1_ctrl" 
target_ctrls = "tongue_01_ctrl"

[[source_target_data]]
source_ctrls = "tongue2_ctrl" 
target_ctrls = "tongue_02_ctrl"

[[source_target_data]]
source_ctrls = "tongue4_ctrl" 
target_ctrls = "tongue_03_ctrl"

[[source_target_data]]
source_ctrls = "nose_ctrl" 
target_ctrls = "nose_ctrl"

[[source_target_data]]
source_ctrls = "l_top_lipB_ctrl" 
target_ctrls = "lip_topLeft_02_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_top_lipA_ctrl" 
target_ctrls = "lip_topLeft_01_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "top_lip_ctrl" 
target_ctrls = "lip_topCenter_ctrl"

[[source_target_data]]
source_ctrls = "l_bot_lipB_ctrl" 
target_ctrls = "lip_botLeft_02_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_bot_lipA_ctrl" 
target_ctrls = "lip_botLeft_01_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "bot_lip_ctrl" 
target_ctrls = "lip_botCenter_ctrl"

[[source_target_data]]
source_ctrls = "l_chin_tentacle_ik_ctrlA" 
target_ctrls = "flexiChinTentacle_left_01_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_chin_tentacle_ik_ctrlB, l_chin_tentacle_ik_ctrlA" 
target_ctrls = "flexiChinTentacle_left_02_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_chin_tentacle_ik_ctrlB" 
target_ctrls = "flexiChinTentacle_left_03_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_chin_tentacle1_fkCtrl" 
target_ctrls = "fkChinTentacle_left_01_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_chin_tentacle2_fkCtrl" 
target_ctrls = "fkChinTentacle_left_02_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_chin_tentacle3_fkCtrl" 
target_ctrls = "fkChinTentacle_left_03_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_chin_tentacle4_fkCtrl" 
target_ctrls = "fkChinTentacle_left_04_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_chin_tentacle5_fkCtrl" 
target_ctrls = "fkChinTentacle_left_05_ctrl"
mirror = true

[[source_target_data]]
source_ctrls = "l_chin_tentacle6_fkCtrl" 
target_ctrls = "fkChinTentacle_left_06_ctrl"
mirror = true

```
