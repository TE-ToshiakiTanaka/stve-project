import os
import sys

from stvex.utility import *
from stvex.script import testcase_base

class TestCase_Picture(testcase_base.TestCase_Unit):

    def picture_crop(self, filepath, point="", rename=""):
        try:
            pic = self.picture.open(filepath)
            if point == "":
                width, height = pic.size
                point = POINT(0, 0, width, height)
            crop_pic = self.picture.crop(pic, point)
            if rename == "": rename = filepath
            return self.picture.save(crop_pic, rename)
        except Exception as e:
            L.warning(e)
            raise e

    def picture_is_pattern(self, reference, target):
        try:
            return self.picture.is_pattern(reference, target)
        except Exception as e:
            L.warning(e)
            raise e

    def picture_find_pattern(self, reference, target):
        try:
            return self.picture.search_pattern(reference, target)
        except Exception as e:
            L.warning(e)
            raise e

    def picture_get_rgb(self, filepath, point=""):
        try:
            pic = self.picture.open(filepath)
            return self.picture.get_rgb(pic, point)
        except Exception as e:
            L.warning(e)
            raise e
