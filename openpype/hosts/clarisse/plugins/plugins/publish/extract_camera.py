import os
from pprint import pformat
import pyblish.api

from openpype.hosts.clarisse.api.exports import export_context_alembic
from openpype.pipeline import publish

import ix

class ExtractClarisseCamera(publish.Extractor):

    order = pyblish.api.ExtractorOrder
    label = "Extract Clarisse Camera from Context"
    hosts = ["clarisse"]
    families = ["camera"]

    def process(self, instance):

        self.log.info("instance.data: `{}`".format(
            pformat(instance.data)))

        cam = instance.data["clarisse_camera_context"]
        options_ui = ix.get_item(instance.data["export_ui_object"])
        export_context_alembic(creator_type="camera",
                               selection=str(cam),
                               mode="trigger",
                               item_object=options_ui)

        selcam = ix.get_item(str(instance.data["export_ui_object"]))
        cam_filename = selcam.attrs.filename[0]

        assert os.path.isfile(cam_filename)

        folder, file = os.path.split(cam_filename)
        filename, ext = os.path.splitext(file)

        representation = {
            "name": ext.lstrip("."),
            "ext": ext.lstrip("."),
            "files": file,
            "stagingDir": folder,
        }

        if "representations" not in instance.data:
            instance.data["representations"] = []

        instance.data["representations"].append(representation)