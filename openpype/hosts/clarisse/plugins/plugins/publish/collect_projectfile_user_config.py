import os
import pyblish.api


from openpype.hosts.clarisse.api.pipeline import get_current_clarisseproject_fullpath


class CollectProjectFileConfig(pyblish.api.ContextPlugin):
    """Collect project local user config file"""

    order = pyblish.api.CollectorOrder + 0.4992
    label = "Collect Project Config File"
    hosts = ["clarisse"]

    def process(self, context):
        """Collect project config from user folder"""

        current_project_file = get_current_clarisseproject_fullpath()
        assert current_project_file
        workdir = os.environ.get("AVALON_WORKDIR")
        workdir_config_path = os.path.join(workdir, "overrides", "clarisse", "user_configs")
        config_name = "clarisse.cfg"

        destination_path = os.path.join(workdir_config_path, "{}".format(config_name))

        context.data['currentUserConfig'] = destination_path
        context.data['currentUserConfigFolder'] = workdir_config_path