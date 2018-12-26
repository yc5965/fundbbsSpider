import pymysql
from scrapy.conf import settings
import pymongo


class IndexSpiderPipeline(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        db = pymongo.MongoClient(settings['MG_CONN'])[settings['MG_DB']]
        # 存放数据的数据库表名
        self.post = db["fund_caixinIndex"]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.update(
            {"id": item["id"]},
            {'$set': data},
            True)
        return item


class WeeklySpiderPipeline(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        db = pymongo.MongoClient(settings['MG_CONN'])[settings['MG_DB']]
        # 存放数据的数据库表名
        self.post = db["fund_caixinWeekly"]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.update(
            {"id": item["id"]},
            {'$set': data},
            True)
        return item


class CompanyspiderPipeline(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        db = pymongo.MongoClient(settings['MG_CONN'])[settings['MG_DB']]
        # 存放数据的数据库表名
        self.post = db["fund_company"]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.update(
            {'file_url': data["file_url"],
             'title': data["title"],
             'time': data["time"],
             'announcement_url': data["announcement_url"], },
            {'$set': data},
            True)
        return item


class fundspiderPipeline(object):
    def __init__(self):
        # 创建MONGODB数据库链接
        db = pymongo.MongoClient(settings['MG_CONN'])[settings['MG_DB']]
        # 存放数据的数据库表名
        self.post = db["fund_announcement"]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.update(
            {'file_url': data["file_url"],
             'fund_code': data["fund_code"],
             'announcement_title': data["announcement_title"],
             'announcement_time': data["announcement_time"],
             'announcement_url': data["announcement_url"], },
            {'$set': data},
            True)
        return item
