import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poisson import Poisson

""" Partie 4 : Influence de la Densité

Simulation d'un banc de poissons 2D avec les règles d'Aoki limitées aux 6 plus proches voisins.

Contrairement au modèle initial des cercles concentriques, des études montrent 
que les poissons sont principalement influencés par leurs six voisins les plus proches, 
indépendamment de la densité globale du banc.
"""

#---------------- Paramètres de simulation ---------------------
n = 50           # Nombre de poissons
xmin, xmax = 0, 20 
ymin, ymax = 0, 20
dt = 0.05

# Coefficients de force pour chaque règle
k_repulsion = 0.05
k_alignement = 0.03
k_attraction = 0.01

# Vitesse maximale des poissons
vitesse_max = 1.5

#---------------- Initialisation des poissons ---------------------
poissons = Poisson.creer_banc(n, xmin, xmax, ymin, ymax, -0.5, 0.5)

#----------------- Configuration du graphique -------------------
fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_title('Simulation avec 6 voisins les plus proches')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_facecolor('white')
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')

# Données initiales
positions = np.array([[p.x, p.y] for p in poissons])
directions_x, directions_y = [], []

# Normaliser les vecteurs de direction pour avoir des flèches de taille uniforme
for p in poissons:
    vx, vy = p.Vx, p.Vy
    norme = np.sqrt(vx**2 + vy**2)
    if norme == 0:
        norme = 1  # Éviter la division par zéro
    directions_x.append(vx / norme)
    directions_y.append(vy / norme)

# Affichage des flèches (poissons)
fleches = ax.quiver(positions[:, 0], positions[:, 1], directions_x, directions_y, 
                   color='blue', width=0.005, scale=30, pivot='mid')

# Information sur le modèle
info_text = ax.text(0.05, 0.95, 'Modèle: 6 voisins les plus proches uniquement', 
                    transform=ax.transAxes, fontsize=10)

#----------------- Fonctions pour l'animation ----------------------
def init():
    return (fleches, info_text)

def update(frame):
    """Mise à jour des positions, vitesses et affichage à chaque frame."""
    
    # Application des règles d'Aoki avec seulement les 6 plus proches voisins
    Poisson.appliquer_regles_aoki_six_voisins(poissons, k_repulsion, k_alignement, 
                                             k_attraction, vitesse_max)
    
    # Déplacement des poissons
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax)
    
    # Mise à jour des positions dans le graphique
    positions = np.array([[p.x, p.y] for p in poissons])
    vitesses_x = np.array([p.Vx for p in poissons])
    vitesses_y = np.array([p.Vy for p in poissons])
    
    # Normaliser les vecteurs de vitesse pour avoir des flèches de taille uniforme
    normes = np.sqrt(vitesses_x**2 + vitesses_y**2)
    normes[normes == 0] = 1  # Éviter la division par zéro
    vitesses_x_norm = vitesses_x / normes
    vitesses_y_norm = vitesses_y / normes
    
    fleches.set_offsets(positions)
    fleches.set_UVC(vitesses_x_norm, vitesses_y_norm)
    
    return (fleches, info_text)

#------------------ Animation ------------------------------------
# Création de l'animation
ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=20)

# Affichage
plt.show()
