import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poisson import Poisson
import matplotlib.colors as mcolors

# Création d'un banc de poissons
nb_poissons = 20
# Partie 1 utilisera une zone de -5 à 5 pour être compatible avec la nouvelle classe Poisson
# Si un espace de [0,10] est crucial, la création et les rebonds devront être ajustés différemment.
ZONE_LIMITE_PARTIE1 = 5
poissons = Poisson.creer_banc(nb_poissons, zone_limite=ZONE_LIMITE_PARTIE1)

# Configuration du graphique
fig, ax = plt.subplots(figsize=(10, 10))
# Ajustement des limites du graphique pour correspondre à ZONE_LIMITE_PARTIE1
ax.set_xlim(-ZONE_LIMITE_PARTIE1, ZONE_LIMITE_PARTIE1)
ax.set_ylim(-ZONE_LIMITE_PARTIE1, ZONE_LIMITE_PARTIE1)
ax.set_title('Simulation de poissons en temps réel (Partie 1 modifiée)')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Positions initiales
positions = np.array([[p.x, p.y] for p in poissons])
velocities_x = np.array([p.Vx for p in poissons])
velocities_y = np.array([p.Vy for p in poissons])
speeds = np.array([p.get_vitesse() for p in poissons])

# Points pour représenter les poissons
scatter = ax.scatter(positions[:, 0], positions[:, 1], c=speeds, cmap='viridis', s=100, alpha=0.8)

# Flèches pour représenter les directions des poissons
quiver = ax.quiver(positions[:, 0], positions[:, 1], velocities_x, velocities_y, width=0.003, scale=40)

# Pas de temps pour la simulation
dt = 0.05

# Fonction d'initialisation pour l'animation
def init():
    return scatter, quiver

# Fonction de mise à jour pour l'animation
def update(frame):
    # Mise à jour de la position de chaque poisson
    for poisson in poissons:
        poisson.move(dt) # Utilise la méthode renommée 'move'
        poisson.check_boundary(ZONE_LIMITE_PARTIE1) # Utilise la méthode renommée et paramétrée
    
    # Mise à jour des positions dans le graphique
    positions = np.array([[p.x, p.y] for p in poissons])
    velocities_x = np.array([p.Vx for p in poissons])
    velocities_y = np.array([p.Vy for p in poissons])
    speeds = np.array([p.get_vitesse() for p in poissons])
    
    scatter.set_offsets(positions)
    scatter.set_array(speeds)
    
    quiver.set_offsets(positions)
    quiver.set_UVC(velocities_x, velocities_y)
    
    return scatter, quiver

# Création de l'animation
ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=20)

# Ajout d'une barre de couleur pour montrer la vitesse
cbar = plt.colorbar(scatter)
cbar.set_label('Vitesse')

# Affichage
plt.show()
