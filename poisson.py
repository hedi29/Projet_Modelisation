import numpy as np
import random

class Poisson:
    
    def __init__(self, x, y, Vx, Vy, color='blue'):
        # Initialisation de la position (x, y) 
        self.x, self.y = x, y
        # Initialisation de la vitesse (Vx, Vy)
        self.Vx, self.Vy = Vx, Vy
        # Initialisation des autres proprietes 
        self.is_contaminated = False
        self.color = color

    def deplacer(self, Dt):
        """Gère les deplacements des poissons en fonction de la vitesse (Vx, Vy) et le pas du temps Dt"""
        self.x += self.Vx * Dt
        self.y += self.Vy * Dt
    
    def verifier_bords(self, xmin, xmax, ymin, ymax):
        """Gère les rebonds sur les bords """
        # Gestion des bords au niveau de l'axe des x 
        if self.x < xmin:
            self.x = xmin
            self.Vx = -self.Vx  
        elif self.x > xmax:
            self.x = xmax
            self.Vx = -self.Vx
        # Gestion des bords au niveau de l'axe des y 
        if self.y < ymin:
            self.y = ymin
            self.Vy = -self.Vy
        elif self.y > ymax:
            self.y = ymax
            self.Vy = -self.Vy
    
    def contaminer(self, dV=0.1):
        """Contamine le poisson et modifie son etat"""
        if not self.is_contaminated:
            self.is_contaminated = True
            self.color = 'green'
            dVx = random.uniform(-dV, dV)
            dVy = random.uniform(-dV, dV)
            self.Vx = self.Vx + dVx
            self.Vy = self.Vy + dVy

    def get_position(self):
        """Retourne la position du poisson en tuple (x, y)."""
        return (self.x, self.y)

    def get_vitesse(self):
        """Calcule la vitesse totale du poisson"""
        return np.sqrt(self.Vx**2 + self.Vy**2)
    
    @staticmethod
    def distance_euclidienne(poisson1, poisson2):
        """Calcule la distance euclidienne entre deux poissons."""
        pos1 = np.array(poisson1.get_position())
        pos2 = np.array(poisson2.get_position())
        return np.linalg.norm(pos1 - pos2)
    
    @staticmethod
    def creer_banc(nb_poissons, xmin, xmax, ymin, ymax, Vmin=-1, Vmax=1):
        """Crée un banc de poissons avec des positions et vitesses aléatoires dans [-zone_limite, zone_limite]"""
        poissons = []
        for _ in range(nb_poissons):
            x = np.random.uniform(xmin, xmax)
            y = np.random.uniform(ymin, ymax)
            Vx = np.random.uniform(Vmin, Vmax)
            Vy = np.random.uniform(Vmin, Vmax)
            poissons.append(Poisson(x, y, Vx, Vy))
        return poissons
    
        
        
