import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poisson import Poisson

""" Partie 1 : Mouvement Aleatoire

Simulation d'un banc de poissons 2D avec rebond sur les bords.

"""
#---------------- Paramètres de simulation ---------------------
n = 20           # Nombre de poissons
xmin, xmax = 0, 10 
ymin, ymax = 0, 10
dt = 0.05       # pas de temps

#---------------- Initialisation des poissons ---------------------

poissons = Poisson.creer_banc(n,  xmin, xmax, ymin, ymax)

#----------------- Configuration du graphique -------------------

fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_title('Simulation de poissons en temps réel')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_facecolor('white')
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')

# Données initiales
positions = np.array([[p.x, p.y] for p in poissons])
vitesses_x, vitesses_y = np.array([p.Vx for p in poissons]), np.array([p.Vy for p in poissons])

# fléche
normes = np.sqrt(vitesses_x**2 + vitesses_y**2)
normes[normes == 0] = 1  # Éviter la division par zéro
vitesses_x_norm = vitesses_x / normes
vitesses_y_norm = vitesses_y / normes

fleches = ax.quiver(positions[:, 0], positions[:, 1], vitesses_x_norm, vitesses_y_norm, 
                   color='blue', width=0.005, scale=30, pivot='mid')

#----------------- Fonctions pour l'animation ----------------------

def init():
    return (fleches,)

def update(frame):
    """Mise à jour des positions, vitesses et affichage à chaque frame."""
     
    for poisson in poissons:
        poisson.deplacer(dt) 
        poisson.verifier_bords(xmin, xmax, ymin, ymax)
    
    # Mise à jour des positions dans le graphique
    positions = np.array([[p.x, p.y] for p in poissons])
    vitesses_x = np.array([p.Vx for p in poissons])
    vitesses_y = np.array([p.Vy for p in poissons])
    
    # fléche
    normes = np.sqrt(vitesses_x**2 + vitesses_y**2)
    normes[normes == 0] = 1 
    vitesses_x_norm = vitesses_x / normes
    vitesses_y_norm = vitesses_y / normes
    
    fleches.set_offsets(positions)
    fleches.set_UVC(vitesses_x_norm, vitesses_y_norm)
    
    return (fleches,)

#------------------ Animation ------------------------------------

# Création de l'animation
ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=20)

# Affichage
plt.show()
