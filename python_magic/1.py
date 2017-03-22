#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:xd
class inch(float):
    "Convert from inch to meter"
    def __new__(cls, arg=0.0):
        # return float.__new__(cls, arg*0.0254)
        return float.__new__(cls, arg*0.0254)
class inch1(float):
    "THIS DOESN'T WORK!!!"
    # def __init__(self, arg=0.0):
    #     float.__init__(self, 123)
    pass

class Singleton(object):
    def __new__(cls, value):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        # if not hasattr(cls, 'instance'):
        #     cls.instance = super(Singleton, cls).__new__(cls)
        # return cls.instance
        return super(Singleton, cls).__new__(cls)
    def ad(self):
        return "123"

obj1 = Singleton()
obj2 = Singleton()

obj1.attr1 = 'value1'
print obj1.ad()
# print obj1.attr1, obj2.attr1
# obj2.attr1 = "value2"
# print obj1.attr1, obj2.attr1
# print obj1 is obj2
# print obj2.ad()