from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger


class BlendMatrixModule:
    """Blend one object between two others with world matrices."""

    def __init__(
        self,
        rig_module_name: str,
        mirror_direction: str | None,
        main_object: str,
        blend_objects: list[str],
        switch_attr: str,
    ):
        """Args:
        rig_module_name: Custom name for the rig module.
        mirror_direction: Mirror side as in "left" or "right".
        main_object: Object that receives the blend.
        blend_objects: Two objects to blend between. Index 0 at switch 0, index 1 at switch 1.
        switch_attr: Existing attribute plug that drives the blend. Example "ctrl.blend".

        """
        self.mod_name = rig_module_name
        self.mirr_side = f"_{mirror_direction}_" if mirror_direction else "_"
        self.main_object = main_object
        self.blend_objects = blend_objects
        self.switch_attr = switch_attr
        self.logger = get_logger()

    def build(self):
        """Entry point. Connect the main object between the two blend objects."""
        if len(self.blend_objects) != 2:
            error_msg = f"{self.mod_name}: blend_objects needs exactly 2 objects."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        obj_a, obj_b = self.blend_objects
        obj_main = self.main_object

        blend_nd = cmds.createNode(
            "blendMatrix",
            name=f"{self.mod_name}{self.mirr_side}blendMatrix",
        )
        cmds.connectAttr(f"{obj_a}.worldMatrix[0]", f"{blend_nd}.inputMatrix")
        cmds.connectAttr(f"{obj_b}.worldMatrix[0]", f"{blend_nd}.target[0].targetMatrix")
        cmds.connectAttr(self.switch_attr, f"{blend_nd}.target[0].weight")

        mult_nd = cmds.createNode(
            "multMatrix",
            name=f"{self.mod_name}{self.mirr_side}multMatrix",
        )
        cmds.connectAttr(f"{blend_nd}.outputMatrix", f"{mult_nd}.matrixIn[0]")
        cmds.connectAttr(f"{obj_main}.parentInverseMatrix[0]", f"{mult_nd}.matrixIn[1]")

        decomp_nd = cmds.createNode(
            "decomposeMatrix",
            name=f"{self.mod_name}{self.mirr_side}decomposeMatrix",
        )
        cmds.connectAttr(f"{mult_nd}.matrixSum", f"{decomp_nd}.inputMatrix")
        cmds.connectAttr(f"{decomp_nd}.outputTranslate", f"{obj_main}.translate")
        cmds.connectAttr(f"{decomp_nd}.outputScale", f"{obj_main}.scale")
        self.connect_rotate(obj_main, mult_nd, decomp_nd)

    def connect_rotate(self, main: str, mult_nd: str, decomp_nd: str):
        """Connect decomposed rotate. Joints subtract jointOrient."""
        if cmds.objectType(main) != "joint":
            cmds.connectAttr(f"{decomp_nd}.outputRotate", f"{main}.rotate")
            return

        # ----- extra jointOrient setup when blending joints -----
        rot_pick = cmds.createNode(
            "pickMatrix",
            name=f"{self.mod_name}{self.mirr_side}rotate_pickMatrix",
        )
        cmds.connectAttr(f"{mult_nd}.matrixSum", f"{rot_pick}.inputMatrix")
        cmds.setAttr(f"{rot_pick}.useTranslate", False)
        cmds.setAttr(f"{rot_pick}.useScale", False)
        cmds.setAttr(f"{rot_pick}.useShear", False)

        # jointOrient is always xyz
        jo_mtx = cmds.createNode(
            "composeMatrix",
            name=f"{self.mod_name}{self.mirr_side}jointOrient_composeMatrix",
        )
        cmds.connectAttr(f"{main}.jointOrient", f"{jo_mtx}.inputRotate")
        cmds.setAttr(f"{jo_mtx}.inputRotateOrder", 0)

        jo_inv = cmds.createNode(
            "fourByFourMatrix",
            name=f"{self.mod_name}{self.mirr_side}jointOrient_fourByFourMatrix",
        )
        for i in range(4):
            col = cmds.createNode(
                "columnFromMatrix",
                name=f"{self.mod_name}{self.mirr_side}jointOrient_{i}_columnFromMatrix",
            )
            cmds.setAttr(f"{col}.input", i)
            cmds.connectAttr(f"{jo_mtx}.outputMatrix", f"{col}.matrix")
            for axis, src in zip("0123", "XYZW", strict=True):
                cmds.connectAttr(f"{col}.output{src}", f"{jo_inv}.in{i}{axis}")

        rot_mult = cmds.createNode(
            "multMatrix",
            name=f"{self.mod_name}{self.mirr_side}rotate_multMatrix",
        )
        cmds.connectAttr(f"{rot_pick}.outputMatrix", f"{rot_mult}.matrixIn[0]")
        cmds.connectAttr(f"{jo_inv}.output", f"{rot_mult}.matrixIn[1]")

        rot_decomp = cmds.createNode(
            "decomposeMatrix",
            name=f"{self.mod_name}{self.mirr_side}rotate_decomposeMatrix",
        )
        cmds.connectAttr(f"{rot_mult}.matrixSum", f"{rot_decomp}.inputMatrix")
        cmds.connectAttr(f"{main}.rotateOrder", f"{rot_decomp}.inputRotateOrder")
        cmds.connectAttr(f"{rot_decomp}.outputRotate", f"{main}.rotate")
