# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class DiorScrapePipeline(object):

    def __init__(self):
        self.url_seen = set()

    # filter for dropping duplicate or irrelavant urls
    def process_item(self, item, spider):

        if item["url_to"] in self.url_seen:
            # print("------------------------------")
            # print("****Duplicate URL found****")
            # print("------------------------------")
            raise DropItem("Duplicate url found")
            pass
        elif "https://www.dior.com" not in item["url_to"]:
            raise DropItem("Irrelavant domain")
        elif "en_us" not in item["url_to"]:
            raise DropItem("Irrelavant domain")
            pass
        else:
            self.url_seen.add(item["url_to"])
            print("------------------------------")
            print("****Pipeline finished****")
            print("------------------------------")
            return item
        # print(self.url_seen)
