__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "opteam_fi"
    allowed_domains = ["opteam.fi"]
    start_urls = ["http://www.opteam.fi/tyonhakijalle/avoimet-tyopaikat/"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//tr")
        jobs.remove(jobs[0])

        for row in jobs:
            item = JobData()
            item['title'] = row.select("./td[1]/a/text()").extract()[0].lower()
            item['link'] = row.select("./td[1]/a/@href").extract()[0]
            item['location'] = row.select("./td[2]/text()").extract()[0].lower()
            # We need to specify where we fetch data from
            item['source'] = "www.opteam.fi"
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        description_list = response.xpath("//div[@class='medium-8 columns white box']/p/text()").extract()
        item = response.meta['item']
        item['description'] = ""
        for i in description_list:
            item['description'] += i
        return item





