#!/usr/bin/env python2

from verdandi.constants import CONTENT_DIRECTORY

class AssetsMixin(object):

	assets = []
	asset_directory = CONTENT_DIRECTORY


	def get_assets(self):
		return self.assets

	def collect_assets(self, output_directory):
		pass
