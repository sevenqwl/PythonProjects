#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"


# coding: utf-8
import threading
import time


def fun(semaphore, num):
    # 获得信号量，信号量减一
    semaphore.acquire()
    print ("Thread %d is running." % num)
    time.sleep(3)
    # 释放信号量，信号量加一
    semaphore.release()
    # 再次释放信号量，信号量加一，这是超过限定的信号量数目，这时会报错ValueError: Semaphore released too many times
    # semaphore.release()


if __name__=='__main__':
    # 初始化信号量，数量为2，最多有2个线程获得信号量，信号量不能通过释放而大于2
    semaphore = threading.BoundedSemaphore(2)

    # 运行4个线程
    for num in range(4):
        t = threading.Thread(target=fun, args=(semaphore, num))
        t.start()