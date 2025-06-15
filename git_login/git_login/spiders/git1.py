import scrapy


class Git1Spider(scrapy.Spider):
    name = "git1"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/zzsophcz"]

    def start_requests(self):
        url = self.start_urls[0]

        temp='GHCC=Required:1-Analytics:1-SocialMedia:1-Advertising:1; _octo=GH1.1.1455469427.1749286308; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg; preferred_color_mode=light; tz=Asia%2FShanghai; ai_session=YTZPvPPPtlG71iR6t2KJqX|1749637851002|1749637891665; logged_in=yes; dotcom_user=zzsophcz'
        cookies = {data.split('=')[0]: data.split('=')[-1] for data in temp.split(';')}
        yield scrapy.Request(url=url, callback=self.parse, cookies=cookies)


    def parse(self, response):
        print(response.xpath('//span[@class="p-nickname vcard-username d-block"]/text()').extract_first())
        pass
