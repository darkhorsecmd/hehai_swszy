# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from urllib import parse
from hehai_swszy.filterTags import filter_tags
from scrapy.loader import ItemLoader
from utils.common import get_md5
from hehai_swszy.items import HehaiTurtoInfo
from scrapy.selector import Selector


class HehaiShxySpider(scrapy.Spider):
    name = 'hehai_swszy'
    allowed_domains = ['shxy.hhu.edu.cn']
    start_urls = ['http://shxy.hhu.edu.cn/3208/list.htm']

    def parse(self, response):
        post_urls = response.css(
            '.wp_column.column-4.selected .sub_list.list-paddingleft-2 .sub-item a::attr(href)').extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_each_url, dont_filter=True)

    def parse_each_url(self, response):

        post_nodes = response.css('#wp_content_w6_0 table a::attr(href)').extract()
        for post_node in post_nodes:
            yield Request(post_node, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        res = response.selector.xpath("//table//tbody")
        res_name = res.xpath("//tr[1]//td[2]")
        res_sex = res.xpath("//tr[1]//td[4]")
        res_nation = res.xpath("//tr[2]//td[2]")
        res_birth_date = res.xpath("//tr[2]//td[4]")
        res_politics = res.xpath("//tr[3]//td[2]")
        res_education = res.xpath("//tr[4]//td[2]")
        res_degree = res.xpath("//tr[4]//td[4]")
        res_position = res.xpath("//tr[5]//td[4]")
        res_address = res.xpath("//tr[6]//td[2]")
        res_phone = res.xpath("//tr[7]//td[4]")
        res_email = res.xpath("//tr[8]//td[2]")
        res_description = res.xpath("//tr[9]")
        # 获得突破的地址，只保存图片的url
        image_post_url = res.xpath(
            "//img/@src").extract_first()
        image_url = parse.urljoin(response.url, image_post_url)
        url = response.url
        url_object_id = get_md5(response.url)
        name = res_name.xpath('string(.)').extract()[0]
        if name is not None:
            name = name.strip().replace("\xa0", "").replace(" ", "")
        sex = res_sex.xpath('string(.)').extract()[0]
        if sex is not None:
            sex = sex.strip().replace("\xa0", "").replace(" ", "")
        nation = res_nation.xpath('string(.)').extract()[0]
        if nation is not None:
            nation = nation.strip().replace("\xa0", "").replace(" ", "")
        birth_date = res_birth_date.xpath('string(.)').extract()[0]
        if birth_date is not None:
            birth_date = birth_date.strip().replace("\xa0", "").replace(" ", "")
        politics = res_politics.xpath('string(.)').extract()[0]
        if politics is not None:
            politics = politics.strip().replace("\xa0", "").replace(" ", "")
        education = res_education.xpath('string(.)').extract()[0]
        if education is not None:
            education = education.strip().replace("\xa0", "").replace(" ", "")
        degree = res_degree.xpath('string(.)').extract()[0]
        if degree is not None:
            degree = degree.strip().replace("\xa0", "").replace(" ", "")
        position = res_position.xpath('string(.)').extract()[0]
        if position is not None:
            position = position.strip().replace("\xa0", "").replace(" ", "")
        address = res_address.xpath('string(.)').extract()[0]
        if address is not None:
            address = address.strip().replace("\xa0", "").replace(" ", "")
        phone = res_phone.xpath('string(.)').extract()[0]
        if phone is not None:
            phone = phone.strip().replace("\xa0", "").replace(" ", "")
        email = res_email.xpath('string(.)').extract()[0]
        if email is not None:
            email = email.strip().replace("\xa0", "").replace(" ", "")
        description = res_description.xpath('string(.)').extract()[0]

        item = HehaiTurtoInfo()
        item["url"] = url
        item["url_object_id"] = url_object_id
        item["name"] = name  # 姓名
        item["sex"] = sex  # 性别
        item["image_url"] = image_url
        item["nation"] = nation  # 民族
        item["birth_date"] = birth_date  # 出生日期
        item["politics"] = politics  # 政治面貌
        item["education"] = education  # 学历
        item["degree"] = degree  # 学位
        item["position"] = position  # 技术职称
        item["address"] = address  # 通讯地址
        item["phone"] = phone  # 联系电话
        item["email"] = email  # 电子邮箱
        item["description"] = description  # 详细介绍
        yield item
