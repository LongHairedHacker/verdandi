#!/usr/bin/env python2

import sys
sys.path.append('../')

from verdandi.verdandi import Verdandi
from verdandi.modules.page import Page

class TestPage1(Page):
	title = "A cool new Page"
	menu_title = "New Page"
	menu_label = "new_cool_page"
	

class TestPage2(Page):
	title = "An other cool Page"
	url = "page2.html"
	menu_title = "Other new Page"
	menu_label = "cool_page1"


class TestPage3(Page):
	title = "Yet an other cool Page"
	menu_title = "Other new Page2"
	menu_label = "cool_page2"
	menu_parent = "cool_page1"
	url = "subdir/page3.html"


class TestBlog(Verdandi):
	modules = [TestPage1(),
				TestPage2(),
				TestPage3()]


testblog = TestBlog()
testblog.run()
