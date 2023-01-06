from openpype.pipeline import (
    load,
    get_representation_path
)
from openpype.hosts.clarisse.api.pipeline import imprint_container
from openpype.hosts.clarisse.api.lib import get_imports_context, create_import_contexts

import ix

class WorkfileReferenceLoader(load.LoaderPlugin):
    """Reference project file into Clarisse"""

    label = "Reference File"
    families = ["workfile"]
    representations = ["project"]
    order = 0

    icon = "code-fork"
    color = "orange"

    def load(self, context, name=None, namespace=None, data=None):
        filepath = self.fname

        # Command fails on unicode so we must force it to be strings
        filepath = str(filepath)

        # Create the file reference
        imports_context = str(get_imports_context()) + "/projects"

        create_sub_contexts = create_import_contexts()

        node_name = "{}_{}".format(namespace, name) if namespace else name
        namespace = namespace if namespace else context["asset"]["name"]
        node = ix.cmds.CreateFileReference(imports_context, [filepath])
        ix.cmds.RenameItem(str(node),
                           namespace)

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
        filepath = str(filepath)
        ix.cmds.SetReferenceFilename([node], filepath)

        # Update the representation id
        ix.cmds.SetValues([str("{}.openpype_representation[0]".format(node))],
                          [str(representation["_id"])])
        ix.application.check_for_events()


    def remove(self, container):
        node = container["node"]
        ix.cmds.DeleteItems([node.get_full_name()])
        ix.application.check_for_events()
