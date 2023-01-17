import os
from pprint import pformat
import pyblish.api

from openpype.hosts.clarisse.api.exports import export_context_alembic
from openpype.pipeline import publish

import ix

class ExtractClarissePointCacheModel(publish.Extractor):

    order = pyblish.api.ExtractorOrder
    label = "Extract Clarisse Geometry from Context"
    hosts = ["clarisse"]
    families = ["model"]

    def process(self, instance):

        self.log.info("instance.data: `{}`".format(
            pformat(instance.data)))

        item = instance.data["clarisse_geo_context"]
        options_ui = ix.get_item(instance.data["export_ui_object"])

        export_context_alembic(creator_type="geometry",
                               selection=str(item),
                               mode="trigger",
                               item_object=options_ui)

        sel_item = ix.get_item(str(item))
        item_filename = sel_item.attrs.filename[0]

        assert os.path.isfile(item_filename)

        folder, file = os.path.split(item_filename)
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