# -*- coding: utf-8 -*-

import scrapy
import time
from fundSpider.items import CompanySpiderItem
from urllib import parse
from fundSpider.urlFilter import CompanyFilter


class YhCompanySpider(scrapy.Spider):
    name = 'yhCompanySpider'
    allowed_domains = ['yhfund.com.cn']
    custom_settings = {
        'ITEM_PIPELINES': {
            "fundSpider.pipelines.CompanyspiderPipeline": 300
        }
    }

    def __init__(self, SPIDER_TYPE=None, *args, **kwargs):
        super(YhCompanySpider, self).__init__(*args, **kwargs)
        self.SPIDER_TYPE = SPIDER_TYPE
        print(SPIDER_TYPE)

    # 因为start_urls默认是get请求，uj所以要重写parse方法
    def start_requests(self):
        url = 'http://www.yhfund.com.cn/servlet/fund/FundAction?function=allFundDiscPageNew'
        post_data = {
            'curPage': "1",
            'numPerPage': "15",
            'totalRows': "10545",
        }

        yield scrapy.FormRequest(url=url, formdata=post_data, callback=self.parse_post, dont_filter=True)

    def parse_post(self, response):
        titles = response.xpath("//ul[@class='information_list']/li/@title").extract()
        fundtimes = response.xpath("//ul[@class='information_list']/li/span/text()").extract()
        links = response.xpath("//ul[@class='information_list']/li/a/@href").extract()
        filter = CompanyFilter()
        for i in range(len(links)):
            item = CompanySpiderItem()
            base_url = 'http://www.yhfund.com.cn/cgi-bin/article/ArticleAction?'
            item['company'] = "银华"
            item['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['title'] = titles[i].split("--2")[0]
            link = "/upload" + links[i].split("/upload")[-1].split("'")[0]
            key = parse.urlencode({"title": item['title']}, encoding="GB18030") + "&function=DownLoad&url=" + link
            item["file_url"] = base_url + key
            item['announcement_url'] = ''
            item["content_text"] = ''
            item['content'] = ''
            item["announcement_type"] = "公司公告"
            item['time'] = fundtimes[i]
            if filter.company_request(item):
                yield item
            else:
                if self.SPIDER_TYPE == 'INCREMENT' or self.SPIDER_TYPE == None:
                    break
                elif self.SPIDER_TYPE == 'ALL':
                    continue
                else:
                    raise Exception("参数设置错误")
