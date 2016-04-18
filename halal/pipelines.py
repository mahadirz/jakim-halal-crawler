# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging

class HalalPipeline(object):
    def process_item(self, item, spider):
        valid = True
        #for data in item:
            #if not data:
                #valid = False
                #raise DropItem("Missing {0}!".format(data))
        if valid:
            logging.info("Item added {0}!".format(item))
        return item
