# -*- coding: utf-8 -*-

import scrapy
import time
from fundbbsSpider.items import FundSpiderItem
import json
import jsonpath
from fundbbsSpider.urlFilter import FundFilter
import uuid


class ThfundSpider(scrapy.Spider):
    name = 'thFundSpider'
    allowed_domains = ['thfund.com.cn', 'cdn-thweb.tianhongjijin.com.cn']
    url = "http://www.thfund.com.cn/thfund/fundlist/api/?risk=any_risk&limit=any_limit&type=any_type&pager=pager_"
    offset = 1
    start_urls = [url + str(offset)]
    custom_settings = {
        'ITEM_PIPELINES': {
            "fundbbsSpider.pipelines.fundspiderPipeline": 300
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
        update_date = jsonpath.jsonpath(data, "$..date")
        unit_net_value = jsonpath.jsonpath(data, "$..最新净值")
        cumulative_net_value = jsonpath.jsonpath(data, "$..累计净值")
        last_three_months = jsonpath.jsonpath(data, "$..近3月涨幅")
        last_year = jsonpath.jsonpath(data, "$..近1年涨幅")
        since_this_year = jsonpath.jsonpath(data, "$..今年以来涨幅")
        since_established = jsonpath.jsonpath(data, "$..成立以来")
        for i in range(len(codes)):
            item = FundSpiderItem()
            fund_url = ("http://www.thfund.com.cn/fundinfo/" + str(codes[i]))
            item['fund_name'] = fund_name[i]
            item['fund_code'] = codes[i]
            item['fund_url'] = fund_url
            item['update_date'] = update_date[i]
            item['unit_net_value'] = unit_net_value[i]
            item['cumulative_net_value'] = cumulative_net_value[i]
            item['last_three_months'] = last_three_months[i]
            item['last_year'] = last_year[i]
            item['since_this_year'] = since_this_year[i]
            item['since_established'] = since_established[i]

            yield scrapy.Request(item['fund_url'], meta={'item': item}, callback=self.type_parse, dont_filter=True)
        if self.offset < 10:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse, dont_filter=True)

    def type_parse(self, response):
        item_parent = response.meta['item']
        filter = FundFilter()
        today_variety = response.xpath("//table[@id='trend_table']/tbody/tr[1]/td[4]/text()").extract()
        if today_variety:
            item_parent['today_variety'] = today_variety[0]
        else:
            item_parent['today_variety'] = "0%"
        item_parent['fund_manager_image'] = response.xpath(
            "//div[@class='col-md-5 padding-clear pull-left ']/img/@src").extract()[0]
        introduction = response.xpath(
            "//h4[@class='margin-bottom-10']/text()|//div[@class='bot_tx_left']/p/text()|//div[@class='col-md-10 margin-left-d45 padding-clear padding-bottom-40']/p[3]/text()").extract()
        manager_introduction = ''
        for each in introduction:
            manager_introduction += each.strip()+","
        item_parent['manager_introduction'] = manager_introduction
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
                item['announcement_time'] = announcement_time[j]
                item['announcement_title'] = announcement_title[j]
                if filter.fund_request(item) or j < 1:
                    item['company'] = "天弘"
                    item['fund_url'] = item_parent['fund_url']
                    item['fund_name'] = item_parent['fund_name']
                    item['update_date'] = item_parent['update_date']
                    item['unit_net_value'] = item_parent['unit_net_value']
                    item['cumulative_net_value'] = item_parent['cumulative_net_value']
                    item['last_three_months'] = item_parent['last_three_months']
                    item['last_year'] = item_parent['last_year']
                    item['since_this_year'] = item_parent['since_this_year']
                    item['since_established'] = item_parent['since_established']
                    item['today_variety'] = item_parent['today_variety']
                    item['manager_introduction'] = item_parent['manager_introduction']
                    item['fund_manager_image'] = item_parent['fund_manager_image']
                    item['announcement_type'] = announcement_type.split("(")[0]
                    item['announcement_id'] = str(uuid.uuid4())
                    if announcement_links[j].startswith("/"):
                        base_url = "http://www.thfund.com.cn"
                        item['file_url'] = ''
                        item['announcement_url'] = base_url + announcement_links[j]
                        item['announcement_title'] = announcement_title[j]
                        item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        yield scrapy.Request(item['announcement_url'], meta={'item': item},
                                             callback=self.announcement_parse, dont_filter=True)

                    elif announcement_links[j].startswith("http"):
                        item['file_url'] = announcement_links[j]
                        item['announcement_url'] = ''
                        item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        item['content'] = ''
                        item['content_text'] = ''
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
        item['content_text'] = content_text
        yield item
