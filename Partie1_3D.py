import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from poisson_3D import Poisson3D

""" Partie 1 : Mouvement Aléatoire en 3D

Simulation d'un banc de poissons 3D avec rebond sur les bords.

Chaque poisson est représenté par une position et une vitesse en 3D entre autres parametres.
La simulation est animée à l'aide de matplotlib.
"""

# Paramètres de simulation
nombre_poissons = 20  # Augmenter le nombre de poissons pour mieux voir l'effet
largeur_bassin = 100  # xmax
hauteur_bassin = 100  # ymax
profondeur_bassin = 100  # zmax
xmin, xmax = 0, largeur_bassin
ymin, ymax = 0, hauteur_bassin
zmin, zmax = 0, profondeur_bassin
dt = 0.1

# Initialisation des poissons
poissons = Poisson3D.creer_banc(nombre_poissons, xmin, xmax, ymin, ymax, zmin, zmax, Vmin=-10, Vmax=10)

# Configuration du graphique
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(zmin, zmax)
ax.set_title('Mouvement aléatoire de poissons en 3D')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Création des points pour l'affichage
scatter = ax.scatter([], [], [], c='blue', marker='o', s=50)

# Fonction d'initialisation pour l'animation
def init():
    return scatter,

# Fonction de mise à jour
def update(frame):
    # Déplacer chaque poisson et vérifier les collisions avec les bords
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax, zmin, zmax)
    
    # Mise à jour des positions pour l'affichage
    positions = np.array([p.get_position() for p in poissons])
    
    # Mise à jour explicite des données du scatter
    scatter._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])
    
    # Forcer un rafraîchissement du graphique
    fig.canvas.draw_idle()
    
    return scatter,

# Création de l'animation avec blit=False pour les animations 3D
ani = animation.FuncAnimation(fig, update, frames=200, 
                             init_func=init, interval=50, 
                             blit=False)

# Affichage
plt.show()
