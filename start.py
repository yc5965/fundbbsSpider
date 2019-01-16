from scrapy import cmdline

#cmdline.execute("scrapy crawl caixinWeeklySpider -a SPIDER_TYPE=INCREMENT".split())

cmdline.execute("scrapy crawl thFundSpider -a SPIDER_TYPE=ALL".split())
