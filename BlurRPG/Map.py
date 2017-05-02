import Events
import Utilities

class LocalMap(object):
    def __init__(self):
        self.map_array = []
        self.map_cell_to_event = {'M' : Events.MonsterFight, ' ' : Events.Blank, 'I' : Events.Inn, 'D' : Events.DisappearingBansheeWarner}

    def load_map_from_file(self, path):
        with open(path) as f:
            for line in f:
                list_made_from_line = line.rstrip('\n').split(',')
                self.map_array.append(list_made_from_line)

    def __str__(self):
        return('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in self.map_array]))

    def print_map_with_player(self, player_position):
        Utilities.clear()
        old_cell = self[player_position.y][player_position.x]
        self[player_position.y][player_position.x] = 'P'
        #map_to_print = ('\n'.join([''.join(['{:4}'.format(item) for item in row])
                    #for row in self.map_array]))
        map_to_print = self.__str__()
        self[player_position.y][player_position.x] = old_cell
        print(map_to_print)

    def is_occupied(self, position):
        return self[position.y][position.x]=='S'

    def __getitem__(self, item):
        return self.map_array[item]

    def clear_cell(self, row, col):
        self[row][col] = ' '