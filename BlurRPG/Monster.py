class Monster(object):
    def __init__(self, strength, vitality, defence, agility, name='Monster'):
        self.stats = {'strength': strength, 'defence': defence, 'hp': vitality, 'agility': agility}
        self.equipment = {'weapon': None, 'armor': None}
        self.name = name

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

Banshee = Monster(8, 100, 8, 8, 'Banshee')
