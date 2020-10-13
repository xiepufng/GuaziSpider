# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 定义要爬取的数据
    bran = scrapy.Field()
    mileage = scrapy.Field()
    discharge = scrapy.Field()
    ascription = scrapy.Field()
    transfer = scrapy.Field()
