# -*- coding: utf-8 -*-

import time
import scrapy
from fundbbsSpider.items import FundSpiderItem
from fundbbsSpider.urlFilter import FundFilter
from urllib import parse
import uuid


class YhFundSpider(scrapy.Spider):
    name = 'yhFundSpider'
    allowed_domains = ['yhfund.com.cn']
    start_urls = ['http://www.yhfund.com.cn/main/qxjj/index.shtml']

    custom_settings = {
        'ITEM_PIPELINES': {
            "fundbbsSpider.pipelines.fundspiderPipeline": 300
        }
    }

    def __init__(self, SPIDER_TYPE=None, *args, **kwargs):
        super(YhFundSpider, self).__init__(*args, **kwargs)
        self.SPIDER_TYPE = SPIDER_TYPE

    def parse(self, response):
        links = response.xpath("//table[@class='table_a']/tbody/tr/td[1]/a/@href").extract()
        fund_names = response.xpath("//table[@class='table_a']/tbody/tr/td[1]/a/text()").extract()
        fund_codes = response.xpath("//table[@class='table_a']/tbody/tr/td[2]/text()").extract()
        unit_net_value = response.xpath("//table[@class='table_a']/tbody/tr/td[4]/text()").extract()
        cumulative_net_value = response.xpath("//table[@class='table_a']/tbody/tr/td[5]/text()").extract()
        last_three_months = response.xpath("//table[@class='table_a']/tbody/tr/td[8]/text()").extract()
        last_year = response.xpath("//table[@class='table_a']/tbody/tr/td[9]/text()").extract()
        since_this_year = response.xpath("//table[@class='table_a']/tbody/tr/td[10]/text()").extract()
        since_established = response.xpath("//table[@class='table_a']/tbody/tr/td[11]/text()").extract()
        for i in range(len(links)):
            item = FundSpiderItem()
            link = "http://www.yhfund.com.cn" + links[i]
            item["fund_name"] = fund_names[i]
            item["fund_code"] = fund_codes[i]
            item["fund_url"] = link
            item["unit_net_value"] = unit_net_value[i]
            item["cumulative_net_value"] = cumulative_net_value[i].strip()
            item["last_three_months"] = last_three_months[i].strip()
            item["last_year"] = last_year[i].strip()
            item["since_this_year"] = since_this_year[i].strip()
            item["since_established"] = since_established[i].strip()
            yield scrapy.Request(link, meta={'item': item}, callback=self.fndFacts, dont_filter=True)

    def fndFacts(self, response):
        item = response.meta['item']
        link = response.url.replace("fndFacts", "fundDisc")
        web_url = "http://www.yhfund.com.cn"
        item["today_variety"] = response.xpath("//div[@class='earnings_rate']/span[2]/strong/text()").extract()[0]
        fund_manager_images = response.xpath("//div[@class='photo_box']/img/@src").extract()
        date = response.xpath("/div[@class='earnings_rate']/span[2]/text()").extract()[0]
        update_date = date.split("(")[1].split(")")[0],
        item["update_date"] = update_date
        if fund_manager_images:
            item["fund_manager_image"] = web_url + fund_manager_images[0]
        else:
            item["fund_manager_image"] = ""
        introduction = response.xpath("//div[@id='showOtherInfo']/div[@class='manager_infor']/p").extract()
        manager_introduction = ""
        for each in introduction:
            manager_introduction += each
        item["manager_introduction"] = manager_introduction
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
                item['company'] = "银华"
                item["fund_name"] = item_parent["fund_name"]
                item["fund_code"] = item_parent["fund_code"]
                item["fund_url"] = item_parent["fund_url"]
                item["update_date"] = item_parent["update_date"]
                item["unit_net_value"] = item_parent["unit_net_value"]
                item["cumulative_net_value"] = item_parent["cumulative_net_value"]
                item["last_three_months"] = item_parent["last_three_months"]
                item["last_year"] = item_parent["last_year"]
                item["since_this_year"] = item_parent["since_this_year"]
                item["since_established"] = item_parent["since_established"]
                item["today_variety"] = item_parent["today_variety"]
                item["fund_manager_image"] = item_parent["fund_manager_image"]
                item["manager_introduction"] = item_parent["manager_introduction"]
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
                item['announcement_id'] = str(uuid.uuid4())
                if filter.fund_request(item) or i < 1:
                    yield item
                else:
                    if self.SPIDER_TYPE == 'INCREMENT' or self.SPIDER_TYPE == None:
                        break
                    elif self.SPIDER_TYPE == 'ALL':
                        continue
                    else:
                        raise Exception("参数设置错误")
