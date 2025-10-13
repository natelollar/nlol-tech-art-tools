from maya import cmds


def mirr_jnt_axis_flip(
    axis_180_flip: str = "z",
    direction_label: str = "left",
    new_label: str = "right",
) -> None:
    """Duplicate then mirror joints with chosen axis' flipped (rotated 180 degrees).
    This can be used to achieve mirrored joints with a similar facing translation orient.
    Mirrors in worldspace by inverting "x" position.

    Args:
        axis_180_flip: Choose axis to rotate 180. Can be any combination of "xyz" letters.
        direction_label: Joint direction label.
        new_label: New direction label to replace original.

    """
    my_sel = cmds.ls(selection=True)

    for jnt in my_sel:
        new_joint = cmds.mirrorJoint(
            jnt,
            mirrorYZ=True,
            mirrorBehavior=True,
            searchReplace=(direction_label, new_label),
        )
        cmds.makeIdentity(
            new_joint,
            apply=True,
        )  # freeze joint rotations to zero out gimbal

        for axis in axis_180_flip:
            cmds.setAttr(new_joint[0] + f".rotate{axis.upper()}", 180)
            print(f"{axis.upper()} flipped: {jnt}")

        cmds.makeIdentity(new_joint, apply=True)  # refreeze joint rotations

        # copy over joint wire color
        for color in "RGB":
            jnt_clr = cmds.getAttr(jnt + f".wireColor{color}")
            cmds.setAttr(new_joint[0] + f".wireColor{color}", jnt_clr)


# Test:
# mirr_jnt_same_orient()
