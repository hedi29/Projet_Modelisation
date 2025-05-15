import numpy as np
import random
from scipy.spatial import KDTree

class Poisson:
    
    def __init__(self, x, y, Vx, Vy, color='blue'):
        
        self.x, self.y = x, y     # Initialisation de la position (x, y) 
        self.Vx, self.Vy = Vx, Vy # Initialisation de la vitesse (Vx, Vy)
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
    
    def contaminer(self, Vx, Vy, dV, norm=True):
        """Contamine le poisson et modifie son etat"""
        if not self.is_contaminated:
            self.is_contaminated = True
            self.color = 'green'
            
            if norm:

                self.Vx = Vx + random.uniform(-dV, dV)
                self.Vy = Vy + random.uniform(-dV, dV)
            else:
                # Calcul du vecteur vitesse
                vector = np.array([Vx, Vy])
                
                # Calcul de la norme (magnitude) actuelle
                norm = np.linalg.norm(vector)
                
                
                # Variation aléatoire de la norme
                norm_variation = norm * (1 + random.uniform(-dV, dV))
                
                # Conserver la direction mais ajuster la norme
                vector_normalized = vector / norm
                new_vector = vector_normalized * norm_variation
                
                self.Vx = new_vector[0]
                self.Vy = new_vector[1]
            
    

    def get_position(self):
        """Retourne la position du poisson en tuple (x, y)."""
        return (self.x, self.y)

    def get_vitesse(self):
        """Calcule la vitesse totale du poisson"""
        return np.sqrt(self.Vx**2 + self.Vy**2)
    
    def get_vitesse_np(self):
        """Retourne le vecteur vitesse du poisson sous forme de numpy array [Vx, Vy]."""
        return np.array([self.Vx, self.Vy])
    
    def set_vitesse(self, v, Vmax=1.5):
        """
        Met à jour la vitesse du poisson avec une limitation de vitesse maximale.
        """
        if not isinstance(v, np.ndarray):
            v = np.array(v)
        V = np.linalg.norm(v)
        if V > Vmax:
            v = (v / V) * Vmax
        self.Vx = v[0]
        self.Vy = v[1]
    
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
            x, y = np.random.uniform(xmin, xmax), np.random.uniform(ymin, ymax)
            Vx, Vy = np.random.uniform(Vmin, Vmax), np.random.uniform(Vmin, Vmax)
            poissons.append(Poisson(x, y, Vx, Vy))
        return poissons
    
    @staticmethod
    def calculer_force_repulsion(poisson, voisin, k_repulsion=0.05):
        """Calcule la force de répulsion entre deux poissons."""
        pos_i, pos_j  = np.array(poisson.get_position()), np.array(voisin.get_position())
        vecteur_d = pos_i - pos_j
        norme_d = np.linalg.norm(vecteur_d)
        if norme_d > 0: 
            return k_repulsion * (vecteur_d / norme_d)
        else:
            return np.zeros(2)
    
    @staticmethod
    def calculer_force_alignement(poisson, voisins, k_alignement=0.03):
        """Calcule la force d'alignement entre un poisson et ses voisins."""
        if not voisins:
            return np.zeros(2)
        direction_moyenne = np.zeros(2)
        for voisin in voisins:
            direction_moyenne += voisin.get_vitesse_np()
        
        if len(voisins) > 0:
            direction_moyenne = direction_moyenne / len(voisins)
            
        return k_alignement * direction_moyenne
    
    @staticmethod
    def calculer_force_attraction(poisson, voisin, k_attraction=0.01):
        """Calcule la force d'attraction entre deux poissons."""
        pos_i = np.array(poisson.get_position())
        pos_j = np.array(voisin.get_position())
        vecteur_d = pos_i - pos_j
        norme_d = np.linalg.norm(vecteur_d)
        
        if norme_d > 0: 
            return k_attraction * (-vecteur_d / norme_d)
        else:
            return np.zeros(2)
    
    @staticmethod
    def appliquer_regles_aoki(poissons, rayon_repulsion=1.0, rayon_alignement=2.5, 
                             rayon_attraction=5.0, k_repulsion=0.05, k_alignement=0.03, 
                             k_attraction=0.01, Vmax=1.5):
        """Applique les règles d'Aoki à l'ensemble du banc de poissons."""
       
        positions = np.array([[p.x, p.y] for p in poissons])
        kdtree = KDTree(positions)
        
        for i, poisson in enumerate(poissons):
            # Etat actuel du poisson
            p_i = np.array(poisson.get_position())
            v_i = np.array([poisson.Vx, poisson.Vy])
            
            # Initialisation des forces
            F_repulsion = np.zeros(2)
            F_alignement = np.zeros(2)
            F_attraction = np.zeros(2)
            
            # Listes pour stocker les voisins dans chaque zone
            voisins_repulsion = []
            voisins_alignement = []
            voisins_attraction = []
            
            # Trouver tous les voisins dans le rayon d'attraction
            indices = kdtree.query_ball_point(p_i, rayon_attraction)
            
            for j in indices:
                if i == j:  
                    continue
                    
                voisin = poissons[j]
                distance = Poisson.distance_euclidienne(poisson, voisin)
                
                # Classification des voisins selon leur distance
                if distance < rayon_repulsion:
                    voisins_repulsion.append(voisin)
                elif distance < rayon_alignement:
                    voisins_alignement.append(voisin)
                elif distance < rayon_attraction:
                    voisins_attraction.append(voisin)
            
            # Calcul des forces pour chaque type de voisin
            for voisin in voisins_repulsion:
                F_repulsion += Poisson.calculer_force_repulsion(poisson, voisin, k_repulsion)
                
            F_alignement = Poisson.calculer_force_alignement(poisson, voisins_alignement, k_alignement)
            
            for voisin in voisins_attraction:
                F_attraction += Poisson.calculer_force_attraction(poisson, voisin, k_attraction)
            # Mise à jour de la vitesse 
            v = v_i + F_repulsion + F_alignement + F_attraction
        
            poisson.set_vitesse(v, Vmax)
        
    @staticmethod
    def appliquer_regles_aoki_six_voisins(poissons, k_repulsion=0.05, k_alignement=0.03, 
                                        k_attraction=0.01, Vmax=1.5):
        """
        Applique les règles d'Aoki à l'ensemble du banc de poissons,
        mais en considérant uniquement les 6 plus proches voisins de chaque poisson.
        """
        positions = np.array([[p.x, p.y] for p in poissons])
        kdtree = KDTree(positions)
        
        for i, poisson in enumerate(poissons):
            # Etat actuel du poisson
            p_i = np.array(poisson.get_position())
            v_i = np.array([poisson.Vx, poisson.Vy])
            
            # Initialisation des forces
            F_repulsion = np.zeros(2)
            F_alignement = np.zeros(2)
            F_attraction = np.zeros(2)
            
            # Recherche des 7 voisins les plus proches (le poisson lui-même inclus)
            distances, indices = kdtree.query(p_i, k=7)  # k=7 car le premier est le poisson lui-même
            
            # Enlever le premier indice (le poisson lui-même)
            indices = indices[1:] if len(indices) > 1 else []
            
            # Pour chaque voisin parmi les 6 plus proches
            for j in indices:
                voisin = poissons[j]
                distance = Poisson.distance_euclidienne(poisson, voisin)
                
                # Appliquer toutes les forces en fonction de la distance
                # Force de répulsion (plus forte pour les voisins très proches)
                if distance < 1.0:  # Rayon de répulsion
                    F_repulsion += Poisson.calculer_force_repulsion(poisson, voisin, k_repulsion)
                
                # Force d'alignement (pour les voisins à distance moyenne)
                elif distance < 2.5:  # Rayon d'alignement
                    F_alignement += Poisson.calculer_force_alignement(poisson, [voisin], k_alignement)
                
                # Force d'attraction (pour les voisins plus éloignés)
                elif distance < 5.0:  # Rayon d'attraction
                    F_attraction += Poisson.calculer_force_attraction(poisson, voisin, k_attraction)
            
            # Mise à jour de la vitesse
            v = v_i + F_repulsion + F_alignement + F_attraction
            
            # Limitation de la vitesse maximale
            poisson.set_vitesse(v, Vmax)
        
        
