

import threading
import time

def sayhi(num):
    print('running on number:%s' %num)
    time.sleep(num)
    print(3)

if __name__ == "__main__":
    '''
    t1 = threading.Thread(target=sayhi, args=(1,))
    t2 = threading.Thread(target=sayhi, args=(2,))

    t1.start()
    t2.start()

    print(t1.getName())
    print(t2.getName())

    t1.join()
    t2.join()'''
    t_list = []
    for i in range(10):
        t = threading.Thread(target=sayhi, args=[i,])
        t.start()
        t_list.append(t)

    for j in t_list:
        j.join()
        print(j)


    print("------main-----")
