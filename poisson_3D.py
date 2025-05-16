import numpy as np
import random
from scipy.spatial import KDTree

class Poisson3D:
    
    def __init__(self, x, y, z, Vx, Vy, Vz, color='blue'):
        
        self.x, self.y, self.z = x, y, z   
        self.Vx, self.Vy, self.Vz = Vx, Vy, Vz 
        self.is_contaminated = False 
        self.color = color  

    def deplacer(self, Dt):
        """Déplace le poisson en fonction de sa vitesse"""
        self.x += self.Vx * Dt
        self.y += self.Vy * Dt
        self.z += self.Vz * Dt
    
    def verifier_bords(self, xmin, xmax, ymin, ymax, zmin, zmax):
        """Gère les rebonds sur les bords"""
        # l'axe des x 
        if self.x < xmin:
            self.x = xmin
            self.Vx = -self.Vx  
        elif self.x > xmax:
            self.x = xmax
            self.Vx = -self.Vx
        # l'axe des y 
        if self.y < ymin:
            self.y = ymin
            self.Vy = -self.Vy
        elif self.y > ymax:
            self.y = ymax
            self.Vy = -self.Vy
        # l'axe des z
        if self.z < zmin:
            self.z = zmin
            self.Vz = -self.Vz
        elif self.z > zmax:
            self.z = zmax
            self.Vz = -self.Vz
    
    def contaminer(self, Vx, Vy, Vz, dV, norm=True):
        """Contamine le poisson et modifie son etat"""
        if not self.is_contaminated:
            self.is_contaminated = True
            self.color = 'green'
            
            if norm:
                self.Vx = Vx + random.uniform(-dV, dV)
                self.Vy = Vy + random.uniform(-dV, dV)
                self.Vz = Vz + random.uniform(-dV, dV)
            
            else:
                # Calcul du vecteur vitesse
                vector = np.array([Vx, Vy, Vz])
                
                # Calcul de la norme (magnitude) actuelle
                norm_value = np.linalg.norm(vector)
                
                if norm_value > 0:
                    # Variation aléatoire de la norme
                    norm_variation = norm_value * (1 + random.uniform(-dV, dV))
                    
                    # Conserver la direction mais ajuster la norme
                    vector_normalized = vector / norm_value
                    new_vector = vector_normalized * norm_variation
                    
                    self.Vx = new_vector[0]
                    self.Vy = new_vector[1]
                    self.Vz = new_vector[2]
    
    def get_position(self):
        """Retourne la position du poisson"""
        return (self.x, self.y, self.z)

    def get_vitesse(self):
        """Calcule la vitesse totale du poisson"""
        return np.sqrt(self.Vx**2 + self.Vy**2 + self.Vz**2)
    
    def get_vitesse_np(self):
        """Retourne le vecteur vitesse du poisson"""
        return np.array([self.Vx, self.Vy, self.Vz])
    
    def set_vitesse(self, v, Vmax=1.5):
        """Met à jour la vitesse du poisson"""
        if not isinstance(v, np.ndarray):
            v = np.array(v)
        V = np.linalg.norm(v)
        if V > Vmax:
            v = (v / V) * Vmax
        self.Vx = v[0]
        self.Vy = v[1]
        self.Vz = v[2]
    
    @staticmethod
    def distance_euclidienne(poisson1, poisson2):
        """Calcule la distance euclidienne entre deux poissons"""
        pos1 = np.array(poisson1.get_position())
        pos2 = np.array(poisson2.get_position())
        return np.linalg.norm(pos1 - pos2)
    
    @staticmethod
    def creer_banc(nb_poissons, xmin, xmax, ymin, ymax, zmin, zmax, Vmin=-1, Vmax=1):
        """Crée un banc de poissons avec des positions et vitesses aléatoires"""
        poissons = []
        for _ in range(nb_poissons):
            x = np.random.uniform(xmin, xmax)
            y = np.random.uniform(ymin, ymax)
            z = np.random.uniform(zmin, zmax)
            Vx = np.random.uniform(Vmin, Vmax)
            Vy = np.random.uniform(Vmin, Vmax)
            Vz = np.random.uniform(Vmin, Vmax)
            poissons.append(Poisson3D(x, y, z, Vx, Vy, Vz))
        return poissons
        
    @staticmethod
    def calculer_force_repulsion(poisson, voisin, k_repulsion=0.05):
        """Calcule la force de répulsion entre deux poissons"""
        pos_i = np.array(poisson.get_position())
        pos_j = np.array(voisin.get_position())
        vecteur_d = pos_i - pos_j
        norme_d = np.linalg.norm(vecteur_d)
        if norme_d > 0: 
            return k_repulsion * (vecteur_d / norme_d)
        else:
            return np.zeros(3)
    
    @staticmethod
    def calculer_force_alignement(poisson, voisins, k_alignement=0.03):
        """Calcule la force d'alignement entre un poisson et ses voisins"""
        if not voisins:
            return np.zeros(3)
        direction_moyenne = np.zeros(3)
        for voisin in voisins:
            direction_moyenne += voisin.get_vitesse_np()
        
        if len(voisins) > 0:
            direction_moyenne = direction_moyenne / len(voisins)
            
        return k_alignement * direction_moyenne
    
    @staticmethod
    def calculer_force_attraction(poisson, voisin, k_attraction=0.01):
        """Calcule la force d'attraction entre deux poissons"""
        pos_i = np.array(poisson.get_position())
        pos_j = np.array(voisin.get_position())
        vecteur_d = pos_i - pos_j
        norme_d = np.linalg.norm(vecteur_d)
        
        if norme_d > 0: 
            return k_attraction * (-vecteur_d / norme_d)
        else:
            return np.zeros(3)
    
    @staticmethod
    def appliquer_regles_aoki(poissons, rayon_repulsion=1.0, rayon_alignement=2.5, 
                             rayon_attraction=5.0, k_repulsion=0.05, k_alignement=0.03, 
                             k_attraction=0.01, Vmax=1.5):
        """Applique les règles d'Aoki à l'ensemble du banc de poissons"""
       
        positions = np.array([p.get_position() for p in poissons])
        kdtree = KDTree(positions)
        
        for i, poisson in enumerate(poissons):
            # Etat actuel du poisson
            p_i = np.array(poisson.get_position())
            v_i = poisson.get_vitesse_np()
            
            # Initialisation des forces
            F_repulsion = np.zeros(3)
            F_alignement = np.zeros(3)
            F_attraction = np.zeros(3)
            
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
                distance = Poisson3D.distance_euclidienne(poisson, voisin)
                
                # Classification des voisins selon leur distance
                if distance < rayon_repulsion:
                    voisins_repulsion.append(voisin)
                elif distance < rayon_alignement:
                    voisins_alignement.append(voisin)
                elif distance < rayon_attraction:
                    voisins_attraction.append(voisin)
            
            # Calcul des forces pour chaque type de voisin
            for voisin in voisins_repulsion:
                F_repulsion += Poisson3D.calculer_force_repulsion(poisson, voisin, k_repulsion)
                
            F_alignement = Poisson3D.calculer_force_alignement(poisson, voisins_alignement, k_alignement)
            
            for voisin in voisins_attraction:
                F_attraction += Poisson3D.calculer_force_attraction(poisson, voisin, k_attraction)
                
            # Mise à jour de la vitesse 
            v = v_i + F_repulsion + F_alignement + F_attraction
        
            poisson.set_vitesse(v, Vmax)
            
    @staticmethod
    def appliquer_regles_aoki_six_voisins(poissons, k_repulsion=0.05, k_alignement=0.03, 
                                        k_attraction=0.01, Vmax=1.5):
        """Applique les règles d'Aoki avec 6 voisins"""
        positions = np.array([p.get_position() for p in poissons])
        kdtree = KDTree(positions)
        
        for i, poisson in enumerate(poissons):
            # Etat actuel du poisson
            p_i = np.array(poisson.get_position())
            v_i = poisson.get_vitesse_np()
            
            # Initialisation des forces
            F_repulsion = np.zeros(3)
            F_alignement = np.zeros(3)
            F_attraction = np.zeros(3)
            
            # Recherche des 7 voisins les plus proches (le poisson lui-même inclus)
            distances, indices = kdtree.query(p_i, k=7)  # k=7 car le premier est le poisson lui-même
            
            # Enlever le premier indice (le poisson lui-même)
            indices = indices[1:] if len(indices) > 1 else []
            distances = distances[1:] if len(distances) > 1 else []
            
            # Pour chaque voisin parmi les 6 plus proches
            for j, dist in zip(indices, distances):
                voisin = poissons[j]
                
                # Appliquer toutes les forces en fonction de la distance
                # Force de répulsion (plus forte pour les voisins très proches)
                if dist < 10.0:  # Rayon de répulsion
                    F_repulsion += Poisson3D.calculer_force_repulsion(poisson, voisin, k_repulsion)
                
                # Force d'alignement (pour les voisins à distance moyenne)
                elif dist < 25.0:  # Rayon d'alignement
                    F_alignement += Poisson3D.calculer_force_alignement(poisson, [voisin], k_alignement)
                
                # Force d'attraction (pour les voisins plus éloignés)
                elif dist < 50.0:  # Rayon d'attraction
                    F_attraction += Poisson3D.calculer_force_attraction(poisson, voisin, k_attraction)
            
            # Mise à jour de la vitesse
            v = v_i + F_repulsion + F_alignement + F_attraction
            
            # Limitation de la vitesse maximale
            poisson.set_vitesse(v, Vmax)
            
    @staticmethod
    def voisins_visibles(poisson, poissons, vision_angle=60, rayon_max=50.0):
        """Retourne la liste des poissons visibles"""
        visibles = []
        p = np.array(poisson.get_position())
        v = poisson.get_vitesse_np()
        norme_v = np.linalg.norm(v)
        
        if norme_v == 0:
            return visibles
        
        direction_poisson = v / norme_v
        demi_angle = np.deg2rad(vision_angle / 2)
        
        for autre in poissons:
            if autre is poisson:
                continue
            p_autre = np.array(autre.get_position())
            d = p_autre - p
            norme_d = np.linalg.norm(d)
            
            if norme_d == 0 or norme_d > rayon_max:
                continue
            
            direction = d / norme_d
            angle = np.arccos(np.clip(np.dot(direction_poisson, direction), -1, 1))
            
            if angle <= demi_angle:
                visibles.append(autre)
        return visibles
    
    @staticmethod
    def appliquer_regles_influence_visuelle(poissons, vision_angle=60,
                                           rayon_repulsion=10.0, rayon_alignement=25.0, rayon_attraction=50.0,
                                           k_repulsion=0.05, k_alignement=0.03, k_attraction=0.01,
                                           Vmax=15.0):
        """Applique les règles avec voisins visibles"""
        for poisson in poissons:
            
            visibles = Poisson3D.voisins_visibles(poisson, poissons, vision_angle, rayon_max=rayon_attraction)
           
            F_repulsion = np.zeros(3)
            F_alignement = np.zeros(3)
            F_attraction = np.zeros(3)
           
            voisins_alignement = []
            for voisin in visibles:
                
                distance = Poisson3D.distance_euclidienne(poisson, voisin)
                
                if distance < rayon_repulsion:
                    F_repulsion += Poisson3D.calculer_force_repulsion(poisson, voisin, k_repulsion)
                
                elif distance < rayon_alignement:
                    voisins_alignement.append(voisin)
                
                elif distance < rayon_attraction:
                    F_attraction += Poisson3D.calculer_force_attraction(poisson, voisin, k_attraction)
           
            F_alignement = Poisson3D.calculer_force_alignement(poisson, voisins_alignement, k_alignement)
            v = poisson.get_vitesse_np() + F_repulsion + F_alignement + F_attraction
            poisson.set_vitesse(v, Vmax)
