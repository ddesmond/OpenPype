import ix

from openpype.pipeline.create import (
    LegacyCreator
)

class CreateRenderOutput(LegacyCreator):
    """Creates an image with a layer set ready for render"""

    label = "Render Layer"
    family = "render"
    icon = "sign-out"
    defaults = ["Main"]

    def __init__(self, *args, **kwargs):
        super(CreateRenderOutput, self).__init__(*args, **kwargs)

        # Remove the active, we are checking the bypass flag of the nodes
        self.data.pop("active", None)

        # Set node type to create for output
        self.data.update({"node_type": "alembic"})

    def _process(self, instance):
        """Creator main entry point.

        Args:
            instance (pyImage): selected Image layer

        """
        print("INSTANCE DATA", instance)
        filename = "$PDIR/pyblish/{}.exr".format(str(self.name))
        ix.log_info("SETUP PATH is {}".format(filename))

        # TODO write render layer creation
        pass



