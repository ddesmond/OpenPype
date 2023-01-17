import os
from pprint import pformat
import pyblish.api

from openpype.hosts.clarisse.api.exports import run_export_context, create_check_dirs
from openpype.pipeline import publish



class ExtractClarisseExportContextOutput(publish.Extractor):

    order = pyblish.api.ExtractorOrder
    label = "Extract Clarisse Project from Context"
    hosts = ["clarisse"]
    families = ["refcontext"]

    def process(self, instance):
        import ix
        self.log.info("instance.data: `{}`".format(
            pformat(instance.data)))

        selctx = str(instance.data["clarisse_ref_context"])
        ctx_filename = instance.data["export_filename"]
        create_check_dirs()

        run_export_context(ctx_select=selctx,filename=ctx_filename)

        assert os.path.isfile(ctx_filename)

        folder, file = os.path.split(ctx_filename)
        filename, ext = os.path.splitext(file)

        representation = {
            "name": ext.lstrip("."),
            "ext": ext.lstrip("."),
            "files": file,
            "stagingDir": folder,
        }

        if "representations" not in instance.data:
            instance.data["representations"] = []

        instance.data["representations"].append(representation)