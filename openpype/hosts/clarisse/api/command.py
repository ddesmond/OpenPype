import logging
import ix

from openpype.pipeline.context_tools import get_current_project_asset

from .lib import command_batch

log = logging.getLogger(__name__)


def reset_frame_range():
    """ Set timeine frame range.
    """

    asset_doc = get_current_project_asset()
    asset_data = asset_doc["data"]

    fps = float(asset_data.get("fps", 25))
    ix.cmds.SetFps(fps)
    frame_start = str(asset_data.get(
        "frameStart",
        asset_data.get("edit_in")))

    frame_end = str(asset_data.get(
        "frameEnd",
        asset_data.get("edit_out")))
    log.info(frame_start)
    log.info(frame_end)

    with command_batch("OpenPype: reset frame range"):
        image = "project://scene/image"
        ix.cmds.SetValue(image + ".background.first_frame", frame_start)
        ix.cmds.SetValue(image + ".background.last_frame", frame_end)
        ix.cmds.SetCurrentFrameRange(float(frame_start), float(frame_end))
        log.info("Frame range set")


def reset_resolution():
    """Set resolution to project resolution."""

    asset = get_current_project_asset()
    asset_data = asset["data"]

    width = asset_data.get("resolutionWidth")
    height = asset_data.get("resolutionHeight")

    if not width or not height:
        log.info("No width or height set in asset. "
                 "Skipping reset resolution..")
        return

    image = ix.get_item('project://scene/image')
    current_width = image.attrs.resolution[0]
    current_height = image.attrs.resolution[1]
    if width == current_width and height == current_height:
        # No change needed
        return

    with command_batch("OpenPype: reset resolution"):
        image.attrs.resolution_preset = "Custom"
        image.attrs.resolution[0] = width
        image.attrs.resolution[1] = height
        image.attrs.resolution_multiplier = "2"
