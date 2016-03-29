import os
import sys

from stvex.utility import *
from stvex.utility import LOG as L
from stvex.script import testcase_base

class TestCase_Browser(testcase_base.TestCase_Unit):

    @classmethod
    def browser_start(cls, url):
        try:
            # driver = os.path.join(DRIVER_DIR, "chromedriver.exe")
            return cls.browser.start(url)
        except Exception as e:
            L.warning(e)

    @classmethod
    def browser_screenshot(cls, filename="screen.png", host=TMP_DIR):
        try:
            return cls.browser.screenshot(host, filename)
        except Exception as e:
            L.warning(e)

    @classmethod
    def browser_click(cls, element, x, y, by="class"):
        try:
            return cls.browser.click(element, x, y, by)
        except Exception as e:
            L.warning(e)

    @classmethod
    def browser_quit(cls):
        try:
            return cls.browser.quit()
        except Exception as e:
            L.warning(e)

    @classmethod
    def browser_get_by_id(cls, element):
        try:
            return cls.browser.find_element_by_id(element)
        except Exception as e:
            L.warning(e)

    @classmethod
    def browser_get_by_class(cls, element):
        try:
            return cls.browser.find_element_by_class(element)
        except Exception as e:
            L.warning(e)
