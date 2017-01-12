#!/usr/bin/env python2

import os
import codecs
import copy
import markdown

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
			os.makedirs(out_dir)

		print "Rendering %s" % out_path

		out_file = codecs.open(out_path, 'wb', 'utf-8')
		out_file.write(result)
		out_file.close()


	def read_content_file(self, path):
		content_file = codecs.open(path, 'r', 'utf-8')

		meta = self.read_content_file_metadata(content_file)

		result = {}
		try:
			result['title'] = meta['title']
			result['creation_time'] = parser.parse(meta['creation_time'].decode('ascii'))
			result['edit_time'] = parser.parse(meta['edit_time'].decode('ascii'))

			result['content'] = content_file.read()
		except KeyError as error:
			raise RuntimeError("Incomplete metadata, missing %s in file: %s" % (error, path))

		content_file.close()

		return result


	def read_content_file_metadata(self, content_file):
		# Abuse the markdown meta data extension
		# https://pythonhosted.org/Markdown/extensions/meta_data.html
		# It can't be used on the full file since our content can be something else than markdown.

		markdown_converter = markdown.Markdown(extensions = ['markdown.extensions.meta'])

		lines = ""
		line = content_file.readline()
		while line.strip() != '':
			lines += line
			line = content_file.readline()
		lines += "\n"

		markdown_converter.convert(lines)

		meta = markdown_converter.Meta
		for key in meta.keys():
			if len(meta[key]) == 1:
				meta[key] = meta[key][0]

		return meta
