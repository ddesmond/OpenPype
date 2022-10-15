import os
import pyblish.api

from openpype.hosts.clarisse.api.pipeline import get_current_clarisseproject_fullpath


class CollectCurrentProjectFile(pyblish.api.ContextPlugin):
    """Collect current project file"""

    order = pyblish.api.CollectorOrder - 0.4
    label = "Collect Current Project File"
    hosts = ["clarisse"]

    def process(self, context):
        """Collect project file"""

        current_project_file = get_current_clarisseproject_fullpath()
        assert current_project_file

        context.data['currentFile'] = current_project_file