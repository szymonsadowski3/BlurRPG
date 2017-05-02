import Map
import Utilities as Util

class GameChapter(object):
    def __init__(self, player, id, init_player_position = Util.Position(0,0), title=None):
        self.player = player
        self.id = id
        self.map = Map.LocalMap(player)
        self.map.load_map_from_file('maps/map{}.txt'.format(id))
        self.init_player_position = init_player_position
        self.title = title

    def __str__(self):
        if self.title:
            return "Chapter {}: {}".format(self.id, self.title)
        return "Chapter {}".format(self.id)
