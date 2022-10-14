import openpype.api
import pyblish.api
import ix


class ValidateWorkfilePaths(pyblish.api.InstancePlugin):
    """Validate workfile paths so they are absolute."""

    order = pyblish.api.ValidatorOrder
    families = ["workfile"]
    hosts = ["clarisse"]
    label = "Validate Workfile Paths"
    optional = True
    node_types = ["file", "alembic"]
    prohibited_vars = ["$PDIR"]

    def process(self, instance):
        # collect all filenames in the project

        # check for PDIRS

        # resolve pdirs to full paths
        pass