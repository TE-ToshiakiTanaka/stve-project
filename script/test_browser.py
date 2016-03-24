import os
import sys

from stvex.utility import *
from stvex.script import testcase_base

class TestCase_Browser(testcase_base.TestCase_Unit):

    def browser_start(self, url):
        try:
            return self.browser.start(url)
        except Exception as e:
            L.warning(e)
            raise e

    def browser_screenshot(self, filename="screen.png", host=TMP_DIR):
        try:
            return self.browser.screenshot(host, filename)
        except Exception as e:
            L.warning(e)
            raise e

    def browser_click(self, element, x, y, by="class"):
        try:
            return self.browser.click(element, x, y, by)
        except Exception as e:
            L.warning(e)
            raise e

    def browser_quit(self):
        try:
            return self.browser.quit()
        except Exception as e:
            L.warning(e)
            raise e

    def browser_get_by_id(self, element):
        try:
            return self.browser.find_element_by_id(element)
        except Exception as e:
            L.warning(e)
            raise e

    def browser_get_by_class(self, element):
        try:
            return self.browser.find_element_by_class(element)
        except Exception as e:
            L.warning(e)
            raise e
