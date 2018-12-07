#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"
#
# from threading import Timer
#
# def fun(test):
#     print("hello world %s" %test)
#
# if __name__ == "__main__":
#     test = "alex"
#     t = Timer(5.0, fun, args=(test,))
#     t.start()


# coding: utf-8
import threading

count = 0
def fun(lcok):
    # 全局变量
    global count
    for i in range(1000):
        # 获得加锁
       # lcok.acquire()
        count += 1
        print(count)
        # 释放锁
        #lcok.release()

if __name__ == '__main__':
    # 声明一个锁
    lcok = threading.Lock()
    # 创建多个线程，一同执行
    for i in range(101):
        thread = threading.Thread(target=fun, args=(lcok,))
        thread.start()