from selenium import webdriver

from scrapy import Field, Item
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.exceptions import CloseSpider

from time import sleep
import re

class Link(Item):
    link = Field()
    ID = Field()


URL = "https://www.99.co/singapore/sale/?page_num=%d"
SLEEP_TIME = 5
SHORT_BREAK = 60


class LinkListsSpider(Spider):
    name = "LinkSpider"

    # Prompt: asking for page range
    print("Please specify the page range (min=1, max=285): ")
    FIRST_PAGE = int(input("starting page: "))
    LAST_PAGE = int(input("last page: "))

    start_urls = [URL % FIRST_PAGE]

    def __init__(self, FIRST_PAGE=FIRST_PAGE, LAST_PAGE=LAST_PAGE):
        # store the page range in the spider
        self.page_number = FIRST_PAGE
        self.MAX_PAGE = LAST_PAGE

    def parse(self, response):

        print('=' * 50)
        print("Scraping page: ", self.page_number)
        print('=' * 50)

        # extracting individual property urls on the current listing page 
        # the url can be shortened by "https://www.99.co/singapore/sale/property/" + an unique ID
        # for instance:
        # https://www.99.co/singapore/sale/property/lentor-place-landed-9NCFy3hBAtkdCYKA8Y4Drk?enquiry_position=1&enquiry_source=Search
        # is equivalent to:
        # https://www.99.co/singapore/sale/property/9NCFy3hBAtkdCYKA8Y4Drk
        # "9NCFy3hBAtkdCYKA8Y4Drk" is the ID being extracted
        # altough we only need the url, but we are saving both url and ID for clarity purposes
        urls = response.xpath('//*[@class="_1XIV4"]//a/@href').extract()
        for url in urls:
            l = Link()
            try:
                l["ID"] = re.findall(r"([A-Za-z\d]{20,23})", url)[0]
                l["link"] = "https://www.99.co/singapore/sale/property/" + l["ID"]
            except:
                l["ID"] = ""
                l["link"] = ""

            yield l

        if self.page_number % 10 == 0:
            sleep(SHORT_BREAK)  # rest for 1 min for each 10 pages scraped
        else:
            sleep(SLEEP_TIME)

        self.page_number += 1 # go to next page

        # request the next page until the spider reaches max page number
        if self.page_number <= self.MAX_PAGE:
            yield Request(url=URL % self.page_number, callback=self.parse, dont_filter=True)
        else:
            raise CloseSpider("reach last page")

