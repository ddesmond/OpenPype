import os
import pyblish.api

from openpype.hosts.clarisse.api.config_manager import copy_user_config
from openpype.hosts.clarisse.api.pipeline import get_current_clarisseproject


class IntergateUserConfigFile(pyblish.api.ContextPlugin):
    """Copy project local user config file to a context location
    so Deadline can load it"""

    order = pyblish.api.IntegratorOrder - 0.11
    label = "Copy Current Project Config File"
    hosts = ["clarisse"]

    def process(self, context):
        """Copy project config from user folder to task overrides folder"""


        if os.environ.get("CLARISSE_LOADED_CONFIG"):
            print("Global configuration is set. No integration for preferences.")
            print("Reusing the global prefs path.")
            context.data["currentUserConfig"] = os.environ.get("CLARISSE_LOADED_CONFIG")
            context.data["finalUserConfigFile"] = os.environ.get("CLARISSE_LOADED_CONFIG")

        else:
            from datetime import datetime
            todays_date = "{:%Y_%m_%d}".format(datetime.now())

            print("Global configuration is NOT set. Integrating preferences file.")
            destination_path_temp = context.data['currentUserConfig']
            project_file_name = get_current_clarisseproject()
            destination_path = destination_path_temp.replace("clarisse.cfg", str(todays_date + "_clarisse.cfg"))
            workdir_config_path = context.data['currentUserConfigFolder']

            try:
                os.makedirs(workdir_config_path)
            except:
                pass

            copy_user_config(destination_path=destination_path)
            context.data['finalUserConfigFile'] = destination_path