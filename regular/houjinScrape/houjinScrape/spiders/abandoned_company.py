import scrapy
from scrapy.loader import ItemLoader
import re
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from items import HoujinItem
import datetime
class ClosedCompanySpider(scrapy.Spider):
    name = 'abandoned_company'
    allowed_domains = ['houjin.jp']
    start_urls = ['https://houjin.jp/events/closed']

    def start_requests(self):
        for url in self.start_urls:

            # using tor
            # meta = {'proxy': 'socks5://127.0.0.1:9050'}

            # default
            # meta = {'proxy': 'http://192.168.11.16:3128'}

            # yield scrapy.Request(url, meta=meta,callback=self.get_company)
            yield scrapy.Request(url,callback=self.get_corp)


    def get_corp(self, response):
        corp_links = response.xpath("//section[@class='main-section']/section/a/@href").getall()
        for corp_link in corp_links:
            corp_link = 'https://houjin.jp' + corp_link
            print(corp_link)
            yield response.follow(corp_link,self.parse_item)
        next_page = response.xpath("//a[@rel='next']/@href").get()
        next_page = 'https://houjin.jp' + next_page     
        target_date = re.findall(r'^.{10}',response.xpath("//span[contains(@class,'event-type-closed last-event')]/text()").get())[0]
        target_date = datetime.datetime.strptime(target_date,"%Y/%m/%d")
        if next_page and target_date >= datetime.datetime(2021,1,1,0,0,0):
            yield response.follow(next_page,self.get_corp)
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

        
