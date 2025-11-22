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