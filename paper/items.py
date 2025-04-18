# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhiwangItem(scrapy.Item):
    # define the fields for your item here like:
    学校=scrapy.Field()
    期刊=scrapy.Field()
    数量=scrapy.Field()
    属于=scrapy.Field()
    总分类=scrapy.Field()
