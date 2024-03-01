"""
其他激活函数请直接照事例给出
n==0为ReLu函数
n==1为sigmoid函数
"""


from math import pow, e


def func(x, n):
    if n == 0:
        if x < 0:
            return 0
        else:
            return x
    elif n == 1:
        return 1.0 / (1 + pow(e, -x))


def d_func(x, n):
    if n == 0:
        if x < 0:
            return 0
        else:
            return 1
    elif n == 1:
        return pow(e, -x)/(1+pow(e, -x))**2
