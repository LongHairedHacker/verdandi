#!/usr/bin/env python2

import os
import sys
import SocketServer
import traceback

from time import sleep
from jinja2 import Environment, FileSystemLoader
from SimpleHTTPServer import SimpleHTTPRequestHandler
from multiprocessing import Process
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from constants import CONTENT_DIRECTORY, OUTPUT_DIRECTORY, TEMPLATE_DIRECTORY, SERVE_PORT, SERVE_BIND_ADDRESS


class DirectoryObserver(FileSystemEventHandler):
	def __init__(self, verdandi):
		self._verdandi = verdandi

	def on_any_event(self, event):
		print "File changed: %s" % event.src_path
		self._verdandi.generate_output(False)



class Verdandi(object):

	output_directory = OUTPUT_DIRECTORY
	modules = []
	base_url = ""


	def __init__(self):
		self.jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIRECTORY))
		self.jinja_env.globals['base_url'] = self.base_url


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
		if not os.path.exists(self.output_directory):
			os.mkdir(self.output_directory)
		if os.listdir(self.output_directory) != []:
			print "[Warn] Ouput directory is not empty"
		for module in self.modules:
			module.collect_assets(self.output_directory)


	def render(self):
		if not os.path.exists(self.output_directory):
			os.mkdir(self.output_directory)
		for module in self.modules:
			module.render(self.output_directory, self.jinja_env)


	def run(self):
		if len(sys.argv) > 1 and sys.argv[1] == 'serve':
			self.generate_output(False)
			self.serve()
		else:
			self.generate_output()
			sys.exit(0)


	def generate_output(self, fail_on_exception = True):
		try:
			self.pass_messages()
			self.collect_assets()
			self.render()
		except Exception:
			print "[Error] I have a bad feeling about this ..."
			traceback.print_exc()
			if fail_on_exception:
				sys.exit(1)



	def serve(self):
		def serve():
			os.chdir(self.output_directory)
			httpd = SocketServer.TCPServer((SERVE_BIND_ADDRESS, SERVE_PORT), SimpleHTTPRequestHandler)
			print "Serving under %s:%d" % (SERVE_BIND_ADDRESS, SERVE_PORT)
			httpd.serve_forever()


		event_handler = DirectoryObserver(self)
		observer = Observer()
		observer.schedule(event_handler, CONTENT_DIRECTORY, recursive=True)
		observer.schedule(event_handler, TEMPLATE_DIRECTORY, recursive=True)
		observer.start()

		server_process = Process(target=serve)
		server_process.start()

		try:
			server_process.join()
		except KeyboardInterrupt:
			pass

		observer.stop()
		observer.join()

		print "Be vigilant!"
		sys.exit(0)
