from enum import Enum
from commands.CommandException import CommandException

class Track(Enum):
    TURF = 0
    DIRT = 1

    def __str__(self):
        return ['芝', 'ダート'][self.value]

class Condition(Enum):
    GOOD = 0
    SLIGHTLY_HEAVY = 1
    HEAVY = 2
    BAD = 3

    def __str__(self):
        return ['良', '稍重', '重', '不良'][self.value]

class Race:
    valid_distances = [1000, 1200, 1400, 
                       1500, 1600, 1800, 
                       2000, 2200, 2300, 2400, 
                       2500, 2600, 3000, 3200, 3400, 3600]

    def __init__(self, distance: int, type: Track, condition: Condition):
        if distance not in Race.valid_distances:
            raise CommandException('Race distance invalid')

        self.type = type
        self.condition = condition
        self.distance = distance
    
    def get_speed_adjustment(self):
        if self.condition == Condition.BAD:
            return -50
        else:
            return 0

    def get_power_adjustment(self):
        if self.type == Track.TURF:
            if self.condition == Condition.GOOD:
                return 0
            else:
                return -50
        else:
            if self.condition == Condition.SLIGHTLY_HEAVY:
                return -50
            else:
                return -100

    def get_hp_consumption_rate(self):
        if self.condition == Condition.GOOD or self.condition == Condition.SLIGHTLY_HEAVY:
            return 1
        elif self.condition == Condition.HEAVY:
            if self.type == Track.TURF:
                return 1.02
            else: 
                return 1.01
        else:
            return 1.02

    def __str__(self):
        return str(self.distance) + 'm ' + str(self.type) + ' ' + str(self.condition)

def parse_track(input: str) -> Track:
    input = input.lower()
    if input == 'turf' or input == '芝':
        return Track.TURF
    elif input == 'dirt' or input == 'ダート':
        return Track.DIRT
    else:
        raise CommandException('Invalid track type')

def parse_condition(input: str) -> Condition:
    input = input.lower()
    if input == 'good' or input == '良':
        return Condition.GOOD
    elif input == 'slightly heavy' or input == '稍重':
        return Condition.SLIGHTLY_HEAVY
    elif input == 'heavy' or input == '重':
        return Condition.HEAVY
    elif input == 'bad' or input == '不良':
        return Condition.BAD
    else:
        raise CommandException('Invalid track condition')