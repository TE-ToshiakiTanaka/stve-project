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
        self.assertTrue("stve.picture" in self.service.keys())
        self.assertTrue(self.service["stve.picture"].version() != None)
        pic = self.service["stve.picture"].get()

        self.assertTrue(self.get("system.tmp") != None)
        img = pic.open(os.path.join(self.get("system.tmp"), "test01.png"))
        self.assertTrue(img != None)
        rgb = pic.get_rgb(img)
        self.assertTrue(len(rgb) == 3)
        L.info(rgb)

    @classmethod
    def tearDownClass(cls):
        L.info("*** End TestCase     : %s *** " % __file__)
