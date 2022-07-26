# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MirknigItem(scrapy.Item):

    title = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    year = scrapy.Field()
    digital_format = scrapy.Field()
    pages = scrapy.Field()
    size = scrapy.Field()
    language = scrapy.Field()
    description = scrapy.Field()
