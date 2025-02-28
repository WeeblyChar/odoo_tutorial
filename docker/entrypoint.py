#!/usr/bin/env python3

import os
os.environ["PYTHONPATH"] = "/usr/local/lib/python3.12/dist-packages"
# ^-- Apparently this is a must only for my container due to the Open Telemetry's library being in a weird directory

import odoo
import sys

# Start Odoo
if __name__ == "__main__":
    sys.argv.extend(["-i", "base"])  # Ensure base module installation
    odoo.cli.main()
