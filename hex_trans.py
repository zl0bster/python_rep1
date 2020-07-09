# -*- coding: utf-8 -*-
#
# transform dex to hex

def dex_to_hex(n):
    alphabet = "0123456789ABCDEF"
    base = 16
    n = int(n)
    result = ''
    while n > 0:
        k = n // base
        rest = n % base
        result = alphabet[rest] + result
        n = k
    return result

for i in range(0,128):
    print('{} = {}'.format(i, dex_to_hex(i)))