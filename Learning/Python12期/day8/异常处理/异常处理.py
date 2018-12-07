
'''
while True:
    a = [1,2,3,4,5]
    num1 = input('num1:')
    num2 = input('num2:')
    try:
        num1 = int(num1)
        num2 = int(num2)
        result = num1 + num2
        a[11]
    # except ValueError as e:
    #     print('Value Error')
    # except IndexError as e:
    #     print('Index Error')
    except Exception as e:
        print ('出现异常，信息如下：')
        print (e)
'''



class SevenException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

a = 1
try:
    assert a == 1
    raise SevenException('我的异常')
except SevenException as e:
    print(e)
else:
    print("else")
finally:
    print("finally")


