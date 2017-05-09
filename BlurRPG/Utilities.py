import collections
import os
import sys,time,random
from Cfg import Cfg

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

Direction = collections.namedtuple('Direction', 'dx dy')

clear = lambda: os.system('cls')

def get_numeric_safe(prompt):
    while True:
        try:
            res = int(input(prompt))
            break
        except (ValueError, NameError):
            print(Cfg.get('NUMS_PLS'))
    return res

def get_numeric_safe_in_range(prompt, lower, upper):
    while True:
        try:
            res = int(input(prompt))
            if res<lower or res>upper:
                print(Cfg.get('RANGE_PLS') % (lower, upper))
                continue
            break
        except (ValueError, NameError):
            print(Cfg.get('NUMS_PLS'))
    return res

def get_numeric_or_default(prompt, default):
    try:
        res = int(input(prompt))
    except (ValueError, NameError):
        return default
    return res

def get_numeric_in_range_or_default(prompt, lower, upper, default):
    try:
        res = int(input(prompt))
        if res < lower or res > upper:
            return default
    except (ValueError, NameError):
        return default
    return res

def print_dict_in_order(dict):
    print(sorted(dict.items(), key=lambda x: x[1], reverse=False))

def pprint_list(list):
    print('{', end='')
    for ind, val in enumerate(list):
        ending = ', ' if ind!=len(list)-1 else ''
        print("%d: %s" % (ind, val), end=ending)
    print('}')

def slow_print(msg, typing_speed=1300, endline=True): #http://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing
    for l in msg:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    if endline:
        print('')

def slow_prin(msg, typing_speed=130, endline=True): #http://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing
    print(msg, end='\n' if endline else '')