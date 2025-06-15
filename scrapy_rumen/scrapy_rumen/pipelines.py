# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class ScrapyRumenPipeline:

    def __init__(self):
        self.file=open("itcast.json","w")

    # 这里的item实际上是parse方法提交的temp字典
    def process_item(self, item, spider):
        #处理数据,将数据变成json形式保存
        #由于使用了数据建模，dumps方法的参数要求是字典，下面强转
        item=dict(item)#只有在scrapy中可以这样弄
        #使用dumps方法将字典序列化（变成字符串和中文字符形式）
        json_data=json.dumps(item)+',\n'
        #将数据写入文件
        self.file.write(json_data)
        return item

    def __del__(self):
        self.file.close()

