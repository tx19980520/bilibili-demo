import scrapy


class EpisodesItem(scrapy.Item):
    url = scrapy.Field()
    coverpath = scrapy.Field()
    animeId = scrapy.Field()
    url = scrapy.Field()
