__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request

class JobDataSpider(CrawlSpider):
    name = "elektrik24_ee"
    allowed_domains = ["elektrik24.ee"]
    start_urls = ["http://elektrik24.ee/too-ja-praktikapakkumised?page=1"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//table[@class='datatable']/tbody/tr[@class='']")

        for row in jobs:
            item = JobData()
            item['title'] = row.select("./td[1]/a/text()").extract()[0].lower()
            item['link'] = row.select("./td[1]/a/@href").extract()[0]
            item['location'] = row.select("./td[2]/text()").extract()[0].lower().strip()
            item['source'] = "www.elektrik24.ee"
            item['sponsor'] = 1
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        description_list = response.xpath("//div[@id='content-small']/ul/li/text()").extract()
        if len(description_list) < 1:
            description_list = response.xpath("//div[@id='content-small']/li/text()").extract()
            list = description_list
            if len(description_list) < 1:
                        description_list = response.xpath("//div[@id='content-small']/p/text()").extract()



        item = response.meta['item']
        item['description'] = ""
        for i in description_list:
            item['description'] += i
        return item
