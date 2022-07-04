import string
import random


def get_code():
    value = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6)) 

    return value