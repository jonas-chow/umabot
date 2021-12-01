from enum import Enum

class Aptitudes(Enum):
    S = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7

    def __str__(self):
        return self.name
        

distance_aptitude_speed_modifiers = {
    Aptitudes.S: 1.05, 
    Aptitudes.A: 1, 
    Aptitudes.B: 0.9, 
    Aptitudes.C: 0.8, 
    Aptitudes.D: 0.6, 
    Aptitudes.E: 0.4, 
    Aptitudes.F: 0.2, 
    Aptitudes.G: 0.1
}

distance_aptitude_accel_modifiers = {
    Aptitudes.S: 1, 
    Aptitudes.A: 1, 
    Aptitudes.B: 1, 
    Aptitudes.C: 1,
    Aptitudes.D: 1, 
    Aptitudes.E: 0.6, 
    Aptitudes.F: 0.5, 
    Aptitudes.G: 0.4
}

track_aptitude_power_modifiers = {
    Aptitudes.S: 1.05, 
    Aptitudes.A: 1, 
    Aptitudes.B: 0.9, 
    Aptitudes.C: 0.8,
    Aptitudes.D: 0.7, 
    Aptitudes.E: 0.5, 
    Aptitudes.F: 0.3, 
    Aptitudes.G: 0.1
}

strategy_aptitude_int_modifiers = {
    Aptitudes.S: 1.1, 
    Aptitudes.A: 1, 
    Aptitudes.B: 0.85, 
    Aptitudes.C: 0.75,
    Aptitudes.D: 0.6, 
    Aptitudes.E: 0.4, 
    Aptitudes.F: 0.2, 
    Aptitudes.G: 0.1
}