import Items
import Utilities
from Cfg import Cfg

def basic_bartender(interlocutor):
    bartender = NPC('Joshua',
                    Cfg.get('JOSHUA_STORY'), interlocutor)
    bartender.list_of_wares_to_sell = [Items.basic_beer()]
    return bartender

class NPC(object):
    def __init__(self, name, story_of_life, interlocutor):
        self.name = name
        self.story_of_life = story_of_life
        self.conversation_options = [Cfg.get('ASK_STORY'), Cfg.get('OFFER_TRADE')]
        self.conversation_option_to_function = {0: self.display_story_of_life,
                                     1: self.trade}
        self.list_of_wares_to_sell = []
        self.interlocutor = interlocutor

    def perform(self):
        while True:
            Utilities.clear()
            self.display_conversation_options()
            choice = Utilities.get_numeric_in_range_or_default('\n' + Cfg.get('WHAT_TO_CONVERSE') + ' ', 0, len(self.conversation_options) - 1, -1)
            if choice!=-1:
                func_to_call = self.conversation_option_to_function.get(choice, None)
                if func_to_call:
                    func_to_call()
                else:
                    break
            else:
                break


    def display_conversation_options(self):
        # for option_str, option_id in sorted(self.conversation_options.items()):
        #     print("%d. %s" % (option_id, option_str))
        Utilities.pprint_list(self.conversation_options)

    def display_story_of_life(self):
        Utilities.clear()
        Utilities.slow_print(self.story_of_life)

    def trade(self):
        Utilities.clear()
        Utilities.slow_print('TRADE .\n')
        if self.list_of_wares_to_sell:
            for count, ware in enumerate(self.list_of_wares_to_sell):
                print("%d. %s" % (count, ware))
            choice = Utilities.get_numeric_or_default('\n' + Cfg.get('ASK_BUY') + ' ', -1)
            if choice!=-1 and choice<len(self.list_of_wares_to_sell):
                ware = self.list_of_wares_to_sell[choice]
                if ware:
                    self.interlocutor.try_to_buy(ware)
        else:
            print(Cfg.get('NO_SALE'))