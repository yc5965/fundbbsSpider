# -*- coding: utf-8 -*-
import time
import scrapy
import re
import hashlib
import random
import json
import jsonpath
from fundbbsSpider.items import IndexSpiderItem
from scrapy.conf import settings
from  fundbbsSpider.urlFilter import IndexFilter


class CaixinIndexSpider(scrapy.Spider):
    name = 'caixinIndexSpider'
    allowed_domains = ['caixin.com']
    start_urls = ['http://www.caixin.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            "fundbbsSpider.pipelines.IndexSpiderPipeline": 300
        }
    }

    def __init__(self, SPIDER_TYPE=None, *args, **kwargs):
        super(CaixinIndexSpider, self).__init__(*args, **kwargs)
        self.SPIDER_TYPE = SPIDER_TYPE
        self.password = settings["PASSWORD"]
        self.loginName = settings["LOGINNAME"]
        self.rand = random.uniform(0, 1)
        self.index_links = []

    def parse(self, response):
        toutiao_link = response.xpath("//div[@class='toutiao_box']/div/div/dl/dt/a/@href").extract()
        img_link = response.xpath("//div[@class='img_list_box']/ul/li/p/a/@href").extract()
        news_link = response.xpath("//div[@class='news_list']/dl/dd/p/a/@href").extract()
        links = toutiao_link + img_link + news_link
        urlFilter = IndexFilter()
        for each in links:
            if re.match("http://[a-z.]*/[0-9]*-[0-9]*-[0-9]*/[0-9]*.html", each):
                count = urlFilter.filter_request(each)
                if count[0][0] == 0:
                    self.index_links.append(each)
        urls = urlFilter.fill_request()
        if urls:
            self.index_links += urls[0]
        if self.index_links:
            md = hashlib.md5()
            md.update(self.password.encode("utf-8"))
            pwd = md.hexdigest()
            login_url = "https://gateway.caixin.com/api/ucenter/user/v1/loginJsonp?callback=jQuery17204291106502992419_" + str(
                int(
                    time.time() * 1000)) + "&account=" + self.loginName + "&password=" + pwd + "&device=CaixinWebsite&deviceType=5&unit=1&userTag=null&areaCode=%2B86&_=" + str(
                int((time.time() * 1000)))
            yield scrapy.Request(login_url, callback=self.login_parse, dont_filter=True)

    def login_parse(self, response):
        for each in self.index_links:
            yield scrapy.Request(each, callback=self.index_parse, dont_filter=True)

    def index_parse(self, response):
        item = IndexSpiderItem()
        item["id"] = response.url.split("/")[-1].split(".html")[0]
        item["article_title"] = response.xpath("normalize-space(//div[@id='conTit']/h1/text()[1])").extract()[0]
        item["original_time"] = response.xpath("normalize-space(//div[@id='artInfo']|//div[@id='conTit']/ul/li[@class='time'])").extract()[0]
        article_introduction = response.xpath("//p[@class='zhaiyao'][1]/text()|//div/div[@id='subhead']/text()[1]").extract()
        item["article_content"] = response.xpath("//div[@id='Main_Content_Val']/p").extract()
        image_url = response.xpath("//div[@id='the_content']/div/dl/dt/img/@src").extract()
        if len(article_introduction) == 0:
            item["article_introduction"] = ""
        else:
            item["article_introduction"] = article_introduction[0]

        if len(image_url) == 0:
            item["image_url"] = ""
        else:
            item["image_url"] = image_url[0]
        item["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["page_url"] = response.url
        item["video_url"] = ""
        if item["original_time"].startswith("来源"):
            dateTime = item["original_time"].split("日期 ")[1].split("日")[0]
            item["article_time"] = dateTime.replace("年", "-").replace("月", "-") + " 00:00"
        else:
            dateTime = item["original_time"].split("来源")[0]
            item["article_time"] = dateTime.replace("年", "-").replace("月", "-").replace("日", "")

        content_url = "http://gateway.caixin.com/api/newauth/checkAuthByIdJsonp?callback=jQuery17204740247761864116_" + str(
            int(time.time() * 1000)) + "&type=0&id=" + item["id"] + "&page=1&rand=" + str(
            self.rand) + "feeCode=null&_= " + str(int(time.time() * 1000))
        yield scrapy.Request(content_url, meta={'item': item}, callback=self.freed_item, dont_filter=True)

    def freed_item(self, response):
        item = response.meta['item']
        json_con = response.text.split('resetContentInfo(')[1].split(')"})')[0]
        unicodestr = json.loads(json.loads('"' + json_con + '"'))
        article_contents = jsonpath.jsonpath(unicodestr, "$..content")
        totalPage = jsonpath.jsonpath(unicodestr, "$..totalPage")
        try:
            if totalPage[0] != 0:
                content_url = "http://gateway.caixin.com/api/newauth/checkAuthByIdJsonp?callback=jQuery17204740247761864116_" + str(
                    int(time.time() * 1000)) + "&type=0&id=" + item["id"] + "&page=0&rand=" + str(
                    self.rand) + "feeCode=null&_= " + str(int(time.time() * 1000))
                yield scrapy.Request(content_url, meta={'item': item}, callback=self.page_item, dont_filter=True)
            elif totalPage[0] == 0:
                item["article_content"] = article_contents
                yield item
        except Exception:
            yield item

    def page_item(self, response):
        item = response.meta['item']
        json_con = response.text.split('resetContentInfo(')[1].split(')"})')[0]
        unicodestr = json.loads(json.loads('"' + json_con + '"'))
        article_contents = jsonpath.jsonpath(unicodestr, "$..content")
        item["article_content"] = article_contents
        yield item
