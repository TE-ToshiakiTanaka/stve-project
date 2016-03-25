import os
import sys
import time

from stvex.utility import *
from stvex.utility import LOG as L
from stvex.script import testcase_normal

class TestCase(testcase_normal.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        L.info("*** Start TestCase   : %s *** " % __file__)

    def test_1_login(self):
        L.info("*** Login ***")
        self.assertTrue(self.login())

    def test_2_event(self):
        L.info("*** Event ***")
        self.assertTrue(self.event())

    def test_3_event_battle(self):
        L.info("*** Event Battle ***")
        self.assertTrue(self.event_battle())

    def test_4_result(self):
        L.info("*** Result ***")
        self.assertTrue(self.result())

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
        cls.browser_quit()
