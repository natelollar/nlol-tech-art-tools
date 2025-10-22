from nlol.core import general_utils

from maya import cmds

swap_side_str = general_utils.swap_side_str


def mirror_selected_ctrls(to_other_side: bool = False):
    """Mirror selected ctrl values to other side, or mirror selected from other side.
    Either "left to right" or "right to left",
    or mirror selected ctrl if no other side,
    for a center ctrl for example. Uses mirror attributes
    on ctrl transform, for example, "mirrorTranslateX".
    Can save out mirror attrs with "mirror_attrs_export_import.py".

    Args:
        to_other_side: Mirror selected ctrl to other side,
            instead of mirroring selected ctrl itself. Though,
            mirroing a center ctrl will mirror itself either way.

    """
    selected = cmds.ls(selection=True)

    new_transform_data = {} # get data in current state before transforming
    for sel_ctrl in selected:
        for attr_prefix in ["mirrorTranslate", "mirrorRotate"]:
            for axis in "XYZ":
                mirr_attr = f"{attr_prefix}{axis}"
                transform_attr = mirr_attr.replace("mirrorT", "t")
                transform_attr = transform_attr.replace("mirrorR", "r")

                opposite_ctrl = swap_side_str(sel_ctrl)

                if to_other_side: # get values for opposite side
                    mirr_mult_val = cmds.getAttr(f"{opposite_ctrl}.{mirr_attr}")
                    if mirr_mult_val == 0:  # skip
                        continue

                    sel_trans_val = cmds.getAttr(f"{sel_ctrl}.{transform_attr}")
                    # 1 or -1 times selected ctrl value
                    new_trans_val = mirr_mult_val * sel_trans_val

                    # append final ctrl attribute and value
                    ctrl_attr = f"{opposite_ctrl}.{transform_attr}"
                    new_transform_data[ctrl_attr] = new_trans_val
                else:  # get values for selected side
                    mirr_mult_val = cmds.getAttr(f"{sel_ctrl}.{mirr_attr}")
                    if mirr_mult_val == 0:
                        continue

                    opposite_trans_val = cmds.getAttr(f"{opposite_ctrl}.{transform_attr}")
                    new_trans_val = mirr_mult_val * opposite_trans_val

                    ctrl_attr = f"{sel_ctrl}.{transform_attr}"
                    new_transform_data[ctrl_attr] = new_trans_val

    # apply transform changes
    for ctrl_attr, val in new_transform_data.items():
        cmds.setAttr(ctrl_attr, val)
