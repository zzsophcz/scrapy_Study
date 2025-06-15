# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyRumenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #实际上使用字典封装的，跟字典一样的使用方法
    # 讲师名字，头衔，详情
    name = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()

# if __name__ == '__main__':
#     item=ScrapyRumenItem()
#     item["name"]="王老师"
#     item["title"]="asd"
#     item["desc"]="gxcvz"
#
#     print(item)
