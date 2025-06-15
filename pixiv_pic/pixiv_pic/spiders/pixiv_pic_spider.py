import scrapy
import pickle

class PixivPicSpiderSpider(scrapy.Spider):
    name = "pixiv_pic_spider"
    allowed_domains = ["pixiv.net"]
    start_urls = ["https://www.pixiv.net/users/49460730"]

    def start_requests(self):
        url=self.start_urls[0]
        ##这段是比较简单的cookie获得方式，从浏览器复制然后处理
        # temp='privacy_policy_notification=0; a_type=0; b_type=1; _im_vid=01JAPXHCHQBAQZ8KXYWSVT6JGA; first_visit_datetime_pc=2024-11-03%2017%3A27%3A23; yuid_b=QTYmVGY; p_ab_id=0; p_ab_id_2=1; p_ab_d_id=571229789; jp1_ad_freq={}; privacy_policy_agreement=7; gam_ad_freq={}; _im_uid.3929=i.JpeA5JXrT-GTrzM1-qXc1w; gam_et_freq={"2628":[0,1745597715016],"2630":[0,1745597693351],"3127":[0,1745597611312],"4935":[0,1745597693353],"4936":[0,1745597611314]}; jp1_et_freq={"5078":[0,1745847728573]}; _cfuvid=3JNfX4iJ9q95N0W2GU1c_GfPHtQDxS6ixHM7NMr4LZU-1749883173131-0.0.1.1-604800000; __utmc=235335808; __utmz=235335808.1749883178.22.11.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); cto_bundle=7mAns19ld0I4akh4R1I3eTZpQnB6VHpsdThsMGt2M1A2b0hIYk90cUNkd1hWVVdXUWklMkI1YmtFR0E0cFExa3p4ZzB5eEN2Zk9KZ003Vk5jaiUyRmJEa0RjQnZhOG1GWGlHb2RBSHlkOHV1aFEzZzluc09RTEFOSWJBUWNLZEJLQjZscFJSWnliOUxCWk5xWVN3bFNKTzYyMGhDVDRRJTNEJTNE; _gid=GA1.2.462409179.1749883495; __utma=235335808.209784871.1695634818.1749883178.1749888104.23; __cf_bm=vSEN4dLC8viqtgO2v6eDgC.r2NXmR30K1Q1JJIL6VHo-1749894855-1.0.1.1-.oA72UKSV24x5sS92YwHpuo.8HOimIQhLgUqrmTO33SxrSbEV_ELhnTM.369VjyX1NSuyxVVQYXWRREeAouwG1B66HfBK7UHtSt3CS5j4shIYi15.MIeRqy7R3ZtbcJd; __utmt=1; cf_clearance=7AKzO3yslWRzxTV8Thluvhc8iY6eQhdwnBdnHP7XUjQ-1749895377-1.2.1.1-g4oNVjJtQ5vf0aAAAzOzMn7wss1YYfcF7aG1ASMmkY9pgru5czoc8sYoFPW9qOyn.dVhQZu51qE1THaW.LpnEXSgqP_5EYJliFy1PJzdCrldF8enUSX5JQmMatFs46VM_rpaFrptSk9b_Pnj3OTKDkwWsj6Abi0BVdwrZ8ymJCZtc_CTfpqSnd7cCCNt3O67QriT7Vb6u7_LmdRtc0xRRtYtbbtrgpVlWYTlL6FXNJq5hmpl7gdCiOMluliGMNwXkZUjcF9X9S4oscJaSZglGxGOiOEpEc.PAKst9CJN0gBNqBvySvlihCo0yZBANZYInkqKQbNmHEQR926jlMo.UJZd52wKrWiH4YZW1lh0dXE; _ga=GA1.1.423436449.1695634818; device_token=bdb7d28cf3476501e93101bf92111b99; cc1=2025-06-14%2019%3A04%3A03; _gcl_au=1.1.797451785.1749895446; PHPSESSID=98873340_0xX0QpvfuVlzFEoeOTdsa5xzg1sm7nCA; c_type=27; _ga_MZ1NL4PHH0=GS2.1.s1749894614$o9$g1$t1749895466$j42$l0$h0; __utmv=235335808.|2=login%20ever=no=1^3=plan=normal=1^5=gender=male=1^9=p_ab_id=0=1^10=p_ab_id_2=1=1; __utmb=235335808.16.10.1749888104; _ga_75BBYNYN9J=GS2.1.s1749891836$o28$g1$t1749895485$j14$l0$h0; FCNEC=%5B%5B%22AKsRol-n5TgI3CjUtb300dXlRD48jVJUrZ3TiyitLcez-8jvHLR4zSHLs-RyKRuAqEMUeVjLBt9dItpc8SShaBi5yBtidQfJ8xaiS3MlVNEX-9k-1_4TY386K7Lhj_8oQ62bAUaoeKL496UPfNQ89OFgnu9PLTxo0g%3D%3D%22%5D%5D'
        # cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}

        ## 这段是Playwright 渲染的使用
        # yield scrapy.Request(url=url, callback=self.parse,cookies=cookies,meta={
        #             "playwright": True  # 开启 Playwright 渲染
        #         })

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

        ##这段是翻页防止死循环的处理
        # # 加入当前页面到访问记录
        # if response.url in self.visited_urls:
        #     self.logger.warning(f"重复页面已访问过：{response.url}，跳过")
        #     return
        # self.visited_urls.add(response.url)

        print(response.url)
        # works=response.xpath('//ul[contains(@class,"sc-bf8cea3f-1")]/li[1]/div/div[2]/a/@href').extract_first()
        work = response.xpath('//ul[contains(@class,"sc-bf8cea3f-1")]/li[2]/div/div[2]/a/@href').extract_first()
        work=response.urljoin(work)
        yield scrapy.Request(url=work, callback=self.parse_detail, meta={"selenium": 'pic'},cookies=response.request.cookies)

    def parse_detail(self, response):
        print("作品详情页面"+response.url)
        pic_url=response.xpath('//div[@role="presentation"]//a/@href').extract_first()#找不到，依旧是动态渲染
        print(pic_url)
        # with open("图片详情页面.html", "w", encoding="utf-8") as f:
        #     f.write(response.text)

        ##这段是验证动态渲染被成功爬下来的处理
        # #保存网页源代码
        # with open("pixiv_rendered_selenium.html", "w", encoding="utf-8") as f:
        #     f.write(response.text)


        ##这段是处理访问收藏页面跳转登录页面再一次模拟登录
        # 处理进入收藏逻辑
        # shouCang_url = response.xpath('//nav/a[contains(@href,"bookmarks")]/@href').extract_first()
        # shouCang_url = response.urljoin(shouCang_url)
        # print(shouCang_url)
        # yield scrapy.Request(url=shouCang_url, callback=self.parse_denglu, meta={'cookies': response.request.cookies})

        ##这段是翻页防止死循环的处理
        # if next_url != None:
        #     next_url = response.urljoin(next_url)
        #     # 检查下一页是否已访问，避免死循环
        #     if next_url not in self.visited_urls:
        #         yield scrapy.Request(url=next_url, callback=self.parse_detail, meta={'cookies': response.request.cookies})
        #     else:
        #         self.logger.info(f"下一页已访问，停止翻页: {next_url}")

    ##这段是处理访问收藏页面跳转登录页面再一次模拟登录
    # def parse_detail(self, response):
    #     print("详情页面"+response.url)
    #
    #
    # def parse_denglu(self, response):
    #     print("处理登录"+response.url)
    #     cookies = response.meta['cookies']
    #     if "return_to" in response.url:
    #         yield scrapy.Request(url=response.url, callback=self.parse_detail,cookies=cookies)




