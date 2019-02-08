import sys
import os
print(sys.path)
print(__file__)  # 打印文件的相对路径
print(os.path.abspath(__file__))  # 获取文件的绝对路径
print(os.path.dirname(os.path.abspath(__file__)))  # os.path.dirname 获取当前路径的上一层路径
print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # os.path.dirname 获取当前路径的上一层路径



base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)  # 添加环境变量

from config import settings

def db_auth(configs):
    if configs.DATABASE["user"] == "root" and configs.DATABASE["password"] == "123":
        print("db authentication passed!")
        return True
    else:
        print("db login error!")

def select(table, column):
    if db_auth(settings):
        if table == "user":
            user_info = {
                "001": ['alex', 22, 'engineer'],
                "002": ['longGe', 43, 'chef'],
                "003": ['xiaoYun', 23, '13baoan']
            }
        return user_info
