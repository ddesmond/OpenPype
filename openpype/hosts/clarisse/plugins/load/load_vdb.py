from openpype.pipeline import (
    load,
    get_representation_path
)
from openpype.hosts.clarisse.api.pipeline import imprint_container
from openpype.hosts.clarisse.api.lib import get_imports_context, create_import_contexts

import ix

class VDBLoader(load.LoaderPlugin):
    """Reference VDB content into Clarisse"""

    label = "Reference VDB File"
    families = ["*"]
    representations = ["vdb"]
    order = 0

    icon = "code-fork"
    color = "orange"

    def load(self, context, name=None, namespace=None, data=None):
        # todo: clarisse ix batch commands?

        filepath = self.fname

        # Command fails on unicode so we must force it to be strings
        # todo: can we do a better conversion, e.g. f.decode("utf8")
        filepath = str(filepath)

        # take care of import contexts
        imports_context = str(get_imports_context()) + "/volumes"
        create_sub_contexts = create_import_contexts()

        node_name = "{}_{}".format(namespace, name) if namespace else name
        namespace = namespace if namespace else context["asset"]["name"]

        # Create the file reference
        node = ix.cmds.CreateObject(namespace, "GeometryVolumeFile", "Global", imports_context)
        ix.cmds.SetValues([str(node) + ".filename[0]"], [str(filepath)])

        # set trigger to check if sequence
        node.call_action("detect_sequence")

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
        ix.cmds.SetValues([str(node)+".filename[0]"], [str(filepath)])

        # todo: do we need to explicitly trigger reload?
        # Update the representation id
        ix.cmds.SetValues([str("{}.openpype_representation[0]".format(node))],
                          [str(representation["_id"])])
        ix.application.check_for_events()

    def remove(self, container):
        node = container["node"]
        ix.cmds.DeleteItems([node.get_full_name()])
        ix.application.check_for_events()
