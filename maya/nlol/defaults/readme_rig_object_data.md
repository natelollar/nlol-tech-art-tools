### Overview: `rig_object_data.toml`
```
Rig object data for specified rig modules.  
```
---
#### [[rig_module]] Parameters:
- `rig_module` (str): Existing rig module.
- `rig_module_name` (str): Custom rig module name. 
- `joints` (str): "String list" of joints. Main joints for the rig module.  
    "fk_control_mod" optional.
- `mirror_direction` (str): Mirror side of control. Currently, works best with "left".  
    Optional.
- `mirror_right` (bool): Use left rig module data for the right side. Currently works with mirror_direction "left"  
    and joints containing "left" or with suffix "_l".  See "left_to_right_str()" function.  
    Optional.
- `get_joint_chain` (bool): Gets joint chain from listed joints.  Include either first joint, or first and last joint.  
    Can use instead of "joints".
- `display_layer` (bool): Whether to create a Maya display layer for the rig modules top group.
---
- `upper_twist_joints, lower_twist_joints` (str): List of joints in string format. Twist joints of the upper or lower limb segments.  
    "biped_leg_mod", "biped_limb_mod" only. 
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
---
*Lists written as "string lists".*  
*nLol naming convention: `<name>_<direction>_<id>_<type>`*

#### Root Level Parameters:
- `rig_name` (str): Name string used for top rig and skeletal mesh groups.
- `unreal_rig` (bool): Sets skeletal mesh group rotate "x" to -90.

#### Parent Space Switching:
- Each built rig module will have objects to constrain for parent space switching and general parenting.  
    - Often the top or end ctrl can be used. 
- Parent space switching can be set up in "rig_parent_spaces.toml".
    - "parent_space_switching.py" will find the parent space switch group based on the input ctrl.