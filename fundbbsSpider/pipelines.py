import pymysql
from scrapy.conf import settings


class IndexSpiderPipeline(object):
    def __init__(self):
        # 创建Mysql数据库链接
        self.conn = pymysql.connect(host=settings['MY_HOST'],
                                    user=settings['MY_USER'],
                                    passwd=settings['MY_PASSWD'],
                                    database=settings['MY_DATABASE'],
                                    charset=settings['MY_CHARSET'])
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(settings["INDEX_INSERT_SQL"],
                            [item["id"], item["article_title"],
                             item["article_time"], item["article_introduction"],
                             item["image_url"], item["article_content"],
                             item["create_time"], item["video_url"],
                             item["page_url"], item["original_time"]])
        self.conn.commit()
        return item


class WeeklySpiderPipeline(object):
    def __init__(self):
        # 创建Mysql数据库链接
        self.conn = pymysql.connect(host=settings['MY_HOST'],
                                    user=settings['MY_USER'],
                                    passwd=settings['MY_PASSWD'],
                                    database=settings['MY_DATABASE'],
                                    charset=settings['MY_CHARSET'])
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(settings["PERIOD_INSERT_SQL"],
                            [item["period_id"], item["weekly_num"],
                             item["weekly_time"], item["weekly_title"],
                             item["weekly_summary"], item["weekly_image"],
                             item["create_time"], item["weekly_issue_image"],
                             item["weekly_url"]])

        self.cursor.execute(settings["WEEKLY_INSERT_SQL"],
                            [item["id"], item["article_type"],
                             item["period_id"], item["article_title"],
                             item["article_summary"], item["article_time"],
                             item["article_image"], item["create_time"],
                             item["article_url"], item["article_content"],
                             item["article_sign"], item["article_deal_time"]])
        self.conn.commit()
        return item


class fundspiderPipeline(object):
    def __init__(self):
        # 创建Mysql数据库链接
        self.conn = pymysql.connect(host=settings['MY_HOST'],
                                    user=settings['MY_USER'],
                                    passwd=settings['MY_PASSWD'],
                                    database=settings['MY_DATABASE'],
                                    charset=settings['MY_CHARSET'])
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(settings["ANNOUNCEMENT_INSERT_SQL"],
                            [item["announcement_id"], item["announcement_title"],
                             item["content"], item["content_text"], item["file_url"],
                             item["announcement_type"], item["announcement_url"],
                             item["announcement_time"], item["create_time"],
                             item["fund_code"]])

        self.cursor.execute(settings["FUND_INSERT_SQL"],
                            [item["fund_code"]+"|"+item["update_date"],item["company"],
                             item["fund_name"],item["fund_url"],item["fund_code"],
                             item["update_date"], item["unit_net_value"],
                             item["cumulative_net_value"], item["today_variety"],
                             item["last_three_months"], item["last_year"],
                             item["since_this_year"], item["since_established"],
                             item["fund_manager_image"], item["manager_introduction"]
                             ])
        self.conn.commit()
        return item
