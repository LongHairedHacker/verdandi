#!/usr/bin/env python2

import os

class TemplateMixin(object):
	template = "base.html"
	url = "index.html"
	context = {}

	def get_context(self):
		return self.context

	def render(self, output_directory, jinja_env):
		template = jinja_env.get_template(self.template)
		html = template.render(self.get_context())
		out_path = os.path.join(output_directory, self.url)
		out_dir = os.path.dirname(out_path)
		if not os.path.isdir(out_dir):
			os.mkdir(out_dir)
		out_file = open(out_path, "wb")
		out_file.write(html)
		out_file.close()
