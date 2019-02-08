'''
def login(func):
    def inner(*args, **kargs):
        print('Passed user verification...')
        return func(*args, **kargs)
    return inner


def home(name):
    print('Welcom [%s] to Home page' % name)

@login  # tv = login(tv)
def tv(name, password):
    print('Welcom [%s] to TV page [%s]' % (name, password))
    return 7

def movie(name):
    print('Welcom [%s] to Movie page' % name)

t = tv('Alex',password=123 )
print(t)
'''


# !/usr/bin/env python
# coding:utf-8

def Before(request, kargs):
    print('before')


def After(request, kargs):
    print('after')


def Filter(before_func, after_func):
    def outer(main_func):
        def wrapper(request, kargs):

            before_result = before_func(request, kargs)
            if (before_result != None):
                return before_result;

            main_result = main_func(request, kargs)
            if (main_result != None):
                return main_result;

            after_result = after_func(request, kargs)
            if (after_result != None):
                return after_result;

        return wrapper

    return outer


@Filter(Before, After)
def Index(request, kargs):
    print('index')

Index('req', 'alex')