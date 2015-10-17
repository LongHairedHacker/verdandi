#!/usr/bin/env python2

import os
from jinja2 import Environment, FileSystemLoader

from constants import OUTPUT_DIRECTORY, TEMPLATE_DIRECTORY

class Verdandi(object):

	template_directory = TEMPLATE_DIRECTORY
	output_directory = OUTPUT_DIRECTORY
	modules = []


	def __init__(self):
		self.jinja_env = Environment(loader=FileSystemLoader(self.template_directory))


	def send_message(self, message):
		results = []

		for module in self.modules:
			results += module.process_message(message)

		return results


	def pass_messages(self):
		messages = self.send_message(None)

		while len(messages) > 0:
			message = messages.pop()
			messages = messages + self.send_message(message)


	def collect_assets(self): 
		for module in self.modules:
			module.collect_assets(self.output_directory)


	def render(self):
		if not os.path.exists(self.output_directory):
			os.mkdir(self.output_directory)
		for module in self.modules:
			module.render(self.output_directory, self.jinja_env)


	def run(self):
		self.pass_messages()
		self.collect_assets()
		self.render()
