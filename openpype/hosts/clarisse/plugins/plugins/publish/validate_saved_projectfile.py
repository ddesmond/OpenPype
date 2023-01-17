import os
import pyblish.api


class ValidateClarisseProjectSave(pyblish.api.ContextPlugin):
    """Ensure current project is saved"""

    order = pyblish.api.ValidatorOrder
    label = "Validate Project is Saved"
    families = ["*"]
    hosts = ["clarisse"]

    def process(self, context):

        projectfile = context.data.get("currentFile")
        assert projectfile, "Must have project file"

        if not os.path.exists(projectfile):
            raise RuntimeError("Project file does not exist: %s" % projectfile)
