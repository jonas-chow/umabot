from commands.command import Command
from commands.stamina.track import Condition, parse_condition, parse_track, Race
from commands.db.raceData import get_cm_track, set_user_track
from commands.CommandException import CommandException

class SetRaceCommand(Command):
    COMMAND_WORD = "setrace"
    FORMAT = "setrace `distance` `track_type` (`track_condition`)\n" + \
        "```\n" + \
        "distance: Race distance in meters\n\n" + \
            "track_type: turf (芝) or dirt (ダート)\n\n" + \
                "track_condition (optional, default good): good (良), slightly heavy (稍重), heavy (重), bad (不良)\n" + \
                    "```"

    def copy(self):
        return SetRaceCommand()

    # proposed format: !setrace dist track_type condition=good
    def set_arguments(self, arguments: str, user_id: int):
        self.arguments = arguments.strip()
        self.user_id = user_id

    def execute(self, dbUrl):
        if self.arguments.lower() == 'cm':
            race: Race = get_cm_track(dbUrl)
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