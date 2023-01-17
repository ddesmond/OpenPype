import ix

from openpype.hosts.clarisse.api.exports import export_context_alembic
from openpype.hosts.clarisse.api.lib import get_export_context, create_exports_contexts, get_selected_context
from openpype.hosts.clarisse.api.pipeline import imprint
from openpype.pipeline.create import (
    LegacyCreator
)


class CreateContextOutputCamera(LegacyCreator):
    """Export contexted camera to file"""

    label = "Export Camera"
    defaults = ["Main"]
    family = "camera"
    icon = "video-camera"

    def __init__(self, *args, **kwargs):
        super(CreateContextOutputCamera, self).__init__(*args, **kwargs)


    def process(self):
        # get user selection, it has to be a context
        ctx_select = get_selected_context()
        assert ctx_select

        config_export = {
                            "transfer_source_data": 0,
                            "write_one_frame_per_file": 0,
                            "export_combiners": 0,
                            "export_scatterers": 0,
                            "scatterer_export_mode": 0,
                            "export_properties": 1,
                            "compatibility_mode": 2,
                            "fill_sparse_properties": 0,
                            "promote_to_geometry_parameter": 0,
                            "bake_indexed_properties": 0
                        }

        export_context = get_export_context()
        create_sub_contexts = create_exports_contexts()

        # check for proper context selection
        node = export_context_alembic(creator_type="camera",
                                      selection=ctx_select,
                                      config_context_export=config_export)

        imprint(node, self.data, group="openpype")



