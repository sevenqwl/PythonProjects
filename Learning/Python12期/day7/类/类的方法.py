

class Animal(object):
    def __init__(self, name):
        self.name = name
        self.num = None

    hobbie = "meat"  # 类变量

    @classmethod  # 类方法，不能访问实例变量
    def talk(self):
        print("%s is talking" % self.hobbie)

    @staticmethod  # 静态方法，不能访问实例变量和类变量
    def walk():
        # print("%s is walking" % self.hobbie)
        print(" is walking")

    @property  # 把方法变成属性，可以访问实例变量和类变量
    def habit(self):
        print("%s habbit is xxoo" % self.name)

    @property
    def total_players(self):
        return self.num

    @total_players.setter  # 修改方法
    def total_players(self, num):
        self.num = num
        print("total players:", self.num)\

    @total_players.deleter  #删除
    def total_players(self):
        print("total players got deleted. ")
        del self.num




# print(Animal.hobbie)
# Animal.talk()

d = Animal('SanJiang')
# d.walk()
# d.habit
print(d.total_players)
d.total_players = 3

del d.total_players
print(d.total_players)