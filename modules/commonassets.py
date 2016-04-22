#!/usr/bin/env python2

from verdandi.mixins.fileassetsmixin import FileAssetsMixin
from verdandi.mixins.messagemixin import MessageMixin
from verdandi.mixins.rendermixin import RenderMixin

class CommonAssets(FileAssetsMixin, MessageMixin, RenderMixin):
	pass
