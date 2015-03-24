__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy import Request
import datetime


class JobDataSpider(CrawlSpider):
    name = "fkaa_ee"
    allowed_domains = ["xn--td-fkaa.ee"]
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    start_urls = []
    for u in list:
        url = "http://www.xn--td-fkaa.ee/index/dashboard-params/page/%d" % u
        start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@id='content']/div[6]/div/table/tr")

        for job in jobs:
            item = JobData()
            item['title'] = job.select("./td[2]/b[1]/a/text()").extract()[0].lower()
            item['link'] = "http://www.xn--td-fkaa.ee/" + job.select("./td[2]/b[1]/a/@href").extract()[0]
            item['location'] = job.select("./td[2]/b[2]/text()").extract()[0].lower().strip()
            expired_day_string = job.select("./td[4]/text()").extract()[1].strip()
            item['expire_day'] = datetime.datetime.strptime(expired_day_string, "%d.%m.%Y")
            items.append(item)
        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        item = response.meta['item']
        if len(response.xpath("//div[@class='eleven columns']/img/@src").extract()) > 0:
            item['description'] = response.xpath("//div[@class='eleven columns']/img/@src").extract()[0]
        elif len(response.xpath("//div[@class='eleven columns']/p/span/text()").extract()) > 0:
            item['description'] = response.xpath("//div[@class='eleven columns']/p/span/text()").extract()[0]
        else:
            description_list = response.xpath("//div[@class='eleven columns']/text()").extract()
            item['description'] = ""
            for des in description_list:
                item['description'] += des
            item['description'] = item['description'].strip()
        return item
