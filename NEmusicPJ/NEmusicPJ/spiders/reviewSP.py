# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from NEmusicPJ.items import CommentItem,SingerItem
from scrapy.conf import settings
import re

#好帖子：https://blog.csdn.net/qq_28304687/article/details/78678831

class ReviewspSpider(scrapy.Spider):
    name = 'reviewSP'
    allowed_domains = ['163.com']
    # start_urls = 'http://music.163.com/#/discover/artist/cat?id={gid}&initial={int}'
    # redis_key = 'ReviewspSpider：start_urls'
    group_id=[1001,1002,1003,2001,2002,2003,6001,6002,6003,7001,7002,7003,4001,4002,4003]
    inital=range(65,91)
    # 通过重写strat_requests方法，实现用户登录
    # 爬虫启动时，会首先执行start_requests函数的调用，执行成功之后，再去执行parse()函数进行解析。
    # start_urls=[]这个列表可要可不要。
    def start_requests(self):
        for gid in self.group_id:
            for int in self.inital:
                singerurl='http://music.163.com/discover/artist/cat?id={gid}&initial={int}'.format(gid=1001,int=65)
                yield Request(url=singerurl,callback=self.parse,method='GET',headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    #scrapy的主程序,分析歌手页面,获取歌手信息
    def parse(self, response):
        singers=response.xpath('//*[@class="nm nm-icn f-thide s-fc0"]/@href').extract()
        for singer in singers:
            singerurl='http://music.163.com'+singer.lstrip()
            yield Request(url=singerurl,method='GET',callback=self.album_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    def album_parse(self,response):
        ultag=response.xpath('//*[@id="m_tabs"]/li[2]/a/@href')
        albumurl='http://music.163.com'+ultag.extract()[0].lstrip()
        yield Request(url=albumurl,method='GET',callback=self.album_pages_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    def album_pages_parse(self,response):
        tmp=response.xpath('//*[@id="artist-home"]/@href').extract()[0]

        artist_id=re.search('id=(\d*)',tmp)
        print(artist_id)
        # string='http://music.163.com/artist/album?id={artist_id}&limit=12&offset=0'.format()
        # pages=response.xpath('//*[@class="zpgi"]/@href').extract()

        # if not pages:
        #     try:
        #         firstpage=re.sub(r'offset=(\d*)','offset=0',pages[0])
        #         pages.append(firstpage)
        #     except:
        #         pass
        # else:
        #     return

        # for url in pages:
        #     albumlisturl='http://music.163.com'+url.lstrip()
            # yield Request(url=albumlisturl,method='GET',callback=self.album_datail_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    def album_datail_parse(self,response):
        albums=response.xpath('//*[@class="tit s-fc0"]/@href').extract()
        for album in albums:
            albumurl='http://music.163.com'+album.lstrip()
            yield Request(url=albumurl,method='GET',callback=self.song_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    def song_parse(self,response):
        songurls=response.xpath('//*[@class="f-cb"]/div/div/span/a/@href')
        for songurl in songurls:
            url='http://music.163.com'+songurl.extract()[0].lstrip()
            yield Request(url=url,method='GET',callback=self.comment_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    #目前只抓取每首歌首页评论
    def comment_parse(self,response):
        song=response.xpath('//*[@class="hd"]/div/em/text()').extract()[0]
        singer=response.xpath('//*[@class="des s-fc4"][1]/span/string(.)').extract()[0]
        album=response.xpath('//*[@class="des s-fc4"][2]/a/text()').extract()[0]

        commentblock=response.xpath('//*[@class="cntwrap"]')
        for each in commentblock:
            item = CommentItem()
            item['song']=song
            item['singer']=singer
            item['album']=album
            item['nickname']=each.xpath('/div[1]/div/a/text()').extract()[0]
            item['comment_content']=each.xpath('/div[1]/div/text()').extract()[0]
            item['likedCount']=each.xpath('/div[@class="rp"]/a[@data-type="like"]/text()').extrct()[0]
            item['time']=each.xpath('/div[@class="rp"]/div[@class="time s-fc4"]/text()').extrct()[0]
            print(item)
            yield item






