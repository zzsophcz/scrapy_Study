# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PixivPicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    image_urls = scrapy.Field()  # 必须字段，图片的 URL 列表
    images = scrapy.Field()  # 自动填充字段，图片处理后的信息
    author = scrapy.Field()
