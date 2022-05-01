# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import os 
print(os.getcwd())
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='../gcp-sodashi-4-scrape.json'