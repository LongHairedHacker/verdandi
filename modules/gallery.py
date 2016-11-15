#!/usr/bin/env python2
import os
from datetime import datetime
from PIL import Image

import markdown

from verdandi.mixins.templatemixin import TemplateMixin
from verdandi.mixins.menuitemmixin import MenuItemMixin
from verdandi.mixins.fileassetsmixin import FileAssetsMixin
from verdandi.mixins.newsitemmixin import NewsItemMixin
from verdandi.constants import CONTENT_DIRECTORY, MARKDOWN_EXTENSIONS

class Gallery(MenuItemMixin, NewsItemMixin, TemplateMixin, FileAssetsMixin):
    gallery_description_file = 'description.md'
    gallery_directory = 'gallery'
    gallery_images_url = 'img/gallery'
    gallery_thumbnail_size = 300
    gallery_thumbnail_quality = 90
    gallery_thumbnail_prefix = 'thumb_'

    menu_title = 'Gallery'
    menu_label = 'gallery'

    news_item_len = 10

    template = "gallery.html"

    content_directory = CONTENT_DIRECTORY
    markdown_extensions = MARKDOWN_EXTENSIONS

    images = []

    def process_message(self, message):
    	if message == None:
            self.full_gallery_path = os.path.join(self.content_directory, self.gallery_directory)
            description_path = os.path.join(self.full_gallery_path, self.gallery_description_file)
            self.description = self.read_content_file(description_path)

            files = os.listdir(self.full_gallery_path)
            self.images = filter(lambda image: os.path.splitext(image)[1] == '.jpg', files)

    	other_messages = super(Gallery, self).process_message(message)

    	return other_messages


    def get_assets(self):
        assets = super(Gallery, self).get_assets()

        for image in self.images:
            src_image = os.path.join(self.gallery_directory, image)
            dst_image =  os.path.join(self.gallery_images_url, image)
            assets += [(src_image, dst_image)]

        return assets


    def get_news_item(self):
        lines = self.description['content'].split('\n')
        elipsized_description = '\n'.join(lines[0:self.news_item_len])

        item = {
            'title': self.description['title'],
            'content': elipsized_description,
            'creation_time': self.description['creation_time'],
            'edit_time': self.description['edit_time'],
            'url' : self.url
        }

        return item


    def get_context(self):
        context = super(Gallery,self).get_context()
        context['title'] = self.description['title']

        markdown_converter = markdown.Markdown(extensions = self.markdown_extensions)

        context['content_creation_time'] = self.description['creation_time']
        context['content_edit_time'] =  self.description['edit_time']

        markdown_source = self.description['content']
        context['description'] = markdown_converter.convert(markdown_source)

        context['images'] = []

        for image in self.images:
            image_url = os.path.join(self.gallery_images_url, image)
            thumb_url = os.path.join(self.gallery_images_url, self.gallery_thumbnail_prefix + image)
            context['images'] += [{'image' : image_url, 'thumb' : thumb_url}]

        return context


    def calulate_thumb_dimesions(self, input_dimensions):
        input_width, input_height = input_dimensions

        thumb_width = 0
        thumb_height = 0

    	input_width = input_width * 1.0
    	input_height = input_height * 1.0

    	if input_width > input_height:
    		thumb_width = self.gallery_thumbnail_size
    		thumb_height = self.gallery_thumbnail_size / input_width * input_height
    	else:
    		thumb_width = self.gallery_thumbnail_size / input_height * input_width
    		thumb_height = self.gallery_thumbnail_size

    	return (int(thumb_width), int(thumb_height))


    def render_files(self, context, output_directory, jinja_env):

        dst_dir = os.path.join(output_directory, self.gallery_images_url)

        for image in self.images:
            src_path = os.path.join(self.full_gallery_path, image)
            dst_path = os.path.join(dst_dir, self.gallery_thumbnail_prefix + image)

            print "Creating thumbnail: %s" % dst_path

            image = Image.open(src_path)
            thumbnail = image.resize(self.calulate_thumb_dimesions(image.size), Image.LANCZOS)
            thumbnail.save(dst_path, quality=self.gallery_thumbnail_quality)

        super(Gallery, self).render_files(context, output_directory, jinja_env)
