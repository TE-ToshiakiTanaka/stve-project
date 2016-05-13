import os
import sys
import time
import fnmatch

from stvex.utility import *
from stvex.utility import LOG as L
from stvex.script import testcase

class TestCase(testcase.TestCase_Base):

    def __init__(self, *args, **kwargs):
        super(TestCase, self).__init__(*args, **kwargs)

    def login(self):
        self.browser_start(self.get("dmm.url")); time.sleep(5)
        self.browser_login(self.get("args.username"), self.get("args.password")); time.sleep(30)
        if self.tap_timeout("bad.png", timeout=1): time.sleep(3)
        if not self.tap_pattern("login*.png"):
            return False
        return True

    def special(self):
        self.tap_pattern("search*.png")
        time.sleep(10)
        self.tap_pattern("search*.png")
        self.tap_pattern("special*.png")
        self.special_cource(self.get("args.cource"))
        self.tap_pattern("skip*.png")
        if not self.enable_pattern("search_start*.png"):
            return False
        self.tap_pattern("search_start*.png")
        if self.enable_pattern("not_start*.png"):
            return False
        return True

    def daily(self):
        self.tap_pattern("search*.png")
        time.sleep(10)
        self.tap_pattern("search*.png")
        self.tap_pattern("daily*.png")
        self.tap_pattern("route_*.png")
        self.tap_timeout("start.png")
        self.tap_pattern("skip*.png")
        if not self.enable_pattern("search_start*.png"):
            return False
        self.tap_pattern("search_start*.png")
        if self.enable_pattern("not_start*.png"):
            return False
        return True

    def battle(self):
        if self.enable_pattern("not_start*.png"):
            return False
        while not self.enable("end.png"):
            if self.enable_timeout("event_start.png", timeout=0.5):
                self.search()
                self.tap_timeout("event_start.png", timeout=0.5)
                time.sleep(5)
            if self.tap_timeout("auto.png", loop=2, timeout=0.5): time.sleep(5)
            if self.tap_timeout("get.png", loop=2, timeout=0.5): time.sleep(5)
        return True

    def search(self):
        if self.enable_pattern("character_*.png"):
            self.tap_timeout("item.png", loop=2, timeout=0.5)

    def story(self):
        self.tap_pattern("search*.png")
        time.sleep(10)
        self.tap_pattern("search*.png")
        self.story_section_cource(self.get("args.section"), self.get("args.cource"))
        self.tap_pattern("skip*.png")
        if not self.enable_pattern("search_start*.png"):
            return False
        self.tap_pattern("search_start*.png")
        if self.enable_pattern("not_start*.png"):
            return False
        return True

    def event(self):
        time.sleep(20)
        self.tap_pattern("event_entry*.png"); time.sleep(10)
        self.tap_pattern("event_route*.png"); time.sleep(10)
        self.tap_pattern("event_stage*.png"); time.sleep(10)
        self.event_cource(self.get("args.cource")); time.sleep(10)
        self.tap_pattern("skip*.png"); time.sleep(10)
        if not self.enable_pattern("search_start*.png"):
            return False
        self.tap_pattern("search_start*.png")
        if self.enable_pattern("not_start*.png"):
            return False
        return True

    def event_battle(self):
        if self.enable_pattern("not_start*.png"):
            return False
        while not self.enable("end.png"):
            if self.enable_timeout("event_start.png", timeout=0.5):
                self.search()
                self.tap_timeout("event_start.png", timeout=0.5)
                time.sleep(5)
            if self.tap_timeout("auto.png", loop=2, timeout=0.5): time.sleep(5)
            if self.tap_timeout("get.png", loop=2, timeout=0.5): time.sleep(5)
            if self.tap_timeout("raid_start.png", loop=2, timeout=0.5):
                while not self.enable("get.png"):
                    if self.enable_timeout("end.png", loop=2, timeout=0.5):
                        break
                    if self.tap_timeout("auto.png", loop=2, timeout=0.5): time.sleep(30)
                    if self.enable_timeout("end.png", loop=2, timeout=0.5):
                        break
                    self.tap_base(620, 340); time.sleep(5)
                    if self.tap_timeout("raid_call.png", loop=2, timeout=0.5): time.sleep(5)
                    if self.tap_timeout("raid_call_help.png", loop=2, timeout=0.5): time.sleep(5)
                    if self.tap_timeout("raid_close.png", loop=2, timeout=0.5):
                        break
                    if self.enable_timeout("event_start.png", timeout=0.5):
                        self.search()
                        self.tap_timeout("event_start.png", timeout=0.5)
                        time.sleep(5)
                    self.tap_timeout("raid_start.png", loop=2, timeout=0.5)
                time.sleep(5)
                if self.tap_timeout("get.png", loop=2, timeout=0.5): time.sleep(5)
        return True

    def result(self):
        return self.enable_timeout("end.png")

    def story_section_cource(self, section="1", cource="1"):
        section_name = "section_%s*.png" % section
        if self.tap_pattern(section_name): time.sleep(3)
        cource_name = "cource_%s*.png" % cource
        if self.tap_pattern(cource_name): time.sleep(3)
        return self.tap_timeout("start.png")

    def special_cource(self, cource="1"):
        cource_name = "cource_%s*.png" % cource
        if self.tap_pattern(cource_name): time.sleep(3)
        return self.tap_timeout("start.png")

    def event_cource(self, cource="1"):
        if int(cource) > 3:
            self.tap_pattern("event_cource_next*.png")
        cource_name = "event_cource_%s*.png" % cource
        L.info(cource_name)
        return self.tap_pattern(cource_name)

    def enable_pattern(self, pattern, loop=3, timeout=0.5):
        targets = self.__search_pattern(pattern)
        for target in targets:
            if self.enable_timeout(target, loop=loop, timeout=timeout):
                return True
        return False

    def tap_pattern(self, pattern, loop=3, timeout=0.5):
        targets = self.__search_pattern(pattern)
        for target in targets:
            if self.tap_timeout(target, loop=loop, timeout=timeout):
                return True
        return False

    def __search_pattern(self, pattern, host=""):
        result = []
        if host == "":
            host = os.path.join(TMP_DIR, self.get("player.name"))
        files = os.listdir(host)
        return fnmatch.filter(files, pattern)
