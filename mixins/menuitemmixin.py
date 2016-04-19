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
			return other_messages + [{'type': 'menu_add_item', 
										'title' : self.menu_title, 
										'parent' : self.menu_parent,
										'label' : self.menu_label,
										'url' : self.url}]

		elif message['type'] == 'menu_add_item':			
			if self.menu_items == None:
				self.menu_items = {}

			label = message['label']
			if label in self.menu_items.keys():
				print '[Warn] Depulicate menu item label: %s in %s' % (label, self.menu_label)
				return other_messages
			
			self.menu_items[label] = {}
			
			for key in ['title', 'parent', 'label', 'url']:
				self.menu_items[label][key] = message[key]

		return other_messages


	def get_menu_path(self):
		path = [self.menu_label]
		while self.menu_items[path[0]]['parent'] != None:
			path = [self.menu_items[path[0]]['parent']] + path
		
		return path

	
	def get_menu_level(self, parent):
		return filter(lambda x: x['parent'] == parent, self.menu_items.values())

	
	def generate_levels(self, path):
		level = path[0]
		next_level = None
		if len(path) > 1:
			next_level = path[1]

		res = '<ul>'

		sorted_level = sorted(self.get_menu_level(level), key=lambda x: x['label'])
		for item in sorted_level:
			if item['label'] == self.menu_label:
				res += '<li><b>%s</b><br>' % item['title']
				res += self.generate_levels(path[1:])
				res += '</li>'
			elif item['label'] == next_level:
				res += '<li><i><a href="/%s">%s</a></i><br/>' % (item['url'], item['title'])
				res += self.generate_levels(path[1:])
				res += '</li>'
			else:
				res += '<li><a href="/%s">%s</a></li>' % (item['url'], item['title'])
		
		res += '</ul>'

		return res

	def generate_menu(self):
		
		path = self.get_menu_path()
		 
		return self.generate_levels([None] + path) 


	def get_context(self):
		context = super(MenuItemMixin, self).get_context()

		context['menu'] = self.generate_menu()

		return context
		
