import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poisson import Poisson
import matplotlib.colors as mcolors

""" Partie 1 : Mouvement Aleatoire

Simulation d'un banc de poissons 2D avec rebond sur les bords.

Chaque poisson est représenté par une position et une vitesse entre autres parametres.
La simulation est animée à l'aide de matplotlib.
"""
#---------------- Paramètres de simulation ---------------------
n = 20           # Nombre de poissons
xmin, xmax = 0, 10 
ymin, ymax = 0, 10
dt = 0.05

#---------------- Initialisation des poissons ---------------------

poissons = Poisson.creer_banc(n,  xmin, xmax, ymin, ymax)

#----------------- Configuration du graphique -------------------

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_title('Simulation de poissons en temps réel')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Données initiales
positions = np.array([[p.x, p.y] for p in poissons])
vitesses_x, vitesses_y = np.array([p.Vx for p in poissons]), np.array([p.Vy for p in poissons])
vitesses = np.sqrt(vitesses_x**2 + vitesses_y**2)

# Affichage : points colorés selon la vitesse + flèches directionnelles
points = ax.scatter(positions[:, 0], positions[:, 1], c=vitesses, cmap='viridis', s=100, alpha=0.8)
fleches = ax.quiver(positions[:, 0], positions[:, 1], vitesses_x, vitesses_y, width=0.003, scale=40)

#----------------- Fonctions pour l'animation ----------------------

def init():
    return points, fleches

def update(frame):
    """Mise à jour des positions, vitesses et affichage à chaque frame."""
     
    for poisson in poissons:
        poisson.deplacer(dt) 
        poisson.verifier_bords(xmin, xmax, ymin, ymax)
    
    # Mise à jour des positions dans le graphique
    positions = np.array([[p.x, p.y] for p in poissons])
    vitesses_x = np.array([p.Vx for p in poissons])
    vitesses_y = np.array([p.Vy for p in poissons])
    vitesses = np.array([p.get_vitesse() for p in poissons])
    
    points.set_offsets(positions)
    points.set_array(vitesses)
    
    fleches.set_offsets(positions)
    fleches.set_UVC(vitesses_x, vitesses_y)
    
    return points, fleches

#------------------ Animation ------------------------------------

# Création de l'animation
ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=20)

# Ajout d'une barre de couleur pour montrer la vitesse
cbar = plt.colorbar(points)
cbar.set_label('Vitesse')

# Affichage
plt.show()
