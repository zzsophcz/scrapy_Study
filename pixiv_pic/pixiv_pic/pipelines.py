# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter

# pipelines.py

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

from urllib.parse import urlparse
import os

class PixivImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        author = item.get('author', 'unknown_author').replace('/', '_')
        for image_url in item.get('image_urls', []):
            yield Request(
                url=image_url,
                headers={'Referer': 'https://www.pixiv.net/'},
                meta={'item': item}  # 把 item 信息带过去
            )

    def file_path(self, request, response=None, info=None, *, item=None):
        # 尝试从 request.meta 中获取 item
        item = request.meta.get('item', {})

        # 画师名
        author = item.get('author', 'unknown_author')
        author = author.replace('/', '_').replace('\\', '_')  # 防止路径出错

        # 提取原始文件名（比如 123263099_p0.png）
        image_url = request.url
        filename = os.path.basename(urlparse(image_url).path)

        # 设置绝对路径的基础目录（你可以根据需要修改这里）
        base_dir = 'F:/pixiv_images'  # 改成你自己的绝对路径

        # # 拼接最终绝对路径：/home/yourusername/pixiv_images/画师名/文件名
        # return os.path.join(base_dir, author, filename)

        #最终路径：画师名/文件名，例如：かまんべーる/123263099_p0.png
        return f'{author}/{filename}'

