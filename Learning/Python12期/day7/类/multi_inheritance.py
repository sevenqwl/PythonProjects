#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

# 多继承
# 经典类：深度优先，新式类：广度优先，3.0版本无论经典类还是新式类都是广度优先

class A:
    n = 'A'
    def f2(self):
        print("f2 from A")

class B(A):
    n = 'B'
    def f1(self):
        print("from B")

    def f2(self):
        print("f2 from B")

class C(A):
    n = 'C'
    def f2(self):
        print("from C")

class D(B,C):  # 继承B,C两个类
    '''Test class'''
    pass

d = D()
d.f1()
d.f2()  # 先找B下的f2,没有找C下的，在没有找A下的，广度优先

print(d.__doc__)  # 类的描述信息
