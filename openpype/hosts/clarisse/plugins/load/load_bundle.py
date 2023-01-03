import os.path

from openpype.pipeline import (
    load,
    get_representation_path
)
from openpype.hosts.clarisse.api.pipeline import imprint_container
from openpype.hosts.clarisse.api.lib import get_imports_context, create_import_contexts

import ix

class BundleLoader(load.LoaderPlugin):
    """Reference content into Clarisse Bundle"""

    label = "Bundle File"
    families = ["*"]
    representations = ["abc", "usd", "usda", "usdc"]
    order = 0

    icon = "code-fork"
    color = "orange"

    def load(self, context, name=None, namespace=None, data=None):

        filepath = str(self.fname)
        filename, extension = os.path.basename(filepath).rsplit('.', 1)

        # Create the file reference
        imports_context = str(get_imports_context()) + "/geometry"
        create_sub_contexts = create_import_contexts()

        node_name = "{}_{}".format(namespace, name) if namespace else name
        namespace = namespace if namespace else context["asset"]["name"]

        if extension == 'abc':
            node = ix.cmds.CreateObject(namespace + "_bndl", "GeometryBundleAlembic", "Global", imports_context)
            ix.cmds.SetValues([str(node) + ".filename[0]"], [str(filepath)])

        elif extension in ["usd", "usda", "usdc"]:
            node = ix.cmds.CreateObject(namespace + "_bndl", "GeometryBundleUsd", "Global", imports_context)
            ix.cmds.SetUsdBundleFilename([str(node) + ".filename[0]"], [str(filepath)], [0])

        else:
            return


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

        filename, extension = os.path.basename(filepath).rsplit('.', 1)

        if extension == 'abc':
            ix.cmds.SetValues([str(node) + ".filename[0]"], [str(filepath)])

        elif extension in ["usd", "usda", "usdc"]:
            ix.cmds.SetUsdBundleFilename([str(node) + ".filename[0]"], [str(filepath)], [0])

        else:
            return

        # Update the representation id
        ix.cmds.SetValues([str("{}.openpype_representation[0]".format(node))],
                          [str(representation["_id"])])
        ix.application.check_for_events()

    def remove(self, container):
        node = container["node"]
        ix.cmds.DeleteItems([node.get_full_name()])
        ix.application.check_for_events()
