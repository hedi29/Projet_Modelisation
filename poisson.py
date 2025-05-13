import numpy as np
import random

class Poisson:
    def __init__(self, x, y, Vx, Vy, color='blue'):
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy
        self.is_contaminated = False
        self.color = color

    def move(self, Dt):
        self.x = self.x + self.Vx*Dt
        self.y = self.y + self.Vy*Dt
    
    def check_boundary(self, zone_limite):
        """Gère les rebonds sur les bords de l'espace carré [-zone_limite, zone_limite]"""
        if self.x < -zone_limite:
            self.x = -zone_limite
            self.Vx = -self.Vx
        elif self.x > zone_limite:
            self.x = zone_limite
            self.Vx = -self.Vx
            
        if self.y < -zone_limite:
            self.y = -zone_limite
            self.Vy = -self.Vy
        elif self.y > zone_limite:
            self.y = zone_limite
            self.Vy = -self.Vy
    
    def contaminate(self, speed_variation_scale=0.1):
        """Mark the fish as contaminated and alter its state."""
        if not self.is_contaminated:
            self.is_contaminated = True
            self.color = 'green'
            variation_vx = random.uniform(-speed_variation_scale, speed_variation_scale)
            variation_vy = random.uniform(-speed_variation_scale, speed_variation_scale)
            current_speed = np.sqrt(self.Vx**2 + self.Vy**2)
            new_vx = self.Vx + variation_vx
            new_vy = self.Vy + variation_vy
            new_speed = np.sqrt(new_vx**2 + new_vy**2)
            self.Vx = new_vx
            self.Vy = new_vy

    def get_position(self):
        """Returns the position of the fish as a tuple (x, y)."""
        return (self.x, self.y)

    def get_vitesse(self):
        """Calcule la vitesse totale du poisson"""
        return np.sqrt(self.Vx**2 + self.Vy**2)
    
    @staticmethod
    def creer_banc(nb_poissons, zone_limite, v_min=-1, v_max=1):
        """Crée un banc de poissons avec des positions et vitesses aléatoires dans [-zone_limite, zone_limite]"""
        poissons = []
        for _ in range(nb_poissons):
            x = np.random.uniform(-zone_limite, zone_limite)
            y = np.random.uniform(-zone_limite, zone_limite)
            vx = np.random.uniform(v_min, v_max)
            vy = np.random.uniform(v_min, v_max)
            poissons.append(Poisson(x, y, vx, vy))
        return poissons
        
        
