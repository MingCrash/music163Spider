# -*- coding: utf-8 -*-

# Scrapy settings for NEmusicPJ project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'NEmusicPJ'

SPIDER_MODULES = ['NEmusicPJ.spiders']
NEWSPIDER_MODULE = 'NEmusicPJ.spiders'

#mongoDB setting
MONGODB_HOST='13.230.98.46'
MONGODB_PORT=27017
MONGODB_DBNAME='NEdata'
MONGODB_COLLECTION='revdata'

#redis setting
REDIS_HOST='13.230.98.46'
REDIS_PORT=6379

#splash setting
# SPLASH_URL = 'http://localhost:8050'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'NEmusicPJ (+http://www.yourdomain.com)'

#Poxy_list
PROXY_LIST=['183.159.94.107:18118',
            '111.183.230.26:61234',
            '182.42.43.247:61234',
            '110.73.2.102:8123',
            '175.155.24.10:808',
            '110.73.2.102:8123',
            '120.26.110.59:8080'
            ]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#Set a custom DUPEFILTER_CLASS
#DUPEFILTER的作用就是去除重复的url,避免重复请求
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

#a custom cache storage backend
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
  'Referer': 'http://music.163.com/'
}

#cookie setting
COOKIE = {
    'Cookie': '__f_=1525100577435; _ntes_nnid=b2e2e773903d48737f247de2f9fe8efe,1525100577569; _ntes_nuid=b2e2e773903d48737f247de2f9fe8efe; _iuqxldmzr_=32; WM_TID=9ECbRumLJhUT1SIeuNJO%2F6Bff5mbYEI4; __utmc=94650624; __e_=1525140741592; __utmz=94650624.1525168627.6.4.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/qq_28304687/article/details/78678782; __utma=94650624.545796608.1525137981.1525182521.1525186669.10; JSESSIONID-WYYY=sy9m9SQ1Adk0ddcshCza1C5PRhfohZxT7mjHd9FqJBl%2B6zxJWBhPo%2BYq6uiefl5%2Fp4FrF4M173ie4z8Pofv%5CStdA6nKbkmgSziBBR%2BB7Rwfxw%2FrOubtUcZUJbsCr5YsNnKj%2FYJcG%5COTFJCwYiWQUMPn37q3VpIVDmw%5CIJDXrw2SwA2nU%3A1525189881463; __utmb=94650624.19.10.1525186669'
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'NEmusicPJ.pipelines.NemusicpjPipeline': 300,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'NEmusicPJ.middlewares.ProxyMiddleware': 750,
   'NEmusicPJ.middlewares.RandomUAMiddleware':400,
   'scrapy_splash.SplashCookiesMiddleware': None,
   'scrapy_splash.SplashMiddleware': None,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'NEmusicPJ.middlewares.NemusicpjSpiderMiddleware': 543,
   'scrapy_splash.SplashDeduplicateArgsMiddleware': None,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
