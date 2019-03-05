#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

data_set = [ 9,1,22,31,45,3,6,2,11 ]

loop_count = 0
for j in range(len(data_set)):
    for i in range(len(data_set) -j -1):
        if data_set[i] > data_set[i+1]:
            tmp = data_set[i]
            data_set[i] = data_set[i+1]
            data_set[i+1] = tmp
        loop_count += 1
    print(data_set)
print(data_set)
print("loop times", loop_count)