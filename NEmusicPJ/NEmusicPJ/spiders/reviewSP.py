# -*- coding: utf-8 -*-
import re
from scrapy import Request
from scrapy.conf import settings
from scrapy_redis.spiders import RedisSpider



#好帖子：https://blog.csdn.net/qq_28304687/article/details/78678831
class ReviewspSpider(RedisSpider):
    name = 'reviewSP'
    allowed_domains = ['163.com']
    group_id=[1001,1002,1003,2001,2002,2003,6001,6002,6003,7001,7002,7003,4001,4002,4003]
    inital=range(65,91)

    redis_key = 'reviewSP:start_urls'
    #js_nextpage是一个XPathResult 对象。
    #document.documentElement表示从html的根节点开始匹配
    script="""
        function main(splash,args):
            splash:go(agrs.url)
            assert(splash:wait(args.wait))
            splash:scroll_position ={y=200}
            js_nextpage="document.evaluate('//*div[@class=‘m-cmmt’]/div[3]/div/a',document.documentElement,null,XPathResult.ORDERED_NODE_ITERATOR_TYPE,null).snapshotItem(-1).click" 
            splash:evaljs(js_nextpage)
            return splash:html()
        end
    """

    # 通过重写strat_requests方法，实现用户登录
    # 爬虫启动时，会首先执行start_requests函数的调用，执行成功之后，再去执行parse()函数进行解析。
    # start_urls=[]这个列表可要可不要。

    # def start_requests(self):
    #     for gid in self.group_id:
    #         for int in self.inital:
    #             singerurl='http://music.163.com/discover/artist/cat?id={gid}&initial={int}'.format(gid=1002,int=65)
    #             print(singerurl)
    #             yield Request(url=singerurl,callback=self.parse,method='GET',headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])


    #scrapy的主程序,分析歌手页面,获取歌手信息
    def parse(self, response):
        singers=response.xpath('//*[@class="nm nm-icn f-thide s-fc0"]/@href').extract()
        for singer in singers:
            singerurl='http://music.163.com'+singer.lstrip()
            yield Request(url=singerurl,method='GET',callback=self.album_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    def album_parse(self,response):
        ultag=response.xpath('//*[@id="m_tabs"]/li[2]/a/@href').extract()[0]
        albumurl='http://music.163.com'+ultag.lstrip()
        artist_id=re.findall('id=(\d*)',ultag)[0]
        return Request(url=albumurl,method='GET',callback=self.album_pages_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'],meta={'artist_id':artist_id})

    #在歌手专辑页面中，获取专辑翻页链接
    def album_pages_parse(self,response):
        pages=[]
        pagenum=response.xpath('//*[@class="u-page"]/a[@class="zpgi"]/text()')
        for i in range(0,len(pagenum)+1):
            page='http://music.163.com/artist/album?id={id}&limit=12&offset={offset}'.format(id=response.meta['artist_id'],offset=i*12)
            pages.append(page)
        for url in pages:
            yield Request(url=url,method='GET',callback=self.album_datail_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    #在专辑翻页中，获取专辑多个专辑链接
    def album_datail_parse(self,response):
        albums=response.xpath('//*[@class="tit s-fc0"]/@href').extract()
        #如果一张专辑都没有
        if not albums:
            return
        else:
            for album in albums:
                albumurl='http://music.163.com'+album.lstrip()
                yield Request(url=albumurl,method='GET',callback=self.song_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    #在专辑页面中，获取专辑多个歌曲链接
    def song_parse(self,response):
        #str--->(encode)--->bytes，bytes--->(decode)--->str
        # print(response.body.decode(response.encoding))
        # print(response.url)
        songurls=response.xpath('//*[@class="f-hide"]/li/a/@href').extract()    #这个xpath是用scrapy shell工具调试出来的
        if not songurls:
            print('songurls is None')
            return
        else:
            for songurl in songurls:
                url='http://music.163.com'+songurl.lstrip()
                yield Request(url=url,method='GET',callback=self.comment_parse,headers=settings['DEFAULT_REQUEST_HEADERS'],cookies=settings['COOKIE'])

    #在歌曲页面中，利用执行splash渲染服务，执行带有JS代码html--->信息完整可读可抓取的DOM
    # def parse(self,response):
    #     comments_pagenum=response.xpath('//*[@id="auto-id-Nv7N1mMQXKsWpCGx"]')

    #在歌曲页面中，获取页面首页评论
    def comment_parse(self,response):
        song=response.xpath('//*[@class="hd"]/div/em/text()').extract_first()
        singer=response.xpath('//*[@class="s-fc7"]/text()').extract_first()   #这个xpath是用scrapy shell工具调试出来的
        album=response.xpath('//*[@class="des s-fc4"]/a[@class="s-fc7"]/text()').extract_first()        #这个xpath是用scrapy shell工具调试出来的

        item=CommentItem()
        item['song'] = song
        item['singer'] = singer
        item['album'] = album
        # commentblock=response.xpath('//*[@class="itm"]').extract()
        # for each in commentblock:
        #     item = CommentItem()
        #     item['song']=song
        #     item['singer']=singer
        #     item['album']=album
        #     item['nickname']=each.xpath('./div[2]/div[1]/div/a/text()').extract()[0]
        #     item['comment_content']=each.xpath('./div[1]/div/text()').extract()[0]
        #     item['likedCount']=each.xpath('./div[@class="rp"]/a[@data-type="like"]/text()').extrct()[0]
        #     item['time']=each.xpath('./div[@class="rp"]/div[@class="time s-fc4"]/text()').extrct()[0]
        print(item)
        yield item