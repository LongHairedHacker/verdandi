#!/usr/bin/env python2
from verdandi.mixins.messagemixin import MessageMixin

class NewsItemMixin(MessageMixin):
	news_item_title = "Not the news item you need ..."
	news_item_content = "... but the news item you deserve."
	news_item_creation_time = None
	news_item_edit_time = None
	news_item_url = '/index.html'

	news_feed_id = None


	def get_news_item(self):
		item = {
			'title': self.news_item_title,
			'content': self.news_item_content,
			'url' : self.news_item_url,
			'creation_time': self.news_item_creation_time,
			'edit_time': self.news_item_edit_time
		}

		return item


	def process_message(self, message):
		other_messages = super(NewsItemMixin, self).process_message(message)

		if message == None and self.news_feed_id != None:
			other_messages += [{
				'type' : 'news_feed_item',
				'feed_id' : self.news_feed_id,
				'item' : self.get_news_item()
			}]

		return other_messages
