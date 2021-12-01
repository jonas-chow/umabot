from enum import Enum
from commands.CommandException import CommandException

class Mood(Enum):
    VERY_GOOD = 0
    GOOD = 1
    NEUTRAL = 2
    BAD = 3
    VERY_BAD = 4

    def __str__(self):
        return ['絶好調', '好調', '普通', '不調', '絶不調'][self.value]

mood_stat_modifiers = {
    Mood.VERY_GOOD: 1.04, 
    Mood.GOOD: 1.02, 
    Mood.NEUTRAL: 1, 
    Mood.BAD: 0.98, 
    Mood.VERY_BAD: 0.96
}

def parse_mood(input: str) -> Mood:
    input = input.lower()
    if input == 'very good' or input == 'zekkouchou' or input == '絶好調':
        return Mood.VERY_GOOD
    elif input == 'good' or input == 'kouchou' or input == '好調':
        return Mood.GOOD
    elif input == 'normal' or input == 'neutral' or input == 'futsuu' or input == '普通':
        return Mood.NEUTRAL
    elif input == 'bad' or input == 'fuchou' or input == '不調':
        return Mood.BAD
    elif input == 'very bad' or input == 'zeffuchou' or input == '絶不調':
        return Mood.VERY_BAD
    else:
        raise CommandException('Failed to parse mood')