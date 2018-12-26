# -*- coding: utf-8 -*-
import time
import scrapy
from scrapy.selector import Selector
from fundbbsSpider.items import CompanySpiderItem
from fundbbsSpider.urlFilter import CompanyFilter


class ThCompanySpider(scrapy.Spider):
    name = 'thCompanySpider'
    allowed_domains = ['thfund.com.cn', 'cdn-thweb.tianhongjijin.com.cn']
    start_urls = ['http://www.thfund.com.cn/cnotice_list',
                  'http://www.thfund.com.cn/notice_list']
    custom_settings = {
        'ITEM_PIPELINES': {
            "fundSpider.pipelines.CompanyspiderPipeline": 300
        }
    }

    def __init__(self, SPIDER_TYPE=None, *args, **kwargs):
        super(ThCompanySpider, self).__init__(*args, **kwargs)
        self.SPIDER_TYPE = SPIDER_TYPE
        print(SPIDER_TYPE)

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath("//div[@class='list-title']/span/a/@href").extract()
        titles = sel.xpath("//div[@class='list-title']/span/a/text()").extract()
        fundtimes = sel.xpath("//span[@class='pull-right']/text()").extract()
        filter = CompanyFilter()
        for i in range(len(links)):
            item = CompanySpiderItem()
            item['company'] = "天弘"
            if links[i].startswith("http"):
                if 'cnotice' in response.url:
                    item["announcement_type"] = "公司公告"
                else:
                    item["announcement_type"] = "基金公告"
                item["file_url"] = links[i]
                item['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item['title'] = titles[i]
                item['time'] = fundtimes[i]
                item['announcement_url'] = ''
                item["content_text"] = ''
                item['content'] = ''
                if filter.company_request(item):
                    yield item
                else:
                    break
            else:
                base_url = "http://www.thfund.com.cn"
                item['title'] = titles[i]
                item['time'] = fundtimes[i]
                item["file_url"] = ''
                item['announcement_url'] = base_url + links[i]
                if filter.company_request(item):
                    yield scrapy.Request(base_url + links[i], meta={'item': item},
                                         callback=self.company_item, dont_filter=True)
                else:
                    if self.SPIDER_TYPE == 'INCREMENT' or self.SPIDER_TYPE == None:
                        break
                    elif self.SPIDER_TYPE == 'ALL':
                        continue
                    else:
                        raise Exception("参数设置错误")

    def company_item(self, response):
        item = response.meta['item']
        content = response.xpath('//div[@class="entry"]').extract()[0]
        content_text = response.xpath('//div[@class="entry"]/descendant::text()').extract()
        url = response.url
        if content:
            item['content'] = content
        if 'cnotice' in url:
            item["announcement_type"] = "公司公告"
        else:
            item["announcement_type"] = "基金公告"
        if content_text:
            text = ''.join(content_text)
            text = text.replace(" ", "")
            item["content_text"] = text
        item['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield item
