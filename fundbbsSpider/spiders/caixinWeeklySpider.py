# -*- coding: utf-8 -*-
import time
import scrapy
import hashlib
import random
import json
import jsonpath
from fundbbsSpider.items import WeeklySpiderItem
from scrapy.conf import settings
from fundbbsSpider.urlFilter import WeeklyFilter


class CaixinWeeklySpider(scrapy.Spider):
    name = 'caixinWeeklySpider'
    allowed_domains = ['caixin.com']
    start_urls = ['http://weekly.caixin.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            "fundbbsSpider.pipelines.WeeklySpiderPipeline": 300
        }
    }

    def __init__(self, SPIDER_TYPE=None, *args, **kwargs):
        super(CaixinWeeklySpider, self).__init__(*args, **kwargs)
        self.SPIDER_TYPE = SPIDER_TYPE
        self.password = settings["PASSWORD"]
        self.loginName = settings["LOGINNAME"]
        self.rand = random.uniform(0, 1)
        self.weekly_links = []

    def parse(self, response):
        if self.SPIDER_TYPE == "INCREMENT":
            urls = response.xpath("//div[@class='mi']/a/@href").extract()
        else:
            urls = response.xpath(
                "//div[@id='col_wq_1']/div[@class='xsjCon']/ul/li/a/@href|//div[@class='mi']/a/@href").extract()
        urlFilter = WeeklyFilter()
        for each in urls:
            count = urlFilter.filter_request(each)
            if count[0][0] == 0:
                self.weekly_links.append(each)
        if self.weekly_links:
            md = hashlib.md5()
            md.update(self.password.encode("utf-8"))
            pwd = md.hexdigest()
            login_url = "https://gateway.caixin.com/api/ucenter/user/v1/loginJsonp?callback=jQuery17204291106502992419_" + str(
                int(
                    time.time() * 1000)) + "&account=" + self.loginName + "&password=" + pwd + "&device=CaixinWebsite&deviceType=5&unit=1&userTag=null&areaCode=%2B86&_=" + str(
                int((time.time() * 1000)))
            yield scrapy.Request(login_url, callback=self.login_parse, dont_filter=True)

    def login_parse(self, response):
        for each in self.weekly_links:
            yield scrapy.Request(each, callback=self.index_parse, dont_filter=True)

    def index_parse(self, response):
        item = WeeklySpiderItem()
        item["weekly_url"] = response.url
        item["period_id"] = response.url.split("com")[1].replace("/", "_")
        item["weekly_num"] = response.xpath("normalize-space(//div[@class='title']/text())").extract()[0]
        item["weekly_time"] = response.xpath("normalize-space(//div[@class='source']/text())").extract()[0]
        item["weekly_title"] = response.xpath("normalize-space(//div[@class='report']/dl/dt/a/text())").extract()[0]
        item["weekly_summary"] = response.xpath("normalize-space(//div[@class='report']/dl/dd/text())").extract()[0]
        item["weekly_image"] = response.xpath("normalize-space(//div[@class='cover']/img/@src)").extract()[0]
        item["weekly_issue_image"] = response.xpath("normalize-space(//div[@class='date']/img/@src)").extract()[0]

        art_type_list1 = response.xpath("//div[@class='magContentlf2']/div[@class='magIntrotit']/span/text()").extract()
        art_type_list2 = response.xpath("//div[@class='magContentce']/div[@class='magIntrotit']/span/text()").extract()
        art_type_list3 = response.xpath("//div[@class='magContentri2']/div[@class='magIntrotit']/span/text()").extract()
        toutiao = response.xpath("//div[@class='report']/dl/dt/a/@href").extract()
        futiao = response.xpath("//div[@class='report']/ul/p/a/@href").extract()

        for i in range(len(art_type_list1)):
            art_title_list1 = response.xpath("//div[@class='magContentlf2']/div[@class='magIntrotit'][" + str(
                i + 1) + "]/following-sibling::dl/dt/a/@href").extract()
            for each in art_title_list1:
                item1 = WeeklySpiderItem(item)
                item1["article_type"] = art_type_list1[i]
                item1["article_sign"] = "1"
                yield scrapy.Request(each, meta={'item': item1}, callback=self.data_process, dont_filter=True)

        for j in range(len(art_type_list2)):
            art_title_list2 = response.xpath("//div[@class='magContentce']/div[@class='magIntrotit'][" + str(
                j + 1) + "]/following-sibling::dl/dt/a/@href").extract()
            for each in art_title_list2:
                item2 = WeeklySpiderItem(item)
                item2["article_type"] = art_type_list1[j]
                item2["article_sign"] = "2"
                yield scrapy.Request(each, meta={'item': item2}, callback=self.data_process, dont_filter=True)

        for k in range(len(art_type_list3)):
            art_title_list3 = response.xpath("//div[@class='magContentri2']/div[@class='magIntrotit'][" + str(
                k + 1) + "]/following-sibling::dl/dt/a/@href").extract()
            for each in art_title_list3:
                item3 = WeeklySpiderItem(item)
                item3["article_type"] = art_type_list1[k]
                item3["article_sign"] = "3"
                yield scrapy.Request(each, meta={'item': item3}, callback=self.data_process, dont_filter=True)

        for each in toutiao:
            tou = WeeklySpiderItem(item)
            tou["article_type"] = "头条"
            tou["article_sign"] = "0"
            yield scrapy.Request(each, meta={'item': tou}, callback=self.data_process, dont_filter=True)

        for each in futiao:
            fu = WeeklySpiderItem(item)
            fu["article_type"] = "次条"
            fu["article_sign"] = "4"
            yield scrapy.Request(each, meta={'item': fu}, callback=self.data_process, dont_filter=True)

    def data_process(self, response):
        item = response.meta['item']
        item["id"] = response.url.split("/")[-1].split(".html")[0]
        item["article_title"] = response.xpath("normalize-space(//div[@id='conTit']/h1/text()[1])").extract()[0]
        item["article_time"] = \
            response.xpath("normalize-space(//div[@id='artInfo']|//div[@id='conTit']/ul/li[@class='time'])").extract()[0]
        article_summary = \
            response.xpath("//p[@class='zhaiyao'][1]/text()|//div/div[@id='subhead']/text()[1]").extract()
        article_image = response.xpath("//div[@id='the_content']/div/dl/dt/img/@src").extract()
        if len(article_summary) == 0:
            item["article_summary"] = ""
        else:
            item["article_summary"] = article_summary[0]

        if len(article_image) == 0:
            item["article_image"] = ""
        else:
            item["article_image"] = article_image[0]
        item["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item["article_url"] = response.url

        if item["article_time"].startswith("来源"):
            dateTime = item["article_time"].split("日期 ")[1].split("日")[0]
            item["article_deal_time"] = dateTime.replace("年", "-").replace("月", "-") + " 00:00"
        else:
            dateTime = item["article_time"].split("来源")[0]
            item["article_deal_time"] = dateTime.replace("年", "-").replace("月", "-").replace("日", "")

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
        if totalPage[0] != 0:
            content_url = "http://gateway.caixin.com/api/newauth/checkAuthByIdJsonp?callback=jQuery17204740247761864116_" + str(
                int(time.time() * 1000)) + "&type=0&id=" + item["id"] + "&page=0&rand=" + str(
                self.rand) + "feeCode=null&_= " + str(int(time.time() * 1000))
            yield scrapy.Request(content_url, meta={'item': item}, callback=self.page_item, dont_filter=True)
        elif article_contents == "" or article_contents == 0 or article_contents == ' ':
            raise Exception("账号无权限，请确认后重试")
        else:
            item["article_content"] = article_contents
            yield item

    def page_item(self, response):
        item = response.meta['item']
        json_con = response.text.split('resetContentInfo(')[1].split(')"})')[0]
        unicodestr = json.loads(json.loads('"' + json_con + '"'))
        article_contents = jsonpath.jsonpath(unicodestr, "$..content")
        item["article_content"] = article_contents
        yield item