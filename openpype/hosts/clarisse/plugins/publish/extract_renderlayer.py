import os
from pprint import pformat
import pyblish.api

from openpype.pipeline import publish

class ExtractClarisseRenderLayer(publish.Extractor):

    order = pyblish.api.ExtractorOrder
    label = "Clarisse Extract Render Layer"
    hosts = ["clarisse"]
    families = ["render", "review"]

    def process(self, instance):

        file_name = instance.data["path"]
        tail, head = os.path.split(file_name)
        file_names = []
        staging_dir = tail
        for i in range(instance.data["frameStart"], instance.data["frameEnd"],1):
            file_frame = head.replace("####", str(i))
            file_names.append(file_frame)

        assert len(file_names) != 0
        print("I have {} files.".format(str(len(file_names))))

        subset = instance.data["subset"]
        extension = "exr"

        self.log.info("instance.data: `{}`".format(
            pformat(instance.data)))

        if "representations" not in instance.data:
            instance.data["representations"] = []

        representation = {
            "name": extension,
            "ext": extension,
            "files": file_names,
            "stagingDir": staging_dir,
        }

        instance.data["representations"].append(representation)