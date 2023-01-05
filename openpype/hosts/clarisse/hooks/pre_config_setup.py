import os
import glob

from openpype.lib import PreLaunchHook
from openpype.settings import (
    get_project_settings,
    get_anatomy_settings
)

allowed_overrides = ["global_default_render_config", "ocio", "users_config", "aov_configs","startup_project"]

SET_CONFIG_FILE_PATH = None
SET_OCIO_ENV_VAR = None
SET_USERS_CONFIG = None
SET_AOV_CONFIGS = None
SET_STARTUP_PROJECT = None

os.environ["CLARISSE_LOADED_CONFIG"] = ""

def get_clarisse_imageio_settings_project(project_name):
    return get_anatomy_settings(project_name)["imageio"]["clarisse"]

def get_clarisse_imageio_settings(project_name):
    return get_project_settings(project_name)


def show_env(launch_env=None):
    project_name = launch_env.env.get("AVALON_PROJECT")
    workdir = launch_env.env.get("AVALON_WORKDIR")
    print("OVERRIDES {}".format(project_name))

    for k in launch_env.env.keys():
        print(k, launch_env.env[k])

def get_overrides(launch_env=None, hostapp="clarisse"):
    """Get all allowed overrides from a loaded context
    """
    available_overrides = dict()

    project_name = launch_env.env.get("AVALON_PROJECT")
    workdir = launch_env.env.get("AVALON_WORKDIR")
    print("Get possible Overrides for project {} and task {}:".format(project_name, workdir))
    for subdir in glob.glob(workdir+"/*/"):
        if "overrides" in str(subdir) and os.path.isdir(str(subdir)):
            for check_app in glob.glob(str(subdir) + "/*/"):
                if hostapp in str(check_app) and os.path.isdir(str(check_app)):
                    for overridetype in glob.glob(str(check_app) + "/*/"):
                        for overtype in allowed_overrides:
                            if str(overtype) in str(overridetype):
                                available_overrides[str(overtype)] = overridetype

    return available_overrides



class PreConfigSetups(PreLaunchHook):
    """Clarisse OCIO and Config setup overrides

    From Clarisse docs:
    When enabling Use Ocio Config File while Ocio Config File field is empty,
    the application will automatically try to resolve the global variable $OCIO to look up for a configuration file.
    When Ocio Config File isn't empty the application ignores $OCIO even if it has been defined.
    """

    app_groups = ["clarisse"]

    def set_ocio(self, data):
        #  we always exepct a config to be named config.ocio and is present in the ocio folder
        config_file = os.path.normpath(data + os.sep + "config.ocio")

        if "clarisse-default" in self.load_config:
            print("OCIO Disabled.")
            os.environ["OCIO"] = ""
            self.launch_context.env["OCIO"] = ""

        else:
            if os.path.isfile(config_file):
                print("--- Seting up OCIO override for the task to {}".format(config_file))
                os.environ["OCIO"] = config_file
                self.launch_context.env["OCIO"] = str(config_file)
                print("--- NEW OCIO ENV VAR OVERRIDE SET TO {}".format(str(os.environ["OCIO"])))

    def unset_ocio(self):
        print("No overrides. Cleaning last task OCIO overrides. Setting up defaults.")
        import platform

        if "clarisse-default" in self.load_config:
            print("OCIO Disabled.")
            os.environ["OCIO"] = ""
            self.launch_context.env["OCIO"] = ""
        else:
            print("OCIO Enabled.")
            # print(get_anatomy_settings(project_name)["imageio"]["clarisse"]["workfile"]["customOCIOConfigPath"][str(platform.system().lower())][0])
            ocio_config_path = get_anatomy_settings(self.project_name)["imageio"]["clarisse"]["workfile"]["customOCIOConfigPath"][str(platform.system().lower())][0]
            os.environ["OCIO"] = str(ocio_config_path)
            self.launch_context.env["OCIO"] = str(ocio_config_path)

    def set_user_config(self, data):
        print("--- Seting up USER CONFIG override for the task {}".format(data))
        pass

    def unset_user_config(self):
        print("No overrides. Cleaning last task USER CONFIG overrides.")
        pass

    def set_global_config(self, data):
        print("--- Seting up Global Config override for the task {}".format(data))
        SET_CONFIG_FILE_PATH = os.path.normpath(data + os.sep + "clarisse_render_config.cfg").replace("\\","/")
        print("DEBUG SOURCE LAUNCH CONTEXT", self.launch_context)
        self.launch_context.launch_args += ["-config_file"]
        self.launch_context.launch_args += ["{}".format(SET_CONFIG_FILE_PATH)]
        print("MODED LAUNCH ARGUMENTS ADDED", self.launch_context.launch_args)
        self.launch_context.env["CLARISSE_LOADED_CONFIG"] = SET_CONFIG_FILE_PATH
        self.launch_context.clear_launch_args(self.launch_context.launch_args)

    def unset_global_config(self):
        os.environ["CLARISSE_LOADED_CONFIG"] = ""
        self.launch_context.env["CLARISSE_LOADED_CONFIG"] = ""
        print("No overrides. Cleaning last task GLOBAL CONFIG overrides.")


    def set_startup_project(self, data):
        print("--- Seting up override for the task {}".format(data))
        pass

    def unset_startup_project(self):
        print("No overrides. Cleaning last task STARTUP PROJECT overrides.")
        pass

    def set_aov_configs(self, data):
        print("--- Seting up override for the task {}".format(data))
        pass

    def unset_aov_configs(self):
        print("No overrides. Cleaning last task AOV CONFIG overrides.")
        pass


    def set_config_type(self, override_type, override_data):
        """Sets override type"""
        overtypes = {
            "ocio": self.set_ocio,
            "users_config": self.set_user_config,
            "global_default_render_config": self.set_global_config,
            "aov_configs": self.set_aov_configs,
            "startup_project": self.set_startup_project
        }

        return overtypes[override_type](override_data)


    def unset_config_type(self, override_type):
        """Sets override type"""
        overtypes = {
            "ocio": self.unset_ocio,
            "users_config": self.unset_user_config,
            "global_default_render_config": self.unset_global_config,
            "aov_configs": self.unset_aov_configs,
            "startup_project": self.unset_startup_project
        }

        return overtypes[override_type]()

    def execute(self):
        self.log.info("PRE-SETUP CLARISSE CONFIGS HOOK")

        self.project_name = self.launch_context.env.get("AVALON_PROJECT")
        self.load_config = get_anatomy_settings(self.project_name)["imageio"]["clarisse"]["workfile"]["OCIO_config"]
        # first we unset all setup, this is needed cos the env seems to be persitent and not cleaned
        # in openpype
        print("Unsetting all in setup.")
        for unset_override in allowed_overrides:
            self.unset_config_type(unset_override)

        #  now we setup all we need again
        overrides = get_overrides(launch_env=self.launch_context)

        print("Running setup.")
        for override in overrides.keys():
            # print("Working on {} -- {}".format(override, overrides[override]))
            self.set_config_type(override, overrides[override])

