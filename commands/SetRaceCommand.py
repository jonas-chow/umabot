from commands.command import Command
from commands.stamina.track import Condition, Track, parse_condition, parse_track, Race
from commands.db.raceData import get_cm_track, set_user_track
from commands.CommandException import CommandException

class SetRaceCommand(Command):
    COMMAND_WORD = "setrace"
    FORMAT = "setrace `distance` `track_type` (`track_condition`)\n" + \
        "```\n" + \
        "distance: Race distance in meters\n\n" + \
            "track_type: turf (芝) or dirt (ダート)\n\n" + \
                "track_condition (optional, default good): good (良), slightly heavy (稍重), heavy (重), bad (不良)\n" + \
                    "```\n" + "Use `!setrace cm` to quickly set the race to the next Chamption's Meeting!"

    def copy(self):
        return SetRaceCommand()

    # proposed format: !setrace dist track_type condition=good
    def set_arguments(self, arguments: str, user_id: int):
        self.arguments = arguments.strip()
        self.user_id = user_id

    def execute(self, dbUrl):
        first_word = self.arguments.lower()

        if first_word in ['cm', 'short', 'mile', 'mid', 'long', 'dirt']:
            if first_word == 'cm':
                race: Race = get_cm_track(dbUrl)
            elif first_word == 'short':
                race: Race = Race(1400, Track.TURF, Condition.BAD)
            elif first_word == 'mile':
                race: Race = Race(1800, Track.TURF, Condition.BAD)
            elif first_word == 'mid':
                race: Race = Race(2400, Track.TURF, Condition.BAD)
            elif first_word == 'long':
                race: Race = Race(3600, Track.TURF, Condition.BAD)
            else:
                race: Race = Race(1800, Track.DIRT, Condition.BAD)
            
            set_user_track(dbUrl, self.user_id, race)
            return 'Race registered successfully: ' + str(race)
        

        words: list[str] = self.arguments.split(' ', -1)
        if (len(words) < 2):
            raise CommandException('Invalid format. \n' + SetRaceCommand.FORMAT)

        dist = words[0]
        try:
            dist = int(dist)
        except ValueError:
            raise CommandException('Race distance invalid')

        track_type = parse_track(words[1])

        if len(words) >= 3:
            condition = parse_condition(' '.join(words[2:]))
        else:
            condition = Condition.GOOD

        race = Race(dist, track_type, condition)
        set_user_track(dbUrl, self.user_id, race)

        return 'Race registered successfully: ' + str(race)