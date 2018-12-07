# _*_coding:utf-8_*_
__author__ = 'Alex Li'

import time
import threading


def run(n):
    print('[%s]------running----\n' % n)
    time.sleep(1)
    print('--done--')


def main():
    for i in range(5):
        t = threading.Thread(target=run, args=[i, ])
        t.start()
        #time.sleep(5)
        print('starting thread', t.getName())


m = threading.Thread(target=main, args=[])
m.setDaemon(True)  # 将main线程设置为Daemon线程,它做为程序主线程的守护线程,当主线程退出时,m线程也会退出,由m启动的其它子线程会同时退出,不管是否执行完任务
m.start()
m.join(timeout=10)
print("---main thread done----")