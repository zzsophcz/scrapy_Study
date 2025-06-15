# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from itemadapter import ItemAdapter


class PixivPicPipeline:
    def process_item(self, item, spider):
        for pic_url in item:
            yield Request(
                url=pic_url,
                headers={
                    'Referer': 'https://www.pixiv.net/',
                }
            )
        return item
