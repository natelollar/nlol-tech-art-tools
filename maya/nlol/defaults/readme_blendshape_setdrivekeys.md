### Overview: `blendshape_setdrivekeys.toml`
```
Connect blendshapes or other object attributes to transform ctrls  
via set driven keys.
For a face ctrl setup, for example, include the ctrls in "rig_helpers.ma".
Include the blendshapes weighted to single meshes in "blendshapes.ma".
```
#### Root Level Parameters:
- `blendshape_objs` (str): Mesh objects containing the blendshape nodes to be iterated over,  
    for connecting set driven keys to ctrls. String name or string list.  Not required if already  
    importing blendshapes automatically. Remembers the imported scene blendshapes.
- `inTangentType, outTangentType` (str): Set driven key's "in/out tangent type"  
    for animation curve. Defaults to "linear".  
    Optional.

#### [[setdrivenkeys]] Parameters:
- `blendshape_attr` (str): The name of the blendshape attribute as in "noseSneerLeft".  
    Does not include the blendshape node name.
- `obj_attr` (str): Full object plus attribute name as in "my_ctrl.my_attribute".  
    Used instead of "blendshape_attr", but not both.  
    Useful for connecting eye roll joints instead of blendshape.
- `transform_crv` (str): The name of the curve to drive the set driven key.
- `crv_attr` (str): The name of the curve's attribute that drives the set driven key.  
    As in "translateX" or "rotateY".
- `blendshape_start, blendshape_end` (float): The start/end blendshape value to be keyed.  
    For the driven attribute; not necassarily a blendshape.  
    Optional.  Defaults to 0.0/1.0.
- `crv_start, crv_end` (float): The start/end transform curve value to be keyed. 
    The driver attribute values. 
    Optional.  Defaults to 0.0/1.0.
- `mirror_right` (str): Mirror the parameters to the other side as well.
- `mirror_right_invert` (str): Inverts just the "crv_end" parameter. As in, -1.0 to 1.0.
- `blendshape_fix_attrs` (str): A string or string list.  The name of the corrective blendshapes  
    that the "transform_crv" and "crv_attr" drive.  A corrective blendshape should be listed for  
    multiple "setdrivenkeys" values in the list.  So if "ctrl.ty" and "ctrl.tx" both drive the  
    corrective blendshape weight, it should be listed in both "blendshape_fix_attrs" keys.  
    Example: blendshape_fix_attrs = "mouthCornerUpOut_left_fixTarget, mouthCornerDownOut_left_fixTarget"  
---
*Lists written as "string lists".*
<br/> 
<br/> 

### *Example `blendshape_setdrivekeys.toml`*:
```
inTangentType="linear"
outTangentType="linear"

[[setdrivenkeys]]
blendshape_attr = "noseSneerLeft"
transform_crv = "noseSneerLeft_ctrl"
crv_attr = "translateY"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "noseSneerLeft"
transform_crv = "noseSneerLeft_ctrl"
crv_attr = "translateY"
blendshape_end = -1.0
crv_end = -1.0
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "eyeLookOutLeft"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateX"
mirror_right = true
mirror_right_invert = true  # inverts crv_end value

[[setdrivenkeys]]
blendshape_attr = "eyeLookInLeft"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateX"
crv_end = -1.0
mirror_right = true
mirror_right_invert = true

[[setdrivenkeys]]
blendshape_attr = "eyeLookUpLeft"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateY"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "eyeLookDownLeft"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateY"
crv_end = -1.0
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "jawOpen"
transform_crv = "jawOpen_ctrl"
crv_attr = "translateY"
crv_end = -1.0

[[setdrivenkeys]]
blendshape_attr = "jawLeft"
transform_crv = "jawOpen_ctrl"
crv_attr = "translateX"
blendshape_end = 1.0
crv_end = 1.0

[[setdrivenkeys]]
blendshape_attr = "jawRight"
transform_crv = "jawOpen_ctrl"
crv_attr = "translateX"
blendshape_end = 1.0
crv_end = -1.0

[[setdrivenkeys]]
blendshape_attr = "browInnerUp"
transform_crv = "browInnerUp_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "browInnerUp"
transform_crv = "browInnerUp_ctrl"
crv_attr = "translateY"
blendshape_end = -1.0
crv_end = -1.0

[[setdrivenkeys]]
blendshape_attr = "browOuterUpLeft"
transform_crv = "browUpDown_left_ctrl"
crv_attr = "translateY"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "browDownLeft"
transform_crv = "browUpDown_left_ctrl"
crv_attr = "translateY"
crv_end = -1.0
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "tongueOut"
transform_crv = "tongueOut_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "cheekSquintLeft"
transform_crv = "cheekSquintLeft_ctrl"
crv_attr = "translateY"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "cheekSquintLeft"
transform_crv = "cheekSquintLeft_ctrl"
crv_attr = "translateY"
blendshape_end = -1.0
crv_end = -1.0
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "cheekPuff"
transform_crv = "cheekPuff_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "cheekPuff"
transform_crv = "cheekPuff_ctrl"
crv_attr = "translateY"
blendshape_end = -1.0
crv_end = -1.0

[[setdrivenkeys]]
blendshape_attr = "eyeWideLeft"
transform_crv = "eyeWideBlink_left_ctrl"
crv_attr = "translateY"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "eyeBlinkLeft"
transform_crv = "eyeWideBlink_left_ctrl"
crv_attr = "translateY"
crv_end = -1.0
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "eyeSquintLeft"
transform_crv = "eyeSquintLeft_ctrl"
crv_attr = "translateY"
crv_end = -1.0
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "jawForward"
transform_crv = "jawForward_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "mouthClose"
transform_crv = "mouthClose_ctrl"
crv_attr = "translateY"
crv_end = -1.0

[[setdrivenkeys]]
blendshape_attr = "mouthFunnel"
transform_crv = "mouthFunnel_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "mouthPucker"
transform_crv = "mouthPucker_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "mouthLeft"
transform_crv = "mouthLeft_ctrl"
crv_attr = "translateX"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "mouthSmileLeft"
transform_crv = "mouthSmileLeft_ctrl"
crv_attr = "translateX"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "mouthFrownLeft"
transform_crv = "mouthFrownLeft_ctrl"
crv_attr = "translateX"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "mouthDimpleLeft"
transform_crv = "mouthDimpleLeft_ctrl"
crv_attr = "translateX"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "mouthStretchLeft"
transform_crv = "mouthStretchLeft_ctrl"
crv_attr = "translateX"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "mouthPressLeft"
transform_crv = "mouthPressLeft_ctrl"
crv_attr = "translateX"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "mouthRollLower"
transform_crv = "mouthRollLower_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "mouthRollUpper"
transform_crv = "mouthRollUpper_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "mouthShrugLower"
transform_crv = "mouthShrugLower_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "mouthShrugUpper"
transform_crv = "mouthShrugUpper_ctrl"
crv_attr = "translateY"

[[setdrivenkeys]]
blendshape_attr = "mouthLowerDownLeft"
transform_crv = "mouthLowerDownLeft_ctrl"
crv_attr = "translateY"
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "mouthUpperUpLeft"
transform_crv = "mouthUpperUpLeft_ctrl"
crv_attr = "translateY"
mirror_right = true


# --------------------------------------------------
# -------------------- squishy face --------------------
[[setdrivenkeys]]
blendshape_attr = "mouthCornerOut_left_target"
transform_crv = "mouthCorner_left_ctrl"
crv_attr = "translateX"
crv_end = 2.0
mirror_right = true
mirror_right_invert = true
blendshape_fix_attrs = "mouthCornerUpOut_left_fixTarget, mouthCornerDownOut_left_fixTarget"

[[setdrivenkeys]]
blendshape_attr = "mouthCornerIn_left_target"
transform_crv = "mouthCorner_left_ctrl"
crv_attr = "translateX"
crv_end = -1.15
mirror_right = true
mirror_right_invert = true
blendshape_fix_attrs = "mouthCornerDownIn_left_fixTarget, mouthCornerUpIn_left_fixTarget"

[[setdrivenkeys]]
blendshape_attr = "mouthCornerUp_left_target"
transform_crv = "mouthCorner_left_ctrl"
crv_attr = "translateY"
crv_end = 1.75
mirror_right = true
blendshape_fix_attrs = "mouthCornerUpOut_left_fixTarget, mouthCornerUpIn_left_fixTarget"

[[setdrivenkeys]]
blendshape_attr = "mouthCornerDown_left_target"
transform_crv = "mouthCorner_left_ctrl"
crv_attr = "translateY"
crv_end = -1.5
mirror_right = true
blendshape_fix_attrs = "mouthCornerDownOut_left_fixTarget, mouthCornerDownIn_left_fixTarget"

[[setdrivenkeys]]
blendshape_attr = "cheekPuff_left_target"
transform_crv = "cheekSquishy_left_ctrl"
crv_attr = "translateX"
crv_end = 1.5
mirror_right = true
mirror_right_invert = true

[[setdrivenkeys]]
blendshape_attr = "cheekSuckIn_left_target"
transform_crv = "cheekSquishy_left_ctrl"
crv_attr = "translateX"
crv_end = -1.5
mirror_right = true
mirror_right_invert = true

[[setdrivenkeys]]
blendshape_attr = "cheeksUp_left_target"
transform_crv = "cheekSquishy_left_ctrl"
crv_attr = "translateY"
crv_end = 1.5
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "cheeksDown_left_target"
transform_crv = "cheekSquishy_left_ctrl"
crv_attr = "translateY"
crv_end = -1.5
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "browInnerUp_left_target"
transform_crv = "browInner_left_ctrl"
crv_attr = "translateY"
crv_end = 1.5
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "browInnerDown_left_target"
transform_crv = "browInner_left_ctrl"
crv_attr = "translateY"
crv_end = -1.5
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "browOuterUp_left_target"
transform_crv = "browOuter_left_ctrl"
crv_attr = "translateY"
crv_end = 1.5
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "browOuterDown_left_target"
transform_crv = "browOuter_left_ctrl"
crv_attr = "translateY"
crv_end = -1.5
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "noseUp_target"
transform_crv = "noseSquishy_ctrl"
crv_attr = "translateY"
crv_end = 1.5
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "noseDown_target"
transform_crv = "noseSquishy_ctrl"
crv_attr = "translateY"
crv_end = -1.5
mirror_right = true

[[setdrivenkeys]]
blendshape_attr = "noseMove_left_target"
transform_crv = "noseSquishy_ctrl"
crv_attr = "translateX"
crv_end = 1.5

[[setdrivenkeys]]
blendshape_attr = "noseMove_right_target"
transform_crv = "noseSquishy_ctrl"
crv_attr = "translateX"
crv_end = -1.5

[[setdrivenkeys]]
blendshape_attr = "lipsPucker_target"
transform_crv = "lipsInOut_ctrl"
crv_attr = "translateZ"
crv_end = 1.0

[[setdrivenkeys]]
blendshape_attr = "lipsSuckIn_target"
transform_crv = "lipsInOut_ctrl"
crv_attr = "translateZ"
crv_end = -1.0

[[setdrivenkeys]]
blendshape_attr = "chinPuff_target"
transform_crv = "chinInOut_ctrl"
crv_attr = "translateZ"
crv_end = 1.0

[[setdrivenkeys]]
blendshape_attr = "chinIn_target"
transform_crv = "chinInOut_ctrl"
crv_attr = "translateZ"
crv_end = -1.0

# --------------------------------------------------
# --------------------------------------------------
# ----- eyes w/ blendshapes set driven keys -----
# right horizontal movement
[[setdrivenkeys]]
object_attr = "fkEyes_left_ctrlAux02OffsetGrp.rotateY"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateX"
blendshape_end = 38.511

[[setdrivenkeys]]
object_attr = "fkEyes_right_ctrlAux02OffsetGrp.rotateY"
transform_crv = "eyeLook_right_ctrl"
crv_attr = "translateX"
blendshape_end = 31.057

# left horizontal movement
[[setdrivenkeys]]
object_attr = "fkEyes_left_ctrlAux02OffsetGrp.rotateY"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateX"
blendshape_end = -31.057
crv_end = -1.0

[[setdrivenkeys]]
object_attr = "fkEyes_right_ctrlAux02OffsetGrp.rotateY"
transform_crv = "eyeLook_right_ctrl"
crv_attr = "translateX"
blendshape_end = -38.511
crv_end = -1.0

# up vertical movement
[[setdrivenkeys]]
object_attr = "fkEyes_left_ctrlAux02OffsetGrp.rotateX"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateY"
blendshape_end = -18.656
mirror_right = true

# down vertical movement
[[setdrivenkeys]]
object_attr = "fkEyes_left_ctrlAux02OffsetGrp.rotateX"
transform_crv = "eyeLook_left_ctrl"
crv_attr = "translateY"
blendshape_end = 14.927
crv_end = -1.0
mirror_right = true

```