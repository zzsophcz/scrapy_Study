import scrapy
import pickle
import re
from pixiv_pic.items import PixivPicItem

#不好定义在类内，因为类内参数第一个是self，在类内会导致参数传递出问题
def save_processed_link(link, file_path='processed_links.txt'):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(link + '\n')

def load_processed_links(file_path='processed_links.txt'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

class PixivPicSpiderSpider(scrapy.Spider):
    name = "pixiv_pic_spider"
    allowed_domains = ["pixiv.net","i.pximg.net"]#添加新域名以便访问图片
    start_urls = ["https://www.pixiv.net/users/98873340"]

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
        self.processed_links = load_processed_links()

    def parse(self, response):

        print(response.url)
        # works=response.xpath('//ul[contains(@class,"sc-bf8cea3f-1")]/li[1]/div/div[2]/a/@href').extract_first()
        works = response.xpath('//ul[contains(@class,"sc-bf8cea3f-1")]/li')
        next_url=response.urljoin(response.xpath('//nav[@class="sc-27a0ff07-0 bbkQMy"]/a[last()]/@href').extract_first())
        print("Next url:", next_url)
        print("作品数量：",len(works))
        for work in works:
            relative_url=response.urljoin(work.xpath('./div/div[2]/a/@href').extract_first())
            print("Work url:", relative_url)
            # 如果链接已处理，跳过
            if relative_url in self.processed_links:
                print("已经处理过该链接，跳过节省时间")
                continue

            # 否则，加入记录并继续处理
            self.processed_links.add(relative_url)
            save_processed_link(relative_url)

            # print(item["link"])
            yield scrapy.Request(url=relative_url, callback=self.parse_detail, meta={"selenium": 'pic'},
                                 cookies=response.request.cookies)
        # print("如果这段消息出现在最后，说明链接都已经是处理过的了")
        if next_url!=response.url and not re.search(r"[?&]p=1(?:$|&)", next_url):
            print("有新的一页，继续爬取作品url")
            yield scrapy.Request(url=next_url, callback=self.parse, meta={"selenium": 'shouCang'},cookies=response.request.cookies)

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





