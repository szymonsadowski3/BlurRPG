from Game import Engine
from Monster import Monster
import random
import Utilities as Util
import NPC
from Cfg import Cfg

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
        self.choices.extend((Cfg.get('ATK_OFE'), Cfg.get('ATK_NEU'), Cfg.get('ATK_DEF')))

        if allow_to_flee:
            self.choices.append(Cfg.get('FLEE_ATTEMPT'))

        self.choice_to_method = {}
        self.monster = monster
        self.allow_to_flee = allow_to_flee

    def print_fight_message(self, attacker_name, defender_name, dmg):
        print(Cfg.get('BATTLE_INFO') % (attacker_name,defender_name,dmg))
        print()

    def print_choices(self):
        for ind, value in enumerate(self.choices):
            print("%d. %s\n" % (ind, value))

    def fight(self, monster, player_attitude):
        dmg = Engine.measure_damage(self.player, monster, player_attitude, defender_attitude=1)
        self.print_fight_message(self.player.name, monster.name, dmg)
        monster.stats['hp'] -= dmg
        dmg = Engine.measure_damage(monster, self.player, attacker_attitude=1, defender_attitude=player_attitude)
        self.player.take_damage(dmg)
        self.print_fight_message(monster.name, self.player.name, dmg)
        return True if (self.player.stats['hp']<=0 or monster.stats['hp']<=0) else False

    def was_flee_successful(self):
        return True if random.randint(0,100)+self.player.stats['agility']>=50 else False

    def run(self):
        Util.clear()
        print(Cfg.get('ATTACKED') % self.monster.name)
        print()
        flag_exit = False
        while not flag_exit:
            self.player.print_status()
            print()
            self.monster.print_status()
            print()
            self.print_choices()
            choice = Util.get_numeric_safe(Cfg.get('BATTLE_CHOICE') + ' ')
            Util.clear()
            if choice<3:
                flag_exit = self.fight(self.monster, choice)
            else:
                if self.was_flee_successful():
                    Util.slow_print(Cfg.get('FLEE_SUCCESS'))
                    return
        Util.slow_print(Cfg.get('DEFEAT_SUCCESS') + '\n')

class Inn(Event):
    def __init__(self, player):
        super(Inn, self).__init__(player)
        self.choices.append(Cfg.get('TALK_INN'))
        self.choice_to_function = {0: self.talk_to_bartender}

    def run(self):
        while True:
            Util.clear()
            print(Cfg.get('ENTER_INN') + '\n')
            self.print_choices()
            choice = Util.get_numeric_or_default(Cfg.get('CHOICE') + ' ', -1)
            func_to_call = self.choice_to_function.get(choice, None)
            if choice!=-1 and func_to_call:
                func_to_call()
            else:
                break

    def talk_to_bartender(self):
        bartender = NPC.basic_bartender(self.player)
        bartender.perform()

class JackCH2(Event):
    def __init__(self, player):
        super(JackCH2, self).__init__(player, disappear_after_run=False)

    def run(self):
        Util.clear()

        for line in Cfg.getLines('NOTICE_JACK'):
            Util.slow_print(line)

        self.player.proceed_to_next_chapter = True

class MazeEnd(Event):
    def __init__(self, player):
        super(MazeEnd, self).__init__(player, disappear_after_run=True)

    def run(self):
        self.player.proceed_to_next_chapter = True

class Blank(Event):
    def run(self):
        pass

class InnCH3(Event):
    def __init__(self, player):
        super(InnCH3, self).__init__(player)

    def run(self):
        Util.clear()
        for line in Cfg.getLines('ENTER_INN_CH3'):
            Util.slow_print(line)

        Util.clear_with_enter()

        result = None

        while result!='WIN':
            result = Util.DiceGame().play()

            if result=='LOSS':
                Util.slow_print('\n' + Cfg.get('JACK_WIN') + '\n')
                Util.slow_print(Cfg.get('PLAY_AGAIN'))
                Util.clear_with_enter()

            elif result=='DRAW':
                Util.slow_print(Cfg.get('DRAW_GAME') + '\n')
                Util.slow_print(Cfg.get('PLAY_AGAIN'))
                Util.clear_with_enter()

            else:
                Util.slow_print(Cfg.get('PLAYER_WIN'))
                Util.clear_with_enter()
                self.player.proceed_to_next_chapter = True
                break

