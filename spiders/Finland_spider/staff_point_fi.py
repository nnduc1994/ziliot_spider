__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "staff_point_fi"
    allowed_domains = ["staffpoint.fi"]
    start_urls = ["https://www.staffpoint.fi/avoimet-tyopaikat/"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//tr")

        for row in jobs:
            item = JobData()
            item['title'] = row.select("./td[1]/a/text()").extract()
            item['link'] = row.select("./td[1]/a/@href").extract()
            item['location'] = row.select("./td[6]/div/text()").extract()
            

            # We need to specify where we fetch data from
            item['source'] = "www.staffpoint.fi"
            items.append(item)

        # it return a first empty rows so we need to delete it before writing.
        items.remove(items[0])

        for item in items:
            item['title'] = item['title'][0].lower()
            item['link'] = "https://www.staffpoint.fi" + item['link'][0]
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
        item_list = []
        header = response.xpath("//div[@class='content_output']/p[1]/text()").extract()
        header = header[0] + header[1]
        item = response.meta['item']
        item['description'] = header
        return item
