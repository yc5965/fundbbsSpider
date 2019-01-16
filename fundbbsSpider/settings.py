# -*- coding: utf-8 -*-

# Scrapy settings for fundbbsSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fundbbsSpider'

SPIDER_MODULES = ['fundbbsSpider.spiders']
NEWSPIDER_MODULE = 'fundbbsSpider.spiders'

# 数据库
MY_HOST = "127.0.0.1"  # "101.37.33.198"
MY_USER = "root"  # "mysqluser"
MY_PASSWD = "root"  # "Mysqluser2017!"
MY_DATABASE = "poms"
MY_CHARSET = "utf8"

# 账号
LOGINNAME = "17316280501"
# 密码
PASSWORD = "lowrisk"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'fundSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'fundSpider.middlewares.FundspiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'fundSpider.middlewares.FundspiderDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
CONCURRENT_ITEMS = 1000

INDEX_INSERT_SQL = """
        REPLACE  INTO py_caixin_index (
	        id,
	        article_title,
	        article_time,
	        article_introduction,
	        image_url,
	        article_content,
	        create_time,
	        video_url,
	        page_url,
	        original_time
            )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

INDEX_FILTER_URL = """
        SELECT
	    COUNT(*)
        FROM
	        py_caixin_index
        WHERE
	        page_url = %s
    """

INDEX_FILL_URL = """
        SELECT
	    page_url
        FROM
	        py_caixin_index
        WHERE
	        article_title = %s

    """

WEEKLY_FILTER_URL = """
        SELECT
	    COUNT(*)
        FROM
	        py_caixin_weekly_period
        WHERE
	        weekly_url = %s
    """

PERIOD_INSERT_SQL = """
        REPLACE  INTO py_caixin_weekly_period (
	        id,
	        weekly_num,
	        weekly_time,
	        weekly_title,
	        weekly_summary,
	        weekly_image,
	        create_time,
	        weekly_issue_image,
	        weekly_url
            )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

WEEKLY_INSERT_SQL = """
        REPLACE  INTO py_caixin_weekly_period (
	        id,
	        article_type,
	        period_id,
	        article_title,
	        article_summary,
	        article_time,
	        article_image,
	        create_time,
	        article_url,  
	        article_content,
	        article_sign,
	        article_deal_time
            )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

ANNOUNCEMENT_INSERT_SQL = """
        REPLACE  INTO fund_announcement_info (
	        id,
	        announcement_title,
	        content,
	        content_text,
	        file_url,
	        announcement_type,
	        announcement_url,
	        announcement_time,  
	        create_time,
	        fund_code
            )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

FUND_INSERT_SQL = """
        REPLACE  INTO fund_date_info (
	        id,
	        company,
	        fund_name,
	        fund_url,
	        fund_code,
	        update_date,
	        unit_net_value,
	        cumulative_net_value,
	        today_variety,  
	        last_three_months,
	        last_year,
	        since_this_year,
	        since_established,  
	        fund_manager_image,
	        manager_introduction
            )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

FUND_FILTER_URL = """
        SELECT
	    COUNT(*)
        FROM
	        fund_announcement_info
        WHERE
	       fund_code = %s and announcement_title = %s  and announcement_time = %s
    """
