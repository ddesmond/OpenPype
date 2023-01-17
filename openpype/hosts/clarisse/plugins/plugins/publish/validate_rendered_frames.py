import os
import pyblish.api

from openpype.pipeline.publish import (
    ValidateContentsOrder,
)


class ValidateFrameRange(pyblish.api.InstancePlugin):
    """Validates the rendered frames on disk.
    This is an OPTIONAL Validator and can be turned off in the publisher window.

    It will check if the actual rendered frame exists in the location.

    """

    label = "Validate Rendered Frames On Disk"
    order = ValidateContentsOrder
    families = ["render",
                "review"]
    optional = True


    def process(self, instance):
        path_render = instance.data["path"]
        failed_frames = []
        for i in range(instance.data["frameStart"], instance.data["frameEnd"],1):
            file_frame = path_render.replace("####", str(i))

            if not os.path.isfile(file_frame):
                failed_frames.append(file_frame)

        if not len(failed_frames) == 0:
            raise RuntimeError("There are missing frames {}".format(failed_frames))



