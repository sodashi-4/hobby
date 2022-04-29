import scrapy


class ClosedCompanySpider(scrapy.Spider):
    name = 'closed_company'
    allowed_domains = ['houjin.jp/events/closed']
    start_urls = ['http://houjin.jp/events/closed/']

    def parse(self, response):
        pass
