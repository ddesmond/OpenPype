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


#  these needs to removed from this file, the startup  loader needs to be separated
#  from the studio wide config

def load_legacy_python():
    # inject legacy DFM python stuff so its accesible
    additional_paths = []
    if len(additional_paths) != 0:
        for add_path in additional_paths:
            sys.path.append(add_path)
            ix.log_info("Loaded new paths {}".format(add_path))

def run_startup_create_menus():
    #  run the separate startup config to setup Menus
    pass

def run_startup_create_shelf():
    #  run the separate startup config to setup Menus
    print("IX_SHELF_CONFIG_FILE Values", os.getenv("IX_SHELF_CONFIG_FILE"))
    pass


# setup rundown for host config
def rundown():
    try:
        load_legacy_python()
        run_startup_create_menus()
        run_startup_create_shelf()
        ix.log_info("Rundown complete.")
    except Exception as RundownError:
        ix.log_error(RundownError)


rundown()