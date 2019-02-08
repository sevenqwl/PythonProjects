

import redis

'''
r = redis.Redis(host='127.0.0.1')
# print(r.keys())
# all_keys = r.keys()
# for k in all_keys:
#     print(k, r.get(k.decode()))

r.set("Name", "ChunYun", ex=3)  # 3秒过期
print(r.get("Name"))
'''
# 连接池

pool = redis.ConnectionPool(host="127.0.0.1")
r = redis.Redis(connection_pool=pool)
# print(r.keys())


# r.set("Name", "A", nx=True)
# print(r.get("Name"))


# r.mset(k1='v1', k2='v2')  # 批量设置值
# print(r.keys())

# r.set("id", "37148119...")
# print(r.getrange("id", 3, 6))  # 相当于切片

# r.set("id", "37148119...")
# r.setrange("id", 3, "AAA")
# print(r.getrange("id", 0, -1))

# setbit setcount
# r.setbit("uv_count", 3, 1)
# r.setbit("uv_count", 3, 1)
# r.setbit("uv_count", 5, 1)
# r.setbit("uv_count", 15, 1)
# print("uv count:", r.bitcount("uv_count"))

# incr
# r.incr("count" ,1)
# print(r.get("count"))

# append
# r.append("name", "__")
# print(r.get("name"))

# hset
# r.hset("stu_info", "stu1", "001")
# r.hmset("stu_info", {"stu2":"002", "stu3":"003", "stu4":"004"})
# print(r.hget("stu_info", "stu3"))
# print(r.hmget("stu_info", "stu3", "stu2"))
# print(r.hgetall("stu_info"))  # 获取所有值
# print(r.hlen("stu_info"))  # 获取hash键值对的个数
# print(r.hkeys("stu_info"))  # 获取所有的key值
# print(r.hvals("stu_info"))  # 获取所有的value值

# lpush rpush
# r.lpush("name_list", "a" , "b", "c")
# r.rpush("name_list", "d" , "e", "f")
# r.linsert("name_list", "BEFORE", "a", "-")


# print(r.llen("name_list"))
# r.ltrim("name_list", 3, 5)  # 移除索引之外的值
# print(r.lrange("name_list", 0, -1))


# set集合
# r.sadd("set_list", 1, 3, 5 ,45, 7, 9)  # 添加集合
# r.sadd("set_list2", 2, 4, 5 ,45, 8, 10)
# print(r.sdiff("set_list", "set_list2" ))  # 在第一个name对应的集合中且不在其他name对应的集合的元素集合
# print(r.sscan("set_list"))
# print(r.sscan("set_list2"))
# r.sdiffstore("dest_set_list", "set_list", "set_list2")
# print(r.sscan("dest_set_list"))
#
# print(r.sinter( "set_list", "set_list2"))  # 交集
# print(r.sismember( "set_list", 2))  # 判断是否在集合中
# print(r.smembers( "set_list"))  # 获取集合的所有成员

# r.smove("set_list2", "dest_set_list", 10)  # 移动set_list2中的10 到 dest_set_list
# print(r.sscan("dest_set_list"))

# print(r.sunion("set_list", "set_list2", "dest_set_list"))  # 获取多个集合的并集


# 有序集合
# r.zadd("z_1", "alex", 5, "rain", 10)
# r.zadd("z_1", "jack", 3, "eric", 60)
# print(r.zscan("z_1"))
# print(r.zcard("z_1"))  # 获取长度
# r.zincrby("z_1", "jack")  # 自增
# print(r.zrange("z_1", 2, 10))  # 按照索引范围获取集合元素
# print(r.zrangebyscore("z_1", 5, 100))  # 按照分数范围获取集合元素
# print(r.zscan("z_1"))
#
# r.delete("name_list")  # 删除key
# print(r.keys(pattern="*count"))  # 获取匹配的key


#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis


class RedisHelper:

    def __init__(self):
        self.__conn = redis.Redis(host='10.211.55.4')
        self.chan_sub = 'fm104.5'
        self.chan_pub = 'fm104.5'

    def public(self, msg):
        self.__conn.publish(self.chan_pub, msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()  # 打开收音机
        pub.subscribe(self.chan_sub)  # 拧到那个频道
        pub.parse_response()  # 准备听
        return pub

RedisHelper