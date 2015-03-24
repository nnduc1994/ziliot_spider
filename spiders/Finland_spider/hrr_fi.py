__author__ = 'nnduc_000'

from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "hrr_fi"
    allowed_domains = ["hrr.rekrytointi.com"]
    start_urls = []
    len = [0, 1, 2, 3, 4, 5]
    for i in len:
        url = "https://hrr.rekrytointi.com/paikat/index.php?o=A_LOJ&list=1&StartPage=%d&rspvt=ftlab6vepygocgwkwkookoc00cgggo8" % i
        start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//table[@class='results clickable_multi']/tr")

        for row in jobs:
            item = JobData()
            check = row.select("./td[1]/a/text()").extract()
            if len(check) > 0:
                item['title'] = check[0].lower()
                item['link'] = "https://hrr.rekrytointi.com" + row.select("./td[1]/a/@href").extract()[0]
                item['location'] = row.select("./td[4]/a/text()").extract()[0].lower()
                # We need to specify where we fetch data from
                item['source'] = "hrr.rekrytointi.com"
                items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        description_list = response.xpath("//div[@class='job_description']/p/text()").extract()
        item = response.meta['item']
        item['description'] = ""
        for i in description_list:
            item['description'] += i
        if item['description'] == "":
            item['description'] = "Click to find more information"
        return item
