from maya import cmds, mel
from nlol.core.general_utils import maya_undo
from nlol.utilities.nlol_maya_logger import get_logger

logger = get_logger()


def get_timeslider_selection() -> tuple[float, float] | None:
    """Return highlighted timeslider range, or None if nothing is highlighted.

    rangeArray end is exclusive, so convert to inclusive.
    """
    slider = mel.eval("$tmp=$gPlayBackSlider")
    if not cmds.timeControl(slider, query=True, rangeVisible=True):
        return None
    start, end = cmds.timeControl(slider, query=True, rangeArray=True)
    return start, end - 1


def get_playback_range() -> tuple[float, float]:
    """Return animation playback start and end."""
    return (
        cmds.playbackOptions(query=True, minTime=True),
        cmds.playbackOptions(query=True, maxTime=True),
    )


def _bookmark_overlaps(mark: str, start: float, end: float) -> bool:
    """True if the bookmark overlaps the given time range."""
    mark_start = cmds.getAttr(f"{mark}.timeRangeStart")
    mark_stop = cmds.getAttr(f"{mark}.timeRangeStop")
    return mark_start <= end and mark_stop >= start


def _move_bookmark(mark: str, offset: float) -> None:
    """Shift a bookmark's start and stop by offset.

    Set stop first when moving later, so start never passes stop.
    """
    start = cmds.getAttr(f"{mark}.timeRangeStart")
    stop = cmds.getAttr(f"{mark}.timeRangeStop")
    if offset >= 0:
        cmds.setAttr(f"{mark}.timeRangeStop", stop + offset)
        cmds.setAttr(f"{mark}.timeRangeStart", start + offset)
    else:
        cmds.setAttr(f"{mark}.timeRangeStart", start + offset)
        cmds.setAttr(f"{mark}.timeRangeStop", stop + offset)


def _move_bookmarks(bookmarks: list[str], offset: int, scope: str) -> int:
    """Offset bookmarks and log how many moved."""
    if not bookmarks:
        logger.warning(f"No bookmarks {scope}.")
        return 0
    for mark in bookmarks:
        _move_bookmark(mark, offset)
    logger.info(f"Offset {len(bookmarks)} bookmark(s) ({scope}) by {offset} frame(s).")
    return len(bookmarks)


@maya_undo
def offset_bookmarks(offset: int) -> int:
    """Offset bookmarks in the timeslider selection, or playback range if none."""
    bookmarks = cmds.ls(type="timeSliderBookmark") or []
    if not bookmarks:
        logger.warning("No animation bookmarks in the scene.")
        return 0

    time_sel = get_timeslider_selection()
    if time_sel:
        start, end = time_sel
        scope = f"in selection ({start:g}-{end:g})"
    else:
        start, end = get_playback_range()
        scope = f"in playback range ({start:g}-{end:g})"

    targets = [mark for mark in bookmarks if _bookmark_overlaps(mark, start, end)]
    return _move_bookmarks(targets, offset, scope)


@maya_undo
def offset_all_bookmarks(offset: int) -> int:
    """Offset all animation bookmarks in the timeline."""
    bookmarks = cmds.ls(type="timeSliderBookmark") or []
    if not bookmarks:
        logger.warning("No animation bookmarks in the scene.")
        return 0
    return _move_bookmarks(bookmarks, offset, "all")
