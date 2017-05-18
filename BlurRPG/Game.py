#!/usr/bin/env python3.5
from Player import Player
import Map
import Utilities as Util
import random
import Items
import importlib
import GameChapter
from Cfg import Cfg
import time
import Events
import Monster


# numeracja
# widzisz monstera jak jest blisko
# np. 3d -> 3 razy w prawo
# ograniczona widocznosc w labiryncie

class Engine(object):
    attitude_modifiers = {0: 0.7, 1: 1, 2: 1.3}  # attitude - 0 offensive, 1 - neutral, 2 - defensive

    direction_mapping = {
        'W': Util.Direction(dx=0, dy=-1),
        'S': Util.Direction(dx=0, dy=1),
        'A': Util.Direction(dx=-1, dy=0),
        'D': Util.Direction(dx=1, dy=0),
    }

    @classmethod
    def read_direction(cls):
        # return cls.wsad_to_direction(input('\n' + Cfg.get('CHOOSE_DIRECTION') + ' ').upper())
        # return self.str_to_dir(msvcrt.getch().decode('ASCII').upper())
        print('\n' + Cfg.get('CHOOSE_DIRECTION') + ' ')
        return cls.wsad_to_direction(Util.getch().upper())

    @classmethod
    def wsad_to_direction(cls, str):
        print(str)
        if str in cls.direction_mapping:
            return cls.direction_mapping[str]
        else:
            return 'exit_to_menu'

    @staticmethod
    def is_direction_colliding(player, map, direction):
        return map.is_occupied(Util.Position(x=player.position.x + direction.dx, y=player.position.y + direction.dy))

    @classmethod
    def measure_damage(cls, attacker, defender, attacker_attitude=1,
                       defender_attitude=1):  # attitude - 0 offensive, 1 - neutral, 2 - defensive
        overall_strength_attacker = attacker.get_overall_stat('strength')
        overall_defence_defender = defender.get_overall_stat('defence')
        overall_agility_attacker = attacker.get_overall_stat('agility')
        dmg_modifier = 2 - (cls.attitude_modifiers[attacker_attitude] + cls.attitude_modifiers[defender_attitude]) / 2
        atk_def_difference = overall_strength_attacker - overall_defence_defender
        damage = dmg_modifier * (1 + overall_agility_attacker / 100) * random.randint(1,
                                                                                      overall_strength_attacker) + atk_def_difference
        return 0 if damage < 0 else int(damage)

    @staticmethod
    def fetch_event_from_map(map, player):
        return map.fetch_event(player)


class Game(object):
    # OPTIONS
    def run_option_move(self):
        while not self.player.proceed_to_next_chapter:
            self.current_map.print_map_with_player(self.player.position)
            direction = Engine.read_direction()
            if direction == 'exit_to_menu':
                break
            if not Engine.is_direction_colliding(self.player, self.current_map, direction):
                self.player.move(direction)
                event = Engine.fetch_event_from_map(self.current_map, self.player)
                going_to_disappear = event.disappear_after_run
                event.run()
                if going_to_disappear:
                    self.current_map.clear_cell(self.player.position.y, self.player.position.x)

    def run_option_backpack(self):
        Util.clear()
        Util.slow_print('BACKPACK . \n')
        self.player.print_backpack()
        choice = Util.get_numeric_in_range_or_default(
            '\n' + Cfg.get('CONSUMPTION') + ' ', 0,
            len(self.player.backpack) - 1, -1)
        if choice == -1:
            return
        else:
            self.player.consume_item_from_backpack(choice)
            Util.clear_with_enter()

    def run_option_eq(self):  # TODO REFACTOR
        Util.clear()
        flag_exit = False
        while not flag_exit:
            Util.slow_print('EQUIPMENT . \n')
            self.player.print_equipment()
            Util.slow_print('BACKPACK . \n')
            self.player.print_backpack()
            flag_exit = self.eq_replacement()

    def eq_replacement(self):
        slot = input(
            '\n' + Cfg.getLines('REPLACEMENT')[0] + '\n' + Cfg.getLines('REPLACEMENT')[1] + ' ')
        if ' ' in slot and slot.split()[1] == 'empty':
            slot = slot.split()[0]
            if slot.lower() in self.player.equipment:
                Util.slow_print(Cfg.get('TAKE_OFF'))
                self.player.takeoff_slot(slot)
                return True
        if slot.lower() in self.player.equipment:
            Util.clear()
            Util.slow_print('BACKPACK . \n')
            self.player.print_backpack()
            item_index = Util.get_numeric_safe_in_range(
                (Cfg.get('EQUIP') % slot.lower()) + ' ', 0, len(self.player.backpack))
            if item_index != -1 and item_index < len(self.player.backpack):
                item_to_add = self.player.backpack[item_index]
                slot_name_to_classname = slot.lower().title()
                classname = getattr(importlib.import_module("Items"), slot_name_to_classname)
                if isinstance(item_to_add, classname):
                    self.player.equip_from_bp(slot.lower(), item_to_add)
                    Util.slow_print(Cfg.get('REPLACEMENT_SUCCESS'))
                    Util.clear()
                else:
                    Util.slow_print(Cfg.get('WRONG_SLOT'))
                    Util.clear()
            else:
                Util.slow_print(Cfg.get('REPLACEMENT_FAIL'))
                Util.clear()
                return False
        else:
            return True
        return False

    def title(self):
        Util.slow_print('BLUR .')

    def player_initialization(self):
        lines = Cfg.getLines('INIT')

        for index, line in enumerate(lines):
            if index != len(lines) - 1:
                Util.slow_print(line)
            else:
                Util.slow_print(line + ' ', endline=False)

        name = input()
        self.player = Player(name, Util.Position(x=0, y=0))
        Util.clear()

    def player_starting_cfg(self):
        pass
        # self.player.put_on_eq_item(Items.sword_of_oblivion, 'weapon')
        # self.player.put_on_eq_item(Items.shadow_armor, 'armor')
        # self.player.add_item_to_backpack(Items.shadow_armor)

    def __init__(self):
        self.player_options = [Cfg.get('PL_MOVE'), Cfg.get('PL_BP'), Cfg.get('PL_EQ')]
        self.current_map = None
        self.title()
        self.player_initialization()
        self.player_starting_cfg()
        self.player_options_to_function = {0: self.run_option_move, 1: self.run_option_backpack, 2: self.run_option_eq}

        self.list_of_chapters = [
                                    GameChapter.GameChapter(self.player, 1, init_player_position=Util.Position(1, 0),
                                                            title='Escape'),
                                    GameChapter.GameChapter(self.player, 2, init_player_position=Util.Position(1, 1)),
                                    GameChapter.GameChapter(self.player, 3, init_player_position=Util.Position(1, 1),
                                                            map_cell_to_event={'I': Events.InnCH3(self.player),
                                                                               ' ': Events.Blank(self.player)}),
                                    GameChapter.GameChapter(self.player, 4, init_player_position=Util.Position(1, 0),
                                                            map_cell_to_event={' ': Events.Blank(self.player),
                                                                               'S': Events.MonsterFight(self.player,
                                                                                                        Monster.get_slime, allow_to_flee=False, money_received=5),
                                                                               'H': Events.CollectHealthPotion(
                                                                                   self.player), 'R': Events.RiddleManInTunnel(self.player)})][-1:]

    def step(self):
        Util.clear()
        self.player.print_status()
        print()
        Util.pprint_list(self.player_options)
        choice = Util.get_numeric_safe_in_range('\n' + Cfg.get('CHOICE') + ' ', 0,
                                                len(self.player_options) - 1)
        self.player_options_to_function[choice]()


if __name__ == "__main__":

    Util.clear()
    game = Game()
    for chapter in game.list_of_chapters:
        game.player.proceed_to_next_chapter = False
        Util.clear()

        chapter.slow_print_self()
        chapter.slow_print_intro()

        game.current_map = chapter.map
        game.player.position = chapter.init_player_position
        while not game.player.proceed_to_next_chapter:
            game.step()
