import scrapy


class Git2Spider(scrapy.Spider):
    name = "git2"
    allowed_domains = ["github.com"]
    start_urls = ["https://github.com/login"]

    def parse(self, response):
        #从登陆页面响应中解析出post数据
        token=response.xpath('//input[@name="authenticity_token"]/@value').extract_first()

        post_data={
            "commit": "Sign in",
            "authenticity_token": token,
            "add_account": "login",
            "login": "zzsophcz@gmail.com",
            "password": "as8823854",
            "webauthn-conditional": "undefined",
            "javascript-support": "true",
            "webauthn-support": "supported",
        }

        yield scrapy.FormRequest(
            url="https://github.com/session",
            callback=self.after_login,
            formdata=post_data
        )

    def after_login(self, response):
        yield scrapy.Request("https://github.com/zzsophcz",callback=self.check_login)

    def check_login(self, response):
        print(response.xpath('//span[@class="p-nickname vcard-username d-block"]/text()').extract_first())

