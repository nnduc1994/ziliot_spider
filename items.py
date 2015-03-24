__author__ = 'nnduc_000'
from scrapy.item import Item, Field


class JobData(Item):
    title = Field()
    link = Field()
    location = Field()
    description = Field()
    source = Field()
    expire_day = Field()
    sponsor = Field()
