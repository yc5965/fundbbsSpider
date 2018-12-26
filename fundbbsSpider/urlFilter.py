from scrapy.conf import settings
import pymongo


class IndexFilter(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        db = pymongo.MongoClient(settings['MG_CONN'])[settings['MG_DB']]
        # 存放数据的数据库表名
        self.post = db["fund_caixinIndex"]

    def filter_request(self, item):
        data = dict(item)
        if (self.post.count({"page_url": data["page_url"]}) > 0):
            return False
        else:
            return True


class WeeklyFilter(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        db = pymongo.MongoClient(settings['MG_CONN'])[settings['MG_DB']]
        # 存放数据的数据库表名
        self.post = db["fund_caixinWeekly"]

    def filter_request(self, item):
        data = dict(item)
        if (self.post.count({"weekly_url": data["weekly_url"]}) > 0):
            return False
        else:
            return True


class FundFilter(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        db = pymongo.MongoClient(settings['MG_CONN'])[settings['MG_DB']]
        # 存放数据的数据库表名
        self.post = db["fund_announcement"]

    def fund_request(self, item):
        data = dict(item)
        if (self.post.count({"fund_code": data["fund_code"],
                             "announcement_title": data["announcement_title"],
                             "announcement_time": data['announcement_time']}) > 0):
            return False
        else:
            return True


class CompanyFilter(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        db = pymongo.MongoClient(settings['MG_CONN'])[settings['MG_DB']]
        # 存放数据的数据库表名
        self.post = db["fund_company"]

    def company_request(self, item):
        data = dict(item)
        if (self.post.count({'file_url': data["file_url"],
                             'title': data["title"],
                             'time': data["time"],
                             'announcement_url': data["announcement_url"], }) > 0):
            return False
        else:
            return True
