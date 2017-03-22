#! /usr/bin/env python
# -*- coding:utf-8 -*-
# author:xd
import pdb

class Tree(object):
    """树类"""

    def __init__(self, type=2):
        self.tree_struct = []
        self.sign = [1, 1]
        self.tree_type = type


    def search_location(self, listobj,result):
        for item in listobj[:len(listobj)-1]:
            result = result[item]
        return result

    def _add_node(self, elem):
        print elem
        print self.sign
        print self.tree_struct
        node = self.search_location(self.sign, self.tree_struct)
        node.insert(self.sign[1], [elem])
        if self.sign[1] == self.tree_type:
            if self.sign[0] == self.tree_type:
                self.sign = [1] * (len(self.sign)+1)
            else:
                self.sign[0] += 1  # self.sign[0] + 1
                self.sign[1] = 1
        else:
            self.sign[1] += 1  # self.sign[1] +1


    def tree_length(self):
        return len(self.tree_struct)

    def add(self, elem):
        # print self.tree_length()
        if self.tree_length() == 0:
            self.tree_struct.append(elem)
            return
        elif self.tree_length() < self.tree_type + 1:
            node = [elem]
            self.tree_struct.append(node)
        elif self.tree_length() == self.tree_type + 1:
            self._add_node(elem)


if __name__ == '__main__':
    """主函数"""
    elems = range(13)
    tree = Tree(3)
    # pdb.set_trace()
    for elem in elems:
        tree.add(elem)
