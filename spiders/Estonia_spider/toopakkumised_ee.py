__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request
import datetime

class JobDataSpider(CrawlSpider):
    name = "toopakkumised_ee"
    allowed_domains = ["toopakkumised.com"]
    list = []
    start_urls = ["http://www.toopakkumised.com"]
    i = 2
    while i < 24:
        list.append(i)
        i = i + 1

    for u in list:
        url = "http://www.toopakkumised.com/page%d.html" % u
        start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//tr[@class='odd' or @class='even']")
        for row in jobs:
            item = JobData()
            if len(row.select("./td[@class='cell1']/a/text()").extract()) > 0:
                item['title'] = row.select("./td[@class='cell1']/a/text()").extract()[0].lower()
                item['link'] = "http://www.toopakkumised.com" + row.select("./td[@class='cell1']/a/@href").extract()[0]
                item['location'] = row.select("./td[@class='cell4']/text()").extract()[0].lower().strip()
                item['source'] = "toopakkumised.com"
                items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        item = response.meta['item']
        expired_day_string = response.xpath("//table/tr[2]/td/table/tr[7]/td[2]/text()").extract()[0]
        item['expire_day'] = datetime.datetime.strptime(expired_day_string, "%d.%m.%Y")

        description_list = []
        description = response.xpath("//table/tr[2]/td/table/tr[5]/td[2]/text()").extract()[0]
        requirements = response.xpath("//table/tr[2]/td/table/tr[6]/td[2]/text()").extract()[0]
        description_list.append(description)
        description_list.append(requirements)

        item['description'] = ""

        for des in description_list:
            item['description'] += des

        return item
