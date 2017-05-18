import Map
import Utilities as Util
from Cfg import Cfg

class GameChapter(object):
    def __init__(self, player, id, init_player_position=Util.Position(0,0), title=None, map_cell_to_event=None):
        self.player = player
        self.id = id
        self.map = Map.LocalMap(player, map_cell_to_event_object=map_cell_to_event)
        self.map.load_map_from_file('maps/map{}.txt'.format(id))
        self.introduction_text = Util.read_lines('intro_texts/ch{}.txt'.format(id))
        self.init_player_position = init_player_position
        self.title = title

    def __str__(self):
        if self.title:
            return "%s %s: %s" % (Cfg.get('CHAPTER'), self.id, self.title)
        return "%s %s"% (Cfg.get('CHAPTER'), self.id)

    def slow_print_self(self):
        Util.slow_print(str(self))

    def slow_print_intro(self):
        for line in self.introduction_text:
            Util.slow_print(line + '\n')

        Util.clear_with_enter()
