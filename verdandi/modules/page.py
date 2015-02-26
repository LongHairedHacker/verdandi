#!/usr/bin/env python2

from verdandi.mixins.templatemixin import TemplateMixin
from verdandi.mixins.menuitemmixin import MenuItemMixin


class Page(TemplateMixin, MenuItemMixin):
	title = 'Page Title'

	def get_context(self):
		context = super(Page,self).get_context()
		context['page_title'] = self.title
		return context
		
		


