import os
import tempfile

from openpype.lib import get_ffmpeg_tool_path, path_to_subprocess_arg, run_subprocess
from openpype.pipeline import publish



class ExtractClarisseRenderThumbnail(publish.Extractor):
    """Extract render layer thumbnail.
    """

    label = "Extract Thumbnail from Render"
    hosts = ["clarisse"]
    families = ["render", "review"]

    def process(self, instance):
        self.log.info("Extracting thumbnail...")

        dst_staging = tempfile.mkdtemp(prefix="pyblish_clarisse_tmp_")
        self.log.debug(
            "Create temp directory {} for thumbnail".format(dst_staging)
        )

        # Store new staging to cleanup paths
        instance.context.data["cleanupFullPaths"].append(dst_staging)

        file_name = instance.data["path"]
        tail, head = os.path.split(file_name)
        head_jpg = head.replace("exr", "jpg")


        if not int(instance.data["frameEnd"]) in [1001, 1002]:
            self.log.info("Extracting thumbnai from sequence.")
            mid_frame_middle = int(int(instance.data["frameEnd"]) - int(instance.data["frameStart"])) / 2
            mid_frame = int(int(instance.data["frameStart"]) + mid_frame_middle)
        else:
            self.log.info("Extracting thumbnai from single frame.")
            mid_frame = int(instance.data["frameStart"])

        file_frame = head.replace("####", str(mid_frame))
        file_frame_jpg = head_jpg.replace("####", str(mid_frame))
        file_frame_path_for_thumb = os.path.join(tail, file_frame)
        file_frame_output_file = str(os.path.join(dst_staging, file_frame_jpg))

        #  process exr to jpg
        ffmpeg_path = get_ffmpeg_tool_path("ffmpeg")

        jpeg_items = [
            path_to_subprocess_arg(ffmpeg_path),
            # override file if already exists
            "-y"
        ]

        # input file
        jpeg_items.extend([
            "-i", path_to_subprocess_arg(file_frame_path_for_thumb),
            # extract only single file
            "-frames:v", "1",
            # Add black background for transparent images
            "-filter_complex", (
                "\"color=black,format=rgb24[c]"
                ";[c][0]scale2ref[c][i]"
                ";[c][i]overlay=format=auto:shortest=1,setsar=1\""
            ),
        ])


        # output file
        jpeg_items.append(path_to_subprocess_arg(file_frame_output_file))

        subprocess_jpeg = " ".join(jpeg_items)

        # run subprocess
        self.log.debug("Executing: {}".format(subprocess_jpeg))
        run_subprocess(
            subprocess_jpeg, shell=True, logger=self.log
        )

        if "representations" not in instance.data:
            instance.data["representations"] = []

        representation = {
            "name": "thumbnail",
            "ext": "jpg",
            "files": file_frame_jpg,
            "stagingDir": dst_staging,
            "thumbnail": True
        }
        instance.data["representations"].append(representation)
