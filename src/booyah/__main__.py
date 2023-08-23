#!/usr/bin/env python
import sys
import os

module_name = "booyah"
# When in a pip may not need to manually add the path to the sys
if module_name not in sys.modules:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, parent_dir)

from booyah.bin.booyah import run
run()
