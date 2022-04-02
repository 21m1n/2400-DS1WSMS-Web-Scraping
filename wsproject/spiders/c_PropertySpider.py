from scrapy import Field, Item
from scrapy.spiders import Spider

from selenium import webdriver
import re

import os
from time import sleep

path = os.getcwd()


class Property(Item):
    # define the fields for your item here like:
    name = Field()
    ptype = Field()
    price = Field()
    addr = Field()
    bed = Field()
    bath = Field()
    area = Field()
    amentities = Field()
    development = Field()
    subway = Field()


class PropertySpider(Spider):
    name = "PropertySpider"

    # Reading urls from links.csv
    # the urls will be passed to Selenium embeded in the middlewares.py
    try:
        with open(path+"/links.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]

    except:
        start_urls = []

    
    # Parsing response sent by Selenium:
    def parse(self, response):

        p = Property()
        print("=" * 50)
        print("parsing property details")
        print("=" * 50)

        
        if "MUST SEE" in response.xpath('//div[@class="_2F2bU _3-13Q"]//text()').extract():
            # if the page layout is "MUST SEE":
            try:
                p['name'] = response.xpath(
                    '//div[@class="_1X3XB _3oRNy"]//h1/text()').extract()
                p['addr'] = response.xpath(
                    '//div[@class="_1X3XB _3oRNy"]//h1/following-sibling::p/text()').extract()
            except:
                p['name'] = ""
                p['addr'] = ""
            try:
                ptype = response.xpath('//ol//li/a/span/text()').extract()

                if "Condos" in ptype or "Condominiums" in ptype:
                    p['ptype'] = "Condo"
                elif "HDB" in ptype or "HDB Resale" in ptype:
                    p['ptype'] = "HDB"
                elif "Landed Houses" in ptype:
                    p['ptype'] = "Landed Houses"
                else:
                    p['ptype'] = "unknown"

            except:
                p['ptype'] = ""

            try:
                p['price'] = response.xpath(
                    '//div[@class="_3nxNN"]//h3/text()').extract()[0]  # price
            except:
                p['price'] = ""

            try:
                desc = response.xpath(
                    '//div[@class="_3nxNN"]//h3/text()').extract()

                bed = desc[1]
                bath = desc[2]
                area = desc[3]

                p['bed'] = re.search(r"(\d*)", bed).group(1)
                p['bath'] = re.search(r"(\d*)", bath).group(1)
                p['area'] = re.search(r"([\d+\,]*\d*)", area).group(1)

            except:
                p['bed'] = ""
                p['bath'] = ""
                p['area'] = ""

            try:
                p['amentities'] = response.xpath(
                    '//div[@class="_3arfp"]//text()').extract()
            except:
                p['amentities'] = ""

            try:
                p['development'] = " ".join(response.xpath(
                    '//table[@class="AIQgb"]//text()').extract())
            except:
                p['development'] = ""

            try:
                p['subway'] = response.xpath(
                    '//span[contains(@class,"Tappable-inactive")]//div[@class="EE0Og"]/text()').extract()
            except:
                p['subway'] = ""

        else:

            # if the page layout is "NORMAL":
            try:
                p['name'] = response.xpath(
                    '//*[@class="_3k7xe"]//h1/text()').extract()
            except:
                p['name'] = ""

            try:
                ptype = response.xpath('//ol//li/a/span/text()').extract()

                if "Condos" in ptype or "Condominiums" in ptype:
                    p['ptype'] = "Condo"
                elif "HDB" in ptype or "HDB Resale" in ptype:
                    p['ptype'] = "HDB"
                elif "Landed Houses" in ptype:
                    p['ptype'] = "Landed Houses"
                else:
                    p['ptype'] = "unknown"

            except:
                p['ptype'] = ""

            try:
                p['price'] = response.xpath(
                    '//*[@class="_3Iom7"]//h3/text()').extract()  # price
            except:
                p['price'] = ""

            try:
                p['addr'] = response.xpath(
                    '//*[@class="_3k7xe"]/*[@class="x0JSc"]/text()').extract()
            except:
                p['addr'] = ""

            try:
                desc = response.xpath(
                    '//*[@class="x0JSc _1QR5z"]/text()').extract()

                p['bed'] = ""
                p['bath'] = ""
                p['area'] = ""

                for i, x in enumerate(desc):
                    if 'Beds' in x:
                        p['bed'] = re.search(r"(\d*)", desc[i]).group(1)
                    if 'Baths' in x:
                        p['bath'] = re.search(r"(\d*)", desc[i]).group(1)
                    if 'sqft' in x:
                        p['area'] = re.search(
                            r"([\d+\,]*\d*)", desc[i]).group(1)

            except:
                p['bed'] = ""
                p['bath'] = ""
                p['area'] = ""

            try:
                p['amentities'] = response.xpath(
                    '//*[@class="_2M8p3"]//p/text()').extract()
            except:
                p['amentities'] = ""

            try:
                p['development'] = " ".join(response.xpath(
                    '//*[@class="_70VMS"]/p/text()').extract())
            except:
                p['development'] = ""

            try:
                p['subway'] = response.xpath(
                    '//span[contains(@class,"Tappable-inactive")]//div[@class="EE0Og"]/text()').extract()
            except:
                p['subway'] = ""

        yield p
