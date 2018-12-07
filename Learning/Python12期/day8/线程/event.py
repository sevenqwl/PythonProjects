
# 通过Event来实现两个或多个线程间的交互，下面是一个红绿灯的例子，即起动一个线程做交通指挥灯，生成几个线程做车辆，车辆行驶按红灯停，绿灯行的规则。

import threading, time
import random

def light():
    if not event.isSet():
        event.set()  # wait就不阻塞， 绿灯状态
    count = 0
    while True:
        if count < 10:
            print('\033[42;1m--green light on---\033[0m')
        elif count < 13:
            print('\033[43;1m--yellow light on---\033[0m')
        elif count < 30:
            if event.isSet():
                event.clear()
            print('\033[41;1m--red light on---\033[0m')
        else:
            count = 0
            event.set()  # 打开绿灯

        time.sleep(1)
        count += 1

def car(n):
    while True:
        time.sleep(1)
        if event.isSet():  # 绿灯状态
            print('car [%s] is running....' %n)
        else:
            print('car [%s] is waiting for the red light...' %n)
            event.wait()



if __name__ == "__main__":
    event = threading.Event()
    Light = threading.Thread(target=light)
    Light.start()

    for i in range(3):
        t = threading.Thread(target=car, args=(i,))
        t.start()