__version__ = (0, 2, 0)
import os
import sys

LIB_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not LIB_PATH in sys.path:
    sys.path.insert(0, LIB_PATH)

from android import module
from android.module import Android

class Factory(object):
    def __init__(self):
        pass

    def version(self):
        return __version__

    def get(self, serial, host=module.PROFILE_PATH):
        return Android(serial, host)


NAME = "stvex.android"
FACTORY = Factory()
