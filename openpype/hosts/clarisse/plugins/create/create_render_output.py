import ix

from openpype.hosts.clarisse.api.pipeline import imprint
from openpype.pipeline.context_tools import get_current_project_asset
from openpype.pipeline.create import (
    LegacyCreator
)

class CreateRenderOutput(LegacyCreator):
    """Creates an image with a layer set ready for render"""

    label = "Create a Render Output"
    family = "render"
    identifier = "render_layer"
    icon = "sign-out"
    defaults = ["Main"]

    def __init__(self, *args, **kwargs):
        super(CreateRenderOutput, self).__init__(*args, **kwargs)

        # Remove the active, we are checking the bypass flag of the nodes
        self.data.pop("active", None)

        # Set node type to create for output
        self.data.update({"node_type": "render_layer"})

    def process(self):
        """Creator main entry point.

        Args:
            instance (pyImage): selected Image layer

        """
        filename = "$PDIR/pyblish/{}.####.exr".format(str(self.name))
        ix.log_info("SETUP PATH is {}".format(filename))

        asset_doc = get_current_project_asset()
        asset_data = asset_doc["data"]

        frame_start = str(asset_data.get(
            "frameStart",
            asset_data.get("edit_in")))

        frame_end = str(asset_data.get(
            "frameEnd",
            asset_data.get("edit_out")))


        clarisse_image = ix.cmds.CreateObject("render_shot", "Image", "Global", "build://project/scene")

        layer_shot = ix.cmds.AddLayer(str(clarisse_image) + ".layers", "Layer3d")
        newnamed = ix.cmds.RenameItem(str(clarisse_image) + ".layer_3d", self.name)
        render_layer = str(clarisse_image) + "." + str(newnamed)
        rlayer = ix.get_item(render_layer)
        rlayer.attrs.render_to_disk = True
        rlayer.attrs.save_as = filename

        rlayer.attrs.first_frame = frame_start
        rlayer.attrs.last_frame = frame_end
        #  setup some options
        # set DWAB compression
        rlayer.attrs.open_exr_output_compression_mode = "10"


        for d in self.data.keys():
            print(d, self.data[d])

        imprint(rlayer, self.data, group="openpype")
