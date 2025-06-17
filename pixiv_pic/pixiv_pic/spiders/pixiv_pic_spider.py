import scrapy
import pickle
import re
from pixiv_pic.items import PixivPicItem
#分布式爬虫导入
from scrapy_redis.spiders import RedisSpider
import os

class PixivPicSpiderSpider(RedisSpider):
    name = "pixiv_pic_spider"
    # allowed_domains = ["pixiv.net","i.pximg.net"]#添加新域名以便访问图片
    # start_urls = ["https://www.pixiv.net/users/49460730"]
    #https://www.pixiv.net/users/49460730 ssy
    #https://www.pixiv.net/users/59028877 lyx
    redis_key = "pixivPicSpider"

    ##这个函数是翻页防止死循环的处理
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        #表示在自定义前，先调用父类的初始化方法，保证 Scrapy 能正常工作。
        super(PixivPicSpiderSpider, self).__init__(*args, **kwargs)
        # self.processed_links = load_processed_links()

    def parse(self, response):
        # 加载 cookies（只在首次请求时用）
        # 当前文件在 pixiv_pic/spiders 中，向上两层才能到项目根目录
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        cookie_path = os.path.join(BASE_DIR, 'pixiv_cookies.pkl')

        with open(cookie_path, 'rb') as f:
            cookies_list = pickle.load(f)

        cookies_dict = {c['name']: c['value'] for c in cookies_list}

        # 构造一个新的请求（携带 cookie）
        yield scrapy.Request(
            url=response.url,   # 就是 Redis 中传进来的 起始URL
            callback=self.parse_shouCang,  # 你的实际解析函数
            meta={"selenium": 'shouCang'},
            cookies=cookies_dict,
            dont_filter=True  # 避免被去重（可选）
        )

    def parse_shouCang(self, response):

        print(response.url)
        # works=response.xpath('//ul[contains(@class,"sc-bf8cea3f-1")]/li[1]/div/div[2]/a/@href').extract_first()
        works = response.xpath('//ul[contains(@class,"sc-bf8cea3f-1")]/li')
        next_url=response.urljoin(response.xpath('//nav[@class="sc-27a0ff07-0 bbkQMy"]/a[last()]/@href').extract_first())
        print("Next url:", next_url)
        print("作品数量：",len(works))
        for work in works:
            relative_url=response.urljoin(work.xpath('./div/div[2]/a/@href').extract_first())
            print("Work url:", relative_url)

            # print(item["link"])
            yield scrapy.Request(url=relative_url, callback=self.parse_detail, meta={"selenium": 'pic'},
                                 cookies=response.request.cookies)
        # print("如果这段消息出现在最后，说明链接都已经是处理过的了")
        if next_url!=response.url and not re.search(r"[?&]p=1(?:$|&)", next_url):
            print("有新的一页，继续爬取作品url")
            yield scrapy.Request(url=next_url, callback=self.parse_shouCang, meta={"selenium": 'True'},cookies=response.request.cookies)

    def parse_detail(self, response):
        # pass
        print("作品详情页面"+response.url)
        pic_url=response.xpath('//div[@role="presentation"]//a/@href').extract()#找不到，依旧是动态渲染
        author = response.xpath('//div[@class="sc-d91e2d15-1 iiAAJk"]/a/div[1]/text()').extract_first()
        if pic_url!=None:
            print("图片地址",pic_url)
            item = PixivPicItem()
            item['image_urls'] = pic_url
            item['author'] = author
            yield item





