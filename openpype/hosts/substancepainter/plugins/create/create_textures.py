# -*- coding: utf-8 -*-
"""Creator plugin for creating textures."""

from openpype.pipeline import CreatedInstance, Creator
from openpype.lib import (
    EnumDef,
    UILabelDef,
    NumberDef
)

from openpype.hosts.substancepainter.api.pipeline import (
    set_project_metadata,
    get_project_metadata
)
from openpype.hosts.substancepainter.api.lib import get_export_presets

import substance_painter.project


class CreateTextures(Creator):
    """Create a texture set."""
    identifier = "io.openpype.creators.substancepainter.textureset"
    label = "Textures"
    family = "textureSet"
    icon = "picture-o"

    default_variant = "Main"

    def create(self, subset_name, instance_data, pre_create_data):

        if not substance_painter.project.is_open():
            return

        instance = self.create_instance_in_context(subset_name, instance_data)
        set_project_metadata("textureSet", instance.data_to_store())

    def collect_instances(self):
        workfile = get_project_metadata("textureSet")
        if workfile:
            self.create_instance_in_context_from_existing(workfile)

    def update_instances(self, update_list):
        for instance, _changes in update_list:
            # Update project's metadata
            data = get_project_metadata("textureSet") or {}
            data.update(instance.data_to_store())
            set_project_metadata("textureSet", data)

    def remove_instances(self, instances):
        for instance in instances:
            # TODO: Implement removal
            # api.remove_instance(instance)
            self._remove_instance_from_context(instance)

    # Helper methods (this might get moved into Creator class)
    def create_instance_in_context(self, subset_name, data):
        instance = CreatedInstance(
            self.family, subset_name, data, self
        )
        self.create_context.creator_adds_instance(instance)
        return instance

    def create_instance_in_context_from_existing(self, data):
        instance = CreatedInstance.from_existing(data, self)
        self.create_context.creator_adds_instance(instance)
        return instance

    def get_instance_attr_defs(self):

        return [
            EnumDef("exportPresetUrl",
                    items=get_export_presets(),
                    label="Output Template"),
            EnumDef("exportFileFormat",
                    items={
                        None: "Based on output template",
                        # TODO: implement extensions
                    },
                    default=None,
                    label="File type"),
            EnumDef("exportSize",
                    items={
                        None: "Based on each Texture Set's size",
                        #  The key is size of the texture file in log2.
                        #  (i.e. 10 means 2^10 = 1024)
                        7: "128",
                        8: "256",
                        9: "512",
                        10: "1024",
                        11: "2048",
                        12: "4096"
                    },
                    default=None,
                    label="Size"),

            EnumDef("exportPadding",
                    items={
                        "passthrough": "No padding (passthrough)",
                        "infinite": "Dilation infinite",
                        "transparent": "Dilation + transparent",
                        "color": "Dilation + default background color",
                        "diffusion": "Dilation + diffusion"
                    },
                    default="infinite",
                    label="Padding"),
            NumberDef("exportDilationDistance",
                      minimum=0,
                      maximum=256,
                      decimals=0,
                      default=16,
                      label="Dilation Distance"),
            UILabelDef("*only used with "
                       "'Dilation + <x>' padding"),
        ]

    def get_pre_create_attr_defs(self):
        # Use same attributes as for instance attributes
        return self.get_instance_attr_defs()
