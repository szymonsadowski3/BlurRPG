import Events
import Utilities
import Monster
from Cfg import Cfg
import collections

COLLISION_SYMBOL = '#'

legend_mapping = collections.OrderedDict(
    [('#', Cfg.get('HASH')), ('P', Cfg.get('PLAYER')), ('E', Cfg.get('MAZE_END')), ('J', Cfg.get('JACK')),
     ('S', Cfg.get('SLIME')), ('C', Cfg.get('CHEST')), ('T', Cfg.get('TREASURE')), ('R', Cfg.get('RIDDLE'))])


class LocalMap(object):
    def __init__(self, player, map_cell_to_event_object=None):
        self.player = player
        self.map_array = []

        if not map_cell_to_event_object:
            self.map_cell_to_event_object = {' ': Events.Blank(self.player),
                                             'I': Events.Inn(self.player), 'J': Events.JackCH2(self.player),
                                             'E': Events.MazeEnd(self.player)}
        else:
            self.map_cell_to_event_object = map_cell_to_event_object

    def load_map_from_file(self, path):
        with open(path) as f:
            for line in f:
                list_made_from_line = line.rstrip('\n').split(',')
                self.map_array.append(list_made_from_line)

        self.containing_symbols = self.get_containing_symbols()
        self.legend = {k: v for k, v in legend_mapping.items() if k in self.containing_symbols or k == 'P'}

    def __str__(self):
        return ('\n'.join([''.join(['{:2}'.format(item) for item in row])
                           for row in self.map_array]))

    def legend_str(self):
        to_ret = ''
        for k, v in self.legend.items():
            to_ret += '[{}]: {} |'.format(k, v)
        return to_ret

    def print_map_with_player(self, player_position):
        Utilities.clear()
        old_cell = self[player_position.y][player_position.x]
        self[player_position.y][player_position.x] = 'P'
        map_to_print = self.__str__()
        self[player_position.y][player_position.x] = old_cell
        print(map_to_print)
        print('\n' + self.legend_str())

    def is_occupied(self, position):
        return self[position.y][position.x] == COLLISION_SYMBOL

    def __getitem__(self, item):
        return self.map_array[item]

    def clear_cell(self, row, col):
        self[row][col] = ' '

    def get_containing_symbols(self):
        symbols = set()

        for row in self.map_array:
            for cell in row:
                symbols.add(cell)

        return list(symbols)

    def fetch_event(self, player):
        symbol = self[player.position.y][player.position.x]
        fetched = self.map_cell_to_event_object[symbol]
        if isinstance(fetched, Events.MonsterFight):
            fetched.reset()
        return fetched
        # event = self.map_cell_to_event[symbol]
        # if event == Events.MonsterFight:
        #     monster_to_fight = self.map_symbol_to_monster[symbol]
        #     return Events.MonsterFight(player, monster_to_fight)
        # else:
        #     return event(player)
