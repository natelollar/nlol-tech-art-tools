### Overview: `blendshape_setdrivekeys.toml`
```
Connect blendshapes or other object attributes to transform ctrls  
via set driven keys.
For a face ctrl setup, for example, include the ctrls in "rig_helpers.ma".
Include the blendshapes weighted to single meshes in "blendshapes.ma".
```
#### Root Level Parameters:
- `blendshape_objs` (str): Mesh objects containing the blendshape nodes to be iterated over,  
    for connecting set driven keys to ctrls. String name or string list.
- `inTangentType, outTangentType` (str): Set driven key's "in/out tangent type"  
    for animation curve. Defaults to "linear".  
    Optional.

#### [[rig_module]] Parameters:
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

---
*Lists written as "string lists".*
