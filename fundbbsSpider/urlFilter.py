from scrapy.conf import settings
import pymysql


class IndexFilter(object):
    def __init__(self):
        # 创建Mysql数据库链接
        self.conn = pymysql.connect(host=settings['MY_HOST'],
                                    user=settings['MY_USER'],
                                    passwd=settings['MY_PASSWD'],
                                    database=settings['MY_DATABASE'],
                                    charset=settings['MY_CHARSET'])
        self.cursor = self.conn.cursor()

    def filter_request(self, url):
        self.cursor.execute(settings["INDEX_FILTER_URL"], [url])
        cls = self.cursor.fetchall()
        return cls

    def fill_request(self):
        self.cursor.execute(settings["INDEX_FILL_URL"], [""])
        urls = self.cursor.fetchall()
        return urls


class WeeklyFilter(object):
    def __init__(self):
        # 创建Mysql数据库链接
        self.conn = pymysql.connect(host=settings['MY_HOST'],
                                    user=settings['MY_USER'],
                                    passwd=settings['MY_PASSWD'],
                                    database=settings['MY_DATABASE'],
                                    charset=settings['MY_CHARSET'])
        self.cursor = self.conn.cursor()

    def filter_request(self, url):
        self.cursor.execute(settings["WEEKLY_FILTER_URL"], [url])
        cls = self.cursor.fetchall()
        return cls


class FundFilter(object):
    def __init__(self):
        # 创建Mysql数据库链接
        self.conn = pymysql.connect(host=settings['MY_HOST'],
                                    user=settings['MY_USER'],
                                    passwd=settings['MY_PASSWD'],
                                    database=settings['MY_DATABASE'],
                                    charset=settings['MY_CHARSET'])
        self.cursor = self.conn.cursor()

    def fund_request(self, item):
        data = dict(item)
        self.cursor.execute(settings["FUND_FILTER_URL"],
                            [data["fund_code"], data["announcement_title"], data['announcement_time']])
        count = self.cursor.fetchall()
        if count[0][0] > 0:
            return False
        else:
            return True
