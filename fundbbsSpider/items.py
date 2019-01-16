import scrapy


class IndexSpiderItem(scrapy.Item):
    # 编号
    id = scrapy.Field()
    # 标题
    article_title = scrapy.Field()
    # 时间
    article_time = scrapy.Field()
    # 简介
    article_introduction = scrapy.Field()
    # 图片链接
    image_url = scrapy.Field()
    # 文章内容
    article_content = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 视频链接
    video_url = scrapy.Field()
    # 文章链接
    page_url = scrapy.Field()
    # 完整的时间
    original_time = scrapy.Field()


class WeeklySpiderItem(scrapy.Item):
    # 期刊编号
    period_id = scrapy.Field()
    # 期号
    weekly_num = scrapy.Field()
    # 期刊时间
    weekly_time = scrapy.Field()
    # 标题
    weekly_title = scrapy.Field()
    # 头条主题
    weekly_summary = scrapy.Field()
    # 期刊封面图片链接
    weekly_image = scrapy.Field()
    # 周刊期号图片链接
    weekly_issue_image = scrapy.Field()
    # 周刊目录链接
    weekly_url = scrapy.Field()

    # 编号
    id = scrapy.Field()
    # 文章类型
    article_type = scrapy.Field()
    # 标题
    article_title = scrapy.Field()
    # 主题概要
    article_summary = scrapy.Field()
    # 文章完整时间
    article_time = scrapy.Field()
    # 文章图片链接
    article_image = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
    # 文章链接
    article_url = scrapy.Field()
    # 文章内容
    article_content = scrapy.Field()
    # 类型标志
    article_sign = scrapy.Field()
    # 文章时间
    article_deal_time = scrapy.Field()


class FundSpiderItem(scrapy.Item):
    # 网站
    company = scrapy.Field()
    # 基金名称
    fund_name = scrapy.Field()
    # 基金代码
    fund_code = scrapy.Field()
    # 链接
    fund_url = scrapy.Field()
    # 更新日期
    update_date = scrapy.Field()
    # 单位净值
    unit_net_value = scrapy.Field()
    # 累计净值
    cumulative_net_value = scrapy.Field()
    # 最近日涨跌幅
    today_variety = scrapy.Field()
    # 最近三个月
    last_three_months = scrapy.Field()
    # 最近一年
    last_year = scrapy.Field()
    # 今年以来
    since_this_year = scrapy.Field()
    # 成立以来
    since_established = scrapy.Field()
    # 基金经理头像
    fund_manager_image = scrapy.Field()
    # 经理介绍
    manager_introduction = scrapy.Field()



    #公告编号
    announcement_id = scrapy.Field()
    # 标题
    announcement_title = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 内容文本
    content_text = scrapy.Field()
    # 内容页面链接
    file_url = scrapy.Field()
    # 公告类型
    announcement_type = scrapy.Field()
    # 公告链接
    announcement_url = scrapy.Field()
    # 公告时间
    announcement_time = scrapy.Field()
    # 创建时间
    create_time = scrapy.Field()
