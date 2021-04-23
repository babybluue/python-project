import scrapy


class Dy2018btSpider(scrapy.Spider):
    name = 'dy2018bt'

    start_urls = ['https://www.dy2018.com/html/gndy/jddyy/']

    a = 0

    def parse(self, response):
        for title in response.css('table.tbspan'):
            self.a += 1
            yield from response.follow_all(title.css('a.ulink'), self.getBt)
        for nextlink in response.css('div.co_content8 div.x a'):
            if nextlink.css('a::text').get() == '下一页':
                yield from response.follow_all(nextlink.css('a'), self.parse)

    def getBt(self, response):
        yield{
            self.a: response.css('div.contain div.title_all h1::text').get(),
            'bt': response.css('div.co_content8 div#downlist a::text').getall(),
            'ftp': response.css('div.co_content8 div#Zoom a::text').get()
        }
