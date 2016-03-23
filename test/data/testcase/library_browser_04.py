import os
import sys
import time

from stve.log import LOG as L
from stve.script import StveTestCase


class TestCase(StveTestCase):
    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        L.info("*** Start TestCase   : %s *** " % __file__)

    def test(self):
        self.assertTrue("stve.browser" in self.service.keys())
        b = self.service["stve.browser"].get("FireFox")
        self.assertTrue(b != None)
        b.start(self.get("browser.url"))
        time.sleep(10)
        b.quit()

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
