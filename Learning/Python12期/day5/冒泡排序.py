
# 冒泡排序
data = [10, 4, 33, 21, 54, 3, 8, 11, 5, 22, 2, 1, 17, 13, 16]

'''
for j in range(1,len(data)-1):
    for i in range(len(data)-j):
        if data[i] > data[i+1]:
            tmp = data[i+1]
            data[i+1] = data[i]
            data[i] = tmp

print(data)
'''
# j = 1
# def num(j):
#
#     for i in range(len(data) - j):
#         if (len(data) - j) > 0:
#             if data[i] > data[i + 1]:
#                 tmp = data[i + 1]
#                 data[i + 1] = data[i]
#                 data[i] = tmp
#                 # print(i)
#                 # print(len(data) - j)
#                 if (i+1) == (len(data) - j):
#                     j += 1
#                     print(data)
#                     num(j)
#         else:
#             print(data)
#
# num(j)

