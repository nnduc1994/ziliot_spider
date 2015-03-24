from scrapy.contrib.spiders.crawl import CrawlSpider
from scraper_app.items import JobData
from scrapy.selector import HtmlXPathSelector
from scrapy import Request


class JobDataSpider(CrawlSpider):
    name = "manpower_fi"
    allowed_domains = ["www.manpower.fi"]
    start_urls = []
    len = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    for i in len:
        url = "https://www.manpower.fi/fin/tyon-haku/?search=&offset=%d" % i
        start_urls.append(url)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        jobs = hxs.select("//div[@class='span9 tablet-span9']/article")

        for row in jobs:
            item = JobData()
            item['title'] = row.select("./div[@class='media-body']/a/h3/text()").extract()[0].lower()
            item['link'] = "https://www.manpower.fi" + row.select("./div[@class='media-body']/a/@href").extract()[0]
            item['source'] = "www.manpower.fi"
            items.append(item)

        for item in items:
            request = Request("%s" % item['link'], callback=self.description_parse)
            request.meta['item'] = item
            yield request

    def description_parse(self, response):
        item = response.meta['item']
        item['location'] = response.xpath("//div[@class='mp-jobdetails-bold pull-left'][1]/text()").extract()[0].lower()
        description_list = response.xpath("//div[@class='mp-article-body']/section/text()").extract()

        item['description'] = ""
        for i in description_list:
            item['description'] += i

        return item
