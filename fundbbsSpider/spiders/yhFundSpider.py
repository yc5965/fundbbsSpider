# -*- coding: utf-8 -*-

import time
import scrapy
from fundSpider.items import FundSpiderItem
from fundSpider.urlFilter import FundFilter
from urllib import parse


class YhFundSpider(scrapy.Spider):
    name = 'yhFundSpider'
    allowed_domains = ['yhfund.com.cn']
    start_urls = ['http://www.yhfund.com.cn/main/qxjj/index.shtml']

    custom_settings = {
        'ITEM_PIPELINES': {
            "fundSpider.pipelines.fundspiderPipeline": 300
        }
    }

    def __init__(self, SPIDER_TYPE=None, *args, **kwargs):
        super(YhFundSpider, self).__init__(*args, **kwargs)
        self.SPIDER_TYPE = SPIDER_TYPE
        print(SPIDER_TYPE)

    def parse(self, response):
        links = response.xpath("//table[@class='table_a']/tbody/tr/td[1]/a/@href").extract()
        fund_names = response.xpath("//table[@class='table_a']/tbody/tr/td[1]/a/text()").extract()
        fund_codes = response.xpath("//table[@class='table_a']/tbody/tr/td[2]/text()").extract()
        for i in range(len(links)):
            item = FundSpiderItem()
            link = "http://www.yhfund.com.cn" + links[i].replace("fndFacts", "fundDisc")
            item["fund_name"] = fund_names[i]
            item["fund_code"] = fund_codes[i]
            item["fund_url"] = link
            yield scrapy.Request(link, meta={'item': item}, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        item_parent = response.meta['item']
        announcement_types = response.xpath("//div[@class='a_box']/h4/text()").extract()
        filter = FundFilter()
        for i in range(len(announcement_types)):
            announcement_links = response.xpath("//ul[@class='information_list'][" + str(i) + "]/li/a/@href").extract()
            announcement_times = response.xpath(
                "//ul[@class='information_list'][" + str(i) + "]/li/span/text()").extract()
            announcement_title = response.xpath("//ul[@class='information_list'][" + str(i) + "]/li/a/text()").extract()
            for j in range(len(announcement_links)):
                item = FundSpiderItem()
                item["fund_name"] = item_parent["fund_name"]
                item["fund_code"] = item_parent["fund_code"]
                item["fund_url"] = item_parent["fund_url"]
                item['company'] = "银华"
                base_url = 'http://www.yhfund.com.cn/cgi-bin/article/ArticleAction?'
                item['announcement_type'] = announcement_types[i]
                item['announcement_title'] = announcement_title[j]
                item["announcement_url"] = ''
                item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                item['content'] = ''
                item["content_text"] = ''
                link = "/upload" + announcement_links[j].split("/upload")[-1].split("'")[0]
                key = parse.urlencode({"title": item['announcement_title']},
                                      encoding="GB2312") + "&function=DownLoad&url=" + link
                item["file_url"] = base_url + key
                item['announcement_time'] = announcement_times[j]
                if filter.fund_request(item):
                    yield item
                else:
                    if self.SPIDER_TYPE == 'INCREMENT' or self.SPIDER_TYPE == None:
                        break
                    elif self.SPIDER_TYPE == 'ALL':
                        continue
                    else:
                        raise Exception("参数设置错误")
