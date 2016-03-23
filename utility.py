import os
import sys

from stve.log import Log

LOG = Log("Project.STVE")

WORK_DIR = os.path.normpath(os.path.dirname(__file__))
LIB_DIR = os.path.normpath(os.path.join(WORK_DIR, "library"))
SCRIPT_DIR = os.path.normpath(os.path.join(WORK_DIR, "script"))
