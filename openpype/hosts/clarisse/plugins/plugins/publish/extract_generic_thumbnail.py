import os
import pyblish.api

from openpype.hosts.clarisse.api.pipeline import get_current_clarisseproject_fullpath
from openpype.pipeline import publish, registered_host


class ExtractGenericThumbnail(publish.Extractor):
    """Workfile Extract Generic thumbnail if none is present.
    This usualy works for workfiles and alikes where there
    are no preview or render thumbnails.
    """

    label = "Set a Generic Thumbnail"
    hosts = ["clarisse"]
    families = ["workfile","refcontext"]
    order = pyblish.api.ExtractorOrder - 0.00001


    def _instance_has_thumbnail(self, instance):
        if "representations" not in instance.data:
            self.log.warning(
                "Instance does not have 'representations' key filled"
            )
            instance.data["representations"] = []

        for repre in instance.data["representations"]:
            if repre["name"] == "thumbnail":
                return True
        return False

    def process(self, instance):
        self.log.info("Checking for source thumbnail representation.")

        where_the_generic_thumbs_are = os.path.join(os.getenv("OP_PIPELINE_ROOT"), "code", "generic_thumbnails", "extensions")

        thumbnail_source = instance.data.get("thumbnailSource")
        if not thumbnail_source:
            self.log.debug("Thumbnail source representation not filled. Creating a generic thumbnail.")


            dst_filename = "project.png"
            new_repre = {
                "name": "thumbnail",
                "ext": "png",
                "files": dst_filename,
                "stagingDir": where_the_generic_thumbs_are,
                "thumbnail": True,
                "tags": ["thumbnail"]
            }

            # adding representation
            self.log.debug(
                "Adding generic thumbnail representation: {}".format(new_repre)
            )
            if "representations" not in instance.data:
                instance.data["representations"] = []

            instance.data["representations"].append(new_repre)
            instance.data["thumbnailPath"] = where_the_generic_thumbs_are
            self.log.debug("Generic thumbnail representation created.")

