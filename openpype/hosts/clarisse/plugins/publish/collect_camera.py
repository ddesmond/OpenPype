import os
import pyblish.api
from openpype.hosts.clarisse.api.pipeline import get_export_containers
from openpype.pipeline import (
    legacy_io
)
import ix



class CollectCameraNode(pyblish.api.ContextPlugin):
    """Collect camera exports
    """

    order = pyblish.api.CollectorOrder - 0.01
    label = "Collect Clarisse Cameras"
    hosts = ["clarisse"]
    family = "camera"

    def process(self, context):
        """Inject the current camera output and file"""

        task = legacy_io.Session["AVALON_TASK"]
        cam_collection = get_export_containers(creatortype="camera")
        # create instances
        for cam in cam_collection:
            selcam = ix.get_item(str(cam))
            cam_filename = selcam.attrs.filename[0]
            print("CAM COLLECTED", str(selcam))
            folder, file = os.path.split(cam_filename)
            filename, ext = os.path.splitext(file)
            cam_name = str(cam).split("/")[-1]
            instance = context.create_instance(name=str(cam_name))
            subset = 'camera' + task.capitalize()

            data = {}
            data.update({
                "subset": subset,
                "asset": os.getenv("AVALON_ASSET", None),
                "label": str(cam_name),
                "publish": True,
                "family": 'camera',
                "families": ['camera'],
                "setMembers": [""],
                "frameStart": context.data['frameStart'],
                "frameEnd": context.data['frameEnd'],
                "handleStart": context.data['handleStart'],
                "handleEnd": context.data['handleEnd'],
                "clarisse_camera_context": str(selcam),
                "export_ui_object": str(cam)
            })

            instance.context.data["cleanupFullPaths"].append(folder)

            instance.data.update(data)