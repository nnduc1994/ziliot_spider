__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "go_on_fi"
    allowed_domains = ["go-on.fi"]
    start_urls = ["http://www.go-on.fi/tyopaikat?start=0",
                  "http://www.go-on.fi/tyopaikat?start=20",
                  "http://www.go-on.fi/tyopaikat?start=40",
                  "http://www.go-on.fi/tyopaikat?start=60",
                  "http://www.go-on.fi/tyopaikat?start=80"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//tr")

        for row in jobs:
            item = JobData()
            item['title'] = row.select("./td[1]/a/text()").extract()
            item['link'] = row.select("./td[1]/a/@href").extract()
            item['location'] = row.select("./td[2]/text()").extract()
            # We need to specify where we fetch data from
            item['source'] = "www.go-on.fi"
            items.append(item)

        # it return a first empty rows so we need to delete it before writing.
        items.remove(items[0])

        for item in items:
            item['title'] = item['title'][0].lower()
            item['link'] = "http://www.go-on.fi" + item['link'][0]
            item['location'] = item['location'][0]
            item['location'] = " ".join(item['location'].split()).lower()
            # check if location is empty or not
            if item['location'] == "":
                item['location'] = "find more about location on website"

        # Now we are going to get the description of the job
        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        description_list = response.xpath("//div[@class='col-md-6']/p/text()").extract()
        item = response.meta['item']
        item['description'] = ""
        for i in description_list:
            item['description'] += i
        return item
