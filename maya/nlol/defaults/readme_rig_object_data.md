### Overview: `rig_object_data.toml`
```
Rig object data for specified rig modules.  
```
#### Root Level Parameters:
- `rig_name` (str): Name string used for top rig and skeletal mesh groups.  
    Optional.
- `unreal_rig` (bool): Sets skeletal mesh group rotate "x" to -90.  
    Optional.

#### [[rig_module]] Parameters:
- `rig_module` (str): Existing rig module.
- `rig_module_name` (str): Custom rig module name. 
- `joints` (str): "String list" of joints. Main joints for the rig module.  
    "fk_control_mod" optional.
- `mirror_direction` (str): Mirror side of control. Currently, works best with "left".  
    Optional.
- `mirror_right` (bool): Use left rig module data for the right side. Currently works with mirror_direction "left"  
    and joints containing "left" or with suffix "_l".  See "swap_side_str()" function.  
    Optional.
- `get_joint_chain` (bool): Gets joint chain from listed joints.  Include either first joint, or first and last joint.  
    Can use instead of "joints".
- `display_layer` (bool): Whether to create a Maya display layer for the rig modules top group.
---
- `upper_twist_joints, lower_twist_joints` (str): List of joints in string format. Twist joints of the upper or lower limb segments.  
    "biped_leg_mod", "biped_limb_mod" only. 
- `main_object_names`: Main object names to be used instead of raw joint names. String name list matching number of "joints".
    "biped_leg_mod", "biped_limb_mod" only. 
- `upper_twist_name, lower_twist_name`: Main upper/lower twist object name instead of raw joint names. Single string name
    to be used as base name for all twist joints.
    "biped_leg_mod", "biped_limb_mod" only. 
- `joint_chains` : (list[str])  List of string lists containing either start or start and end joints for a chain. 
    "flexi_surface_ik_chain_mod" only. 
- `foot_locators` (str): Foot locators instead of using default names, for reverse foot ctrls.  
    Should be 4 listed in order; toe end, heel, lateral foot side and medial foot side.
    "biped_leg_mod" only. 
- `invert_toe_wiggle, invert_toe_spin, invert_foot_lean, invert_foot_tilt, invert_foot_roll` (bool): Invert rotation direction of 
    specified reverse foot attribute. Useful, for instance, if feet have same joint axis orientation, but are on different mirror sides,
    in this case "tilt" rotation would need to be inverted for one side.
    "biped_leg_mod" only. 
- `constraint` (bool): Whether to constrain the joint to the ctrl.  
    "fk_control_mod" only. 
- `use_joint_names` (bool): Use joint names for control names. Replaces the end type with "ctrl". Requires nLol naming convention.  
    "fk_control_mod" only. 
- `blend_joints` (str): Blend control between these two joints. Parent spacing not needed if used.  
    "fk_control_mod", "fk_control_blend_mod" only.
- `hide_translate, hide_rotate, hide scale` (bool): Lock and hide control attribute.  
    "fk_control_mod" only.
- `aim_vector, up_vector` (str): Eye axis aiming out to the aim ctrl and directly up.  
    Chosen based on world space if parameter not included.  
    "eye_aim_mod" only.
- `origin_joint, mid_joints, top_joints, bot_joints, flexi_joints_main, flexi_joints_offset` (str):  
    Custom joint lists for more complex rig modules.
    "piston_mod", "tentacle_mod".
- `flexi_surface`, `flexi_surface_main`, `flexi_surface_offset` (str): Name of flexi surface geo from "rig_helpers.ma" file.
    This geo is used for creating stretchy joint setups and for applying cloth simulation. Usually has skinning and joints kept in  "rig_helpers.ma".
    "flexi_surface_ik_chain_mod", "flexi_surface_fk_ctrl_mod", "tentacle_mod".

#### Parent Space Switching:
- Each built rig module will have objects to constrain for parent space switching and general parenting.  
    - Often the top or end ctrl can be used. 
- Parent space switching can be set up in "rig_parent_spaces.toml".
    - "parent_space_switching.py" will find the parent space switch group based on the input ctrl.
---
*Lists written as "string lists".*  
*nLol naming convention: `<name>_<direction>_<id>_<type>`*
<br/> 
<br/> 

### *Example `rig_object_data.toml`*:
```
[[rig_module]]
rig_module = "world_control_mod" 
rig_module_name = "world" 

[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "global" 
joints = "root_jnt"
constraint = false

[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "root" 
joints = "root_jnt"

[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "cog" 
joints = "cog_loc"
constraint = false
display_layer = true

[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "pelvis" 
joints = "pelvis_jnt"

# ---------- legs ----------
[[rig_module]]
rig_module = "digitigrade_leg_mod" 
rig_module_name = "leg"
mirror_direction = "left" 
joints = "hip_left_jnt, knee_left_jnt, ankle_left_jnt, foot_left_jnt, toeMain_left_jnt"
invert_foot_lean = true
invert_foot_tilt = true
mirror_right = true
# flip_spring_solver = true

# ---------- tail ----------
[[rig_module]]
rig_module = "tentacle_mod" 
rig_module_name = "tail"
joints = "tail_01_jnt, tail_09_jnt"
flexi_joints_main = "tailBase_01_jnt, tailBase_09_jnt"
flexi_joints_offset = "tailOffset_01_jnt, tailOffset_03_jnt"
get_joint_chain = true
flexi_surface_main = "flexiSurfaceTailBase_geo"
flexi_surface_offset = "flexiSurfaceTailOffset_geo"
use_flexi_ik_chain = true

# ---------- spine ----------
[[rig_module]]
rig_module = "fk_ik_spline_chain_mod" 
rig_module_name = "spine" 
joints = "spine_01_jnt, spine_04_jnt"
get_joint_chain = true

# ----- arms/wings -----
[[rig_module]]
rig_module = "biped_limb_mod" 
rig_module_name = "arm" 
mirror_direction = "left"
joints = "shoulder_left_jnt, elbow_left_jnt, wrist_left_jnt" 
polevector_ctrl_distance = 150
mirror_right = true

[[rig_module]]
rig_module = "fk_aim_mod" 
rig_module_name = "elbow" 
mirror_direction = "left"
joints = "wingElbow_01_left_jnt"
aim_object = "ikArmPoleVector_left_ctrl"
mirror_right = true

[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "wingFinger" 
mirror_direction = "left" 
joints = """
wingFinger_a01_left_jnt, 
wingFinger_b01_left_jnt,
wingFinger_c01_left_jnt,
wingFinger_c02_left_jnt,
wingFinger_d01_left_jnt,
wingFinger_e01_left_jnt
"""
use_joint_names = true
mirror_right = true

# ----- shoulder/clavicle -----
[[rig_module]]
rig_module = "fk_ik_single_chain_mod" 
rig_module_name = "shoulder" 
mirror_direction = "left"
joints = "clavicle_left_jnt, shoulder_left_jnt" 
mirror_right = true
enable_auto_clav = true
ik_wrist_ctrl = "ikEndArm_left_ctrl"

# ----- neck -----
[[rig_module]]
rig_module = "fk_ik_spline_chain_mod" 
rig_module_name = "neck" 
joints = "neck_01_jnt, head_jnt"
get_joint_chain = true

# ----- face -----
# lower face
[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "lowerFace" 
joints = "lip_botCenter_jnt"
use_joint_names = true

[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "lowerFace" 
mirror_direction = "left" 
joints = "lip_botLeft_01_jnt, lip_botLeft_02_jnt"
use_joint_names = true
mirror_right = true

# upper face
[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "upperFace" 
joints = "lip_topCenter_jnt, nose_jnt, jaw_jnt"
use_joint_names = true

[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "upperFace" 
mirror_direction = "left" 
joints = "lip_topLeft_01_jnt, lip_topLeft_02_jnt, eyeLid_topLeft_jnt, eyeLid_botLeft_jnt, horn_left_jnt"
use_joint_names = true
mirror_right = true

[[rig_module]]
rig_module = "fk_control_mod" 
rig_module_name = "upperFace" 
mirror_direction = "left" 
joints = "eye_left_jnt"
use_joint_names = true
mirror_right = true
add_aux_grp = true

# tongue
[[rig_module]]
rig_module = "fk_chain_mod" 
rig_module_name = "tongue" 
joints = "tongue_01_jnt, tongue_03_jnt"
get_joint_chain = true

# ---------- chin ----------
[[rig_module]]
rig_module = "tentacle_mod" 
rig_module_name = "chinTentacle"
mirror_direction = "left"
joints = "chinTentacle_01_left_jnt"
flexi_joints_main = "chinTentacleBase_01_left_jnt"
flexi_joints_offset = "chinTentacleOffset_01_left_jnt"
get_joint_chain = true
flexi_surface_main = "flexiSurfaceChinBase_left_geo"
flexi_surface_offset = "flexiSurfaceChinOffset_left_geo"
mirror_right = true

```