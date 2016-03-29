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
