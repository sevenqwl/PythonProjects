#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"


import threading
import time
import logging

# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )
#
# def worker(event):
#     logging.debug('Waiting for redis ready.....')
#     event.wait()
#     logging.debug('redis ready, and connect to redis server and do some work [%s]', time.ctime())
#     time.sleep(1)
#
# redis_ready = threading.Event()
# t1 = threading.Thread(target=worker, args=(redis_ready,), name='t1')
# t1.start()
#
# t2 = threading.Thread(target=worker, args=(redis_ready,), name='t2')
# t2.start()
#
# logging.debug('first of all, check redis server, make sure it is OK, and then trigger the redis ready event')
# time.sleep(3)
# redis_ready.set()


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )

def worker(event):
    while not event.is_set():
        logging.debug('Waiting for redis ready.....')
        event.wait(1)
    logging.debug('redis ready, and connect to redis server and do some work [%s]', time.ctime())
    time.sleep(1)

redis_ready = threading.Event()
t1 = threading.Thread(target=worker, args=(redis_ready,), name='t1')
t1.start()

t2 = threading.Thread(target=worker, args=(redis_ready,), name='t2')
t2.start()

logging.debug('first of all, check redis server, make sure it is OK, and then trigger the redis ready event')
time.sleep(3)
redis_ready.set()