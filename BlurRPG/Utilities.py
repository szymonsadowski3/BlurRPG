import collections
import os
import sys
import time
import random
from Cfg import Cfg
import os.path
import operator


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

CLEAR_CMD = 'clear'

Direction = collections.namedtuple('Direction', 'dx dy')

clear = lambda: os.system(CLEAR_CMD)

def clear_with_enter():
    input('\n[PRESS ENTER TO PROCEED]: ')
    os.system(CLEAR_CMD)


def get_true_or_false(prompt, ending=' '):
    res = input(prompt + ending).strip().upper()
    return res == 'T'

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
    print('{', end = '')
    for ind, val in enumerate(list):
        ending = ', ' if ind!=len(list)-1 else ''
        print("%d: %s" % (ind, val), end=ending)
    print('}')

def slow_prin(msg, typing_speed=1300, endline=True): #http://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing
    for l in msg:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    if endline:
        print('')
    time.sleep(0.5)

def slow_print(msg, typing_speed=130, endline=True): #http://stackoverflow.com/questions/4099422/printing-slowly-simulate-typing
    print(msg, end='\n' if endline else '')

def file_exists(fname):
    return os.path.isfile(fname)

def read_lines(fname):
    if file_exists(fname):
        with open(fname) as f:
            content = f.readlines()
        return [x.strip() for x in content]
    else:
        return []


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch().decode("utf-8")


getch = _Getch()

###GAMES###
####GUESSING GAME####
class GuessingGame:
    def __init__(self, num_of_tries, range_upper_bound):
        self.num_of_tries = num_of_tries
        self.range_upper_bound = range_upper_bound

    def play(self):
        to_guess = 0
        player_guess = -1

        for i in range(self.num_of_tries):
            print('Try nr. %d' % (i+1))
            print('=' * len('Try nr'))

            print("OK, so i will guess number from 0 to ", self.range_upper_bound)
            print("You have %d tries" % self.num_of_tries)
            to_guess = random.randint(0, self.range_upper_bound)

            player_guess = get_numeric_safe_in_range('Tell me your choice number: ', 0, self.range_upper_bound - 1)

            if player_guess==to_guess:
                return True

            less_more = 'Too small number you told!' if player_guess < to_guess else 'Too big number you told!'
            print(less_more)

        print('You wasted all your chances')
        return False
####END OF GUESSING GAME####

####DICE GAME####

###COMB CHECKER
def get_counter(series):
    peeps = [x.peeps for x in series]
    return collections.Counter(peeps)

def check_series(series):
    pass

def is_poker(series):
    """
    >>> is_poker([Dice(5), Dice(5), Dice(5), Dice(5), Dice(5)])
    True
    >>> is_poker([Dice(5), Dice(5), Dice(5), Dice(5), Dice(3)])
    False
    """
    counter_obj = get_counter(series)
    return 5 in counter_obj.values()

def is_four_of_kind(series):
    """
    >>> is_four_of_kind([Dice(5), Dice(5), Dice(5), Dice(5), Dice(4)])
    True
    >>> is_four_of_kind([Dice(5), Dice(5), Dice(5), Dice(3), Dice(3)])
    False
    """
    counter_obj = get_counter(series)
    return 4 in counter_obj.values()

def is_full_house(series):
    """
    >>> is_full_house([Dice(2), Dice(5), Dice(5), Dice(2), Dice(5)])
    True
    >>> is_full_house([Dice(5), Dice(5), Dice(3), Dice(4), Dice(3)])
    False
    """
    counter_obj = get_counter(series)
    return (3 in counter_obj.values()) and (2 in counter_obj.values())

def is_great_straight(series):
    """
    >>> is_great_straight([Dice(6), Dice(5), Dice(4), Dice(3), Dice(2)])
    True
    >>> is_great_straight([Dice(5), Dice(4), Dice(3), Dice(2), Dice(1)])
    False
    """
    peeps = [x.peeps for x in series]
    sorted_peeps = sorted(peeps)
    return sorted_peeps == [2, 3, 4, 5, 6]

def is_little_straight(series):
    """
    >>> is_little_straight([Dice(5), Dice(4), Dice(3), Dice(2), Dice(1)])
    True
    >>> is_little_straight([Dice(6), Dice(5), Dice(3), Dice(3), Dice(2)])
    False
    """
    peeps = [x.peeps for x in series]
    sorted_peeps = sorted(peeps)
    return sorted_peeps == [1, 2, 3, 4, 5]

def is_three_of_a_kind(series):
    """
    >>> is_three_of_a_kind([Dice(5), Dice(5), Dice(3), Dice(5), Dice(1)])
    True
    >>> is_three_of_a_kind([Dice(6), Dice(5), Dice(3), Dice(3), Dice(2)])
    False
    """
    counter_obj = get_counter(series)
    return 3 in counter_obj.values()

def is_two_pair(series):
    """
    >>> is_two_pair([Dice(5), Dice(5), Dice(3), Dice(3), Dice(1)])
    True
    >>> is_two_pair([Dice(6), Dice(5), Dice(3), Dice(3), Dice(2)])
    False
    """
    how_many_pairs = 0
    counter_obj = get_counter(series)
    for val in counter_obj.values():
        if val == 2:
            how_many_pairs += 1

    return how_many_pairs == 2

def is_one_pair(series):
    """
    >>> is_one_pair([Dice(5), Dice(5), Dice(3), Dice(2), Dice(1)])
    True
    >>> is_one_pair([Dice(6), Dice(5), Dice(3), Dice(2), Dice(1)])
    False
    """
    counter_obj = get_counter(series)
    return 2 in counter_obj.values()

def is_high_card(series):
    """
    >>> is_high_card([Dice(6), Dice(5), Dice(3), Dice(2), Dice(1)])
    True
    >>> is_high_card([Dice(6), Dice(5), Dice(4), Dice(3), Dice(2)])
    False
    """
    how_many_ones = 0
    counter_obj = get_counter(series)
    for val in counter_obj.values():
        if val == 1:
            how_many_ones += 1

    return (how_many_ones == 5) and (not is_great_straight(series)) and (
        not is_little_straight(series))

funcs = [is_poker, is_four_of_kind, is_full_house, is_great_straight,
         is_little_straight, is_three_of_a_kind, is_two_pair, is_one_pair,
         is_high_card]

def get_combination_value(series):
    comb_val = 0

    for index, func in enumerate(funcs):
        if func(series):
            exponenta = len(funcs) - index
            comb_val += 10 ** exponenta
            comb_val += sum(series)
            break

    return comb_val

###END OF COMB CHECKER

class Dice:
    def __init__(self, peeps=None):
        self.peeps = 1 if not peeps else peeps

    def roll(self):
        self.peeps = random.randint(1, 6)

    def __repr__(self):
        return str(self.peeps)

    def __str__(self):
        return str(self.peeps)

    def __radd__(self, other):
        return other + self.peeps

    def __gt__(self, other):
        return self.peeps > other.peeps

    def __eq__(self, other):
        return self.peeps == other.peeps

class DiceGame:
    def roll_series(self, series, mask=None):
        if not mask:
            mask = [True, True, True, True, True]
        for i, dice in enumerate(series):
            if mask[i]:
                dice.roll()

    def __init__(self):
        self.player_series = [Dice() for _ in range(5)]
        self.cpu_series = [Dice() for _ in range(5)]

    def cpu_mask(self, cpu_series):
        mask = [False, False, False, False, False]
        sorted_series = sorted(cpu_series)
        cntr = get_counter(cpu_series)
        max_peeps = max(cntr.items(), key=operator.itemgetter(1))[0]

        for index, dice in enumerate(cpu_series):
            if dice.peeps != max_peeps:
                mask[index] = True

        return mask

    def play(self):
        clear()
        slow_print(Cfg.get('FST_ROUND'))
        clear_with_enter()

        slow_print(Cfg.get('PLAYER_ROLLING') + '\n')
        self.roll_series(self.player_series)
        slow_print(Cfg.get('U_ROLLED') + ' ')
        slow_print(str(self.player_series))

        slow_print('\n' + Cfg.get('CPU_ROLLING') + '\n')
        self.roll_series(self.cpu_series)
        slow_print(Cfg.get('CPU_ROLLED') + ' ')
        slow_print(str(self.cpu_series) + '\n')

        mask = self.get_mask()

        clear()
        slow_print(Cfg.get('SND_ROUND'))
        clear_with_enter()

        slow_print(Cfg.get('PLAYER_ROLLING') + '\n')
        self.roll_series(self.player_series, mask)
        slow_print(Cfg.get('U_ROLLED') + ' ')
        slow_print(str(self.player_series))

        slow_print(Cfg.get('CPU_ROLLING') + '\n')
        self.roll_series(self.cpu_series, self.cpu_mask(self.cpu_series))
        slow_print(Cfg.get('CPU_ROLLED') + ' ')
        slow_print(str(self.cpu_series))

        player_val = get_combination_value(self.player_series)
        cpu_val = get_combination_value(self.cpu_series)

        if cpu_val == player_val:
            slow_print('\n' + Cfg.get('DRAW') + '\n')
            return 'DRAW'
        elif cpu_val <= player_val:
            slow_print('\n' + Cfg.get('WIN') + '\n')
            return 'WIN'
        else:
            slow_print('\n' + Cfg.get('LOSS') + '\n')
            return 'LOSS'

    def valid_mask(self, mask):
        fs = mask.count('F')
        ts = mask.count('T')
        return len(mask) == 5 and (fs + ts == 5)

    def get_mask(self):
        while True:
            mask = input('Type in which die you want to reroll [mask True/False] e.g. [TTFTT]: ').upper()
            if self.valid_mask(mask):
                break

        return [x == 'T' for x in mask]
####END OF DICE GAME####
###EOGAMES###
