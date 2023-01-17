import os
import pyblish.api
from openpype.hosts.clarisse.api.pipeline import get_export_containers
from openpype.pipeline import (
    legacy_io
)
import ix



class CollectContextOutputNode(pyblish.api.ContextPlugin):
    """Collect context exports
    """

    order = pyblish.api.CollectorOrder - 0.01
    label = "Collect Clarisse Export Context"
    hosts = ["clarisse"]
    family = "refcontext"

    def process(self, context):
        """Inject the current camera output and file"""

        task = legacy_io.Session["AVALON_TASK"]
        item_collection = get_export_containers(creatortype="context")

        # create instances
        for item in item_collection:
            item_sel = ix.get_item(str(item))
            item_filename = item_sel.attrs.filename[0]

            folder, file = os.path.split(item_filename)
            filename, ext = os.path.splitext(file)
            item_name = str(item).split("/")[-1]
            instance = context.create_instance(name=str(item_name))
            subset = 'context' + task.capitalize()

            data = {}
            data.update({
                "subset": subset,
                "asset": os.getenv("AVALON_ASSET", None),
                "label": str(item_name),
                "publish": True,
                "family": 'refcontext',
                "families": ["refcontext", "workfile"],
                "setMembers": [""],
                "frameStart": context.data['frameStart'],
                "frameEnd": context.data['frameEnd'],
                "handleStart": context.data['handleStart'],
                "handleEnd": context.data['handleEnd'],
                "clarisse_ref_context": str(item_sel.get_attribute("op_sourced_path").get_string(0)),
                "export_ui_object": str(item),
                "export_filename": str(item_filename)
            })

            instance.context.data["cleanupFullPaths"].append(folder)

            instance.data.update(data)