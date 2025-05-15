import numpy as np
import random
from scipy.spatial import KDTree

class Poisson_3D:
    
    def __init__(self, x, y, z, Vx, Vy, Vz, color='blue'):
        
        self.x, self.y, self.z = x, y, z           # Position 3D (x, y, z)
        self.Vx, self.Vy, self.Vz = Vx, Vy, Vz     # Vitesse 3D (Vx, Vy, Vz)
        self.is_contaminated = False 
        self.color = color
    
    def deplacer(self, Dt):
        """Gère les déplacements des poissons en fonction de la vitesse (Vx, Vy, Vz) et le pas du temps Dt"""
        self.x += self.Vx * Dt
        self.y += self.Vy * Dt
        self.z += self.Vz * Dt
    
    def verifier_bords(self, xmin, xmax, ymin, ymax, zmin, zmax):
        """Gère les rebonds sur les bords d'un cube 3D"""
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
            
        # Gestion des bords au niveau de l'axe des z
        if self.z < zmin:
            self.z = zmin
            self.Vz = -self.Vz
        elif self.z > zmax:
            self.z = zmax
            self.Vz = -self.Vz
    
    def contaminer(self, Vx, Vy, Vz, dV, norm=True):
        """Contamine le poisson et modifie son état"""
        if not self.is_contaminated:
            self.is_contaminated = True
            self.color = 'green'
            
            if norm:
                # Modification de chaque composante individuellement
                self.Vx = Vx + random.uniform(-dV, dV)
                self.Vy = Vy + random.uniform(-dV, dV)
                self.Vz = Vz + random.uniform(-dV, dV)
            else:
                # Modification de la norme du vecteur vitesse
                vector = np.array([Vx, Vy, Vz])
                norm = np.linalg.norm(vector)
                
                if norm == 0:
                    norm = 0.1
                    vector = np.array([0.1, 0, 0])
                
                # Variation aléatoire de la norme
                norm_variation = norm * (1 + random.uniform(-dV, dV))
                
                # Conserver la direction mais ajuster la norme
                vector_normalized = vector / norm
                new_vector = vector_normalized * norm_variation
                
                self.Vx = new_vector[0]
                self.Vy = new_vector[1]
                self.Vz = new_vector[2]
    
    def get_position(self):
        """Retourne la position du poisson en tuple (x, y, z)."""
        return (self.x, self.y, self.z)
    
    def get_vitesse(self):
        """Calcule la vitesse totale (norme) du poisson"""
        return np.sqrt(self.Vx**2 + self.Vy**2 + self.Vz**2)
    
    def get_vitesse_np(self):
        """Retourne le vecteur vitesse du poisson sous forme de numpy array [Vx, Vy, Vz]."""
        return np.array([self.Vx, self.Vy, self.Vz])
    
    def set_vitesse(self, v, Vmax=1.5):
        """Met à jour la vitesse du poisson avec une limitation de vitesse maximale."""
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
        """Calcule la distance euclidienne entre deux poissons en 3D."""
        pos1 = np.array(poisson1.get_position())
        pos2 = np.array(poisson2.get_position())
        return np.linalg.norm(pos1 - pos2)
    
    @staticmethod
    def creer_banc(nb_poissons, xmin, xmax, ymin, ymax, zmin, zmax, Vmin=-1, Vmax=1):
        """Crée un banc de poissons 3D avec des positions et vitesses aléatoires"""
        poissons = []
        for _ in range(nb_poissons):
            x = np.random.uniform(xmin, xmax)
            y = np.random.uniform(ymin, ymax)
            z = np.random.uniform(zmin, zmax)
            Vx = np.random.uniform(Vmin, Vmax)
            Vy = np.random.uniform(Vmin, Vmax)
            Vz = np.random.uniform(Vmin, Vmax)
            poissons.append(Poisson_3D(x, y, z, Vx, Vy, Vz))
        return poissons
    
    @staticmethod
    def calculer_force_repulsion(poisson, voisin, k_repulsion=0.05):
        """Calcule la force de répulsion entre deux poissons en 3D."""
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
        """Calcule la force d'alignement entre un poisson et ses voisins en 3D."""
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
        """Calcule la force d'attraction entre deux poissons en 3D."""
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
        """Applique les règles d'Aoki à l'ensemble du banc de poissons en 3D."""
        
        positions = np.array([[p.x, p.y, p.z] for p in poissons])
        kdtree = KDTree(positions)
        
        for i, poisson in enumerate(poissons):
            # État actuel du poisson
            p_i = np.array(poisson.get_position())
            v_i = np.array([poisson.Vx, poisson.Vy, poisson.Vz])
            
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
                distance = Poisson_3D.distance_euclidienne(poisson, voisin)
                
                # Classification des voisins selon leur distance
                if distance < rayon_repulsion:
                    voisins_repulsion.append(voisin)
                elif distance < rayon_alignement:
                    voisins_alignement.append(voisin)
                elif distance < rayon_attraction:
                    voisins_attraction.append(voisin)
            
            # Calcul des forces pour chaque type de voisin
            for voisin in voisins_repulsion:
                F_repulsion += Poisson_3D.calculer_force_repulsion(poisson, voisin, k_repulsion)
                
            F_alignement = Poisson_3D.calculer_force_alignement(poisson, voisins_alignement, k_alignement)
            
            for voisin in voisins_attraction:
                F_attraction += Poisson_3D.calculer_force_attraction(poisson, voisin, k_attraction)
                
            # Mise à jour de la vitesse 
            v = v_i + F_repulsion + F_alignement + F_attraction
        
            poisson.set_vitesse(v, Vmax)
    
    @staticmethod
    def appliquer_regles_aoki_six_voisins(poissons, k_repulsion=0.05, k_alignement=0.03, 
                                        k_attraction=0.01, Vmax=1.5):
        """
        Applique les règles d'Aoki à l'ensemble du banc de poissons 3D,
        mais en considérant uniquement les 6 plus proches voisins de chaque poisson.
        """
        positions = np.array([[p.x, p.y, p.z] for p in poissons])
        kdtree = KDTree(positions)
        
        for i, poisson in enumerate(poissons):
            # État actuel du poisson
            p_i = np.array(poisson.get_position())
            v_i = np.array([poisson.Vx, poisson.Vy, poisson.Vz])
            
            # Initialisation des forces
            F_repulsion = np.zeros(3)
            F_alignement = np.zeros(3)
            F_attraction = np.zeros(3)
            
            # Recherche des 7 voisins les plus proches (le poisson lui-même inclus)
            distances, indices = kdtree.query(p_i, k=7)  # k=7 car le premier est le poisson lui-même
            
            # Enlever le premier indice (le poisson lui-même)
            indices = indices[1:] if len(indices) > 1 else []
            
            # Pour chaque voisin parmi les 6 plus proches
            for j in indices:
                voisin = poissons[j]
                distance = Poisson_3D.distance_euclidienne(poisson, voisin)
                
                # Appliquer toutes les forces en fonction de la distance
                # Force de répulsion (plus forte pour les voisins très proches)
                if distance < 1.0:  # Rayon de répulsion
                    F_repulsion += Poisson_3D.calculer_force_repulsion(poisson, voisin, k_repulsion)
                
                # Force d'alignement (pour les voisins à distance moyenne)
                elif distance < 2.5:  # Rayon d'alignement
                    F_alignement += Poisson_3D.calculer_force_alignement(poisson, [voisin], k_alignement)
                
                # Force d'attraction (pour les voisins plus éloignés)
                elif distance < 5.0:  # Rayon d'attraction
                    F_attraction += Poisson_3D.calculer_force_attraction(poisson, voisin, k_attraction)
            
            # Mise à jour de la vitesse
            v = v_i + F_repulsion + F_alignement + F_attraction
            
            # Limitation de la vitesse maximale
            poisson.set_vitesse(v, Vmax)
    
    @staticmethod
    def est_visible(poisson_observateur, poisson_cible, angle_cone_deg=60):
        """
        Détermine si un poisson cible est visible par un poisson observateur en 3D,
        c'est-à-dire s'il se trouve dans son cône de vision.
        """
        # Si les poissons sont identiques, retourner False
        if poisson_observateur == poisson_cible:
            return False
            
        # Direction de déplacement de l'observateur (vecteur normalisé)
        v_direction = np.array([poisson_observateur.Vx, poisson_observateur.Vy, poisson_observateur.Vz])
        norme_v = np.linalg.norm(v_direction)
        if norme_v == 0:
            return False  # Si l'observateur ne bouge pas, il ne voit rien
            
        v_direction = v_direction / norme_v
        
        # Vecteur de l'observateur vers la cible
        p_obs = np.array(poisson_observateur.get_position())
        p_cible = np.array(poisson_cible.get_position())
        v_distance = p_cible - p_obs
        
        # Si la distance est nulle, retourner False
        norme_d = np.linalg.norm(v_distance)
        if norme_d == 0:
            return False
            
        v_distance = v_distance / norme_d
        
        # Calcul de l'angle entre la direction de déplacement et le vecteur distance
        cos_angle = np.dot(v_direction, v_distance)
        
        # Convertir l'angle du cône en radians et calculer le cosinus
        angle_cone_rad = np.radians(angle_cone_deg / 2)  # Demi-angle
        cos_angle_cone = np.cos(angle_cone_rad)
        
        # Le poisson est visible si l'angle est inférieur à la moitié de l'angle du cône
        return cos_angle > cos_angle_cone
    
    @staticmethod
    def appliquer_regles_aoki_vision(poissons, angle_vision=60, 
                                   rayon_repulsion=1.0, rayon_alignement=2.5, rayon_attraction=5.0,
                                   k_repulsion=0.05, k_alignement=0.03, k_attraction=0.01, 
                                   Vmax=1.5):
        """
        Applique les règles d'Aoki à l'ensemble du banc de poissons 3D,
        mais en considérant uniquement les poissons visibles dans le cône de vision.
        """
        for i, poisson in enumerate(poissons):
            # État actuel du poisson
            p_i = np.array(poisson.get_position())
            v_i = np.array([poisson.Vx, poisson.Vy, poisson.Vz])
            
            # Initialisation des forces
            F_repulsion = np.zeros(3)
            F_alignement = np.zeros(3)
            F_attraction = np.zeros(3)
            
            # Listes pour stocker les voisins visibles dans chaque zone
            voisins_repulsion = []
            voisins_alignement = []
            voisins_attraction = []
            
            # Déterminer les poissons visibles
            for j, voisin in enumerate(poissons):
                if i != j and Poisson_3D.est_visible(poisson, voisin, angle_vision):
                    
                    # Classement des voisins selon leur distance
                    distance = Poisson_3D.distance_euclidienne(poisson, voisin)
                    if distance < rayon_repulsion:
                        voisins_repulsion.append(voisin)
                    elif distance < rayon_alignement:
                        voisins_alignement.append(voisin)
                    elif distance < rayon_attraction:
                        voisins_attraction.append(voisin)
            
            # Calcul des forces pour chaque type de voisin visible
            for voisin in voisins_repulsion:
                F_repulsion += Poisson_3D.calculer_force_repulsion(poisson, voisin, k_repulsion)
                
            if voisins_alignement:
                F_alignement = Poisson_3D.calculer_force_alignement(poisson, voisins_alignement, k_alignement)
            
            for voisin in voisins_attraction:
                F_attraction += Poisson_3D.calculer_force_attraction(poisson, voisin, k_attraction)
                
            # Mise à jour de la vitesse
            v = v_i + F_repulsion + F_alignement + F_attraction
            
            # Limitation de la vitesse maximale
            poisson.set_vitesse(v, Vmax) 