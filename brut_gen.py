# -*- coding: utf-8 -*-
#
# creates sequence generator of combinations of defined length

def fn_calls_counter(func):
    """decorator counts number of function calls"""
    fn_calls_counter.count = 0

    def wrapper(*args, **kwargs):
        fn_calls_counter.count += 1
        result = func(*args, **kwargs)
        print("{0} was called: {1}".format(func.__name__, fn_calls_counter.count))
        return result

    return wrapper


@fn_calls_counter
def seq_gen(length=3, alphabet='0123456789') -> str:
    """generates sequence of combinations of defined length using alphabet"""
    base = len(alphabet)
    total_count = 0
    for current_length in range(1, length + 1):
        combination_count = base ** current_length
        for n in range(0, combination_count):
            combination = ''
            while n > 0:
                k = n // base
                rest = n % base
                combination = alphabet[rest] + combination
                n = k
            comb_len = len(combination)
            if comb_len < current_length:
                leading = alphabet[0] * (current_length - comb_len)
            else:
                leading = ''
            combination = leading + combination
            yield combination
            total_count += 1
    print('total count = {}'.format(total_count))
    return total_count


# counted_gen = fn_calls_counter(seq_gen)
# gen = counted_gen(3, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

gen = seq_gen(4, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
try:
    while True:
        print(next(gen))
except StopIteration:
    print('end iteration')
finally:
    print('the end')
