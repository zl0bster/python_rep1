# -*- coding: utf-8 -*-
#
# creates sequence generator of combinations of defined length

def seq_gen(length=3, alphabet='0123456789'):
    # generates sequence of combinations of defined length
    base = len(alphabet)
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
    return


try:
    gen = seq_gen(3, '0123456789ABCDEF')
    while True:
        print(next(gen))
except StopIteration:
    print('end iteration')
