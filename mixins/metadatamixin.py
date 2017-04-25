#!/usr/bin/env python2
import copy

from verdandi.mixins.templatemixin import TemplateMixin

class MetadataMixin(TemplateMixin):

    metadata = {}

    def get_metadata(self):
        return copy.copy(self.metadata)

    def get_context(self):
        context = super(MetadataMixin, self).get_context()
        metadata = self.get_metadata()

        for key, value in metadata.items():
            context['meta_%s' % key] = value

        return context
