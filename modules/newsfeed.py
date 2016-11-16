#!/usr/bin/env python2

import os
import markdown

from dateutil import parser

from verdandi.mixins.templatemixin import TemplateMixin
from verdandi.mixins.menuitemmixin import MenuItemMixin
from verdandi.mixins.fileassetsmixin import FileAssetsMixin
from verdandi.constants import CONTENT_DIRECTORY, MARKDOWN_EXTENSIONS


class NewsFeed(MenuItemMixin, TemplateMixin, FileAssetsMixin):

	title = "News feed title"
	template = "newsfeed.html"
	feed_template = "newsfeed.rss"
	feed_url = "feed.rss"
	news_item_directory = "news"
	news_feed_id = "news"

	markdown_extensions = MARKDOWN_EXTENSIONS
	content_directory = CONTENT_DIRECTORY

	items = []


	def process_message(self, message):
		other_messages = super(NewsFeed, self).process_message(message)

		if message == None:
			self.items = []
	 	elif message['type'] == 'news_feed_item':
			if message['feed_id'] == self.news_feed_id:
				self.items += [message['item']]

		return other_messages


	def get_context(self):
		context = super(NewsFeed,self).get_context()
		context['title'] = self.title
		context['url'] = "/%s" % self.url
		context['feed_url'] = "/%s" % self.feed_url

		markdown_converter = markdown.Markdown(extensions = self.markdown_extensions)

		rendered_items = []
		for item in self.items:
			item['content'] = markdown_converter.convert(item['content'])
			item['url'] = "/%s" % item['url']
			rendered_items += [item]

		item_directory = os.path.join(self.content_directory, self.news_item_directory)
		for news_file in os.listdir(item_directory):
			filename, ext = os.path.splitext(news_file)
			if ext == '.md':
				item = {}

				full_path = os.path.join(item_directory, news_file)

				item = self.read_content_file(full_path)

				item['content'] = markdown_converter.convert(item['content'])
				item['anchor'] = filename
				item['url'] = "/%s#%s" % (self.url, filename)

				rendered_items += [item]

		rendered_items = sorted(rendered_items, key=lambda item: item['creation_time'], reverse=True)
		context['items'] = rendered_items

		return context


	def render_files(self, context, output_directory, jinja_env):
		self.render_to_file(self.feed_template, self.feed_url, context, output_directory, jinja_env)
		super(NewsFeed, self).render_files(context, output_directory, jinja_env)
