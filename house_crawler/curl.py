#! /usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from lxml import etree
from io import StringIO
import mechanicalsoup
parser = etree.HTMLParser()


class anquke(object):
    def __init__(self):
        self.strat_url = "http://chongqing.anjuke.com/sale/"
        self.req = requests.Session()

    def curl(self, url):
        self.req.get(url)

    def parser(self, html):
        body = etree.HTML(html)
        print etree.tostring(body)
        a = body.xpath('//*[@id="houselist-mod"]/li[1]/div[2]/div[1]/a')
        print a

    def run(self):
        html = self.req.get(self.strat_url).content
        self.parser(html)



# anquke().run()
