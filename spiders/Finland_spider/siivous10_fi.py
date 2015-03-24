__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "siivous10_fi"
    allowed_domains = ["siivous10.fi"]
    start_urls = ["http://siivous10.fi/category/tyopaikat/"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@id='content']/div")
        jobs.remove(jobs[-1])
        for row in jobs:
            item = JobData()
            item['title'] = row.select("./div[@class='post-content']/h2/a/text()").extract()[0].lower()
            item['link'] = row.select("./div[@class='post-content']/h2/a/@href").extract()[0]
            item['location'] = "uusima, helsinki, vantaa, espoo"
            item['source'] = "www.siivous10.fi"
            item['description'] = ""
            info = row.select("./div[@class='post-content']/p/text()").extract()
            for des in info:
                item['description'] += des
            item['sponsor'] = 1
            items.append(item)
        return items


