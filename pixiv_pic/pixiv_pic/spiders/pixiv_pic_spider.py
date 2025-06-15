import scrapy
import pickle
from pixiv_pic.items import PixivPicItem

class PixivPicSpiderSpider(scrapy.Spider):
    name = "pixiv_pic_spider"
    allowed_domains = ["pixiv.net","i.pximg.net"]#添加新域名以便访问图片
    start_urls = ["https://www.pixiv.net/users/49460730"]

    def start_requests(self):
        url=self.start_urls[0]

        with open("pixiv_cookies.pkl", "rb") as f:
            cookies_list = pickle.load(f)
            print("Cookies loaded:", cookies_list)
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies_list}

        yield scrapy.Request(url=url, callback=self.parse, meta={"selenium": 'shouCang'},cookies=cookies_dict)

    ##这个函数是翻页防止死循环的处理
    def __init__(self, *args, **kwargs):
        #表示在自定义前，先调用父类的初始化方法，保证 Scrapy 能正常工作。
        super().__init__(*args, **kwargs)
        self.visited_urls = set()  # 记录访问过的页面防止死循环

    def parse(self, response):


        print(response.url)
        # works=response.xpath('//ul[contains(@class,"sc-bf8cea3f-1")]/li[1]/div/div[2]/a/@href').extract_first()
        works = response.xpath('//ul[contains(@class,"sc-bf8cea3f-1")]/li')
        print(len(works))
        for work in works:
            item={}
            item["link"]=response.urljoin(work.xpath('./div/div[2]/a/@href').extract_first())
            # print(item["link"])
            #获取图片url字典
            yield scrapy.Request(url=item["link"], callback=self.parse_detail, meta={"selenium": 'pic'},
                                 cookies=response.request.cookies)
    def parse_detail(self, response):
        # pass
        print("作品详情页面"+response.url)
        pic_url=response.xpath('//div[@role="presentation"]//a/@href').extract_first()#找不到，依旧是动态渲染
        author = response.xpath('//div[@class="sc-d91e2d15-1 iiAAJk"]/a/div[1]/text()').extract_first()
        if pic_url!=None:
            print("图片地址"+pic_url)
            item = PixivPicItem()
            item['image_urls'] = [pic_url]
            item['author'] = author
            yield item

            # yield scrapy.Request(
            #     url=pic_url,
            #     headers={
            #         'Referer': 'https://www.pixiv.net/',  # 必须加 Referer
            #     },
            #     callback=self.save_image
            # )

    def save_image(self, response):
            image_name = response.url.split('/')[-1]
            with open(f'pixiv_images/{image_name}', 'wb') as f:
                f.write(response.body)
                print(f"[+] 图片已保存为 {image_name}")




