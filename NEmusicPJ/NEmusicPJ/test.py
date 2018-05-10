# -*- coding: utf-8 -*-

import re
import random
import requests
from lxml import etree
from scrapy.conf import settings
from scrapy import Request


#search返回一个match对象
str='/user/home?id=29879272'
dd=re.search('id=(\d*)',str).group()
print(dd)

#抽取29879272
#findall直接返回匹配结果
tmp='/user/home?id=29879272'
artist_id = re.findall('id=(\d*)', tmp)[0]
print(artist_id)

proxy_list = settings['PROXY_LIST']
print(proxy_list)
dd=random.choice(proxy_list)
print(dd,type(dd))

def parse(self,response):
    print(response.body)

response2=Request(url='http://music.163.com/album?id=35045434',callback=parse)

response=requests.get(url='http://music.163.com/album?id=35045434').content
print(response)
selector=etree.HTML(response)
tbody=selector.xpath('//*[@class="m-table "]/tbody')
print(tbody)


# import sys
# from PyQt5.QtCore import QUrl
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWebEngineWidgets import QWebEnginePage,QWebEngineView
#
# class Render(QWebEngineView):  # 子类Render继承父类QWebEngineView
#     def __init__(self,url):
#         super.__init__(self)   # 子类构造函数继承父类
#         self.app=QApplication(sys.argv)
#         self.loadFinished.connect(self._loadFinished)
#         self.load(QUrl(url))
#         self.app.exec_()
#
#     def _loadFinished(self):
#         self.page().toHtml(self.callable)
#
#     def callable(self,data):
#         self.html = data
#         self.app.quit()

# url = 'http://example.webscraping.com/places/default/dynamic'
# r = Render(url)
# result = r.html
# tree = lxml.html.fromstring(result)
# a = tree.cssselect('#result')[0].text_content()
# print(a)



# def render(source_html):
#     """Fully render HTML, JavaScript and all."""
#
#     import sys
#     from PyQt5.QtWidgets import QApplication
#     from PyQt5.QtWebKitWidgets import QWebPage
#
#     class Render(QWebPage):
#         def __init__(self, html):
#             self.html = None
#             self.app = QApplication(sys.argv)
#             QWebPage.__init__(self)
#             self.loadFinished.connect(self._loadFinished)
#             self.mainFrame().setHtml(html)
#             self.app.exec_()
#
#         def _loadFinished(self, result):
#             self.html = self.mainFrame().toHtml()
#             self.app.quit()
#
#     return Render(source_html).html