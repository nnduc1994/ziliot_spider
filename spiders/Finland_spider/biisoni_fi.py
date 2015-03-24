__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "biisoni_fi"
    allowed_domains = ["biisoni.fi"]
    start_urls = ["http://www.biisoni.fi/etsin_tyota/tyopaikat"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@id='twocols']/table/tr")
        jobs.remove(jobs[0])
        for row in jobs:
            item = JobData()
            item['title'] = row.select("./td[1]/a/text()").extract()[0].lower()
            if "avoin" not in item['title']:
                item['link'] = row.select("./td[1]/a/@href").extract()[0]
                item['location'] = row.select("./td[2]/text()").extract()[0].lower()
                # We need to specify where we fetch data from
                item['source'] = "www.biisoni.fi"
                items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        paragarph = response.xpath("//div[@id='twocols']/p")
        item = response.meta['item']
        item['description'] = ""
        for p in paragarph:
            text = p.select("./text()").extract()
            for t in text:
                item['description'] += t
        return item
