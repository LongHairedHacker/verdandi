#!/usr/bin/env python2

import os
import sys
import SocketServer
import inotify.adapters

from jinja2 import Environment, FileSystemLoader
from SimpleHTTPServer import SimpleHTTPRequestHandler
from multiprocessing import Process

from constants import CONTENT_DIRECTORY, OUTPUT_DIRECTORY, TEMPLATE_DIRECTORY, SERVE_PORT, SERVE_BIND_ADDRESS

class Verdandi(object):

	output_directory = OUTPUT_DIRECTORY
	modules = []


	def __init__(self):
		self.jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIRECTORY))


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
		self.generate_output()

		if len(sys.argv) > 1 and sys.argv[1] == 'serve':
			self.serve()


	def generate_output(self):
		self.pass_messages()
		self.collect_assets()
		self.render()


	def serve(self):

		def has_create_or_modify(watch):
			result = False
			for event in watch.event_gen():
				if event == None:
					break

				result = result or ('IN_CREATE' in event[1])
				result = result or ('IN_DELETE' in event[1])
				result = result or ('IN_MODIFY' in event[1])

			return result

		content_watch = inotify.adapters.InotifyTree(CONTENT_DIRECTORY)
		template_watch = inotify.adapters.InotifyTree(TEMPLATE_DIRECTORY)


		def serve():
			os.chdir(self.output_directory)
			httpd = SocketServer.TCPServer((SERVE_BIND_ADDRESS, SERVE_PORT), SimpleHTTPRequestHandler)
			print "Serving under %s:%d" % (SERVE_BIND_ADDRESS, SERVE_PORT)
			httpd.serve_forever()


		server_process = Process(target=serve)
		server_process.start()

		while True:
			if has_create_or_modify(content_watch) or has_create_or_modify(template_watch):
				self.generate_output()
