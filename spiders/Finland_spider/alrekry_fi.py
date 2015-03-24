__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "alrekry_fi"
    allowed_domains = ["alrekry.fi"]
    start_urls = ["http://www.alrekry.fi/avoimet_tyopaikat.php"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//ul[@class='feed']/li")

        for row in jobs:
            item = JobData()
            item['link'] = "http://www.alrekry.fi/" + row.select("./a/@href").extract()[0].lower()
            item['title'] = row.select("./a/b/text()").extract()[0].lower()
            item['source'] = "www.alrekry.fi"
            string = row.select("./a/text()").extract()[0]
            string = string.replace(", ", "")
            string = string.strip()
            if string == (""):
                string = "unknow unknow"
            list_of_string = string.split(" ")
            if len(list_of_string) == 1:
                item['location'] = list_of_string[0].lower()
            else:
                item['location'] = list_of_string[1].lower()
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        item = response.meta['item']
        item['description'] = ""
        description_list = response.xpath("//span[@id='kuvausteksti']/text()").extract()
        for des in description_list:
            item['description'] += des
        return item
