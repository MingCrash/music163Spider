# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.conf import settings
from fake_useragent import UserAgent
from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import redis
import random


class ProxyMiddleware(HttpProxyMiddleware):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self):
        HttpProxyMiddleware.__init__()
        self.pool = redis.ConnectionPool(max_connections=10,host=settings['REDIS_HOST'],port=settings['REDIS_PORT'])
        self.redscli = redis.Redis(connection_pool=self.pool)

    def __del__(self):
        self.pool.disconnect()

    def process_request(self,request,spider):
        proxy_list=settings['PROXY_LIST']
        #"http://YOUR_PROXY_IP:PORT"
        request.meta['proxy'] ='http://{proxy}'.format(proxy=random.choice(proxy_list))
        return None

    #服务器拒绝以后，换一个新的IP
    def process_response(self, request, response, spider):
        #200 请求已成功，请求所希望的响应头或数据体将随此响应返回。出现此状态码是表示正常状态。
        if response.status != 200:
            # proxy_list = settings['PROXY_LIST']
            # while True:
            #     #换一个新的ip
            #     if random.choice(proxy_list) != response.meta['proxy']:
            #         #修改当前的request请求
            #         request.meta['proxy'] = 'http://{proxy}'.format(proxy=random.choice(proxy_list))
            #         break
            try:
                request.meta['proxy']= self.redscli.rpop()
            except:
                pass


class RandomUAMiddleware(UserAgentMiddleware):
    def __init__(self):
        self.ua=UserAgent()

    def process_request(self,request,spider):
        UserAgent=self.ua.random
        request.headers['User-Agent'] = UserAgent
        return None

class NemusicpjSpiderMiddleware(object):
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

        # Should return either None or an iterable of Response, dict
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

class NemusicpjDownloaderMiddleware(object):
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


