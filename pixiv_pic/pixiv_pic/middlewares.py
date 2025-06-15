# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import pickle
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from scrapy.http import HtmlResponse


class SeleniumSpiderMiddleware(object):
    def process_request(self, request, spider):
        sel_flag = request.meta.get("selenium")  # 标记处理方式
        if not sel_flag:
            return None  # 普通请求，不处理

        driver = webdriver.Chrome()

        try:
            if sel_flag == "shouCang":
                return self.enter_shouCang(driver, request)
            elif sel_flag == "pic":
                return self.handle_pic(driver, request)
            else:
                print("未知 selenium 模式")
                return None
        finally:
            driver.quit()

    def enter_shouCang(self, driver, request):

        url = request.url
        cookies_dict = request.cookies

        # 第一步：先访问主域名页面（用于设置 cookie）
        base_url = "https://www.pixiv.net/"
        driver.get(base_url)
        time.sleep(1)

        # 第二步：注入 cookies
        for name, value in cookies_dict.items():
            cookie = {'name': name, 'value': value, 'domain': '.pixiv.net'}
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"[!] 添加 cookie 失败: {cookie} | 原因: {e}")

        # 第三步：访问目标页面
        driver.get(url)
        time.sleep(2)  # 适当等待页面加载

        # 在这里添加进入个人收藏页面的selenium处理
        button = driver.find_element(By.XPATH, '//nav/a[contains(@href,"bookmarks")]')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(3)

        # 第四步：获取页面源代码
        html = driver.page_source

        # input("暂停查看网页源代码")

        # 第五步：构造 HtmlResponse 对象返回
        return HtmlResponse(
            url=driver.current_url,
            body=html,
            encoding='utf-8',
            request=request
        )

    def handle_pic(self, driver, request):
        url = request.url
        cookies_dict = request.cookies

        # 第一步：先访问主域名页面（用于设置 cookie）
        base_url = "https://www.pixiv.net/"
        driver.get(base_url)
        time.sleep(1)

        # 第二步：注入 cookies
        for name, value in cookies_dict.items():
            cookie = {'name': name, 'value': value, 'domain': '.pixiv.net'}
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"[!] 添加 cookie 失败: {cookie} | 原因: {e}")

        # 第三步：访问目标页面
        driver.get(url)
        time.sleep(2)  # 适当等待页面加载

        # 第四步：获取页面源代码
        html = driver.page_source

        # input("暂停查看网页源代码2")

        # 第五步：构造 HtmlResponse 对象返回
        return HtmlResponse(
            url=driver.current_url,
            body=html,
            encoding='utf-8',
            request=request
        )


