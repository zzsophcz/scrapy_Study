import scrapy
from Douban.items import DoubanItem

class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        movie_list=response.xpath("//*[@class='info']")
        for movie in movie_list:
            item=DoubanItem()

            item['name']=movie.xpath("./div[1]/a/span[1]/text()").extract_first()
            item['info']=movie.xpath("./div[2]/p[1]/text()").extract_first()
            item['score']=movie.xpath("./div[2]/div/span[2]/text()").extract_first()
            item['des']=movie.xpath("./div[2]/p[2]/span/text()").extract_first()

            yield item

        next_url=response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_url!=None:
            next_url=response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)
