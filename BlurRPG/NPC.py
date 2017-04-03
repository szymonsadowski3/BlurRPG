import Items
import Utilities
from pprint import pprint
import Player

def basic_bartender(interlocutor):
    bartender = NPC('Joshua', 'Joshua: My childhood, I spent working on my parents\' farm... As soon as I turned into grown up man I started running this inn... 20 years passed ever since', interlocutor)
    bartender.list_of_wares_to_sell = [Items.basic_beer()]
    return bartender

class NPC(object):
    def __init__(self, name, story_of_life, interlocutor):
        self.name = name
        self.story_of_life = story_of_life
        self.conversation_options = ['Ask about story of his life', 'Offer a trade']
        self.conversation_option_to_function = {0: self.display_story_of_life,
                                     1: self.trade}
        self.list_of_wares_to_sell = []
        self.interlocutor = interlocutor

    def perform(self):
        while True:
            Utilities.clear()
            self.display_conversation_options()
            choice = Utilities.get_numeric_in_range_or_default('\nWhat would you like to converse about?: ', 0, len(self.conversation_options) - 1, -1)
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
            choice = Utilities.get_numeric_or_default('\nWould like to buy something? Type [0-...] or anything else to back: ', -1)
            if choice!=-1 and choice<len(self.list_of_wares_to_sell):
                ware = self.list_of_wares_to_sell[choice]
                if ware:
                    self.interlocutor.try_to_buy(ware)
        else:
            print('This person does not have any goods for sale right now!')