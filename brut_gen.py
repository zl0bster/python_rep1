# -*- coding: utf-8 -*-
#
# creates sequence generator of combinations of defined length
import decorators

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
    # print('total count = {}'.format(total_count))
    return total_count


measured_gen = decorators.fn_time_counter(seq_gen)
# gen = counted_gen(3, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

gen = measured_gen(2, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
try:
    while True:
        print(next(gen))
except StopIteration as calls_number:
    print(calls_number, 'end iteration')
finally:
    print('the end')
