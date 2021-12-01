from enum import Enum
from commands.CommandException import CommandException

class Strategies(Enum):
    NIGE = 0
    SENKOU = 1
    SASHI = 2
    OIKO = 3

    def __str__(self):
        return ['逃げ', '先行', '差し', '追込'][self.value]

# hp_modifiers[strategy]
strategy_hp_modifiers = {Strategies.NIGE: 0.95, Strategies.SENKOU: 0.89, Strategies.SASHI: 1, Strategies.OIKO: 0.995}

# speed_modifiers[phase][strategy]
strategy_speed_modifiers = [
    {Strategies.NIGE: 1, Strategies.SENKOU: 0.978, Strategies.SASHI: 0.938, Strategies.OIKO: 0.931},
    {Strategies.NIGE: 0.98, Strategies.SENKOU: 0.991, Strategies.SASHI: 0.998, Strategies.OIKO: 1},
    {Strategies.NIGE: 0.962, Strategies.SENKOU: 0.975, Strategies.SASHI: 0.994, Strategies.OIKO: 1}
]

# power_modifiers[phase][strategy]
strategy_power_modifiers = [
    {Strategies.NIGE: 1, Strategies.SENKOU: 0.985, Strategies.SASHI: 0.975, Strategies.OIKO: 0.945},
    {Strategies.NIGE: 1, Strategies.SENKOU: 1, Strategies.SASHI: 1, Strategies.OIKO: 1},
    {Strategies.NIGE: 0.996, Strategies.SENKOU: 0.996, Strategies.SASHI: 1, Strategies.OIKO: 0.997}
]

def parse_strat(strat: str) -> Strategies:
    strat = strat.lower()
    if strat == 'nige' or strat == 'runner' or strat == '逃げ':
        return Strategies.NIGE
    elif strat == 'senkou' or strat == 'leader' or strat == '先行':
        return Strategies.SENKOU
    elif strat == 'sashi' or strat == 'betweener' or strat == '差し':
        return Strategies.SASHI
    elif strat == 'oiko' or strat == 'oikomi' or strat == 'chaser' or strat == '追込' or strat == '追い込み':
        return Strategies.OIKO
    else:
        raise CommandException('Unrecognised strategy')