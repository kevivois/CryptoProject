import math


def intarray_to_str(arr) -> str:
    msg = ""
    for idx, int_value in enumerate(arr):
        try:
            msg += int_to_str(int_value)
        except:
            pass
    return msg

def int_to_str(int_value) -> str:
    return int_value.to_bytes(math.ceil(int_value.bit_length() / 8), 'big').decode('utf-8')


def str_to_intarray(s: str):
    return [ord(c) for c in s]
