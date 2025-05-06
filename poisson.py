import numpy as np

class Poisson:
    def __init__(self, x, y, Vx, Vy):
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy

    def Mise_a_jour(self, Dt):
        self.x = self.x + self.Vx*Dt
        self.y = self.y + self.Vy*Dt
        self.Vx = self.Vx
        self.Vy = self.Vy
        
        
