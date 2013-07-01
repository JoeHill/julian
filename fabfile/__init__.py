import os
import sys

from fabric.main import find_fabfile

ROOT = os.path.join(os.path.dirname(__file__), '..') 
sys.stderr.write("=====================================\nROOT: %s\n" % ROOT)

import test
