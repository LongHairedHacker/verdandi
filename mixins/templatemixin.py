#!/usr/bin/env python2

import os
import codecs
import copy

from dateutil import parser

class TemplateMixin(object):
	template = "base.html"
	url = "index.html"
	context = {}

	def get_context(self):
		return copy.copy(self.context)

	def render(self, output_directory, jinja_env):
		context = self.get_context()
		self.render_files(context, output_directory, jinja_env)

	def render_files(self, context, output_directory, jinja_env):
		self.render_to_file(self.template, self.url, context, output_directory, jinja_env)


	def render_to_file(self, template, url, context, output_directory, jinja_env):
		template = jinja_env.get_template(template)
		result = template.render(context)

		out_path = os.path.join(output_directory, url)
		out_dir = os.path.dirname(out_path)
		if not os.path.isdir(out_dir):
			os.mkdir(out_dir)

		print "Rendering %s" % out_path

		out_file = codecs.open(out_path, 'wb', 'utf-8')
		out_file.write(result)
		out_file.close()


	def read_content_file(self, path):
		content_file = codecs.open(path, 'r', 'utf-8')

		result = {}

		first_line = content_file.readline()
		second_line = content_file.readline()

		third_line = content_file.readline().strip()
		while third_line == '':
			third_line = content_file.readline().strip()

		result['title'] = third_line

		result['content'] = content_file.read().decode('utf-8')

		result['creation_time'] = parser.parse(first_line)
		result['edit_time'] = parser.parse(second_line)

		content_file.close()


		return result
