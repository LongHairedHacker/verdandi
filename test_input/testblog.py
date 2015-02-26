#!/usr/bin/env python2

import sys
sys.path.append('../')

from verdandi.verdandi import Verdandi
from verdandi.modules.page import Page

class TestPage1(Page):
	title = "A cool new Page"

class TestPage2(Page):
	title = "An other cool Page"
	url = "page2.html"

class TestPage3(Page):
	title = "Yet an other cool Page"
	url = "subdir/page3.html"


class TestBlog(Verdandi):
	modules = [TestPage1(),
				TestPage2(),
				TestPage3()]


testblog = TestBlog()
testblog.run()
