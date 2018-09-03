# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiorScrapeUrls(scrapy.Item):
    # The source URL
    # dior_url = scrapy.Field()
    # The destination URL
    url_to = scrapy.Field()
    page_products = scrapy.Field(serializer=str)


class DiorProduct(scrapy.Item):
    # extend item field with region meta data
    # page_response = scrapy.Field(serializer=str)
    region = scrapy.Field(serializer=str)
    name = scrapy.Field(serializer=str)
    price = scrapy.Field(serializer=str)
    prod_sku_id = scrapy.Field(serializer=str)
    code = scrapy.Field(serializer=str)
    brand = scrapy.Field(serializer=str)
    available = scrapy.Field(serializer=str)
    region = scrapy.Field(serializer=str)
    description = scrapy.Field(serializer=str)


class ProductDiscription(scrapy.Item):
    prod_sku_id = scrapy.Field(serializer=str)
    description = scrapy.Field(serializer=str)
