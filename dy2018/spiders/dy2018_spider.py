import scrapy


class Dy2018Spider(scrapy.Spider):

    name = 'dy2018'

    start_urls = ['https://www.dy2018.com/html/gndy/jddyy/']
    a = 0

    def parse(self, response):
        for title in response.css('table.tbspan'):
            self.a += 1
            yield{
                self.a: title.css('a.ulink::text').get()
            }
        for nextlink in response.css('div.co_content8 div.x a'):
            if nextlink.css('a::text').get() == '下一页':
                yield from response.follow_all(nextlink.css('a'), callback=self.parse)
