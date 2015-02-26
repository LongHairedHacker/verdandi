#!/usr/bin/env python2

import os
from jinja2 import Environment, FileSystemLoader

class Verdandi(object):

	template_dir = "templates"
	output_directory = "rendered_root"
	modules = []


	def __init__(self):
		self.jinja_env = Environment(loader=FileSystemLoader(self.template_dir))


	def send_message(self, message):
		results = []

		for module in self.modules:
			results += module.process_message(message)
		
		return results


	def pass_messages(self):		
		messages = self.send_message(None)

		while len(messages) > 0:
			message = messages.pop()
			print message	
			messages = messages + self.send_message(message)
			
	
	def render(self):
		if not os.path.exists(self.output_directory):
			os.mkdir(self.output_directory)	
		for module in self.modules:
			module.render(self.output_directory, self.jinja_env)


	def run(self):
		self.pass_messages()
		self.render()
