#!/usr/bin/env python2
from verdandi.mixins.messagemixin import MessageMixin

class MenuItemMixin(MessageMixin):

	menu_title = "Menu title"
	menu_label = None
	menu_parent = None
	url = "index.html"

	menu_items = None

	def process_message(self, message):
		other_messages = super(MenuItemMixin, self).process_message(message)

		if message == None:
			self.menu_items = {}
			return other_messages + [{'type': 'menu_add_item',
										'title' : self.menu_title,
										'parent' : self.menu_parent,
										'label' : self.menu_label,
										'url' : self.url}]

		elif message['type'] == 'menu_add_item':

			label = message['label']
			if label in self.menu_items.keys():
				print '[Warn] Depulicate menu item label: %s in %s' % (label, self.menu_label)
				return other_messages

			self.menu_items[label] = {}

			for key in ['title', 'parent', 'label', 'url']:
				self.menu_items[label][key] = message[key]

		return other_messages


	def get_menu_level(self, parent):
		level = filter(lambda x: x['parent'] == parent, self.menu_items.values())
		return sorted(level, key=lambda x: x['label'])


	def generate_levels(self, parent):
		level = self.get_menu_level(parent)

		if len(level) == 0:
			return ''

		res = '<ul>\n'
		for item in level:
			res += '<li><a href="/%s">%s</a>\n' % (item['url'], item['title'])
			res += self.generate_levels(item['label'])
			res += '</li>\n'

		res += '</ul>\n'

		return res


	def generate_menu(self):
		return self.generate_levels(None)


	def get_context(self):
		context = super(MenuItemMixin, self).get_context()

		context['menu'] = self.generate_menu()

		return context
