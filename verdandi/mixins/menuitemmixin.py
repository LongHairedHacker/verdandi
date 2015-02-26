#!/usr/bin/env python2

class MenuItemMixin(object):

	menu_title = "Menu title"
	menu_label = None
	menu_parent = None
	url = "index.html"

	def process_message(self, message):
		if message == None:
			return [{'type': 'menu_add_item', 
						'title' : self.menu_title, 
						'parent' : self.menu_parent,
						'label' : self.menu_label,
						'url' : self.url}]

		return []
