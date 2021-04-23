import scrapy


class DyMoviesSpider(scrapy.Spider):
    name = 'dymovies'
    start_urls = ['https://www.dy2018.com/0/']
    a = 0

    def parse(self, response):
        for list in response.css('div.co_content2 table a'):
            yield from response.follow_all(list.css('a'), self.getMovieList)

    def getMovieList(self, response):
        for title in response.css('table.tbspan'):
            yield from response.follow_all(title.css('a.ulink'), self.getBt)
        for nextlink in response.css('div.co_content8 div.x a'):
            if nextlink.css('a::text').get() == '下一页':
                yield from response.follow_all(nextlink.css('a'), self.getMovieList)

    def getBt(self, response):
        rank = response.css(
            'div.co_content8 div.position strong.rank::text').get()
        if rank is not None:
            if float(rank) > 7:
                self.a += 1
                yield{
                    self.a: response.css('div.contain div.title_all h1::text').get(),
                    'bt': response.css('div.co_content8 div#downlist a::text').getall(),
                    'ftp': response.css('div.co_content8 div#Zoom table a::text').get()
                }
