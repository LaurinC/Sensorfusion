"""
Random functions needed in conversion of tlv packages

copied from pymmw: https://github.com/m6c7l/pymmw/blob/master/source/lib/utility.py
"""

def intify(value, base = 16, size = 2):
    if type(value) not in (tuple, list, bytes,):
        value = (value,)
    if (type(value) in (bytes,) and base == 16) or (type(value) in (list, tuple,)):
        return sum([item * ((base ** size) ** i) for i, item in enumerate(value)]) 
    else:
        return sum([((item // 16) * base + (item % 16)) * ((base**size) ** i) for i, item in enumerate(value)])

def q_to_dec(value, n):
    return value / (1 << n)

def q_to_db(value):
    return q_to_dec(value, 9) * 6
