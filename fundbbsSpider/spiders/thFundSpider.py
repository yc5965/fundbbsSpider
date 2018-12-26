# -*- coding: utf-8 -*-

import scrapy
import time
from fundSpider.items import FundSpiderItem
import json
import jsonpath
from fundSpider.urlFilter import FundFilter


class ThfundSpider(scrapy.Spider):
    name = 'thFundSpider'
    allowed_domains = ['thfund.com.cn', 'cdn-thweb.tianhongjijin.com.cn']
    url = "http://www.thfund.com.cn/thfund/fundlist/api/?risk=any_risk&limit=any_limit&type=any_type&pager=pager_"
    offset = 1
    start_urls = [url + str(offset)]
    custom_settings = {
        'ITEM_PIPELINES': {
            "fundSpider.pipelines.fundspiderPipeline": 300
        }
    }

    def __init__(self, SPIDER_TYPE=None, *args, **kwargs):
        super(ThfundSpider, self).__init__(*args, **kwargs)
        self.SPIDER_TYPE = SPIDER_TYPE
        print(SPIDER_TYPE)

    def parse(self, response):

        data = json.loads(response.text)
        data = json.dumps(data, ensure_ascii=False)
        data = json.loads(data)
        codes = jsonpath.jsonpath(data, "$..基金代码")
        fund_name = jsonpath.jsonpath(data, "$..基金名称")
        for i in range(len(codes)):
            item = FundSpiderItem()
            fund_url = ("http://www.thfund.com.cn/fundinfo/" + str(codes[i]))
            item['fund_name'] = fund_name[i]
            item['fund_code'] = codes[i]
            item['fund_url'] = fund_url
            yield scrapy.Request(item['fund_url'], meta={'item': item}, callback=self.type_parse, dont_filter=True)
        if self.offset < 10:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse, dont_filter=True)

    def type_parse(self, response):
        item_parent = response.meta['item']
        filter = FundFilter()
        announcement_types = response.xpath(
            "//div[@id='htab3']/descendant::h5[@class='font14 font-color-d23337']/text()").extract()
        for k in range(len(announcement_types)):
            announcement_type = announcement_types[k]
            announcement_links = response.xpath(
                "//div[@class='row margin-clear'][" + str(k + 2) + "]/div[@class='col-md-12']/p/a/@href").extract()
            announcement_title = response.xpath(
                "//div[@class='row margin-clear'][" + str(k + 2) + "]/div[@class='col-md-12']/p/a/text()").extract()
            announcement_time = response.xpath("//div[@class='row margin-clear'][" + str(
                k + 2) + "]/div[@class='col-md-12']/p/small[@class='pull-right']/text()").extract()
            for j in range(len(announcement_links)):
                item = FundSpiderItem()
                item['fund_code'] = item_parent['fund_code']
                item["announcement_time"] = announcement_time[j]
                item["announcement_title"] = announcement_title[j]
                if filter.fund_request(item):
                    item['company'] = "天弘"
                    item['fund_url'] = item_parent['fund_url']
                    item['fund_name'] = item_parent['fund_name']
                    item['announcement_type'] = announcement_type.split("(")[0]
                    if announcement_links[j].startswith("/"):
                        base_url = "http://www.thfund.com.cn"
                        item["file_url"] = ''
                        item['announcement_url'] = base_url + announcement_links[j]
                        item['announcement_title'] = announcement_title[j]
                        item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        yield scrapy.Request(item['announcement_url'], meta={'item': item},
                                             callback=self.announcement_parse, dont_filter=True)

                    elif announcement_links[j].startswith("http"):
                        item["file_url"] = announcement_links[j]
                        item["announcement_url"] = ''
                        item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        item['content'] = ''
                        item["content_text"] = ''
                        yield item

                else:
                    if self.SPIDER_TYPE == 'INCREMENT' or self.SPIDER_TYPE == None:
                        break
                    elif self.SPIDER_TYPE == 'ALL':
                        continue
                    else:
                        raise Exception("参数设置错误")

    def announcement_parse(self, response):
        item = response.meta['item']
        content = ""
        content_text = ""
        if item["announcement_url"]:
            content = response.xpath('//div[@class="entry"]').extract()[0]
            content_text = response.xpath('//div[@class="entry"]/descendant::text()').extract()
            text = ''.join(content_text)
            content_text = text.replace(" ", "")
        else:
            content_text = ""
            content = ""
        item['content'] = content
        item["content_text"] = content_text
        yield item
