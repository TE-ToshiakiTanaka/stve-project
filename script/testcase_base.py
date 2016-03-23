import os
import sys
import argparse

from stve.script import StveTestCase
from stvex.utility import *

class TestCase_Unit(StveTestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase_Unit, self).__init__(*args, **kwargs)
        self.register(LIB_DIR)
        self.get_service()

    def arg_parse(self, parser):
        parser.add_argument(action='store', dest="testcase",
                            help='TestCase Name.')
        parser.add_argument('-m', action='store', dest='mobile',
                            help='Test Target Mobile Phone.')
        return parser

    @classmethod
    def get_service(cls):
         cls.adb = cls.service["stvex.android"].get(cls.get("args.mobile"))
