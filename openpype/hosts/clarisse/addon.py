import os
from openpype.modules import OpenPypeModule
from openpype.modules.interfaces import IHostAddon

CLARISSE_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class ClarisseAddon(OpenPypeModule, IHostAddon):
    name = "clarisse"
    host_name = "clarisse"

    def initialize(self, module_settings):
        self.enabled = True

    def add_implementation_envs(self, env, app):
        """Modify environments to contain all required for implementation."""

        startup_script = os.path.join(CLARISSE_ROOT_DIR,
                                      "startup",
                                      "startup.py")
        env["CLARISSE_STARTUP_SCRIPT"] = startup_script

        # Set default environments if are not set via settings
        defaults = {
            "OPENPYPE_LOG_NO_COLORS": "True"
        }
        for key, value in defaults.items():
            if not env.get(key):
                env[key] = value

    def get_launch_hook_paths(self, app):
        if app.host_name != self.host_name:
            return []
        return [
            os.path.join(CLARISSE_ROOT_DIR, "hooks")
        ]

    def get_workfile_extensions(self):
        return [".project"]
