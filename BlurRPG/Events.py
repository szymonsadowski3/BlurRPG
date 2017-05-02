from Game import Engine
from Monster import Monster
import random
import Utilities as Util
import NPC

class Event(object):
    def __init__(self, player, disappear_after_run=False):
        self.choices = []
        self.player = player
        self.disappear_after_run = disappear_after_run

    def run(self):
        raise NotImplementedError('Subclass must implement abstract method')

    def print_choices(self):
        Util.pprint_list(self.choices)
        print()
        # for key, value in self.choices.items():
        #     print("%d. %s\n" % (key, value))

class MonsterFight(Event):
    def __init__(self, player, monster, allow_to_flee=True):
        super(MonsterFight, self).__init__(player)
        self.choices.extend(('Attack offensive', 'Attack neutral', 'Attack defensive'))

        if allow_to_flee:
            self.choices.append('Try to flee')

        self.choice_to_method = {}
        self.monster = monster
        self.allow_to_flee = allow_to_flee

    def print_fight_message(self, attacker_name, defender_name, dmg):
        print("%s attacks %s causing %d damage!\n" % (attacker_name,defender_name,dmg))

    def print_choices(self):
        for ind, value in enumerate(self.choices):
            print("%d. %s\n" % (ind, value))

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
        Util.clear()
        print('{} Attacked You!\n'.format(self.monster.name))
        flag_exit = False
        while not flag_exit:
            self.player.print_status()
            print()
            self.monster.print_status()
            print()
            self.print_choices()
            choice = Util.get_numeric_safe('What are you going to do?: ')
            Util.clear()
            if choice<3:
                flag_exit = self.fight(self.monster, choice)
            else:
                if self.was_flee_successful():
                    Util.slow_print('You successfully fled from battlefield .')
                    return
        Util.slow_print('You successfully defeated your enemy!\n')

class Inn(Event):
    def __init__(self, player):
        super(Inn, self).__init__(player)
        self.choices.append('Talk to bartender')
        self.choice_to_function = {0: self.talk_to_bartender}

    def run(self):
        while True:
            Util.clear()
            print('You entered Inn!\n')
            self.print_choices()
            choice = Util.get_numeric_or_default('Your choice: ', -1)
            func_to_call = self.choice_to_function.get(choice, None)
            if choice!=-1 and func_to_call:
                func_to_call()
            else:
                break

    def talk_to_bartender(self):
        bartender = NPC.basic_bartender(self.player)
        bartender.perform()

class DisappearingBansheeWarner(Event):
    def __init__(self, player):
        super(DisappearingBansheeWarner, self).__init__(player, disappear_after_run=True)
        self.choices.append('Approach')
        self.choice_to_function = {0: self.talk}

    def run(self):
        while True:
            Util.clear()
            print('You noticed weird stranger standing on the crossroads...\n')
            self.print_choices()
            choice = Util.get_numeric_or_default('Your choice: ', -1)
            func_to_call = self.choice_to_function.get(choice, None)
            if choice!=-1 and func_to_call:
                func_to_call()
                self.player.proceed_to_next_chapter = True
                return

    def talk(self):
        Util.clear()
        Util.slow_print('You approached this spooky fella...\n\n When you tried to greet him, the stranger lowered his eyes and told:\n')
        Util.slow_print("'Vaporize as soon as possible not to meet with Banshee'\n")
        Util.slow_print("Then he disappeared and only thin mist remained...\n")

class Blank(Event):
    def run(self):
        pass