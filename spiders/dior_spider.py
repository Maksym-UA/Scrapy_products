# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import DropItem
from dior_scrape.items import DiorScrapeUrls
from dior_scrape.items import DiorProduct
import re
import json

product_ids = []   # storage of unique products for verification
page_products = []  # storage of products from one link
products_discriptions = []  # storage of products desscription


class DiorSpider(CrawlSpider):
    # The name of the spider
    name = "dior_spider"
    # The domains that are allowed (links to other domains are skipped)
    allowed_domains = ["dior.com"]
    start_urls = [
        "https://www.dior.com/en_us",
        ]

    # This spider has one rule: extract all (unique and canonicalized) links,
    # follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method for parsing items
    def parse_items(self, response):
        link_data = []  # The list of link items found on the particular page

        # Only extract canonicalized and unique links (w/h respect to the
        # current page)
        # filtering of duplicate/irrelavant URLs is done the pipeline
        links = LinkExtractor(
            canonicalize=True,
            unique=True).extract_links(response)

        # Now go through all the found links and look for goods on each link
        for link in links:
            # print(type(link.url))

            # Check whether the domain of the URL of the link is allowed;
            # so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True

            if is_allowed:
                # look for js variables that contain array of objects/products
                data = re.findall("var GTMImpressions =(.+?);\n",
                                  response.body.decode("utf8"), re.S)
                # print("***** length %s " % len(data))

                if len(data) > 0:  # verify the response is not None
                    data_str = data[0]  # convert from unicode to string
                    d_str = data_str[2:-1]  # .strip("\").split(",")
                    # remove leading and ending commas
                    result = re.sub(r"^\s+", "", d_str)
                    # print(type(result))
                    data_to_json = json.loads(result)

                    # alternative searches of product info
                    # data = response.css(".block-fp")
                    # discription1 = data[0].css("p::text").extract_first()
                    # discription2 = data[1].css("p::text").extract_first()

                    # find additional info (here it is within one div)
                    d = response.css(".suggestions-wrapper").extract()

                    if d:
                        product_discr = ProductDiscription()
                        data = re.findall(
                            "id(.+?)\,", d[0].decode("utf-8"), re.S)[0]
                        item_sku_id = data[3:-1].encode("utf-8")
                        discription3 = re.findall(
                            "suggestions-product-text(.+?)\<",
                            d[0].decode("utf-8"), re.S)[0][2:].encode("utf-8")
                        product_discr["prod_sku_id"] = item_sku_id
                        product_discr["description"] = discription3
                        products_discriptions.append(product_discr)

                    item = DiorScrapeUrls()  # initiate scrapy link_item object
                    # item['dior_url'] = response.url
                    item['url_to'] = link.url
                    if "en_us" in item["url_to"]:
                        region = 'en_us'

                    # create a new item and add it to the list of
                    # found items
                    d_len = len(data_to_json['ecommerce']['impressions'])-1
                    for i in range(d_len):
                        product = DiorProduct()
                        product_id = data_to_json['ecommerce']['impressions'][i]["id"]
                        if product_id not in product_ids:
                            product["prod_sku_id"] = product_id.encode("utf8")
                            product["code"] = data_to_json['ecommerce']['impressions'][i]["code"].encode("utf-8")
                            product["name"] = data_to_json['ecommerce']['impressions'][i]["name"].encode("utf-8")
                            product["price"] = data_to_json['ecommerce']['impressions'][i]["price"].encode("utf-8")
                            product["region"] = region
                            product["brand"] = data_to_json['ecommerce']['impressions'][i]["brand"].encode("utf-8")
                            product["description"] = ""
                            for i in range(len(products_discriptions)-1):
                                if products_discriptions[i]["prod_sku_id"] == product["prod_sku_id"]:
                                    product["description"] = products_discriptions[i]["description"]

                            product_ids.append(product_id)
                            page_products.append(dict(product))
                        else:
                            print("duplicate unit")

                    if len(page_products) > 0:  # populate list only w/ actual
                        # item["page_products"] = page_products
                        link_data.append(item)

        with open('dior.json', 'w') as fd:
            json.dump(page_products, fd, indent=3, sort_keys=True)

        print("------------------------------")
        print("****One URL crawled****")
        print("------------------------------")

        # Return all the found items
        return link_data

# scrapy crawl dior_spider -o links.csv -t csv
# scrapy crawl dior_spider -o dior_goods.json # save to json
