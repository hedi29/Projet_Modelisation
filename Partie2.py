import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import random
from poisson import Poisson

""" Partie 2 : Propagation des Mouvements - L'effet Trafalgar

Simulation d'un banc de poissons 2D avec propagation d'une contamination.

"""
#---------------- Paramètres de simulation ---------------------
n = 20           # Nombre de poissons
xmin, xmax = 0, 10 
ymin, ymax = 0, 10
dt = 0.05
distance_contamination = 0.5  # Distance à laquelle un poisson peut être contaminé
variation_norme = False # Si False, la norme de la vitesse du poisson contaminé est modifiée sinon chaque composante de la vitesse est modifiée
pas_de_variation_norme = 0.05 # le variation de la norme ou de chaque composante de la vitesse

#---------------- Initialisation des poissons ---------------------
poissons = Poisson.creer_banc(n, xmin, xmax, ymin, ymax)

# Sélection aléatoire du leader
leader = random.choice(poissons)
leader.is_contaminated = True
leader.color = 'red'  # Le leader est rouge

#----------------- Configuration du graphique -------------------
fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_title('Simulation de l\'effet Trafalgar')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_facecolor('white')
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')

# Données initiales
positions = np.array([[p.x, p.y] for p in poissons])
directions_x, directions_y = [], []

# fleche 
for p in poissons:
    vx, vy = p.Vx, p.Vy
    norme = np.sqrt(vx**2 + vy**2)
    if norme == 0:
        norme = 1  # Éviter la division par zéro
    directions_x.append(vx / norme)
    directions_y.append(vy / norme)

# Couleurs des poissons (leader=rouge, contaminés=vert, non-contaminés=bleu)
colors = ['red' if p == leader else 'blue' for p in poissons]

# Affichage des flèches 
fleches = ax.quiver(positions[:, 0], positions[:, 1], directions_x, directions_y, 
                   color=colors, width=0.005, scale=30, pivot='mid')

# Cercle de contamination autour du leader
cercle_contamination = Circle((leader.x, leader.y), distance_contamination, 
                             fill=False, color='red', linestyle='--', alpha=0.7)
ax.add_patch(cercle_contamination)

# Compteur de poissons contaminés
contamination_text = ax.text(0.05, 0.95, 'Poissons contaminés: 1', transform=ax.transAxes)

#----------------- Fonctions pour l'animation ----------------------
def init():
    return (fleches, cercle_contamination, contamination_text)

def update(frame):
    global leader
    
    # Vérifier les contaminations
    for poisson in poissons:
        if not poisson.is_contaminated:
            # Vérifier si un poisson contaminé (leader ou autre) est à proximité
            for contaminateur in [p for p in poissons if p.is_contaminated]:
                if Poisson.distance_euclidienne(poisson, contaminateur) < distance_contamination:
                    # Contaminer avec la vitesse du leader
                    poisson.contaminer(contaminateur.Vx, contaminateur.Vy, dV=pas_de_variation_norme, norm = variation_norme)
                    break
    
    # Déplacer tous les poissons
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax)
    
    # Mise à jour des positions et directions dans le graphique
    positions = np.array([[p.x, p.y] for p in poissons])
    
    directions_x, directions_y = [], []
    colors = []
    
    # Préparation des données pour l'affichage
    for p in poissons:
        vx, vy = p.Vx, p.Vy
        norme = np.sqrt(vx**2 + vy**2)
        if norme == 0:
            norme = 1
        directions_x.append(vx / norme)
        directions_y.append(vy / norme)
        
        # Définir les couleurs: rouge pour le leader, vert pour les contaminés, bleu pour les non-contaminés
        if p == leader:
            colors.append('red')
        elif p.is_contaminated:
            colors.append('green')
        else:
            colors.append('blue')
    
    fleches.set_offsets(positions)
    fleches.set_UVC(directions_x, directions_y)
    fleches.set_color(colors)
    
    # Mise à jour du cercle de contamination autour du leader seulement
    cercle_contamination.set_center((leader.x, leader.y))
    
    # Mise à jour du compteur de contamination
    nb_contamines = sum(p.is_contaminated for p in poissons)
    contamination_text.set_text(f'Poissons contaminés: {nb_contamines}/{len(poissons)}')
    
    return (fleches, cercle_contamination, contamination_text)

#------------------ Animation ------------------------------------
# Création de l'animation
ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=20)

# Affichage
plt.show()
