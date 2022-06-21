from gc import callbacks
import scrapy
from scrapy.loader import ItemLoader
import re
import os
import requests
import sys
from lxml import html

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from items import HoujinItem
import datetime

URL = 'https://houjin.jp/'

class ClosedCompanySpider(scrapy.Spider):
    name = 'abandoned_company'
    start_urls = ['https://houjin.jp/events/closed']

    def start_requests(self):
        for url in self.start_urls:

            # using tor
            # meta = {'proxy': 'socks5://127.0.0.1:9050'}

            # default
            # meta = {'proxy': 'http://192.168.11.16:3128'}

            # yield scrapy.Request(url, meta=meta,callback=self.get_company)
            yield scrapy.Request(url,callback=self.get_corp)


    def get_corp(self,response):
        for i in range(20,2):
            request_uri = f'https://houjin.jp/events?from=&page={i}&pref_id=&to=&type=closed'
            res = requests.get(request_uri)
            source = html.fromstring(res.text)
            paths = source.xpath("//section[@class='c-corp-item']/a/@href")
            for path in paths:
                yield scrapy.Request(URL + path, callback=self.parse_item)


    def parse_item(self, response):
        # with open(f"{self.name}.html", "w") as f:
        #     f.write(response.text)
        loader = ItemLoader(item=HoujinItem(), response=response)
        loader.add_xpath('corp_number',"//table//tr[1]/td/text()")
        loader.add_xpath('corp_name',"//h1[contains(@class,'corp-name')]/text()")
        loader.add_xpath('post_number',"//table//tr[4]/td/p[1]/text()")
        corp_address = "".join(response.xpath("//td[@class='corp-address']//span/text()").getall())
        loader.add_value('address',corp_address)
        loader.add_xpath('president_name',"//table//tr[5]/td/text()")
        loader.add_xpath('url',"//table//tr[6]/td/text()")
        loader.add_xpath('tel',"//table//tr[7]/td/text()")
        loader.add_xpath('corp_created_at',"//table//tr[8]/td/text()")
        abandoned_at = re.findall(r'^.{10}',response.xpath("//div[contains(@class,'company-notify-ribbon notify-close')]/p/text()").get())
        loader.add_value('corp_abandoned_at', abandoned_at)
        loader.add_xpath('industry',"//table//tr[9]/td/text()")
        loader.add_xpath('corp_num_created_at',"//table//tr[10]/td/p[1]/text()")
        loader.add_value('scraped_date', str(datetime.date.today()))
        yield loader.load_item()