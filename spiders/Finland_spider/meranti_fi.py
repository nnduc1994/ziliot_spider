__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "meranti_fi"
    allowed_domains = ["meranti.fi"]
    start_urls = ["http://www.meranti.fi/yhteys/avoimet_tyopaikat"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@id='main']/div[@class='vacancy']")

        for row in jobs:
            item = JobData()
            item['title'] = row.select("./h3/text()").extract()[0].lower()
            item['link'] = "http://www.meranti.fi/yhteys/avoimet_tyopaikat"
            item['location'] = "oulu"
            # We need to specify where we fetch data from
            item['source'] = "www.meranti.fi"
            item['sponsor'] = 1
            item['description'] = row.select("./div[@class='vacancy-content']/text()").extract()[0].strip()
            if item['description'] == "":
                item['description'] = row.select("./div[@class='vacancy-content']/p/text()").extract()[0].strip()
            items.append(item)

        return items


