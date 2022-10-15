from openpype.pipeline import (
    load,
    get_representation_path
)
from openpype.hosts.clarisse.api.pipeline import imprint_container
from openpype.hosts.clarisse.api.lib import get_imports_context, create_import_contexts

import ix

class ReferenceLoader(load.LoaderPlugin):
    """Reference Camera into Clarisse"""

    label = "Reference Camera File"
    families = ["*"]
    representations = ["abc"]
    order = 0

    icon = "code-fork"
    color = "orange"

    def load(self, context, name=None, namespace=None, data=None):
        # todo: clarisse ix batch commands?

        filepath = self.fname

        # Command fails on unicode so we must force it to be strings
        # todo: can we do a better conversion, e.g. f.decode("utf8")
        filepath = str(filepath)

        # Create the file reference
        imports_context = str(get_imports_context()) + "/cameras"
        create_sub_contexts = create_import_contexts()

        node = ix.cmds.CreateFileReference(imports_context, [filepath])

        # Imprint it with some data so ls() can find this
        # particular loaded content and can return it as a
        # valid container
        imprint_container(
            node,
            name=name,
            namespace=namespace,
            context=context,
            loader=self.__class__.__name__
        )
        ix.application.check_for_events()


    def update(self, container, representation):
        node = container["node"]
        filepath = get_representation_path(representation)

        # Command fails on unicode so we must force it to be strings
        # todo: can we do a better conversion, e.g. f.decode("utf8")
        filepath = str(filepath)
        ix.cmds.SetReferenceFilename([node], filepath)

        # todo: do we need to explicitly trigger reload?
        # Update the representation id
        ix.cmds.SetValue("{}.openpype_representation[0]".format(node),
                         str(representation["_id"]))
        ix.application.check_for_events()

    def remove(self, container):
        node = container["node"]
        ix.cmds.DeleteItems([node.get_full_name()])
        ix.application.check_for_events()
