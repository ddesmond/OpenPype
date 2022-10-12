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