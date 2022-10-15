import os
import ix
import pyblish.api

from openpype.hosts.clarisse.api.lib import gather_all_images, gather_all_layers_from_image


class CollectInstances(pyblish.api.ContextPlugin):
    """Collect Clarisse render instances

    """

    order = pyblish.api.CollectorOrder
    label = "Collect Instances"
    hosts = ["clarisse"]


    def attribute_collect(self, layer3d):
        collection_attrib_values = {}
        """get a list of attributes from clarisse layer3d"""

        collect_layer3d_attribs = [
            "render_to_disk",
            "save_as",
            "first_frame",
            "last_frame",
            "frame_step",
            "format",
            "LUT",
            "open_exr_output_compression_mode",
            "enable_deep_output",
            "save_deep_data_as",
            "pixel_aspect_ratio"]

        collected_attributes = {}
        for att in collect_layer3d_attribs:
            # print att, layer3d.get_attribute(att)[0]
            collection_attrib_values[att] = layer3d.get_attribute(att)[0]

        return collection_attrib_values

    def process(self, context):
        print("CLARISSE COLLECTING INSTANCES")
        all_images = gather_all_images()
        for d in context.data:
            print(d, context.data[d])
        for found_image in all_images:
            collected_layers = gather_all_layers_from_image(image=found_image)

            for layer in collected_layers:
                full_name_path = str(layer).split(".")[-1]

                layer_data = self.attribute_collect(layer)
                if layer_data["render_to_disk"]:
                    active = True
                else:
                    active = False

                instance = context.create_instance(str(layer))

                instance.data.update({
                    "asset": os.environ["AVALON_ASSET"],  # todo: not a constant
                    "subset": "default",
                    "path": layer_data["save_as"],
                    "outputDir": os.path.dirname(layer_data["save_as"]),
                    "ext": "exr",  # todo: should be redundant
                    "label": full_name_path,
                    "frameStart": layer_data["first_frame"],
                    "frameEnd": layer_data["last_frame"],
                    "fps": context.data["fps"],
                    "families": ["render", "review"],
                    "family": "render",
                    "active": active,
                    "publish": active  # backwards compatibility
                })

                instance.append(layer)



        # Sort/grouped by family (preserving local index)
        context[:] = sorted(context, key=self.sort_by_family)

        return context

    def sort_by_family(self, instance):
        """Sort by family"""
        return instance.data.get("families", instance.data.get("family"))
