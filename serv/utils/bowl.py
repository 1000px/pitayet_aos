# coding utf-8
"""
bowl's file
common functions
"""
import time
import random
import string

class Bowl():
    """Bowl Class, defined a list of common functions"""
    def __init(self):
        pass

    @staticmethod
    def generate_time_str():
        """return a str for time and hash"""
        key = ''
        length = 6
        while length:
            key += random.choice(string.ascii_letters + string.digits)
            length -= 1
        return time.strftime('%Y_%m_%d_%H%M%S', time.localtime()) + hash(key)
