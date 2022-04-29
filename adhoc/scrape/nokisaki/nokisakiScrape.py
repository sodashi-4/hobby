import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from time import sleep
import re
import warnings
warnings.simplefilter('ignore')
import requests_cache
import datetime

expire_after = datetime.timedelta(weeks=1)
requests_cache.install_cache(cache_name='nokisaki', backend='sqlite', expire_after=expire_after)

df = pd.read_csv('start.csv')

def parce_item(x):    
    if type(x) == str:
        x = re.sub(r"\s","",x)
        return x
    elif type(x) == list:
        lists = []
        for li in x:
            lists.append(re.sub(r"\s","",li)) 
        return lists
    else:
        print(type(x))

for i in range(1,10181):
    sleep(0.35)
    print(i)
    request_url = f'https://business.nokisaki.com/spaces/detail/{i}'

    res = requests.get(request_url)

    source_block = BeautifulSoup(res.text, 'html.parser')
    # source_block

    source = html.fromstring(res.text)
    print(source.xpath("//h1/text()")[0])
    if source.xpath("//h1/text()")[0] != 'エラー':
        use_case_lists = ['販売可','車出店可','PR可','撮影可','教室/セミナー可','防音','鏡あり']
        facility_lists = ['駐車場','鍵','水道','扉','シャッター','床(砂利・土)','床(砂利・土以外)','電気コンセント','照明','暖房','冷房','屋根','トイレ','インターネット']

        name = source.xpath("//h1[@class='space-title']")[0].text

        price = source.xpath("//table//td/span[@class='price-amount']")[0].text

        space_info = source.xpath("//tr[@class='type-extent']/td/text()") # type/広さ

        space_type = space_info[0].split('/')[0]
        space_breadth = space_info[0].split('/')[1]

        use_cases = source.xpath("//div[contains(@class,'space-condition')]//span[contains(@class,'disactive')]/text()[2]")

        facility = source.xpath("//div[contains(@class,'space-setsubi')]//div[contains(@class,'expandable-content')]//div[contains(@class,'disactive')]/text()[2]")   

        address = ''.join(source.xpath("//div[contains(@class,'space-address')]/h3/text()"))
        image = re.findall(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+',source.xpath("//div[@class='image']/@style")[0])[0]
        discription = source.xpath("//div[@class='space-pr']/text()")

        row_data = {
            'name': parce_item(name), 
            'price': parce_item(price), 
            'address': parce_item(address), 
            'discription': parce_item(discription), 
            'space_type': parce_item(space_info[0].split('/')[0]),
            'space_breadth': parce_item(space_info[0].split('/')[1]),
            'use_case': list(set(parce_item(use_cases)) ^ set(use_case_lists)),
            'facility': list(set(parce_item(facility)) ^ set(facility_lists)),
            'image': image,
        }
        print(row_data)
        df = df.append(row_data, ignore_index=True, sort=False)
    else:
        row_data = {
            'name': '-',
            'price': '-',
            'address': '-',
            'discription': '-',
            'space_type': '-',
            'space_breadth': '-',
            'use_case': '-',
            'facility': '-',
            'image': '-'
        }
        print(row_data)
        df = df.append(row_data, ignore_index=True, sort=False)

df.to_csv("nokisaki.csv",index=False)

