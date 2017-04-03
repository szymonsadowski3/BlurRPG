from Player import Player
from Map import *
import Utilities
from Utilities import *
import random
import Items
import importlib

class Engine(object):
    attitude_modifiers = {0: 0.7, 1: 1, 2: 1.3}  # attitude - 0 offensive, 1 - neutral, 2 - defensive

    direction_mapping = {
        'W': Direction(dx=0, dy=-1),
        'S': Direction(dx=0, dy=1),
        'A': Direction(dx=-1, dy=0),
        'D': Direction(dx=1, dy=0),
    }

    @classmethod
    def read_direction(cls):
        return cls.wsad_to_direction(input('\nType where to go [W|S|A|D] or anything else to back: ').upper())
        # return self.str_to_dir(msvcrt.getch().decode('ASCII').upper())

    @classmethod
    def wsad_to_direction(cls, str):
        if str in cls.direction_mapping:
            return cls.direction_mapping[str]
        else:
            return 'exit_to_menu'

    @staticmethod
    def is_direction_colliding(player, map, direction):
        return map.is_occupied(Position(x=player.position.x + direction.dx, y=player.position.y + direction.dy))

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
        return map.map_cell_to_event[map[player.position.y][player.position.x]](player)


class Game(object):
    # OPTIONS
    def run_option_move(self):
        while True:
            self.map.printMapWithPlayer(self.player.position)
            direction = Engine.read_direction()
            if direction == 'exit_to_menu':
                break
            if not Engine.is_direction_colliding(self.player, self.map, direction):
                self.player.move(direction)
                event = Engine.fetch_event_from_map(self.map, self.player)
                event.run()

    def run_option_backpack(self):
        clear()
        slow_print('BACKPACK . \n')
        self.player.print_backpack()
        choice = Utilities.get_numeric_in_range_or_default(
            '\nType number of item you want to consume [0-...] or [anything else] to back: ', 0,
            len(self.player.backpack) - 1, -1)
        if choice == -1:
            return
        else:
            self.player.consume_item_from_backpack(choice)

    def run_option_eq(self):  # TODO REFACTOR
        clear()
        flag_exit = False
        while not flag_exit:
            slow_print('EQUIPMENT . \n')
            self.player.print_equipment()
            slow_print('BACKPACK . \n')
            self.player.print_backpack()
            flag_exit = self.eq_replacement()

    def eq_replacement(self):
        slot = input(
            '\nType in name of slot that you want to empty or replace or \n[slot_name empty] to take off from some slot: ')
        if ' ' in slot and slot.split()[1] == 'empty':
            slot = slot.split()[0]
            if slot.lower() in self.player.equipment:
                slow_print('You took off item you no longer desired to wear')
                self.player.takeoff_slot(slot)
                return True
        if slot.lower() in self.player.equipment:
            clear()
            slow_print('BACKPACK . \n')
            self.player.print_backpack()
            item_index = Utilities.get_numeric_or_default(
                '[%s] Type in index of item that you want to equip: ' % slot.lower(), -1)
            if item_index != -1 and item_index < len(self.player.backpack):
                item_to_add = self.player.backpack[item_index]
                slot_name_to_classname = slot.lower().title()
                classname = getattr(importlib.import_module("Items"), slot_name_to_classname)
                if isinstance(item_to_add, classname):
                    self.player.equip_from_bp(slot.lower(), item_to_add)
                    clear()
            else:
                return True
        else:
            return True
        return False

    def title(self):
        Utilities.slow_print('BLUR .', typing_speed=20)

    def player_initialization(self):
        Utilities.slow_print(
            '\nYou wake up barely feeling any member of your body. \nApparently, you have been dreaming for a long time, paralyzed...')
        Utilities.slow_print('\n\nYou stood up on your feet and got rid of every particle hidden in your dry eyes.')
        Utilities.slow_print('\n\nYou realized that you are in the middle of some wild beach.')
        Utilities.slow_print('\n\nFirstly, you decided to do some mind exercise. \nAfter long period you remembered your name and wrote it on sand using twig \n[TYPE IN YOUR NAME]: ', endline=False)
        name = input()
        self.player = Player(name, Position(x=1, y=0))
        clear()

    def player_starting_cfg(self):
        self.player.put_on_eq_item(Items.sword_of_oblivion, 'weapon')
        # self.player.put_on_eq_item(Items.shadow_armor, 'armor')
        self.player.add_item_to_backpack(Items.shadow_armor)

    def __init__(self):
        self.player_options = ['Move', 'Backpack', 'Equipment']
        self.map = Map()
        self.map.loadMapFromFile('map.txt')
        self.title()
        self.player_initialization()
        self.player_starting_cfg()
        self.player_options_to_function = {0: self.run_option_move, 1: self.run_option_backpack, 2: self.run_option_eq}

    def step(self):
        clear()
        self.player.print_status()
        print()
        Utilities.pprint_list(self.player_options)
        choice = Utilities.get_numeric_safe_in_range('\nYour choice: ', 0, len(self.player_options) - 1)
        self.player_options_to_function[choice]()


if __name__ == "__main__":
    clear()
    game = Game()
    while True:
        game.step()
