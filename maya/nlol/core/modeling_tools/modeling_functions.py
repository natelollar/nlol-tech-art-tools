from maya import cmds, mel


def auto_seams_hard_edges() -> None:
    """Create UV seams at hard edges for multiple objects."""
    selected = cmds.ls(selection=True)

    for obj in selected:
        mel.eval("polyUVHardEdgesAutoSeams 1;")
