#!/usr/bin/env python2
import os
from datetime import datetime

import markdown

from verdandi.mixins.templatemixin import TemplateMixin
from verdandi.mixins.menuitemmixin import MenuItemMixin
from verdandi.constants import CONTENT_DIRECTORY

class Page(TemplateMixin, MenuItemMixin):

	title = "Page Title"
	content_file = "content.md"
	content_directory = CONTENT_DIRECTORY

	markdown_extensions = ['markdown.extensions.sane_lists',
							'markdown.extensions.tables']

	def get_context(self):
		context = super(Page,self).get_context()
		context['page_title'] = self.title

		full_path = os.path.join(self.content_directory, self.content_file)
		markdown_converter = markdown.Markdown(extensions = self.markdown_extensions)

		ctime = os.path.getctime(full_path)
		context['content_creation_time'] = datetime.fromtimestamp(ctime)

		mtime = os.path.getmtime(full_path)
		context['content_edit_time'] = datetime.fromtimestamp(mtime)

		markdown_source = open(full_path, 'r').read()
		context['content'] = markdown_converter.convert(markdown_source)

		return context
