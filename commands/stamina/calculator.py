from math import ceil, log10, sqrt

from commands.stamina.aptitudes import Aptitudes, strategy_aptitude_int_modifiers, distance_aptitude_speed_modifiers, distance_aptitude_accel_modifiers, track_aptitude_power_modifiers
from commands.stamina.moods import Mood, mood_stat_modifiers
from commands.stamina.strategy import Strategies, strategy_hp_modifiers, strategy_speed_modifiers, strategy_power_modifiers
from commands.stamina.track import Race

class Calculator:
    # assumed default values
    def __init__(self):
        self.mood = Mood.VERY_GOOD

        self.speed = 1200
        self.stamina = 600
        self.power = 1200
        self.guts = 300
        self.intelligence = 1200

        self.small_heals = 0.0
        self.med_heals = 0.0
        self.big_heals = 0.0

        self.strategy = Strategies.NIGE
        self.distance_aptitude = Aptitudes.A
        self.track_aptitude = Aptitudes.A
        self.strategy_aptitude = Aptitudes.A
        # self.race = CM_DETAILS

    def set_race(self, race: Race):
        self.race = race
    
    def set_stats(self, speed: int, stamina: int, power: int, guts: int, intelligence: int):
        self.speed = speed
        self.power = power
        self.stamina = stamina
        self.guts = guts
        self.intelligence = intelligence

    def set_mood(self, mood: Mood):
        self.mood  = mood

    def set_strategy(self, strategy: Strategies):
        self.strategy = strategy

    def set_aptitudes(self, track_aptitude: Aptitudes, distance_aptitude: Aptitudes, strategy_aptitude: Aptitudes):
        self.distance_aptitude = distance_aptitude
        self.track_aptitude = track_aptitude
        self.strategy_aptitude = strategy_aptitude

    # small heals: 150 strength e.g. normal white heals, stamina eater
    # med heals: 350 strength e.g. 2* rainbow heals, oguri ult, stamina greed
    # large heals: 550 strength e.g. 3* rainbow heals, gold heals
    # difference from ult levels are not considered because they are too insignificant and complicate user input
    # but the user can input decimals for ult levels
    def set_heals(self, small_heals: float, med_heals: float, big_heals: float):
        self.small_heals = small_heals
        self.med_heals = med_heals
        self.big_heals = big_heals

    def calculate(self):
        base_speed = 20 - (self.race.distance - 2000) / 1000
        mood_stat_bonus = mood_stat_modifiers[self.mood]
        hp_consumption_rate = self.race.get_hp_consumption_rate()

        # distance aptitude factored later, some calculations do not use it
        actual_speed = self.speed * mood_stat_bonus + self.race.get_speed_adjustment()
        actual_stamina = self.stamina * mood_stat_bonus
        # track aptitude factored later, some calculations do not use it
        actual_power = self.power * mood_stat_bonus + self.race.get_power_adjustment()
        actual_guts = self.guts * mood_stat_bonus
        actual_intelligence = self.intelligence * mood_stat_bonus * strategy_aptitude_int_modifiers[self.strategy_aptitude]

        initial_hp = self.race.distance + 0.8 * actual_stamina * strategy_hp_modifiers[self.strategy]
        heal_factor = 1 + (self.small_heals * 150 + self.med_heals * 350 + self.big_heals * 550) / 10000
        healed_hp = initial_hp * heal_factor
        last_hp_consumption = 1 + 200 / sqrt(600 * actual_guts)


        # start dash
        start_starting_speed = 3
        start_target_speed = base_speed * 0.85
        start_accel = 24 + 0.0006 * sqrt(500 * actual_power) * strategy_power_modifiers[0][self.strategy] * \
            distance_aptitude_accel_modifiers[self.distance_aptitude] * track_aptitude_power_modifiers[self.track_aptitude]
        start_time_taken = (start_target_speed - start_starting_speed) / start_accel
        start_distance = (start_target_speed + start_starting_speed) / 2 * start_time_taken
        start_hp_consumed = 20 * hp_consumption_rate * start_time_taken

        # phase 0
        p0_starting_speed = start_target_speed
        p0_target_speed = base_speed * strategy_speed_modifiers[0][self.strategy] + \
            ((actual_intelligence / 5500) * log10(actual_intelligence / 10) - 0.325) / 100 * base_speed
        p0_accel = start_accel - 24

        p0a_time_taken = min((p0_target_speed - p0_starting_speed) / p0_accel, \
            (-p0_starting_speed + sqrt(p0_starting_speed ** 2 + 2 * p0_accel * (self.race.distance / 6 - start_distance))) / p0_accel)
        p0a_distance = (p0_starting_speed + p0_accel * p0a_time_taken / 2) * p0a_time_taken
        p0a_hp_consumed = 20 * hp_consumption_rate * ((p0_accel * p0a_time_taken + p0_starting_speed - base_speed + 12) ** 3 - \
            (p0_starting_speed - base_speed + 12) ** 3) / (3 * p0_accel) / 144


        p0b_distance = max(self.race.distance / 6 - start_distance - p0a_distance, 0)
        p0b_time_taken = p0b_distance / p0_target_speed
        p0b_hp_consumed = 20 * hp_consumption_rate * (p0_target_speed - base_speed + 12) ** 2 / 144 * p0b_time_taken


        # phase 1
        p1_starting_speed = p0_target_speed
        p1_target_speed = base_speed * strategy_speed_modifiers[1][self.strategy] + \
            ((actual_intelligence / 5500) * log10(actual_intelligence / 10) - 0.325) / 100 * base_speed
        if p1_starting_speed <= p1_target_speed:
            p1_accel = 0.0006 * sqrt(500 * actual_power) * strategy_power_modifiers[1][self.strategy] * \
            distance_aptitude_accel_modifiers[self.distance_aptitude] * track_aptitude_power_modifiers[self.track_aptitude]
        else:
            p1_accel = -0.8

        p1a_time_taken = (p1_target_speed - p1_starting_speed) / p1_accel
        p1a_distance = (p1_starting_speed + p1_target_speed) / 2 * p1a_time_taken
        p1a_hp_consumed = 20 * hp_consumption_rate * ((p1_target_speed - base_speed + 12) ** 3 - (p1_starting_speed - base_speed + 12) ** 3) / (3 * p1_accel) / 144


        p1b_distance = self.race.distance / 2 - p1a_distance
        p1b_time_taken = p1b_distance / p1_target_speed
        p1b_hp_consumed = 20 * hp_consumption_rate * (p1_target_speed - base_speed + 12) ** 2 / 144 * p1b_time_taken


        # phase 2/3, last spurt setup for calculating last spurt distance
        ls_target_speed = (base_speed * (strategy_speed_modifiers[2][self.strategy] + 0.01) + \
            sqrt(500 * actual_speed) * distance_aptitude_speed_modifiers[self.distance_aptitude] / 500) * 1.05 + \
            sqrt(500 * actual_speed) * distance_aptitude_speed_modifiers[self.distance_aptitude] / 500
        ls_accel = 0.0006 * sqrt(500 * actual_power) * strategy_power_modifiers[2][self.strategy] * \
            distance_aptitude_accel_modifiers[self.distance_aptitude] * track_aptitude_power_modifiers[self.track_aptitude]

        p2_starting_speed = p1_target_speed
        p2_target_speed = base_speed * strategy_speed_modifiers[2][self.strategy] + \
            sqrt(500 * actual_speed) * distance_aptitude_speed_modifiers[self.distance_aptitude] / 500 + \
            ((actual_intelligence / 5500) * log10(actual_intelligence / 10) - 0.325) / 100 * base_speed
        p2_accel = ls_accel if p2_starting_speed <= p2_target_speed else -0.8


        # this is a mess, but I don't know how to interpret it
        spurt_distance = min(self.race.distance / 3,  \
            (healed_hp - start_hp_consumed - p0a_hp_consumed - p0b_hp_consumed - p1a_hp_consumed - p1b_hp_consumed - \
                (self.race.distance / 3 - 60) * 20 * hp_consumption_rate * last_hp_consumption * \
                    (p2_target_speed - base_speed + 12) ** 2 / 144 / p2_target_speed) / \
            (20 * hp_consumption_rate * last_hp_consumption * ((ls_target_speed - base_speed + 12) ** 2 / 144 / ls_target_speed - \
                (p2_target_speed - base_speed + 12) ** 2 / 144 / p2_target_speed)) + 60)

        # phase 2/3
        p2a_time_taken = 0 if self.race.distance / 3 <= spurt_distance else (p2_target_speed - p2_starting_speed) / p2_accel
        p2a_distance = (p2_starting_speed + p2_target_speed) / 2 * p2a_time_taken
        p2a_hp_consumed = 20 * hp_consumption_rate * last_hp_consumption * \
            ((p2_starting_speed + p2_accel * p2a_time_taken - base_speed + 12) ** 3 - \
            (p2_starting_speed - base_speed + 12) ** 3) / (3 * p2_accel) / 144

        p2b_distance = max(self.race.distance / 3 - spurt_distance - p2a_distance, 0)
        p2b_time_taken = p2b_distance / p2_target_speed
        p2b_hp_consumed = 20 * hp_consumption_rate * last_hp_consumption * (p2_target_speed - base_speed + 12) ** 2 / 144 * p2b_time_taken

        # last spurt
        ls_starting_speed = p1_target_speed if p2a_time_taken == 0 else p2_target_speed

        lsa_time_taken = (ls_target_speed - ls_starting_speed) / ls_accel
        lsa_distance = (ls_starting_speed + ls_target_speed) / 2 * lsa_time_taken
        lsa_hp_consumed = 20 * hp_consumption_rate * last_hp_consumption * \
            ((ls_starting_speed + ls_accel * lsa_time_taken - base_speed + 12) ** 3 - \
            (ls_starting_speed - base_speed + 12) ** 3) / (3 * ls_accel) / 144

        lsb_hp_consumed = min(
            20 * hp_consumption_rate * last_hp_consumption * \
                (ls_target_speed - base_speed + 12) ** 2 / 144 * (self.race.distance / 3 - \
                    p2a_distance - p2b_distance - lsa_distance) / ls_target_speed,
            healed_hp - start_hp_consumed - p0a_hp_consumed - p0b_hp_consumed - \
                p1a_hp_consumed - p1b_hp_consumed - p2a_hp_consumed - p2b_hp_consumed - lsa_hp_consumed)

        lsb_time_taken = lsb_hp_consumed / (20 * hp_consumption_rate * last_hp_consumption * \
            (ls_target_speed - base_speed + 12) ** 2 / 144)
        lsb_distance = ls_target_speed * lsb_time_taken
        
        # out of stam
        decel = -1.2
        decel_distance = self.race.distance / 3 - p2a_distance - p2b_distance - lsa_distance - lsb_distance
        decel_time = (-ls_target_speed + sqrt(ls_target_speed ** 2 + 2 * decel * decel_distance)) / decel

        # ideal spurt
        ideal_accel_time_taken = (ls_target_speed - p1_target_speed) / ls_accel
        ideal_accel_distance = (p1_target_speed + ls_target_speed) / 2 * ideal_accel_time_taken
        ideal_accel_hp_consumption = 20 * hp_consumption_rate * last_hp_consumption * \
            ((p1_target_speed + ls_accel * ideal_accel_time_taken - base_speed + 12) ** 3 - \
            (p1_target_speed - base_speed + 12) ** 3) / (3 * ls_accel) / 144

        ideal_spurt_distance = self.race.distance / 3 - ideal_accel_distance
        ideal_spurt_time_taken = ideal_spurt_distance / ls_target_speed
        ideal_spurt_hp_consumption = 20 * hp_consumption_rate * last_hp_consumption * \
            (ls_target_speed - base_speed + 12) ** 2 / 144 * ideal_spurt_time_taken


        required_hp = start_hp_consumed + p0a_hp_consumed + p0b_hp_consumed + p1a_hp_consumed + \
            p1b_hp_consumed + ideal_accel_hp_consumption + ideal_spurt_hp_consumption
        required_stamina = actual_stamina + (required_hp - healed_hp) / 0.8 / strategy_hp_modifiers[self.strategy] / heal_factor
        return ceil(required_stamina)

    def calculate_skill_rate(self):
        actual_intelligence = self.intelligence * mood_stat_modifiers[self.mood] * strategy_aptitude_int_modifiers[self.strategy_aptitude]
        return max(100 - 9000 / actual_intelligence, 20)

    def calculate_kakari_rate(self):
        actual_intelligence = self.intelligence * mood_stat_modifiers[self.mood] * strategy_aptitude_int_modifiers[self.strategy_aptitude]
        return (6.5 / log10(actual_intelligence / 10 + 1)) ** 2


    def __str__(self):
        return 'Race: ' + str(self.race.distance) + 'm ' + str(self.race.type) + ' ' + str(self.race.condition) + '\n' + \
            str(self.speed) + '/' + str(self.stamina) + '/' + str(self.power) + '/' + str(self.guts) + '/' + str(self.intelligence) + ' ' + \
                str(self.track_aptitude) + '/' + str(self.distance_aptitude) + '/' + str(self.strategy_aptitude) + ' ' + str(self.strategy) + '\n' + \
                    'heals: ' + str(self.small_heals) + '/' + str(self.med_heals) + '/' + str(self.big_heals) + ' ' + str(self.mood) + '\n'
