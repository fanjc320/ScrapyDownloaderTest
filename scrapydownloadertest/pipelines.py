# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
# from urlparse import urlparse
from urllib.parse import urlparse
from os.path import basename,dirname,join

class ScrapydownloadertestPipeline(object):
    def process_item(self, item, spider):
        print("item:", item)
        return item

    # def file_path(self, request, response=None, info=None):
    #     path=urlparse(request.url).path
    #     temp=join(basename(dirname(path)),basename(path))
    #     # return '%s/%s' % (basename(dirname(path)), basename(path))
    #     return "./"


# Custom Images pipeline example：
# https://doc.scrapy.org/en/1.3/topics/media-pipeline.html#custom-images-pipeline-example

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print("MyImagesPipeline image_url:", image_url)
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item