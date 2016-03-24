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
        parser.add_argument('-u', action='store', dest='username',
                            help='Username (E-mail) from DMM.com.')
        parser.add_argument('-p', action='store', dest='password',
                            help='Password from DMM.com.')

        return parser

    @classmethod
    def get_service(cls):
         cls.adb = cls.service["stvex.android"].get(cls.get("args.mobile"))
         cls.browser = cls.service["stvex.browser"].get()
         cls.pic = cls.service["stvex.picture"].get()
