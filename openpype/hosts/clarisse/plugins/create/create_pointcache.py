import ix

from openpype.hosts.clarisse.api.exports import export_context_alembic
from openpype.hosts.clarisse.api.lib import get_export_context, create_exports_contexts, get_selected_context
from openpype.hosts.clarisse.api.pipeline import imprint
from openpype.pipeline.create import (
    LegacyCreator
)


class CreateContextOutputCacheModel(LegacyCreator):
    """Export contexted geometry to a cache file"""

    label = "Create Cache from a Context with geometry"
    defaults = ["Main"]
    family = "model"
    icon = "gears"

    def __init__(self, *args, **kwargs):
        super(CreateContextOutputCacheModel, self).__init__(*args, **kwargs)


    def process(self):
        # get user selection, it has to be a context
        ctx_select = get_selected_context()
        assert ctx_select

        config_export = {
                            "transfer_source_data": 1,
                            "write_one_frame_per_file": 0,
                            "export_combiners": 1,
                            "export_scatterers": 1,
                            "scatterer_export_mode": 1,
                            "export_properties": 1,
                            "compatibility_mode": 2,
                            "fill_sparse_properties": 1,
                            "promote_to_geometry_parameter": 1,
                            "bake_indexed_properties": 1
                        }

        export_context = get_export_context()
        create_sub_contexts = create_exports_contexts()

        # check for proper context selection
        node = export_context_alembic(creator_type="geometry",
                                      selection=ctx_select,
                                      config_context_export=config_export)

        imprint(node, self.data, group="openpype")



