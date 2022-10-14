import ix
import pyblish.api


class ClarisseSaveProject(pyblish.api.ContextPlugin):
    """Save current project file"""

    label = "Save current file"
    order = pyblish.api.ExtractorOrder - 0.49
    hosts = ["clarisse"]
    families = ["*"]

    def process(self, context):
        projectfile = context.data['currentFile']
        assert projectfile

        self.log.info("Saving current project ..")
        ix.save(projectfile)
