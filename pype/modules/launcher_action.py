from . import PypeModule, ITrayAction


class LauncherAction(PypeModule, ITrayAction):
    label = "Launcher"
    name = "launcher_tool"

    def initialize(self, _modules_settings):
        # This module is always enabled
        self.enabled = True

        # Tray attributes
        self.window = None

    def tray_init(self):
        self.create_window()

    def tray_start(self):
        # Register actions
        from pype.tools.launcher import actions
        # actions.register_default_actions()
        actions.register_config_actions()
        actions_paths = self.manager.collect_plugin_paths()["actions"]
        actions.register_actions_from_paths(actions_paths)
        actions.register_environment_actions()

    def connect_with_modules(self, _enabled_modules):
        return

    def create_window(self):
        if self.window:
            return
        from pype.tools.launcher import LauncherWindow
        self.window = LauncherWindow()

    def on_action_trigger(self):
        self.show_launcher()

    def show_launcher(self):
        if self.window:
            self.window.show()
            self.window.raise_()
            self.window.activateWindow()
