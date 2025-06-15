# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json



class DoubanPipeline:
    def __init__(self):
        self.file = open("doubantop250.json", "w")

    def process_item(self, item, spider):
        item = dict(item)  # 只有在scrapy中可以这样弄
        # 使用dumps方法将字典序列化（变成字符串和中文字符形式）
        json_data = json.dumps(item) + ',\n'
        # 将数据写入文件
        self.file.write(json_data)
        return item

    def __del__(self):
        self.file.close()


