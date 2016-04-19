#!/usr/bin/env python2

from verdandi.mixins.assetsmixin import AssetsMixin
from verdandi.mixins.messagemixin import MessageMixin
from verdandi.mixins.rendermixin import RenderMixin

class CommonAssets(AssetsMixin, MessageMixin, RenderMixin):
	pass
