import os
import ix

from openpype.hosts.clarisse.api.exports import export_context_project
from openpype.hosts.clarisse.api.lib import get_export_context, create_exports_contexts
from openpype.hosts.clarisse.api.pipeline import imprint
from openpype.pipeline.create import (
    LegacyCreator
)


class CreateContextProjectOutput(LegacyCreator):
    """Bake a context into a project file"""

    label = "Clarisse Context to project file"
    family = "refcontext"
    icon = "magic"
    defaults = ["Main"]

    def __init__(self, *args, **kwargs):
        super(CreateContextProjectOutput, self).__init__(*args, **kwargs)


    def process(self):
        _app = ix.application
        if _app.get_selection().get_count() > 0:
            item = _app.get_selection().get_item(0)
            if item.is_context():
                context_selected = item.to_context()
                if context_selected:

                    pdir = ix.application.get_factory().get_vars().get("PDIR").get_string()
                    export_context = get_export_context()
                    create_sub_contexts = create_exports_contexts()

                    node = export_context_project(creator_type="context", selection=str(context_selected), pdir=pdir)
                    imprint(node, self.data, group="openpype")




