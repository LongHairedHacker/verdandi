#!/usr/bin/env python2

import os
from pylibsass import sass

from verdandi.mixins.messagemixin import MessageMixin
from verdandi.mixins.rendermixin import RenderMixin
from verdandi.mixins.assetsmixin import AssetsMixin

class SassAssets(MessageMixin, RenderMixin, AssetsMixin):

	def collect_assets(self, output_directory):
		super(SassAssets, self).collect_assets(output_directory)

		assets = self.get_assets()

		for source, destination in assets:
			source_path = os.path.join(self.asset_directory, source)
			dest_path = os.path.join(output_directory, destination);

			dest_dir = os.path.dirname(dest_path)
			if not os.path.exists(dest_dir):
				os.makedirs(dest_dir)

			if os.path.isfile(source_path):
				self.compile_file(source_path, dest_path)
			else:
				print "Skipping %s is not a file" % source_path


	def compile_file(self, source_path, dest_path):
		print "Compiling %s to %s" % (source_path, dest_path)

		sass_file = open(source_path, 'r')
		css_file = open(dest_path, 'w')

		sass_string = sass_file.read().decode('utf-8')
		css_string = sass.compile_str(sass_string)

		css_file.write(css_string.encode('utf-8'))

		sass_file.close()
		css_file.close()
