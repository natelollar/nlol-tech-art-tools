# Rig Module Notes
Notes for rigging setup.

### Module List
- `biped_leg_mod`  
  Standard biped leg rig. Foot included. Takes 4 main joints and optional twist joints.
- `fk_control_mod`  
  Single fk control.  Takes one joint.

### Notes
- Enter joints in order, down the chain.  
  Example: Hip to toe. Shoulder to wrist.

- Build rig first to get control names, then setup parent spaces.  
  Then, directly name parent spaces off of controls.


#### Maya Object Naming
- `<name>_<direction>_<id>_<type>`
  - Hybrid snake_case with camelCase components.
  - Not all components required.
  - `<name>` can be any string. 
  - Stick to convention for `<direction>`, `<id>`, and `<type>`.
  - Primary type at end of type name.
  - Zero padded id.
  - Lowercase alpha-numeric id prefix when needed.
    - `a01, a02, a03, a04`
  - Examples:
    - `fkLip_topCenter_ctrlParentSwitchGrp`
    - `ikTentacleClaw_frontTopRight_ctrlGrp`
    - `middleFinger_left_01_jnt`
    - `enginePart_right_a02_ctrlOffsetGrp`
    - `rig_grp`

- `<direction>` conventions in this order
  - `front, back`
  - `top, bot`
  - `left, center, right`  
  - Examples:
    - `frontTopLeft`
    - `backBotRight`
    - `center`
    - `left`
    - `frontBot`

- `<type>` conventions. (not all possible types listed).
  - `geo`
  - `jnt`
  - `ctrl`
  - group conventions
    - `grp`
    - `allGrp`
    - `offsetGrp`
    - `prntSwchGrp`
    - group prefix is the type grouped
        - `geoGrp`
        - `ctrlGrp`
        - `ctrlOffsetGrp`
  - `ikHandle`
  - `ikHandleEffector`
  - `crv`
  - `ikHandleCrv`
  - `skinCluster`
  - `blendColors`
  - `multiplyDivide`
  - `plusMinusAverage`

#### Maya Attribute Naming
- camelCase

#### Common Abbreviations Defined
- attr = attribute
- const = constraint
- ctrl = control
- dict = dictionary
- dir = direction
- dist = distance
- fk = forward kinematics
- geo = geometry
- grp = group
- ik = inverse kinematics
- jnt = joint
- loc = locator
- mirr = mirror
- mod = module
- msg = message
- nd = node
- obj = object
- offs = offset
- ps = parent space
- pos = position
- prnt = parent
- rot = rotate
- scl = scale
- str = string
- strt = start
- swch = switch
- twst = twist
- tran = translate
- vis = visibility
