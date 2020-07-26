# -*- coding: utf-8 -*-
#
# set of decoration functions

import time

def fn_calls_counter(func):
    """decorator counts number of function calls"""
    fn_calls_counter.count = 0

    def wrapper(*args, **kwargs):
        fn_calls_counter.count += 1
        result = func(*args, **kwargs)
        print("{0} was called: {1}".format(func.__name__, fn_calls_counter.count))
        return result

    return wrapper

def fn_time_counter(func):
    """decorator counts time of function call"""

    def wrapper(*args, **kwargs):
        t = time.clock()
        result = func(*args, **kwargs)
        t2 = time.clock()
        print("{0} was called: {1}".format(func.__name__, t2-t))
        return result

    return wrapper