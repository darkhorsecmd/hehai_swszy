# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HehaiSwszyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HehaiTurtoInfo(scrapy.Item):
    url_object_id = scrapy.Field()  # url_ID
    url = scrapy.Field()  # url 地址
    image_url = scrapy.Field()  # image_url
    name = scrapy.Field()  # 姓名
    sex = scrapy.Field()  # 性别
    nation = scrapy.Field()  # 民族
    birth_date = scrapy.Field()  # 出生日期
    politics = scrapy.Field()  # 政治面貌
    education = scrapy.Field()  # 学历
    degree = scrapy.Field()  # 学位
    position = scrapy.Field()  # 职务
    address = scrapy.Field()  # 通讯地址
    phone = scrapy.Field()  # 联系电话
    email = scrapy.Field()  # 电子邮箱
    description = scrapy.Field()  # 详细介绍
