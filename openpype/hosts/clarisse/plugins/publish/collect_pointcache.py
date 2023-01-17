import os
import pyblish.api
from openpype.hosts.clarisse.api.pipeline import get_export_containers
from openpype.pipeline import (
    legacy_io
)
import ix



class CollectPointCacheModelNode(pyblish.api.ContextPlugin):
    """Collect camera exports
    """

    order = pyblish.api.CollectorOrder - 0.01
    label = "Collect Clarisse Geometry"
    hosts = ["clarisse"]
    family = "model"

    def process(self, context):
        """Inject the current geometry output and file"""

        task = legacy_io.Session["AVALON_TASK"]
        geo_collection = get_export_containers(creatortype="geometry")
        # create instances
        for geo in geo_collection:
            item = ix.get_item(str(geo))
            geo_filename = item.attrs.filename[0]
            folder, file = os.path.split(geo_filename)
            geo_name = str(geo).split("/")[-1]
            instance = context.create_instance(name=str(geo_name))
            subset = 'model' + task.capitalize()

            data = {}
            data.update({
                "subset": subset,
                "asset": os.getenv("AVALON_ASSET", None),
                "label": str(geo_name),
                "publish": True,
                "family": "model",
                "families": ["model","pointcache"],
                "setMembers": [""],
                "frameStart": context.data['frameStart'],
                "frameEnd": context.data['frameEnd'],
                "handleStart": context.data['handleStart'],
                "handleEnd": context.data['handleEnd'],
                "clarisse_geo_context": str(geo),
                "export_ui_object": str(geo)
            })

            instance.context.data["cleanupFullPaths"].append(folder)

            instance.data.update(data)