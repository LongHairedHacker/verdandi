#!/usr/bin/env python2
import os
from datetime import datetime

import markdown

from verdandi.mixins.templatemixin import TemplateMixin
from verdandi.mixins.menuitemmixin import MenuItemMixin
from verdandi.mixins.assetsmixin import AssetsMixin
from verdandi.constants import CONTENT_DIRECTORY, MARKDOWN_EXTENSIONS

class Page(MenuItemMixin, TemplateMixin, AssetsMixin):

	title = "Page Title"
	content_file = "content.md"
	content_directory = CONTENT_DIRECTORY

	markdown_extensions = MARKDOWN_EXTENSIONS


	def get_context(self):
		context = super(Page,self).get_context()
		context['page_title'] = self.title

		full_path = os.path.join(self.content_directory, self.content_file)
		markdown_converter = markdown.Markdown(extensions = self.markdown_extensions)

		content = self.read_content_file(full_path)

		context['content_creation_time'] = content['creation_time']
		context['content_edit_time'] =  content['edit_time']

		markdown_source = content['content']
		context['content'] = markdown_converter.convert(markdown_source)

		return context
