import os
import sys

# we need to add back vendors
sys.path.insert(0, os.path.join(os.getenv("OPENPYPE_ROOT"), "vendor", "python"))

from openpype.pipeline import install_host
from openpype.hosts.clarisse.api import ClarisseHost

import ix

host = ClarisseHost()
install_host(host)

ix.log_info("OpenPype Clarisse integration installed.")



def load_legacy_python():
    # inject legacy DFM python stuff so its accesible
    additional_paths = []
    for add_path in additional_paths:
        sys.path.append(add_path)
        ix.log_info("Loaded Legacy Python path {}".format(add_path))


def load_tools_paths():
    # inject additional tools from anydccs or other location
    additional_paths = []
    for add_path in additional_paths:
        sys.path.append(add_path)
        ix.log_info("Loaded additional path {}".format(add_path))


def run_startup_create_menus():
    #  run the separate startup config to setup Menus
    # custom create menu can go here
    # for your additiona tools
    print("Menus function on startup not running anything.")
    pass


def run_startup_create_shelf():
    #  run the separate startup config to setup shelf
    print("Shelf function on startup not running anything.")
    print("IX_SHELF_CONFIG_FILE Values", os.getenv("IX_SHELF_CONFIG_FILE"))


# setup rundown for host config
def rundown():
    #  runs default setup to run Clarisse in its environment
    try:
        load_legacy_python()
        load_tools_paths()
        run_startup_create_menus()
        run_startup_create_shelf()
        ix.log_info("Rundown complete.")

    except Exception as RundownError:
        ix.log_error(RundownError)


if __name__ == "__main__":
    rundown()