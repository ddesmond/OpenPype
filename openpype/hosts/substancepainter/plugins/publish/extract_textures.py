from openpype.pipeline import KnownPublishError, publish
import substance_painter.export


class ExtractTextures(publish.Extractor):
    """Extract Textures using an output template config.

    Note:
        This Extractor assumes that `collect_textureset_images` has prepared
        the relevant export config and has also collected the individual image
        instances for publishing including its representation. That is why this
        particular Extractor doesn't specify representations to integrate.

    """

    label = "Extract Texture Set"
    hosts = ['substancepainter']
    families = ["textureSet"]

    # Run before thumbnail extractors
    order = publish.Extractor.order - 0.1

    def process(self, instance):

        config = instance.data["exportConfig"]
        result = substance_painter.export.export_project_textures(config)

        if result.status != substance_painter.export.ExportStatus.Success:
            raise KnownPublishError(
                "Failed to export texture set: {}".format(result.message)
            )

        for (texture_set_name, stack_name), maps in result.textures.items():
            # Log our texture outputs
            self.log.info(f"Processing stack: {texture_set_name} {stack_name}")
            for texture_map in maps:
                self.log.info(f"Exported texture: {texture_map}")

            # TODO: Confirm outputs match what we collected
            # TODO: Confirm the files indeed exist
            # TODO: make sure representations are registered

        # Add a fake representation which won't be integrated so the
        # Integrator leaves us alone - otherwise it would error
        # TODO: Add `instance.data["integrate"] = False` support in Integrator?
        instance.data["representations"] = [
            {
                "name": "_fake",
                "ext": "_fake",
                "delete": True,
                "files": []
            }
        ]
