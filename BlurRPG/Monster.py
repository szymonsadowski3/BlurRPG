class Monster(object):
    def __init__(self, strength, vitality, defence, agility):
        self.stats = {'strength': strength, 'defence': defence, 'hp': vitality, 'agility': agility}
        self.equipment = {'weapon': None, 'armor': None}
        self.name = 'Monster'

    # def print_status(self):
    #     print('Monster | ', end='')
    #     for key, value in self.stats.items():
    #         print("%s: %d | " % (key, value), end='')
    #     print('\n============================\n')

    def print_status(self):
        status = '(name: %s, ' % self.name
        for key, value in self.stats.items():
            status += "%s: %d, " % (key, value)
        status = status[:-2:]
        status += ')'
        print(status)
        print('='*len(status))

    def get_overall_stat(self, stat):
        return self.stats[stat]
