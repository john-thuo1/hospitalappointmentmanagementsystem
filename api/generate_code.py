import string
import random


def get_code():
    length_of_code = 6
    value = ''.join(random.choices(string.ascii_uppercase + string.digits, k = length_of_code)) 

    return value