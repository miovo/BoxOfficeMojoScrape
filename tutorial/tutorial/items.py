# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieInfo(scrapy.Item):

    year = scrapy.Field()
    title = scrapy.Field()
    gross_rev = scrapy.Field()
    distributor = scrapy.Field()
    theaters = scrapy.Field()
    release_date = scrapy.Field()

