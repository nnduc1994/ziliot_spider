__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request

class JobDataSpider(CrawlSpider):
    name = "experis_fi"
    allowed_domains = ["experis.fi"]
    start_urls = []
    len = [0, 10, 20, 30]
    for i in len:
        url = "https://www.experis.fi/fin/etsi_tyopaikkoja/?search=&offset=%d" % i
        start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@class='span9 tablet-span9']/article[@class='mp-job-hit media']")

        for row in jobs:
            item = JobData()
            string = row.select("./div[@class='media-body']/a/h3/text()").extract()[0].lower()
            if ", " in string:
                string_list = string.split(", ")
                item['title'] = string_list[0]
                item['location'] = string_list[1]
            else:
                item['title'] = string
                item['location'] = "all"

            item['link'] = "https://www.experis.fi" + row.select("./div[@class='media-body']/a/@href").extract()[0]
            item['source'] = "www.experis.fi"
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        description_list = response.xpath("//div[@class='mp-article-body']/section/text()").extract()
        item = response.meta['item']
        item['description'] = ""
        for i in description_list:
            item['description'] += i
        return item


