__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "vmp_fi"
    allowed_domains = ["vmp.fi"]
    start_urls = []
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i in list:
        url = "http://www.vmp.fi/Suomi/fi/Tyontekija/Avoimet+tyopaikat/?pagenr=%d&tabselected=vacancylist" % i
        start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@id='fragment-2']/ul[@class='link-list']/li")

        for row in jobs:
            item = JobData()
            item['link'] = row.select("./a/@href").extract()[0]
            string = row.select("./a/text()").extract()[0]
            list_of_string = string.split(", ")
            count = string.count(", ")
            if count == 1:
                item['title'] = list_of_string[0].lower()
                item['location'] = list_of_string[1].lower()
            else:
                item['title'] = list_of_string[0].lower()
                item['location'] = list_of_string[-1].lower()

            item['source'] = "www.vmp.fi"
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        description = response.xpath('//div[@id="fragment-3"]/table/tr[2]//td[2]/text()').extract()
        item = response.meta['item']
        item['description'] = description[0]
        return item


