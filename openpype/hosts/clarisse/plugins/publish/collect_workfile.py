import os
import pyblish.api
from openpype.hosts.clarisse.api.pipeline import get_current_clarisseproject_fullpath
from openpype.pipeline import (
    legacy_io, 
    registered_host
)


class CollectWorkfile(pyblish.api.ContextPlugin):
    """Inject the current working file into context"""

    order = pyblish.api.CollectorOrder - 0.01
    label = "Clarisse Workfile"
    hosts = ['clarisse']

    def process(self, context):
        """Inject the current working file"""
        host = registered_host()
        current_file = get_current_clarisseproject_fullpath()
        if not current_file:
            self.log.error("No current filepath detected")

        folder, file = os.path.split(current_file)
        filename, ext = os.path.splitext(file)

        task = legacy_io.Session["AVALON_TASK"]

        # create instance
        instance = context.create_instance(name=filename)
        subset = 'workfile' + task.capitalize()

        data = {}
        data.update({
            "subset": subset,
            "asset": os.getenv("AVALON_ASSET", None),
            "label": subset,
            "publish": True,
            "family": 'workfile',
            "families": ['workfile'],
            "setMembers": [current_file],
            "frameStart": context.data['frameStart'],
            "frameEnd": context.data['frameEnd'],
            "handleStart": context.data['handleStart'],
            "handleEnd": context.data['handleEnd']
        })

        data['representations'] = [{
            'name': ext.lstrip("."),
            'ext': ext.lstrip("."),
            'files': file,
            "stagingDir": folder,
        }]

        instance.data.update(data)