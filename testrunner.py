import os
import sys

from stve.log import Log
from stve.application import StveTestRunner
from stve.workspace import Workspace

from stvep.utility import *
from stvep.script.testcase_base import TestCase_Unit

class TestRunner(object):
    def __init__(self):
        self.runner = StveTestRunner()
        self.workspace = Workspace(WORK_DIR)

        self.tmp = self.workspace.mkdir("tmp")
        self.log = self.workspace.mkdir("log")
        self.report = self.workspace.mkdir("report")

        TestCase_Unit.register(LIB_DIR)

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        sys.exit("Usage: %s <filename>" % sys.argv[0])
    testcase = sys.argv[1]
    runner = TestRunner()
    runner.runner.execute(testcase, SCRIPT_DIR)
