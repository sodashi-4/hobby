from doctest import OutputChecker
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
import re
import numpy as np


def remove_space(element):
    return element.strip()

def list_combine(element):
    if type(element) == list:
        return " ".join(element)


def extract_floor(element):
    floor = re.findall(r"\d+F", element)
    return floor
    
class HoujinItem(scrapy.Item):
    corp_number = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    corp_name = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    post_number = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    address = scrapy.Field(
        # input_processor = MapCompose(list_combine),
        output_processor=TakeFirst()
        )
    president_name = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    url = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    tel = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    corp_created_at = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    corp_abandoned_at = scrapy.Field(
        output_processor=TakeFirst()
    )
    industry = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    corp_num_created_at = scrapy.Field(
        # input_processor = MapCompose(list_combine,remove_space),
        output_processor=TakeFirst()
        )
    scraped_date  = scrapy.Field(
        output_processor = TakeFirst()
    )

# bqのスキーマ定義
#     [{
#     "name":"corp_number", 
#     "type": "INTEGER",
#     "mode": "NULLABLE"
# },{
#     "name": "corp_name", 
#     "type": "STRING",
#     "mode": "NULLABLE"
# },{
#     "name": "post_number",
#     "type": "STRING",
#     "mode": "NULLABLE"
# },{
#     "name": "address",
#     "type": "STRING",
#     "mode": "NULLABLE"
# },{
#     "name": "president_name",
#     "type": "STRING",
#     "mode": "NULLABLE"
# },{
#     "name": "url",
#     "type": "STRING",
#     "mode": "NULLABLE"
# },{
#     "name": "corp_created_at",
#     "type": "DATE",
#     "mode": "NULLABLE"
# },{
#     "name": "industry",
#     "type": "STRING",
#     "mode": "NULLABLE"
# },{
#     "name": "corp_num_created_at",
#     "type": "DATE",
#     "mode": "NULLABLE"
# },{
#     "name": "scraped_date",
#     "type": "STRING",
#     "mode": "NULLABLE"
# }]