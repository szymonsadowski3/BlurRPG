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


def get_slime():
    return Monster(strength=4, vitality=100, defence=4, agility=10, name='Slime')

def get_phantom():
    return Monster(strength=10, vitality=10, defence=10, agility=10, name='Phantom')
