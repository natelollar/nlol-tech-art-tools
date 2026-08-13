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
##### Shared:
- `rig_module` (str): Existing rig module.
- `rig_module_name` (str): Custom rig module name. 
- `joints` (str): "String list" of joints. Main joints for the rig module.  
    Optional on "fk_control_mod", "fk_control_blend_mod".
- `mirror_direction` (str): Mirror side of control. Currently, works best with "left".  
    Optional.
- `mirror_right` (bool): Use left rig module data for the right side. Currently works with mirror_direction "left"  
    and joints containing "left" or with suffix "_l".  See "swap_side_str()" function.  
    Optional.
- `get_joint_chain` (bool): Expand listed joints into the full chain. Include either first joint, or first and last joint.
- `display_layer` (bool): Whether to create a Maya display layer for the rig modules top group.
##### Limb / Leg:
- `upper_twist_joints, lower_twist_joints` (str): List of joints in string format. Twist joints of the upper or lower limb segments.  
    "biped_leg_mod", "biped_limb_mod". 
- `main_object_names` (str): Main object names to be used instead of raw joint names. String name list matching number of "joints".
    "biped_leg_mod", "biped_limb_mod", "digitigrade_leg_mod". 
- `upper_twist_name, lower_twist_name` (str): Main upper/lower twist object name instead of raw joint names. Single string name
    to be used as base name for all twist joints.
    "biped_leg_mod", "biped_limb_mod". 
- `polevector_ctrl_distance` (float): Distance the pole vector ctrl is placed from the hinge joint.  
    "biped_limb_mod".
- `foot_locators` (str): Foot locators instead of using default names, for reverse foot ctrls.  
    Should be 4 listed in order; toe end, heel, lateral foot side and medial foot side.
    "biped_leg_mod", "digitigrade_leg_mod".
- `invert_toe_wiggle, invert_toe_spin, invert_foot_lean, invert_foot_tilt, invert_foot_roll` (bool): Invert rotation direction of  
    specified reverse foot attribute. Useful, for instance, if feet have same joint axis orientation, but are on different mirror sides,  
    in this case "tilt" rotation would need to be inverted for one side.  
    "biped_leg_mod", "digitigrade_leg_mod".  
- `ankle_x_forward` (bool): Ankle X is world flat (forward or back) instead of world up/down.  
    Swaps spin/lean/tilt rotate axes on the reverse foot aux ctrls.  
    "biped_leg_mod", "digitigrade_leg_mod".
- `flip_spring_solver` (bool): Flip the ikHandle twist 180 for the digitigrade driver-joint spring solver.  
    "digitigrade_leg_mod".
##### FK:
- `constraint` (bool): Whether to constrain the joint to the ctrl.  
    "fk_control_mod", "fk_control_blend_mod". 
- `use_joint_names` (bool): Use joint names for control names. Replaces the end type with "ctrl". Requires nLol naming convention.  
    "fk_control_mod", "fk_control_blend_mod". 
- `blend_joints` (str): Blend control between these two joints. Parent spacing not needed if used.  
    "fk_control_mod", "fk_control_blend_mod".
- `hide_translate, hide_rotate, hide_scale` (bool): Lock and hide control attribute.  
    "fk_control_mod", "fk_control_blend_mod".
- `add_aux_grp` (bool): Add an extra aux offset group on the ctrl.  
    "fk_control_mod", "fk_control_blend_mod".
- `iteration_id` (str): Optional id if multiple fk chains are created. Goes before the number id. Example: "a".  
    "fk_chain_mod".
- `aux_offset_grp` (bool): Extra offset group on each fk chain ctrl, for additional connections.  
    "fk_chain_mod".
##### Single / Spline:
- `enable_auto_clav` (bool): Drive ik clavicle/shoulder rotation from wrist/hand ctrl translation.  
    "fk_ik_single_chain_mod".
- `ik_wrist_ctrl` (str): Wrist/hand ctrl name used as the auto-clav endpoint. Required with "enable_auto_clav".  
    "fk_ik_single_chain_mod".
- `hide_fk_end_ctrl` (bool): Hide the last fk ctrl in the spline chain (unskinned end joint).  
    "fk_ik_spline_chain_mod".
- `add_ik_end_ctrl` (bool): Add an ik spline end ctrl so the second-to-last joint can still fk-offset.  
    "fk_ik_spline_chain_mod".
- `curve_dynamics` (bool): Apply nHair dynamics to the ik spline curve.  
    "fk_ik_spline_chain_mod".
- `use_existing_hairsystem` (bool): Reuse an existing hair system for curve dynamics. Creates one if needed.  
    "fk_ik_spline_chain_mod".
- `hairsystem_name` (str): Hair system transform name for curve dynamics. Optional.  
    "fk_ik_spline_chain_mod".
- `curve_easing_style` (str): Spline curve skin-weight easing.  
    Options: smoothstep, smootherstep, smooth_sine, smooth_cubic, or linear.  
    "fk_ik_spline_chain_mod".
##### Flexi / Tentacle:
- `joint_chains` (array of str): List of chains. Each item is a start joint, or "start, end".  
    "flexi_surface_ik_chain_mod". 
- `flexi_surface` (str): Name of flexi surface geo from "rig_helpers.ma" file.  This geo is used for creating stretchy joint setups  
    and for applying cloth simulation. Usually has skinning and joints kept in "rig_helpers.ma".  
    "flexi_surface_ik_chain_mod", "flexi_surface_ik_chain_simple_mod", "flexi_surface_fk_ctrl_mod".  
- `hide_end_ctrl` (bool): Hide the last created fk ctrl.  
    "flexi_surface_ik_chain_mod", "flexi_surface_ik_chain_simple_mod", "flexi_surface_fk_ctrl_mod".
- `flexi_joints_main, flexi_joints_offset` (str): Custom joint lists for more complex rig modules.  
    "tentacle_mod".
- `flexi_surface_main`, `flexi_surface_offset` (str): Same as "flexi_surface".  
    "tentacle_mod".
- `separate_flexi_ctrls` (bool): Leave flexi ctrls as separate ctrls instead of a hierarchy. Useful for complex parent spaces.  
    "tentacle_mod".
- `use_flexi_ik_chain` (bool): Use single-chain ikHandles on flexi ctrls instead of fk, with a stretch toggle.  
    "tentacle_mod".
##### Aim:
- `aim_object` (str): Object/ctrl the fk ctrl aims at.  
    "fk_aim_mod".
- `aim_vector, up_vector` (str): Axis aiming out to the aim ctrl and directly up.  
    Chosen based on world space if parameter not included.  
    "eye_aim_mod", "fk_aim_mod".
- `reverse_right_vectors` (bool): Reverse aim/up vectors on the right side (e.g. "-x" to "x").  
    "eye_aim_mod", "fk_aim_mod".
##### Piston:
- `origin_joint, mid_joints, top_joints, bot_joints` (str): Custom joint lists for more complex rig modules.  
    "piston_mod".
##### Import:
- `locators` (str): Locators in "rig_helpers.ma" used to place imported ctrls. Index-matched to "controls".  
    "import_rig_mod".
- `controls` (str): Ctrls in the imported rig to snap to "locators".  
    "import_rig_mod".
- `remove_namespace` (bool): Remove the import namespace after bringing the file in.  
    "import_rig_mod".
- `reference` (bool): Reference the custom rig file instead of importing.  
    "import_rig_mod".
- `custom_rig_filepath` (str): Full path to the custom rig file, including filename and extension.  
    "import_rig_mod".
- `custom_rig_folderpath` (str): Folder for the custom rig file (no filename). Defaults to parent of the auto-rig folder.  
    "import_rig_mod".
- `custom_rig_filename` (str): Maya filename only, including extension. Defaults to "custom_rig.ma".  
    "import_rig_mod".


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

### *Examples `rig_object_data.toml`*:

#### `biped_limb_mod`  
Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `upper_twist_joints`, `lower_twist_joints`, `main_object_names`, `upper_twist_name`, `lower_twist_name`, `polevector_ctrl_distance`.  
Notes:  
`joints` — usually 3 (shoulder/elbow/wrist or hip/knee/ankle). A 4th joint is an extra end; legs use that via `biped_leg_mod`.  
`get_joint_chain` — expand first/last listed joints into the full chain.  
`main_object_names` — ctrl names instead of joint names.  
`upper_twist_name` / `lower_twist_name` — base names for twist objects.  
`polevector_ctrl_distance` — pole vector distance from elbow/knee.  
`mirror_right` — build the right side from this left entry.  

```toml
[[rig_module]]
rig_module = "biped_limb_mod"
rig_module_name = "arm"
mirror_direction = "left"
joints = "shoulder_left_jnt, elbow_left_jnt, wrist_left_jnt"
mirror_right = true
#get_joint_chain = true
#upper_twist_joints = "upperArmTwist_01_left_jnt, upperArmTwist_02_left_jnt"
#lower_twist_joints = "lowerArmTwist_02_left_jnt, lowerArmTwist_01_left_jnt"
#main_object_names = "upperArm, lowerArm, hand"
#upper_twist_name = "upperArmTwist"
#lower_twist_name = "lowerArmTwist"
#polevector_ctrl_distance = 150
#display_layer = true
```

#### `biped_leg_mod`
Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `upper_twist_joints`, `lower_twist_joints`, `main_object_names`, `upper_twist_name`, `lower_twist_name`, `foot_locators`, `invert_toe_wiggle`, `invert_toe_spin`, `invert_foot_lean`, `invert_foot_tilt`, `invert_foot_roll`, `ankle_x_forward`.  
Notes:  
`joints` — 4 joints: hip/knee/ankle/toe (or thigh/calf/foot/ball).  
`foot_locators` — 4 locators in order: toe end, heel, lateral, medial. 
    Skip to use default names (toeEnd_left_loc, heel_left_loc, lateral_left_loc, medial_left_loc).  
`invert_toe_wiggle` / `invert_toe_spin` / `invert_foot_lean` / `invert_foot_tilt` / `invert_foot_roll` — invert that reverse-foot attr. Useful when both feet share the same axis but are opposite sides.  
`ankle_x_forward` — ankle X is horizontal (forward or back) instead of world up/down. Swaps spin/lean/tilt axes; roll and toe wiggle stay on rotateZ.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "biped_leg_mod"
rig_module_name = "leg"
mirror_direction = "left"
joints = "thigh_l, calf_l, foot_l, ball_l"
mirror_right = true
#get_joint_chain = true
#upper_twist_joints = "thigh_twist_01_l, thigh_twist_02_l"
#lower_twist_joints = "calf_twist_02_l, calf_twist_01_l"
#main_object_names = "upperLeg, lowerLeg, ankle, toe"
#upper_twist_name = "upperLegTwist"
#lower_twist_name = "lowerLegTwist"
#foot_locators = "toeEnd_left_loc, heel_left_loc, lateral_left_loc, medial_left_loc"
#invert_toe_wiggle = true
#invert_toe_spin = true
#invert_foot_lean = true
#invert_foot_tilt = true
#invert_foot_roll = true
#ankle_x_forward = true
#display_layer = true
```

#### `fk_control_mod` / `fk_control_blend_mod`
Required: `rig_module`, `rig_module_name`.  
Optional: `joints`, `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `constraint`, `use_joint_names`, `blend_joints`, `hide_translate`, `hide_rotate`, `hide_scale`, `add_aux_grp`.  
Notes:  
`fk_control_blend_mod` — same module as `fk_control_mod`. Use `blend_joints` to blend the ctrl between two objects.  
`joints` — snap/constrain targets. Can be joints or locators. Multiple names make multiple standalone fk ctrls.  
`constraint` — parent/scale constrain each joint to its ctrl. Default true. Set false to place a ctrl with no joint constraint (e.g. global, cog).  
`use_joint_names` — name ctrls from the joint (`<name>_<direction>_<id>_ctrl`). Requires nLol naming.  
`blend_joints` — two objects to blend the ctrl between (e.g. head and jaw for a mouth corner).  
`hide_translate` / `hide_rotate` / `hide_scale` — lock and hide that channel.  
`add_aux_grp` — extra aux offset group on the ctrl.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "fk_control_mod"
rig_module_name = "pelvis"
joints = "pelvis_jnt"
#mirror_direction = "left"
#mirror_right = true
#get_joint_chain = true
#constraint = false
#use_joint_names = true
#blend_joints = "head_jnt, jaw_jnt"
#hide_translate = true
#hide_rotate = true
#hide_scale = true
#add_aux_grp = true
#display_layer = true
```

#### `world_control_mod`
Required: `rig_module`, `rig_module_name`.  
Optional: `display_layer`.  
Notes:  
Ctrl is created at world origin, world-aligned, hidden, with transforms and visibility locked.  
No `joints`, `mirror_direction`, or `mirror_right`.

```toml
[[rig_module]]
rig_module = "world_control_mod"
rig_module_name = "world"
#display_layer = true
```

#### `fk_chain_mod`
Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `iteration_id`, `aux_offset_grp`.  
Notes:  
Builds a parented fk ctrl chain along the listed joints.  
`get_joint_chain` — usual pattern: list first and last joint, then expand the chain.  
`iteration_id` — extra id if several chains share the same module name. Goes before the number id. Example: `a`.  
`aux_offset_grp` — extra offset group on each ctrl, for additional connections.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "fk_chain_mod"
rig_module_name = "indexFinger"
mirror_direction = "left"
joints = "indexFinger_left_01_jnt, indexFinger_left_03_jnt"
get_joint_chain = true
mirror_right = true
#iteration_id = "a"
#aux_offset_grp = true
#display_layer = true
```

#### `fk_ik_single_chain_mod`
Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `enable_auto_clav`, `ik_wrist_ctrl`.  
Notes:  
Usually 2 joints (clavicle to shoulder/upper arm). FK/IK blend on a single-chain ikHandle.  
`enable_auto_clav` — drive ik clavicle/shoulder rotation from wrist/hand ctrl translation.  
`ik_wrist_ctrl` — wrist/hand ctrl name used as the auto-clav endpoint. Required with `enable_auto_clav`.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "fk_ik_single_chain_mod"
rig_module_name = "shoulder"
mirror_direction = "left"
joints = "clavicle_left_jnt, shoulder_left_jnt"
mirror_right = true
#get_joint_chain = true
#enable_auto_clav = true
#ik_wrist_ctrl = "ikEndArm_left_ctrl"
#display_layer = true
```

#### `fk_ik_spline_chain_mod`
Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `hide_fk_end_ctrl`, `add_ik_end_ctrl`, `curve_dynamics`, `use_existing_hairsystem`, `hairsystem_name`, `curve_easing_style`.  
Notes:  
FK/IK blend along an ikSplineHandle. Typical for spine, neck, or tail.  
`get_joint_chain` — usual pattern: list first and last joint, then expand the chain.  
`hide_fk_end_ctrl` — hide the last fk ctrl (unskinned end joint, e.g. tail tip).  
`add_ik_end_ctrl` — extra ik spline end ctrl so the second-to-last joint can still fk-offset.  
`curve_dynamics` — apply nHair to the spline curve.  
`use_existing_hairsystem` — reuse a hair system already in the scene. Creates one if needed.  
`hairsystem_name` — hair system transform name. Optional; used with `curve_dynamics`.  
`curve_easing_style` — spline curve skin-weight easing: `smoothstep`, `smootherstep`, `smooth_sine`, `smooth_cubic`, or `linear`.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "fk_ik_spline_chain_mod"
rig_module_name = "spine"
joints = "spine_01_jnt, spine_04_jnt"
get_joint_chain = true
#mirror_direction = "left"
#mirror_right = true
#hide_fk_end_ctrl = true
#add_ik_end_ctrl = true
#curve_dynamics = true
#use_existing_hairsystem = true
#hairsystem_name = "main_hairSystem"
#curve_easing_style = "smoothstep"
#display_layer = true
```

#### `flexi_surface_ik_chain_mod`
Required: `rig_module`, `rig_module_name`, `joint_chains`.  
Optional: `mirror_direction`, `mirror_right`, `display_layer`, `flexi_surface`, `hide_end_ctrl`.  
Notes:  
Attaches follicles on a flexi surface, then an fk/ik chain per follicle with optional stretch.  
`joint_chains` — list of chains. Each item is a start joint, or "start, end". The rest of that chain is found automatically.  
`flexi_surface` — geo from `rig_helpers.ma` (poly or nurbs). Name should contain `flexiSurface`. Defaults to `flexiSurface_geo`.  
`hide_end_ctrl` — hide the last fk ctrl on each chain.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "flexi_surface_ik_chain_mod"
rig_module_name = "leatherStrip"
mirror_direction = "left"
joint_chains = [
    "leatherStrip_left_a01_jnt",
    "leatherStrip_left_b01_jnt, leatherStrip_left_b04_jnt",
]
flexi_surface = "flexiSurface_geo"
mirror_right = true
#hide_end_ctrl = true
#display_layer = true
```

#### `flexi_surface_ik_chain_simple_mod`
Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `flexi_surface`, `hide_end_ctrl`.  
Notes:  
One joint chain attached to a flexi surface via follicles and ik single-chain solvers, with stretch and UV slide (slide works when stretch is on). Chain aim should be `x` or `-x`.  
`get_joint_chain` — usual pattern: list first and last joint, then expand the chain.  
`flexi_surface` — geo from `rig_helpers.ma`. Name should contain `flexiSurface`. Defaults to `flexiSurface_geo`.  
`hide_end_ctrl` — hide the last fk ctrl.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "flexi_surface_ik_chain_simple_mod"
rig_module_name = "tail"
joints = "tail_01_jnt, tail_09_jnt"
flexi_surface = "flexiSurfaceTailMain_geo"
get_joint_chain = true
#mirror_direction = "left"
#mirror_right = true
#hide_end_ctrl = true
#display_layer = true
```

#### `flexi_surface_fk_ctrl_mod`
Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `flexi_surface`, `hide_end_ctrl`.  
Notes:  
Standalone fk ctrl per joint, attached to a flexi surface via follicles. Ctrls follow the surface; they are not a parented fk chain.  
`get_joint_chain` — usual pattern: list first and last joint, then expand the chain.  
`flexi_surface` — geo from `rig_helpers.ma`. Name should contain `flexiSurface`. Defaults to `flexiSurface_geo`.  
`hide_end_ctrl` — hide the last fk ctrl.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "flexi_surface_fk_ctrl_mod"
rig_module_name = "sling"
joints = "slingMain_01_jnt, slingMain_05_jnt"
flexi_surface = "flexiSurfaceSling_geo"
get_joint_chain = true
#mirror_direction = "left"
#mirror_right = true
#hide_end_ctrl = true
#display_layer = true
```

#### `eye_aim_mod`
Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `display_layer`, `aim_vector`, `up_vector`, `reverse_right_vectors`.  
Notes:  
Aim ctrls in front of the face, plus fk offset ctrls on the eyes.  
`joints` — left then right eye (exactly 2), or 1 joint for a single eye. Do not use `mirror_right`.  
`aim_vector` — forward axis of the eye joints. Chosen from world forward if omitted.  
`up_vector` — up axis of the eye joints. Chosen from world up if omitted.  
`reverse_right_vectors` — reverse the right eye aim/up axes. Use if the right joint was mirrored with Maya Mirror Joints.

```toml
[[rig_module]]
rig_module = "eye_aim_mod"
rig_module_name = "eyes"
joints = "eye_left_jnt, eye_right_jnt"
#aim_vector = "z"
#up_vector = "y"
#reverse_right_vectors = true
#display_layer = true
```

#### `piston_mod`
Required: `rig_module`, `rig_module_name`, `mid_joints`, `top_joints`, `bot_joints`.  
Optional: `mirror_direction`, `mirror_right`, `display_layer`, `origin_joint`.  
Notes:  
Hydraulic piston with a three-axis gimbal on each end. Build at origin, joints world Y-up, planar on YZ, center straight up/down. See `defaults/otherRigExamples/pistonMod_autoRig`.  
`origin_joint` — optional root for scale/position. Exactly 1 joint if used.  
`mid_joints` — exactly 1 joint, skinned to the piston middle.  
`top_joints` — 3 joints in order (gimbal). Optional 4th is a stretch joint, parented under the first top joint. First two share a position; the third extends toward the connection.  
`bot_joints` — same as top, exactly 3.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "piston_mod"
rig_module_name = "piston"
mid_joints = "piston_mid_jnt"
top_joints = "piston_top_01_jnt, piston_top_02_jnt, piston_top_03_jnt"
bot_joints = "piston_bot_01_jnt, piston_bot_02_jnt, piston_bot_03_jnt"
#origin_joint = "pistonMain_jnt"
#mirror_direction = "left"
#mirror_right = true
#display_layer = true
```

#### `digitigrade_leg_mod`

Required: `rig_module`, `rig_module_name`, `joints`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `main_object_names`, `foot_locators`, `invert_toe_wiggle`, `invert_toe_spin`, `invert_foot_lean`, `invert_foot_tilt`, `invert_foot_roll`, `ankle_x_forward`, `flip_spring_solver`.  
Notes:  
Quadruped-style leg that walks on the toes (dog, cat, bird).  
`joints` — exactly 5: hip, knee, ankle, foot, toe.  
`foot_locators` — 4 locators in order: toe end, heel, lateral, medial. Skip to use default names (`toeEnd_left_loc`, `heel_left_loc`, `lateral_left_loc`, `medial_left_loc`).  
`invert_toe_wiggle` / `invert_toe_spin` / `invert_foot_lean` / `invert_foot_tilt` / `invert_foot_roll` — invert that reverse-foot attr. Useful when both feet share the same axis but are opposite sides.  
`ankle_x_forward` — ankle X is horizontal (forward or back) instead of world up/down. Swaps spin/lean/tilt axes; roll and toe wiggle stay on rotateZ.  
`flip_spring_solver` — flip the driver-joint ikHandle twist 180 if the spring solver aims the wrong way.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "digitigrade_leg_mod"
rig_module_name = "leg"
mirror_direction = "left"
joints = "hip_left_jnt, knee_left_jnt, ankle_left_jnt, foot_left_jnt, toeMain_left_jnt"
mirror_right = true
#get_joint_chain = true
#main_object_names = "upperLeg, middleLeg, lowerLeg, ankle, toe"
#foot_locators = "toeEnd_left_loc, heel_left_loc, lateral_left_loc, medial_left_loc"
#invert_toe_wiggle = true
#invert_toe_spin = true
#invert_foot_lean = true
#invert_foot_tilt = true
#invert_foot_roll = true
#ankle_x_forward = true
#flip_spring_solver = true
#display_layer = true
```

#### `tentacle_mod`

Required: `rig_module`, `rig_module_name`, `joints`, `flexi_joints_main`, `flexi_joints_offset`, `flexi_surface_main`, `flexi_surface_offset`.  
Optional: `mirror_direction`, `mirror_right`, `get_joint_chain`, `display_layer`, `separate_flexi_ctrls`, `use_flexi_ik_chain`.  
Notes:  
Tentacle / tail / stretchy spine. Works with a flexi cloth setup.  
`joints` — skinned joints on the character geo. Attached to `flexi_surface_main` via follicles.  
`flexi_joints_main` — base flexi joint layer. Blends between fk and offset flexi ctrls.  
`flexi_joints_offset` — shorter offset chain to blend against (often ~3 joints).  
`flexi_surface_main` — main flexi geo, skinned to `flexi_joints_main`. Use this mesh for cloth.  
`flexi_surface_offset` — flexi geo skinned to `flexi_joints_offset`.  
`get_joint_chain` — expands `joints`, `flexi_joints_main`, and `flexi_joints_offset` from first/last.  
`separate_flexi_ctrls` — leave flexi ctrls as separate ctrls instead of a hierarchy. Useful for complex parent spaces.  
`use_flexi_ik_chain` — single-chain ikHandles on flexi ctrls instead of fk, with a stretch toggle.  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "tentacle_mod"
rig_module_name = "tail"
joints = "tail_01_jnt, tail_09_jnt"
flexi_joints_main = "tailCloth_01_jnt, tailCloth_09_jnt"
flexi_joints_offset = "tailClothFlexi_start_jnt, tailClothFlexi_end_jnt"
flexi_surface_main = "flexiSurfaceTailMain_geo"
flexi_surface_offset = "flexiSurfaceTailStretch_geo"
get_joint_chain = true
#mirror_direction = "left"
#mirror_right = true
#separate_flexi_ctrls = true
#use_flexi_ik_chain = true
#display_layer = true
```

#### `fk_aim_mod`
Required: `rig_module`, `rig_module_name`, `joints`, `aim_object`.  
Optional: `mirror_direction`, `mirror_right`, `display_layer`, `aim_vector`, `up_vector`, `reverse_right_vectors`.  
Notes:  
Fk ctrl on a joint that aims at another object (e.g. elbow at the arm pole vector).  
`joints` — usually a single joint.  
`aim_object` — object/ctrl to aim at. `mirror_right` also swaps side strings in this name.  
`aim_vector` — local axis that aims at `aim_object`. Defaults to `x`.  
`up_vector` — local axis used to place the world-up guide. Defaults to `y`.  
`reverse_right_vectors` — reverse aim/up on the right side (e.g. `-x` to `x`).  
`mirror_right` — build the right side from this left entry.

```toml
[[rig_module]]
rig_module = "fk_aim_mod"
rig_module_name = "elbow"
mirror_direction = "left"
joints = "wingElbow_01_left_jnt"
aim_object = "ikArmPoleVector_left_ctrl"
mirror_right = true
#aim_vector = "x"
#up_vector = "y"
#reverse_right_vectors = true
#display_layer = true
```

#### `import_rig_mod`
Required: `rig_module`, `rig_module_name`.  
Optional: `mirror_direction`, `mirror_right`, `display_layer`, `locators`, `controls`, `remove_namespace`, `reference`, `custom_rig_filepath`, `custom_rig_folderpath`, `custom_rig_filename`.  
Notes:  
Imports (or references) a pre-built / custom rig `.ma` during the module phase so parent spaces and ctrl shapes still apply. Materials and display layers merge if they already exist.  
Default file: `custom_rig.ma` next to the auto-rig folder (e.g. `.../character/rig/custom_rig.ma`).  
`custom_rig_filename` — Maya filename only, including extension. Defaults to `custom_rig.ma`.  
`custom_rig_folderpath` — folder only, no filename. Defaults to the auto-rig folder’s parent.  
`custom_rig_filepath` — full path including filename. If set, folder/filename are ignored.  
`locators` — locators in `rig_helpers.ma` used to place imported ctrls. Index-matched to `controls`.  
`controls` — ctrls in the imported rig to snap to `locators`. If either list is empty, the import stays where it is.  
`remove_namespace` — remove the import namespace after bringing the file in.  
`reference` — reference the file instead of importing.  
`mirror_right` — build the right side from this left entry (also swaps side strings in `locators` / `controls`).

```toml
[[rig_module]]
rig_module = "import_rig_mod"
rig_module_name = "propExample"
custom_rig_filename = "propExample_rig.ma"
#mirror_direction = "left"
#mirror_right = true
#locators = "prop_left_loc"
#controls = "fkProp_left_ctrl"
#remove_namespace = true
#reference = true
#custom_rig_folderpath = "C:/path/to/rig"
#custom_rig_filepath = "C:/path/to/rig/propExample_rig.ma"
#display_layer = true
```