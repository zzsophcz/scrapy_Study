# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter

# pipelines.py

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class PixivImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item.get('image_urls', []):
            yield Request(
                url=image_url,
                headers={'Referer': 'https://www.pixiv.net/'}
            )

