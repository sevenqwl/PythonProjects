
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Seven"

# 二维数组90度旋转
data = [[col for col in range(4,10)]  for row in range(4,110)]
# print(len(data[0]))

for i in data:
    print(i)

print('')

for r_index,row in enumerate(data[0]):
    print([data[c_index][r_index] for c_index in range(len(data))])