import ix


class CreateUSDOutput():
    """Bake a context into alembic
    no shading will be exported, just geometry"""

    label = "USD export"
    family = "usd"
    icon = "magic"
    defaults = ["Main"]

    def __init__(self, *args, **kwargs):
        super(CreateUSDOutput, self).__init__(*args, **kwargs)

        # Remove the active, we are checking the bypass flag of the nodes
        self.data.pop("active", None)

        # Set node type to create for output
        self.data.update({"node_type": "usd"})

    def _process(self, instance):
        """Creator main entry point.

        Args:
            instance (pyContext): selected context

        """

        filename = "$PDIR/pyblish/%s.usd" % self.name

        # TODO write usd exporter
        pass




