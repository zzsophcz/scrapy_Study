import scrapy
from scrapy_rumen.items import ScrapyRumenItem


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    #2. 检查域名
    allowed_domains = ["itcast.cn"]
    # 1.修改起始url
    start_urls = ["https://www.itheima.com/teacher.html#ajavaee"]

    #对起始url的解析响应
    #3. 编写爬虫逻辑
    def parse(self, response):
        #获取所有教师节点
        nodeList=response.xpath('//div[@class="li_txt"]')
        for node in nodeList:
            temp=ScrapyRumenItem()#这里使用item.py中的数据建模
            temp["name"]=node.xpath('./h3/text()').extract()
            temp["title"]=node.xpath('./h4/text()').extract()
            temp["desc"]=node.xpath('./p/text()').extract()
            print(temp)
            yield temp

