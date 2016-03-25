import os
import sys
import time

from stvex.script import testcase_picture
from stvex.script import testcase_browser
from stvex.utility import *
from stvex.utility import LOG as L

class TestCase_Base(testcase_picture.TestCase_Picture,
                    testcase_browser.TestCase_Browser):

    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)

    def get_reference(self, reference):
        try:
            return os.path.join(TMP_DIR, reference)
        except Exception as e:
            L.warning(e)
            raise e

    def get_target(self, target):
        try:
            return os.path.join(TMP_DIR, self.get("player.name"), target)
        except Exception as e:
            L.warning(e)
            raise e

    def browser_login(self, username, password):
        try:
            self.browser_get_by_id(self.get("dmm.login")).send_keys(username)
            self.browser_get_by_id(self.get("dmm.password")).send_keys(password)
            self.browser_get_by_class(self.get("dmm.submit")).click()
        except Exception as e:
            L.warning(e)
            raise e

    def enable(self, target, reference=""):
        L.debug("enable target : %s" % target)
        if reference == "":
            reference = self.browser_screenshot(self.get("player.capture"))
        return self.picture_is_pattern(
            self.get_reference(reference), self.get_target(target))

    def enable_timeout(self, target, reference="", loop=5, timeout=5):
        result = False
        for _ in xrange(loop):
            if self.enable(target, reference):
                result = True
                break
            time.sleep(timeout)
        return result

    def tap_base(self, x, y):
        L.debug("Tap Coordinate : (x, y) = (%s, %s)" % (x, y))
        self.browser_click(self.get("dmm.target"), x, y)

    def tap(self, target, reference=""):
        result = self.find(target, reference)
        L.info(result)
        if not result == None:
            self.tap_base(result.x + (result.width / 2),
                          result.y + (result.height / 2))
            return True
        else:
            return False

    def __tap_timeout(self, target, reference="", loop=5, timeout=5):
        if not self.enable_timeout(target, reference, loop, timeout):
            return False
        return self.tap(target)

    def tap_timeout(self, target, reference="", loop=5, timeout=5):
        if self.__tap_timeout(target, reference, loop, timeout):
            time.sleep(3)
            return True
        else:
            return False

    def crop(self, target, point, filename=""):
        if filename == "":
            filename = self.get_target(self.get("player.capture_crop"))
        if point == None:
            return self.get_target(target)
        L.debug("Crop Target : %s " % str(point))
        L.debug("Reference   : %s " % self.get_target(target))
        return self.picture_crop(self.get_target(target), point, filename)

    def find(self, target, reference=""):
        L.debug("find target : %s" % target)
        if reference == "":
            reference = self.browser_screenshot(self.get("player.capture"))
        return self.picture_find_pattern(
            self.get_reference(reference), self.get_target(target))
