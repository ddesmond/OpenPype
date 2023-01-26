from openpype.lib import PreLaunchHook



class PreDebugHook(PreLaunchHook):
    """DEBUG hook for clarisse
    """
    app_groups = ["clarisse"]

    def show_env(launch_env=None):
        project_name = launch_env.env.get("AVALON_PROJECT")
        workdir = launch_env.env.get("AVALON_WORKDIR")
        print("OVERRIDES {}".format(project_name))

        for k in launch_env.env.keys():
            print(k, launch_env.env[k])

    def execute(self):
        project_name = self.launch_context.env.get("AVALON_PROJECT")
        workdir = self.launch_context.env.get("AVALON_WORKDIR")
        if not workdir:
            self.log.warning("BUG: Workdir is not filled.")
            return

        self.log.info("OpenPype: Setting up config files")
        self.log.info("Workdir {}".format(workdir))
        self.log.info("Project name {}".format(project_name))

