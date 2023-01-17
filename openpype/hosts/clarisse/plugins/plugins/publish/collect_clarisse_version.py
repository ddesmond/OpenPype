import ix
import pyblish.api


class CollectClarisseVersion(pyblish.api.ContextPlugin):
    """Collect running clarisse version"""

    order = pyblish.api.CollectorOrder
    label = "Collect Clarisse Version"
    hosts = ["clarisse"]

    def process(self, context):
        """Collect running clarisse version and service pack"""
        version = str(ix.application.get_version())
        context.data["clarisseVersion"] = version
        self.log.info("Clarisse version: %s" % version)
