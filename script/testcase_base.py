import os
import sys
import argparse
import ConfigParser

from stve.script import StveTestCase
from stvex.utility import *
from stvex.utility import LOG as L

class TestCase_Unit(StveTestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase_Unit, self).__init__(*args, **kwargs)
        self.register(LIB_DIR)
        self.get_service()
        self.get_config()

    def arg_parse(self, parser):
        parser.add_argument(action='store', dest="testcase",
                            help='TestCase Name.')
        return parser

    @classmethod
    def get_service(cls):
         # cls.adb = cls.service["stvex.android"].get(cls.get("args.mobile"))
         cls.browser = cls.service["stve.browser"].get()
         cls.picture = cls.service["stve.picture"].get()

    @classmethod
    def get_config(cls, conf=""):
        if conf == "":
            conf = os.path.join(SCRIPT_DIR, "config.ini")
        try:
            config = ConfigParser.ConfigParser()
            config.read(conf)
            for section in config.sections():
                for option in config.options(section):
                    cls.set("%s.%s" % (section, option), config.get(section, option))
        except Exception as e:
            L.warning('error: could not read config file: %s' % e)
