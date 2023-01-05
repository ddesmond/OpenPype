import logging
import os

import ix

from openpype.pipeline.context_tools import get_current_project_asset
from .config_manager import legacy_procees_configmanager_setup

from .lib import command_batch, popsup

log = logging.getLogger(__name__)


def reset_frame_range():
    """ Set timeline frame range.
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
        ix.cmds.SetValues([image + ".background.first_frame"], [frame_start])
        ix.cmds.SetValues([image + ".background.last_frame"], [frame_end])
        ix.cmds.SetCurrentFrameRange(float(frame_start), float(frame_end))
        log.info("Frame range set")


def set_project_fps():
    """ Set project fps.
    """

    asset_doc = get_current_project_asset()
    asset_data = asset_doc["data"]

    fps = float(asset_data.get("fps", 25))
    with command_batch("OpenPype: set FPS"):
        ix.cmds.SetFps(fps)
        log.info("Project FPS set")


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


def set_project_config_defaults():
    """Load up configs and set prefs to local user config file
    """
    ix.log_info("Setting up Local user Preferences")

    if os.environ.get("CLARISSE_LOADED_CONFIG"):
        print("Configuration file has already been set from App launch. You cant load any prefs.")
        print("Currently loaded config path is {}".format(os.environ["CLARISSE_LOADED_CONFIG"]))

    else:
        print("Loading up global default preferences into local user config file.")
        legacy_procees_configmanager_setup()
        print("Please re-save your project file manualy.")
        infotext = """
            Clarisse Preferences:\n
            Clarisse User preferences have been changed.
            """
        popsup(info_text=infotext)


def create_support_ticket():
    import webbrowser
    webbrowser.open("https://google.com")
