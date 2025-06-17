# Scrapy settings for pixiv_pic project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "pixiv_pic"

SPIDER_MODULES = ["pixiv_pic.spiders"]
NEWSPIDER_MODULE = "pixiv_pic.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "pixiv_pic.middlewares.PixivPicSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "pixiv_pic.middlewares.PixivPicDownloaderMiddleware": 543,
    "pixiv_pic.middlewares.SeleniumSpiderMiddleware": 543
}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # "pixiv_pic.pipelines.PixivPicPipeline": 300,
   #  "scrapy.pipelines.images.ImagesPipeline": 1,
    'pixiv_pic.pipelines.PixivImagesPipeline': 1,
    #开启此管道会将数据存入Redis数据库中
    'scrapy_redis.pipelines.RedisPipeline' : 400
}
#设置redis数据库
REDIS_URL="redis://127.0.0.1:6379"
#设置下载延迟
DOWNLOAD_DELAY=1

# 图片下载保存路径（绝对路径或相对路径）
IMAGES_STORE = 'images'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
# # 告诉 Scrapy 用 Playwright 作为下载器（代替默认的 HTTP 下载器）
# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }
# # Scrapy 使用异步机制来运行浏览器（Playwright 基于 asyncio）
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# # 指定使用哪个浏览器（chromium、firefox 或 webkit，默认推荐 chromium）
# PLAYWRIGHT_BROWSER_TYPE = "chromium"

#分布式爬虫配置文件固定参数
#设置重复过滤器的模块，（使用scrapy-redis提供的去重类）
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 使用scrapy-redis提供的调度器，这个调度器具备和数据库交互的功能
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#设置当爬虫结束的时候是否保持redis数据库中的去重集合与任务队列(不清空redis数据库)
SCHEDULER_PERSIST=True
# 使用scrapy-redis的队列类（可选：队列或栈或优先队列）
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.FifoQueue" #默认队列（FIFO
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.LifoQueue"  # 栈
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.PriorityQueue"  # 优先级队列

FEED_EXPORT_ENCODING = "utf-8"
