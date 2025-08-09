# Rig Modules Overview
Overview explanation.

## Module List
- `biped_leg`  
  Standard biped leg rig. Foot included. Takes 4 main joints and twist joints.
- `biped_arm`  
  Standard biped arm rig.
- `fk_single`  
  Single fk control.  Takes one joint.
- `fk_chain`  
  Standard fk chain. Takes any number of joints in a chain.
- `fk_spline_chain` 
  Description.
- `spline_chain`  
  Description.

### Notes

- Enter joints in order, down the chain.  
  Example: Hip to toe. Shoulder to wrist.

---

- Build rig first to get control names, then setup parent spaces.  
  Then, directly name parent spaces off of controls, joints, etc.