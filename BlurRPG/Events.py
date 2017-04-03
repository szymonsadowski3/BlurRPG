from Game import Engine
from Monster import Monster
import random
import Utilities
import NPC

class Event(object):
    def __init__(self, player):
        self.choices = []
        self.player = player

    def run(self):
        raise NotImplementedError('Subclass must implement abstract method')

    def print_choices(self):
        Utilities.pprint_list(self.choices)
        print()
        # for key, value in self.choices.items():
        #     print("%d. %s\n" % (key, value))

class MonsterFight(Event):
    def print_fight_message(self, attacker_name, defender_name, dmg):
        print("%s attacks %s causing %d damage!\n" % (attacker_name,defender_name,dmg))

    def print_choices(self):
        for ind, value in enumerate(self.choices):
            print("%d. %s\n" % (ind, value))

    def __init__(self, player):
        super(MonsterFight, self).__init__(player)
        self.choices.extend(('Attack offensive', 'Attack neutral', 'Attack defensive', 'Try to flee'))
        self.choice_to_method = {}

    def fight(self, monster, player_attitude):
        dmg = Engine.measure_damage(self.player, monster, player_attitude, defender_attitude=1)
        self.print_fight_message(self.player.name, 'Monster', dmg)
        monster.stats['hp'] -= dmg
        dmg = Engine.measure_damage(monster, self.player, attacker_attitude=1, defender_attitude=player_attitude)
        self.player.take_damage(dmg)
        self.print_fight_message('Monster', self.player.name, dmg)
        return True if (self.player.stats['hp']<=0 or monster.stats['hp']<=0) else False

    def was_flee_successful(self):
        return True if random.randint(0,100)+self.player.stats['agility']>=50 else False

    def run(self):
        Utilities.clear()
        print('Monster Attacked You!\n')
        monster = Monster(10, 80, 10, 5)
        flag_exit = False
        while not flag_exit:
            self.player.print_status()
            print()
            monster.print_status()
            print()
            self.print_choices()
            choice = Utilities.get_numeric_safe('What are you going to do?: ')
            Utilities.clear()
            if choice<3:
                flag_exit = self.fight(monster, choice)
            else:
                if self.was_flee_successful():
                    Utilities.slow_print('You successfully fled from battlefield .')
                    return
        Utilities.slow_print('You successfully defeated your enemy!\n')

class Inn(Event):
    def __init__(self, player):
        super(Inn, self).__init__(player)
        self.choices.append('Talk to bartender')
        self.choice_to_function = {0: self.talk_to_bartender}
    def run(self):
        while True:
            Utilities.clear()
            print('You entered Inn!\n')
            self.print_choices()
            choice = Utilities.get_numeric_or_default('Your choice: ', -1)
            func_to_call = self.choice_to_function.get(choice, None)
            if choice!=-1 and func_to_call:
                func_to_call()
            else:
                break

    def talk_to_bartender(self):
        bartender = NPC.basic_bartender(self.player)
        bartender.perform()

class Blank(Event):
    def run(self):
        pass