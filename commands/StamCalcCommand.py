from commands.command import Command
from commands.stamina.aptitudes import Aptitudes
from commands.stamina.strategy import parse_strat
from commands.stamina.calculator import Calculator
from commands.stamina.moods import parse_mood
from commands.stamina.track import Race
from commands.db.raceData import get_user_track
from commands.CommandException import CommandException

class StamCalcCommand(Command):
    COMMAND_WORD = "stamcalc"
    FORMAT = "stamcalc `stats` `aptitudes` `strategy` `heals` (`mood`)\n" + \
        "```\n" + \
        "stats: spd/sta/pow/guts/int\n\n" + \
            "  stats from green skills can be added behind a + (e.g. 1400+80/600/1200/600/1200+40)" + \
        "aptitudes: track aptitude/distance aptitude/strategy aptitude\n\n" + \
        "strategy: runner (逃げ), leader (先行), betweener (差し), chaser (追込)\n\n" + \
        "heals: small heals/med heals/large heals\n" + \
            "  Small heals include white heals and stamina eater\n" + \
            "  Med heals include stamina greed, 1-2* heal ults, xmas oguri ult\n" + \
            "  Large heals include gold heals and 3* heal ults\n" + \
            "  Ult levels can be accounted for by adding decimal parts to the heal counts: \n" + \
            "    For level x heal ulti, add 1.02^(x - 1) - 1 to the respective heal count\n\n" + \
        "mood (optional, default very good): very good (絶好調), good (好調), neutral (普通), bad (不調), very bad (絶不調)\n" +\
        "```\n" + "Make sure to use `setrace` to set the race conditions first"

    def copy(self):
        return StamCalcCommand()

    # proposed format: !stamcalc spd/sta/pow/guts/int track/dist/strat strat heals (mood default zekkouchou)
    def set_arguments(self, arguments: str, user_id: int):
        self.arguments = arguments.strip()
        self.user_id = user_id

    def execute(self, dbUrl):
        calculator = Calculator()
        words: list[str] = self.arguments.split()
        if (len(words) < 4):
            raise CommandException('Invalid format. \n' + StamCalcCommand.FORMAT)

        stat_input = words[0].split('/', -1)
        if len(stat_input) != 5:
            raise CommandException('Exactly 5 stats should be provided')

        try:
            stats = [0, 0, 0, 0, 0]
            for index, stat in enumerate(stat_input):
                if '+' in stat:
                    raw, greens = stat.split('+', 1)
                    raw = int(raw)
                    greens = int(greens)
                    effective = raw + greens if raw <= 1200 else 1200 + (raw - 1200) / 2 + greens
                    stats[index] = int(effective)
                else:
                    raw = int(stat)
                    effective = raw if raw <= 1200 else 1200 + (raw - 1200) / 2
                    stats[index] = int(effective)
                if stats[index] < 0:
                    stats[index] = 0
        except ValueError: 
            raise CommandException('Failed to parse stats')

        calculator.set_stats(*stats)

        aptitudes = words[1].split('/', -1)
        if len(aptitudes) != 3:
            raise CommandException('Exactly 3 aptitudes should be provided')
        
        try:
            aptitudes = [Aptitudes[x.upper()] for x in aptitudes]
        except KeyError:
            raise CommandException('Invalid aptitude')

        calculator.set_aptitudes(*aptitudes)

        strat = parse_strat(words[2])
        calculator.set_strategy(strat)

        heals = words[3].split('/', -1)
        try:
            heals = [float(x) for x in heals]
        except ValueError: 
            raise CommandException('Failed to parse heal count')

        if (len(heals) == 2):
            calculator.set_heals(heals[0], 0.0, heals[1])
        elif (len(heals) == 3):
            calculator.set_heals(*heals)
        else:
            raise CommandException('Heal counts should be small/(med)/large')

        if (len(words) >= 5):
            mood = parse_mood(' '.join(words[4:]))     
            calculator.set_mood(mood)

        # fetch race
        race: Race = get_user_track(dbUrl, self.user_id)
        calculator.set_race(race)

        required_stam = calculator.calculate()

        response = str(calculator)

        if required_stam > stats[1]:
            response += "```diff\n- Not enough stam: Need {} stam\n```\n".format(required_stam)
        elif required_stam * 1.1 > stats[1]:
            response += "```fix\n~ Barely enough stam: Need {} stam\n```\n".format(required_stam)
        else:
            response += "```diff\n+ More than enough stam: Need {} stam\n```\n".format(required_stam)

        skill_rate = calculator.calculate_skill_rate()
        kakari_rate = calculator.calculate_kakari_rate()

        response += "Skill rate: {:.2f}%, Kakari Rate: {:.2f}%".format(skill_rate, kakari_rate)

        return response