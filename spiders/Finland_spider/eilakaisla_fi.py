__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "eilakaisla_fi"
    allowed_domains = ["eilakaisla.fi"]
    start_urls = ["http://www.eilakaisla.fi/avoimet-tyopaikat"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@class='jobs-box']/p")
        for row in jobs:
            item = JobData()
            item['link'] = "http://www.eilakaisla.fi/avoimet-tyopaikat" + row.select("./a/@href").extract()[0]
            string = row.select("./a/b/text()").extract()[0]
            list_of_string = string.split(" - ")
            item['title'] = list_of_string[0].lower()
            item['location'] = list_of_string[1].lower()
            item['source'] = "www.eilakaisla.fi"
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        item = response.meta['item']
        item['description'] = ""
        description_list = response.xpath("//div[@id='content']/p/text()").extract()

        for des in description_list:
            item['description'] += des

        return item