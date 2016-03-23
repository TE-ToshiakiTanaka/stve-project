import os
import sys

from stve.log import Log
from stve.application import StveTestRunner
from stve.workspace import Workspace

from stvex.utility import *
from stvex.script.testcase_base import TestCase_Unit

class TestRunner(object):
    def __init__(self):
        self.runner = StveTestRunner()
        self.workspace = Workspace(WORK_DIR)

        self.tmp = self.workspace.mkdir("tmp")
        self.log = self.workspace.mkdir("log")
        self.report = self.workspace.mkdir("report")

        TestCase_Unit.register(LIB_DIR)

    def execute(self, script):
        self.runner.execute(script, SCRIPT_DIR)

    def execute_with_report(self, script):
        self.runner.execute_with_report(script, SCRIPT_DIR, self.report)

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        sys.exit("Usage: %s <filename>" % sys.argv[0])
    testcase = sys.argv[1]
    runner = TestRunner()
    runner.execute_with_report(testcase)
