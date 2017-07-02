from Game import Engine
import Monster
import random
import Utilities as Util
import NPC
from Cfg import Cfg
import Items
import Events

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
    def __init__(self, player, monster_init_func, allow_to_flee=True, money_received = 0):
        super(MonsterFight, self).__init__(player, disappear_after_run=True)
        self.choices.extend((Cfg.get('ATK_OFE'), Cfg.get('ATK_NEU'), Cfg.get('ATK_DEF')))

        if allow_to_flee:
            self.choices.append(Cfg.get('FLEE_ATTEMPT'))

        self.choice_to_method = {}

        print(monster_init_func)
        print(monster_init_func())
        self.monster_init_func = monster_init_func
        self.monster = monster_init_func()
        self.allow_to_flee = allow_to_flee
        self.money_received = money_received

    def reset(self):
        self.monster = self.monster_init_func()

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
                if self.allow_to_flee and self.was_flee_successful():
                    Util.slow_print(Cfg.get('FLEE_SUCCESS'))
                    Util.clear_with_enter()
                    return
        Util.slow_print(Cfg.get('DEFEAT_SUCCESS') + '\n')

        if self.money_received:
            Util.slow_print(Cfg.get('MONEY_RECEIVE') % self.money_received, '\n')
            self.player.get_money(self.money_received)

        Util.clear_with_enter()

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

class CollectHealthPotion(Event):
    def __init__(self, player):
        super(CollectHealthPotion, self).__init__(player, disappear_after_run=True)

    def run(self):
        Util.clear()
        Util.slow_print('\n' + Cfg.get('PICK_UP_HP_POT') + '\n')
        self.player.add_item_to_backpack(Items.health_potion(self.player))
        Util.clear_with_enter()

class CollectChest(Event):
    def __init__(self, player):
        super(CollectChest, self).__init__(player, disappear_after_run=True)
        self.amount = 5

    def run(self):
        Util.clear()
        Util.slow_print(Cfg.get('MONEY_RECEIVE') % self.amount, '\n')
        self.player.get_money(self.amount)
        Util.clear_with_enter()

class RiddleManInTunnel(Event):
    def __init__(self, player):
        super(RiddleManInTunnel, self).__init__(player, disappear_after_run=True)

    def run(self):
        Util.clear()
        Util.slow_print(Cfg.get('RIDDLE') + '\n')
        Util.clear_with_enter()

        for l in Cfg.getLines('RIDDLE_IN_TUNNELS_INTRO'):
            Util.slow_print(l)

        Util.clear_with_enter()

        Util.slow_print(Cfg.get('FST_RIDDLE'))

        answers = Cfg.getLines('FST_RIDDLE_ANSW')
        user_answ = input('\n' + Cfg.get('WHAT_IS_ANSW') + ' ')

        if user_answ.strip().upper() in answers:
            Util.slow_print('\n' + Cfg.get('RIGHT_ANSW'))
            self.player.add_item_to_backpack(Items.old_mans_sword)
        else:
            Util.slow_print(Cfg.get('WRONG_ANSW'))

class GuardCH5(Event):
    def __init__(self, player):
        super(GuardCH5, self).__init__(player, disappear_after_run=False)
        self.choices.append(Cfg.get('TALK_GUARD'))
        self.choices.append(Cfg.get('PASS'))
        self.choice_to_function = {0: self.help, 1: self.pass_guard}

    def run(self):
        break_flag = None
        while break_flag!=True:
            Util.clear()
            print(Cfg.get('NOTICE_GUARD') + '\n')
            self.print_choices()
            choice = Util.get_numeric_or_default(Cfg.get('CHOICE') + ' ', -1)
            func_to_call = self.choice_to_function.get(choice, None)
            if choice!=-1 and func_to_call:
                break_flag = func_to_call()
            else:
                break

    def help(self):
        Util.clear()
        Util.slow_print(Cfg.get('GUARDCH5_IS_SAYING') + '\n')

        if self.player.has_item('Health Potion'):
            will_help = Util.get_true_or_false(Cfg.get('HELP_GUARD_CH5'))

            if will_help:
                self.player.remove_item_from_backpack_by_name('Health Potion')
                Util.slow_print(Cfg.get('GUARD_CH5_THANKS') + '\n')
                self.player.add_item_to_backpack(Items.guards_armor)
                self.player.proceed_to_next_chapter = True
                return True
            else:
                Util.slow_print(Cfg.get('GUARDS_COUGH'))

        else:
            help_him = Util.get_true_or_false(Cfg.get('HELP_GUARD_CH5_2'))
            if help_him:
                Util.slow_print('\n' + Cfg.get('GUARD_CH5_THANKS') + '\n')
                self.player.get_money(5)
                Util.slow_print(Cfg.get('MONEY_RECEIVE') % 5, '\n')
                self.player.proceed_to_next_chapter = True
                return True
            else:
                Util.slow_print(Cfg.get('GUARDS_COUGH'))

        Util.clear_with_enter()


    def trade(self):
        Util.slow_print('GUARDCH5_EXCHANGE' + '\n')

    def pass_guard(self):
        self.player.proceed_to_next_chapter = True
        return True


class Mansion(Event):
    def __init__(self, player):
        super(Mansion, self).__init__(player, disappear_after_run=True)

    def run(self):
        self.player.proceed_to_next_chapter = True


class OldManOnHill(Event):
    def __init__(self, player):
        super(OldManOnHill, self).__init__(player, disappear_after_run=True)

    def run(self):
        Util.clear()
        Util.slow_print(Cfg.get('RIDDLE') + '\n')
        Util.clear_with_enter()

        for l in Cfg.getLines('RIDDLE_ON_HILL_INTRO'):
            Util.slow_print(l)

        Util.clear_with_enter()

        Util.slow_print(Cfg.get('SND_RIDDLE'))

        answers = Cfg.getLines('SND_RIDDLE_ANSW')
        user_answ = input('\n' + Cfg.get('WHAT_IS_ANSW') + ' ')

        if user_answ.strip().upper() in answers:
            Util.slow_print('\n' + Cfg.get('RIGHT_ANSW_ON_HILL'))
            next_event = Events.MonsterFight(self.player,
                                Monster.get_slime,
                                allow_to_flee=False,
                                money_received=5)
            next_event.run()
            # self.player.proceed_to_next_chapter = True
        else:
            Util.slow_print(Cfg.get('WRONG_ANSW_ON_HILL'))
            Util.clear_with_enter()


class MansionBed(Event):
    def __init__(self, player):
        super(MansionBed, self).__init__(player, disappear_after_run=True)

    def run(self):
        Util.clear()

        for line in Cfg.getLines('MANSION_BED'):
            Util.slow_print(line)

        self.player.proceed_to_next_chapter = True
        Util.clear_with_enter()


class MansionTrapdoor(Event):
    def __init__(self, player):
        super(MansionTrapdoor, self).__init__(player, disappear_after_run=True)

    def run(self):
        Util.clear()

        for line in Cfg.getLines('MANSION_TRAPDOOR'):
            Util.slow_print(line)

        self.player.proceed_to_next_chapter = True
        Util.clear_with_enter()


class InfinityMaster(Event):
    def __init__(self, player):
        super(InfinityMaster, self).__init__(player, disappear_after_run=True)

    def run(self):
        Util.clear()

        for line in Cfg.getLines('MANSION_BED'):
            Util.slow_print(line)

        self.player.proceed_to_next_chapter = True
        Util.clear_with_enter()
