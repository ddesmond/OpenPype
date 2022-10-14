import pyblish.api


class CollectInstances(pyblish.api.ContextPlugin):
    """Collect Clarisse render instances

    """

    order = pyblish.api.CollectorOrder
    label = "Collect Instances"
    hosts = ["clarisse"]

    def process(self, context):

        # Sort/grouped by family (preserving local index)
        context[:] = sorted(context, key=self.sort_by_family)

        return context

    def sort_by_family(self, instance):
        """Sort by family"""
        return instance.data.get("families", instance.data.get("family"))
