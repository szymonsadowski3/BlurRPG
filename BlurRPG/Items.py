import Utilities

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
        Utilities.slow_print('You look at %s... This is certainly not consumable...' % self.info['name'])
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

sword_of_oblivion = create_eq_item('Sword of Oblivion', 'weapon', 15, -5, 0, 5)
sword_of_light = create_eq_item('Sword of Light', 'weapon', 5, 5, 5, 0)
shadow_armor = create_eq_item('Shadow Armor', 'armor', 0, 10, 5, 0)

def basic_beer():
    beer = Item('Beer')
    beer.info['cost'] = 1
    def beer_usage():
        Utilities.clear()
        Utilities.slow_print('As you pour this aureate liquid into your throat, you start to feel tiny noise in your head . . .')
        return True
    beer.using = beer_usage
    return beer