#!/usr/bin/env python2
import os
from datetime import datetime

import markdown

from verdandi.mixins.templatemixin import TemplateMixin
from verdandi.mixins.menuitemmixin import MenuItemMixin
from verdandi.mixins.assetsmixin import AssetsMixin
from verdandi.mixins.newsitemmixin import NewsItemMixin
from verdandi.constants import CONTENT_DIRECTORY, MARKDOWN_EXTENSIONS

class Page(MenuItemMixin, NewsItemMixin, TemplateMixin, AssetsMixin):

	title = "Page Title"
	content_file = "content.md"
	content_is_markdown = True
	content_directory = CONTENT_DIRECTORY

	markdown_extensions = MARKDOWN_EXTENSIONS

	news_item_len = 10


	def process_message(self, message):
		if message == None:
			full_path = os.path.join(self.content_directory, self.content_file)
			self.content = self.read_content_file(full_path)

		other_messages = super(Page, self).process_message(message)

		return other_messages


	def get_news_item(self):
		lines = self.content['content'].split('\n')
		elipsized_content = '\n'.join(lines[0:self.news_item_len])

		elipsized_content += '\n\n Read [more](%s) ...' % self.url

		item = {
			'title': self.title,
			'content': elipsized_content,
			'creation_time': self.content['creation_time'],
			'edit_time': self.content['edit_time'],
			'url' : self.url
		}

		return item


	def get_context(self):
		context = super(Page,self).get_context()
		context['page_title'] = self.title

		context['content_creation_time'] = self.content['creation_time']
		context['content_edit_time'] =  self.content['edit_time']

		if self.content_is_markdown:
			markdown_converter = markdown.Markdown(extensions = self.markdown_extensions)
			markdown_source = self.content['content']
			context['content'] = markdown_converter.convert(markdown_source)
		else:
			context['content'] = self.content['content']

		return context
