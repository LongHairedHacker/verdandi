#!/usr/bin/env python2

import sys
sys.path.append('../')

from verdandi.verdandi import Verdandi
from verdandi.modules.page import Page
from verdandi.modules.commonassets import CommonAssets
from verdandi.modules.newsfeed import NewsFeed

class TestPage1(Page):
	title = "A cool new Page"
	menu_title = "New Page"
	menu_label = "new_cool_page"

class TestPage2(Page):
	title = "An other cool Page"
	assets = [('img/foo.png', 'img/'),
				('img/foo.png', 'img/bar.png'),
				('img/foo.png', 'img/bar')]
	url = "page2.html"
	menu_title = "Other new Page"
	menu_label = "cool_page1"


class TestPage3(Page):
	title = "Yet an other cool Page"
	menu_title = "Other new Page2"
	menu_label = "cool_page2"
	menu_parent = "cool_page1"
	url = "subdir/page3.html"

class Assets(CommonAssets):
	assets = [('img', 'img/dir'),
				('img/', 'img/files')]


class News(NewsFeed):
	title = "New News"
	url = "news.html"
	menu_title = "News"
	menu_label = "news"


class TestBlog(Verdandi):
	modules = [TestPage1(),
				TestPage2(),
				TestPage3(),
				Assets(),
				News()]


testblog = TestBlog()
testblog.run()
