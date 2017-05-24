import Utilities
from Cfg import Cfg

class Item(object):
    def __init__(self, name):
        self.info = {'name': name, 'cost': 0}

    def __str__(self):
        representation = '{'
        for key, value in self.info.items():
            representation += "%s: %s, " % (key, value)
        representation = representation[:-2:]
        representation += '}'
        return representation

    def using(self): #returns boolean informing if item has been actually consumed
        Utilities.clear()
        Utilities.slow_print(Cfg.get('NOT_CONSUMABLE') % self.info['name'])
        return False


class EqItem(Item):
    def __init__(self, name):
        super(EqItem, self).__init__(name)
        self.battle_stats = {}

    def __str__(self):
        representation = super(EqItem, self).__str__()[:-1:]
        representation += ', '
        for key, value in self.battle_stats.items():
            representation += "%s: %s, " % (key, value)
        representation = representation[:-2:]
        representation += '}'
        return representation


class Weapon(EqItem):
    def __init__(self, name):
        super(Weapon, self).__init__(name)

class Armor(EqItem):
    def __init__(self, name):
        super(Armor, self).__init__(name)

def create_eq_item(name, slot, strength_boost, defence_boost, vitality_boost, agility_boost):
    class_ = globals()[slot.lower().title()]
    weapon = class_(name)
    weapon.battle_stats = {'strength': strength_boost, 'defence': defence_boost, 'vitality': vitality_boost, 'agility': agility_boost}
    return weapon

old_mans_sword = create_eq_item("Old Man's Sword", 'weapon', 4, -2, 0, 1)
guards_armor = create_eq_item("Guard's Armor", 'weapon', 0, 3, 0, 1)


def basic_beer():
    beer = Item('Beer')
    beer.info['cost'] = 1
    def beer_usage():
        Utilities.clear()
        Utilities.slow_print(Cfg.get('BEER_CONS'))
        return True
    beer.using = beer_usage
    return beer

def health_potion(player):
    pot = Item('Health Potion')
    pot.info['cost'] = 10
    def pot_usage():
        Utilities.clear()
        Utilities.slow_print(Cfg.get('HEAL'))
        Utilities.clear_with_enter()
        player.heal_up()
        return True
    pot.using = pot_usage
    return pot