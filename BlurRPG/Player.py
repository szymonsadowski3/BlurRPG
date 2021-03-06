import Utilities
from Cfg import Cfg

class Player(object):
    def __init__(self, name, position):
        self.stats = {'hp': 100, 'strength': 5, 'defence': 5, 'vitality': 100, 'agility': 5, 'money': 0}
        self.position = position
        self.name = name
        self.backpack = []
        self.equipment = {'weapon': None, 'armor': None}
        self.proceed_to_next_chapter = False

    def has_item(self, item_name):
        item_names_from_bp = [x.info['name'] for x in self.backpack]
        return item_name in item_names_from_bp

    def move(self, direction):
        self.position.x += direction.dx
        self.position.y += direction.dy

    def print_status(self):
        status = '(name: %s, ' % self.name
        for key, value in self.stats.items():
            status += "%s: %d, " % (key, value)
        status = status[:-2:]
        status += ')'
        print(status)
        print('='*len(status))

    def die(self):
        print('You died!')
        exit(0)

    def take_damage(self, dmg):
        self.stats['hp'] -= dmg
        if self.stats['hp'] <= 0:
            self.die()

    def print_equipment(self):
        for type, item in self.equipment.items():
            if not (item is None):
                eq_string = "(%s: %s), " % (type, str(item))
                print(eq_string[:-2:])
            print()

    def print_backpack(self):
        for count, item in enumerate(self.backpack):
            if not (item is None):
                print("(Item|%d|: %s)" % (count, str(item)))
        print()

    def put_on_eq_item(self, eq_item, slot):
        self.equipment[slot] = eq_item

    def get_overall_stat(self, stat):
        overall = self.stats[stat]
        for _, eq_item in self.equipment.items():
            if not (eq_item is None):
                overall += eq_item.battle_stats[stat]
        return overall

    def consume_item_from_backpack(self, index):
        item = self.backpack[index]
        if item:
            if item.using():
                self.backpack.remove(item)

    def add_item_to_backpack(self, item):
        self.backpack.append(item)
        Utilities.slow_print('\n' + Cfg.get('OBTAIN') % item.info['name'])
        Utilities.clear_with_enter()


    def remove_item_from_backpack(self, item):
        self.backpack.remove(item)


    def remove_item_from_backpack_by_name(self, name):
        for item in self.backpack:
            if item.info['name'] == name:
                self.backpack.remove(item)
                return


    def try_to_buy(self, item):
        Utilities.clear()
        if self.stats['money'] >= item.info['cost']:
            self.stats['money'] -= item.info['cost']
            self.add_item_to_backpack(item)
            Utilities.slow_print(Cfg.get('PURCH') % item.info['name'])
        else:
            print(Cfg.get('NO_FUNDS'))

    def equip_from_bp(self, slot_name, from_bp):
        item_removed = self.equipment[slot_name]
        self.equipment[slot_name] = from_bp

        if item_removed:
            self.add_item_to_backpack(item_removed)

        self.remove_item_from_backpack(from_bp)

    def takeoff_slot(self, slot_name):
        item = self.equipment[slot_name]
        if item:
            self.add_item_to_backpack(self.equipment[slot_name])
        self.equipment[slot_name] = None

    def heal_up(self):
        self.stats['hp'] = self.stats['vitality']

    def get_money(self, money):
        self.stats['money'] += money