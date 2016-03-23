import os
import sys

from stvex.utility import LOG as L
from stvex.script.testcase_base import TestCase_Unit

class TestCase(TestCase_Unit):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        L.info("*** Start TestCase   : %s *** " % __file__)

    def test(self):
        self.assertTrue(1 == 1)
        L.info(self.adb.get().SERIAL)

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
