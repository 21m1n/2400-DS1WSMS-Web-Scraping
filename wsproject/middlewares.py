# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from time import sleep

SLEEP_TIME = 3
SCROLL_PAUSE_TIME = 2

class SeleniumMiddleware(object):
    def __init__(self):
        self.timeout = 50
        options = webdriver.firefox.options.Options()
        # disable pop-ups
        options.set_preference('dom.webnotifications.enabled', False)
        options.set_preference('dom.push.enabled', False)
        self.driver = webdriver.Firefox(
            options=options, executable_path="/usr/local/bin/geckodriver")
        # set window size
        self.driver.set_window_size(1920, 1080)
        # set timeout
        self.driver.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def process_request(self, request, spider):
        if spider.name == "PropertySpider":

            # launch webdriver and get url when the spider is PropertySpider
            self.driver.get(request.url)
            sleep(SLEEP_TIME)

            if "Page not found" in self.driver.title: # handling 404 page (property sold out or page deleted)
                print("=" * 50)
                print("page 404")
                print("=" * 50)
                return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8", request=request)

            else:

                print("=" * 50)
                print("selenium is working")
                print("=" * 50)

                #########################
                # webdriver scrolling
                #########################

                Y = 1000 # define a incremental height

                page_height = self.driver.execute_script(
                    "return document.body.scrollHeight")  # return the document height

                # scrolling until webdriver reaches the bottom of the page
                while Y < page_height: 
                    # scroll down to specified height Y
                    self.driver.execute_script(
                        "window.scrollTo(0, {});".format(Y))
                    # Wait to load page
                    sleep(SCROLL_PAUSE_TIME)

                    Y = min(Y + 1000, page_height) # increase Y by 1000 each time

                # load page source
                source = Selector(text=self.driver.page_source)

                #########################
                # locate interactive contents
                #########################

                # if page layout is "MUST_SEE", scroll the webdriver to "neighbourhood" section
                # by using scrollIntoView            
                if "MUST SEE" in source.xpath('//div[@class="_2F2bU _3-13Q"]//text()').extract():

                    try:
                        # locate and navigate to the neighbourhood section
                        element = self.driver.find_element(
                            By.XPATH, '//h3[contains(text(), "neighbourhood")]')
                        self.driver.execute_script(
                            'arguments[0].scrollIntoView(true);', element)
                        # wait for loading element
                        sleep(SLEEP_TIME)
                        # click on the MRT stations element if it exists
                        self.driver.find_element(
                            By.XPATH, '//div[contains(text(), "MRT Stations")]').click()
                        sleep(SLEEP_TIME)
                        return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8", request=request)

                    except:
                        return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8", request=request)

                else:
                    # if page layout is normal, find the "neighbourhood" section by clicking the '#location' botton 
                    # Locate JS script by clicking "#location"
                    try:
                        # navigate to the neighbourhood section by navigation bar
                        self.driver.find_element(
                            By.XPATH, '//*[@href="#location"]').click()

                        sleep(SLEEP_TIME)

                        # click on the MRT stations element if it exists
                        self.driver.find_element(
                            By.XPATH, '//div[contains(text(), "MRT Stations")]').click()
                        sleep(SLEEP_TIME)
                        return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8", request=request)

                    except:
                        print("=" * 50)
                        print("cannot find MRT #location")
                        print("=" * 50)
                        return HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8", request=request)

    # close the webdriver when spider is closed
    def spider_closed(self):
        self.driver.close()
        pass

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s


class WsprojectSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WsprojectDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
