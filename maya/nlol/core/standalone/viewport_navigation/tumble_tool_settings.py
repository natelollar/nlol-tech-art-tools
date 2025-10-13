from maya import cmds
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def reset_tumble_settings():
    """Reset camera tumble tool settings to default. "View < Camera Tools < Tumble Tool"."""
    cmds.tumbleCtx("tumbleContext", edit=True, tumbleScale=1.0)
    cmds.tumbleCtx("tumbleContext", edit=True, objectTumble=False)
    cmds.tumbleCtx("tumbleContext", edit=True, localTumble=1)
    cmds.tumbleCtx("tumbleContext", edit=True, autoSetPivot=False)
    cmds.tumbleCtx("tumbleContext", edit=True, autoOrthoConstrain=True)
    cmds.tumbleCtx("tumbleContext", edit=True, orthoStep=5.0)
    cmds.tumbleCtx("tumbleContext", edit=True, orthoLock=True)

    logger.info('Reset tumble tool settings. "View < Camera Tools < Tumble Tool"')


def apply_tumble_settings():
    """Set camera tumble tool settings needed for "camera_pivot_to_mouse" tool.
    These settings can be set manually in "View < Camera Tools < Tumble Tool".
    """
    reset_tumble_settings()  # reset tumble tool settings first

    cmds.tumbleCtx("tumbleContext", edit=True, localTumble=0)  # tumble about cameras tumble pivot

    logger.info('Tumble Tool settings applied. "View < Camera Tools < Tumble Tool"')
