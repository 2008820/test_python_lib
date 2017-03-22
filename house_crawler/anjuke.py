#! /usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
import sys
import hashlib
import requests
from lxml import etree
from ghost import Ghost
from pymongo import MongoClient
from commont import try_number
from time_parser import parse_time

reload(sys)
sys.setdefaultencoding("utf8")

ghost = Ghost()
parser = etree.HTMLParser()


class anquke(object):
    def __init__(self):
        self.strat_url = "http://chongqing.anjuke.com/sale/o5/"
        self.req = requests.Session()
        ip = "23.252.107.236"
        local_ip = "127.0.0.1"
        self.co = MongoClient(ip)["house"]["house"]
        self.result = {"all_payment": "总价", "webtitle": "网页title", "pubulish": "发布时间", "house_title": "小区名字",
                       "cqloc": "重庆区县", "cqroad": "街道", "years": "年代", "layout": "房屋架构", "area": "面积", "high": "高度",
                       "fitment": "装修程度", "price": "单价", "fpayment": "首付", "image_url": "房屋图片", "_id": "hash"}

    @try_number(5, 10)
    def curl(self, url):
        with ghost.start() as session:
            page, resources = session.open(url)
        if page.http_status == 404:
            return ''
        open("temp.html", "w").write(page.content)
        return page.content

    def _parser_rule(self, rule):
        try:
            return self.detail_body.find("." + rule).text.strip().replace(' ', '')
        except AttributeError:
            print rule
        except:
            print traceback.print_exc()
            raw_input('go on')
            return ''

    def detail_parser(self, html):

        self.detail_body = etree.HTML(str(html))
        if self.detail_body.find('.//title').text == "对不起，您要浏览的网页可能被删除，重命名或者暂时不可用:":
            print 'secces'
            return
        self.result["all_payment"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[1]/span[1]/em')
        self.result["web_title"] = self._parser_rule('//*[@id="content"]/div[2]/h3')
        code_pulish = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/h4/span')
        self.result["pubulish"] = parse_time(code_pulish).split(' ')[1]
        self.result["_id"] = hashlib.md5(code_pulish).hexdigest()
        self.result["house_title"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[1]/dl[1]/dd/a')
        self.result["cqloc"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[1]/dl[2]/dd/p/a[1]')
        self.result["cqroad"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[1]/dl[2]/dd/p/a[2]')
        # location = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[1]/dl[2]/dd/p/text')
        self.result["years"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[1]/dl[3]/dd')
        self.result["layout"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[2]/dl[1]/dd')
        self.result["area"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[2]/dl[2]/dd')
        self.result["high"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[2]/dl[4]/dd')
        self.result["fitment"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[3]/dl[1]/dd')
        self.result["price"] = self._parser_rule('//*[@id="content"]/div[3]/div[1]/div[3]/div/div/div[1]/div[3]/dl[2]/dd')
        self.result["fpayment"] = float(self.result["all_payment"]) * 0.2
        image_url_obj = self.detail_body.findall('.//*[@id="room_pic_wrap"]/div')
        self.result["image_url"] = [item.find('./img').get("data-src") for item in image_url_obj]
        self.save_mongodb()


    def save_mongodb(self):
        if self.co.find_one({"_id": self.result["_id"]}):
            exit("存在停止")
        self.co.update({"_id": self.result["_id"]}, self.result, upsert=True)

    def parser(self, html):
        body = etree.HTML(str(html))
        content = body.xpath('//*[@id="houselist-mod"]/li')
        for item in content:
            detail = item.xpath('.//div[@class="house-details"]')[0]
            url_obj = detail.find('.//a')
            url = url_obj.get('href')
            detail_html = self.curl(url)
            print url
            if not detail_html:
                print "404"*10
                continue

            self.detail_parser(detail_html)

    def run_all(self):
        for i in range(1, 100):
            print i
            url = 'http://chongqing.anjuke.com/sale/o5-p{}/'.format(i)
            html = self.curl(url)
            self.parser(html)


anquke().run_all()
# anquke().detail_parser('asdsd')
