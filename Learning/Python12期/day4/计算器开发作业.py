
import re
import time

def mutilpy_and_dividend(formula):
    print("运算", formula)


def calc(formula):
    parentheses_flag = True
    while parentheses_flag:
        m = re.search("\([^()]\)", formula)
        if m:
            print(m.group())
            time.sleep(1)


if __name__ == "__main__":
    formula = "1 - 2 * ((60 - 30 + (-40 / 5) * (9 - 2 * 5 / 3 + 7 / 3 * 99 / 4 * 2998 + 10 * 568 / 14)) - (-4 * 3) / (16 - 3 * 2))"
    res = calc(formula)