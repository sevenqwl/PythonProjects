#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

#-*- coding:utf-8 -*-

import time
import platform
import redis
import socket
import getpass
import multiprocessing
import struct
import os
import sys

class RedisHelper:
    def __init__(self):
        self.__conn = redis.Redis(host='10.6.0.118')
        self.chan_sub = 'WakeupOnLan'  #订阅频道
        self.chan_pub = 'WakeupOnLan'  #发布频道

    def get(self,key):
        return self.__conn.get(key)

    def set(self,key,value):
        self.__conn.set(key,value)

    def publish(self,msg):
        try:
            self.__conn.publish(self.chan_pub, msg)
            return True
        except:
            time.sleep(60)
            print ("Timed Out")

    def subscribe(self):
        sub = self.__conn.pubsub()  #类似于打开收音机
        sub.subscribe(self.chan_sub)  #等待接收
        return sub


def WOL(IP, macaddress, Port):
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 12 + 5:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')
    data = ''.join(['FFFFFFFFFFFF', macaddress * 16])
    # print(data)
    send_data = b''
    for i in range(0, len(data), 2):
        byte_dat = struct.pack('B', int(data[i: i + 2], 16))
        send_data = send_data + byte_dat
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (IP, Port))
    sock.close()
