__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request
import datetime


class JobDataSpider(CrawlSpider):
    name = "tootukassa_ee"
    allowed_domains = ["tootukassa.ee"]
    start_urls = []
    list = []
    i = 1
    while i < 17:
        list.append(i)
        i = i + 1

    for u in list:
        url = "https://www.tootukassa.ee/toopakkumised?page=%d&results_on_page=100" % u
        start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@id='jobOfferResults']/article/table/tbody/tr")

        for row in jobs:
            item = JobData()
            item['title'] = row.select("./td[1]/a/strong/text()").extract()[0].lower()
            item['link'] = "https://www.tootukassa.ee" + row.select("./td[1]/a/@href").extract()[0]
            item['location'] = row.select("./td[4]/text()").extract()[0]
            expired_day_string = row.xpath("./td[3]/text()").extract()[0]
            item['expire_day'] = datetime.datetime.strptime(expired_day_string, "%d.%m.%Y")
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        item = response.meta['item']
        check = response.xpath("//div[@id='block-system-main']/div[3]/div[5]/p[1]/text()").extract()
        item['description'] = ""
        description_list = []

        if len(check) > 0:
            description_list = check
        else:
            description_list = response.xpath("//div[@id='block-system-main']/div[3]/div[6]/p[1]/text()").extract()

        for des in description_list:
            item['description'] += des

        return item

