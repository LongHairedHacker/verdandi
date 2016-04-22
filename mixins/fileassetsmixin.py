#!/usr/bin/env python2
import os
import shutil

from verdandi.mixins.assetsmixin import AssetsMixin

from verdandi.constants import CONTENT_DIRECTORY


class FileAssetsMixin(AssetsMixin):

	def collect_assets(self, output_directory):
		super(FileAssetsMixin, self).collect_assets(output_directory)
		
		assets = self.get_assets()

		for source, destination in assets:
			source_path = os.path.join(self.asset_directory, source)
			dest_path = os.path.join(output_directory, destination);

			if os.path.isdir(source_path):
				self.copy_dir(source_path, dest_path)
			elif os.path.isfile(source_path):
				self.copy_file(source_path, dest_path)
			else:
				print "Skipping %s is neither directory nor file" % source_path


	def copy_file(self, source_path, dest_path):
		print "Copying %s to %s" % (source_path, dest_path)

		dest_dir = os.path.dirname(dest_path)

		if not os.path.exists(dest_dir):
			os.makedirs(dest_dir)
		shutil.copy(source_path, dest_path)


	def copy_dir(self, source_path, dest_path):
		# /foo/bar /rofl -> contents of bar go to rofl/bar
		# /foo/bar/ /rofl -> contests of bar got to rofl/
		# Trailing slash on destination should have no effect

		# Will be '' in case of a trailing slash: /foo/bar/ else bar
		source_base = os.path.basename(source_path)
		# /rofl will become /rofl/ if base is '' otherwise it will become /rofl/bar
		dest_path = os.path.join(dest_path, source_base)

		if not os.path.exists(dest_path):
			os.makedirs(dest_path)

		# Discover the whole tree and copy each file individually
		for source_dir, _, files in os.walk(source_path):
			rel_path = os.path.relpath(source_dir, source_path)
			# Purely cosmetical for debug output
			if rel_path == '.':
				dest_dir = dest_path
			else:
				dest_dir = os.path.join(dest_path, rel_path)

			for source_file in files:
				file_source_path = os.path.join(source_dir, source_file)
				file_dest_path = os.path.join(dest_dir, source_file)
				self.copy_file(file_source_path, file_dest_path)
