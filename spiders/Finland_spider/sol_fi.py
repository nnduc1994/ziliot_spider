__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request
import datetime

class JobDataSpider(CrawlSpider):
    name = "sol_fi"
    allowed_domains = ["sol.fi"]
    list = [1, 2, 3, 4, 5, 6, 7]
    start_urls = []
    for i in list:
        url = "http://www.sol.fi/henkilostopalvelut/tyonhakijoille/avoimet-tyopaikat.html?p1154=%d" % i
        start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//table[@class='job-search-results']/tbody/tr")
        jobs.remove(jobs[0])

        for row in jobs:
            item = JobData()
            item['title'] = row.select("./td[1]/a/text()").extract()[0].lower()
            item['link'] = row.select("./td[1]/a/@href").extract()[0]
            # We need to specify where we fetch data from
            item['source'] = "www.sol.fi"
            day_string = row.select("./td[2]/text()").extract()[0]
            day_list = day_string.split(" ")
            item['expire_day'] = datetime.datetime.strptime(day_list[0], "%d.%m.%Y")
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        paragarph = response.xpath("//div[@id='content']/div/div[4]/p")
        if len(paragarph) < 1:
             paragarph = response.xpath("//div[@id='content']/div/div[4]")
             if len(paragarph) < 1:
                paragarph = response.xpath("//div[@id='content']/div/div[4]/div[4]")
                if len(paragarph) < 1:
                    paragarph = response.xpath("//div[@id='content']/div/div[4]/div[1]/span/p")
                    if len(paragarph) < 1:
                        paragarph = response.xpath("//div[@id='content']/div/div[4]/div")
        item = response.meta['item']
        item['location'] = response.xpath("//div[@id='content']/div/div[4]/table/tr[2]/td/text()").extract()[1].lower().strip()
        item['description'] = ""
        for p in paragarph:
            text = p.select("./text()").extract()
            for t in text:
                item['description'] += t
        return item