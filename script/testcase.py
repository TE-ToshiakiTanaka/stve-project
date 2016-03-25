import os
import sys

from stvex.script import testcase_picture
from stvex.script import testcase_browser
from stvex.utility import *

class TestCase_Base(testcase_picture.TestCase_Picture,
                    testcase_browser.TestCase_Browser):

    def __init__(self, *args, **kwargs):
        super(TestCase_Base, self).__init__(*args, **kwargs)

    def get_reference(self, reference):
        try:
            return os.path.join(TMP_DIR, self.get("player.name"), reference)
        except Exception as e:
            L.warning(e)
            raise e

    def get_target(self, target):
        try:
            return os.path.join(TMP_DIR, target)
        except Exception as e:
            L.warning(e)
            raise e

    def browser_login(self):
        try:
            self.browser_get_by_id(self.get("dmm.login")).send_keys(self.get("args.username"))
            self.browser_get_by_id(self.get("dmm.password")).send_keys(self.get("args.password"))
            self.browser_get_by_class(self.get("dmm.submit")).click()
        except Exception as e:
            L.warning(e)
            raise e

    def enable(self, reference, target=""):
        L.debug("Reference : %s" % reference)
        if target == "":
            target = self.browser_screenshot(self.get("player.capture"))
        return self.picture_is_pattern(
            self.get_target(target), self.get_reference(reference))

    def enable_timeout(self, reference, target="", loop=5, timeout=5):
        result = False
        for _ in xrange(loop):
            if self.enable(reference, target):
                result = True; break
            time.sleep(timeout)
        return result

    def enable_timeout_crop(self, reference, target, filename="", loop=5, timeout=5):
        if filename == "":
            filename = self.browser_screenshot(self.get("player.capture_crop"))
        return self.enable_timeout_crop_box(target, self.find(reference), filename, loop, timeout)

    def enable_timeout_crop_box(self, reference, point, target="", loop=5, timeout=5):
        if target == "":
            target = self.browser_screenshot(self.get("player.capture"))
        crop_target = self.crop(target, point)
        return self.enable_timeout(reference, crop_target, loop, timeout)

    def tap_base(self, x, y):
        L.debug("Tap Coordinate : (x, y) = (%s, %s)" % (x, y))
        self.browser_click(self.get("dmm.target"), x, y)

    def tap(self, reference, target=""):
        result = self.find(reference, target)
        if not result == None:
            self.tap_base(result.x + (result.width / 2),
                          result.y + (result.height / 2))
            return True
        else:
            return False

    def tap_timeout(self, reference, target="", loop=5, timeout=5):
        if not self.enable_timeout(reference, target, loop, timeout):
            return False
        return self.tap(reference)

    def crop(self, target, point, filename=""):
        if filename == "":
            filename = self.get_target(self.get("player.capture_crop"))
        if point == None:
            return self.get_target(target)
        L.debug("Crop Target : %s " % str(point))
        L.debug("Reference   : %s " % self.get_target(target))
        return self.picture_crop(self.get_target(target), point, filename)

    def find(self, reference, target=""):
        L.debug("Reference : %s" % reference)
        if target == "":
            target = self.browser_screenshot(self.get("player.capture"))
        return self.picture_find_pattern(
            self.get_target(target), self.get_reference(reference))
