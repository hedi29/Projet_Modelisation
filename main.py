import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poisson import Poisson
import matplotlib.colors as mcolors

# Création d'un banc de poissons
nb_poissons = 20
poissons = []

# Initialisation aléatoire des poissons
for i in range(nb_poissons):
    # Position initiale aléatoire entre 0 et 10
    x = np.random.uniform(0, 10)
    y = np.random.uniform(0, 10)
    
    # Vitesse initiale aléatoire entre -1 et 1
    vx = np.random.uniform(-1, 1)
    vy = np.random.uniform(-1, 1)
    
    poissons.append(Poisson(x, y, vx, vy))

# Configuration du graphique
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title('Simulation de poissons en temps réel')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Positions initiales
positions = np.array([[p.x, p.y] for p in poissons])
velocities_x = np.array([p.Vx for p in poissons])
velocities_y = np.array([p.Vy for p in poissons])
speeds = np.sqrt(velocities_x**2 + velocities_y**2)

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
        poisson.Mise_a_jour(dt)
        
        # Rebond sur les bords avec conservation de l'énergie
        if poisson.x < 0:
            poisson.x = 0
            poisson.Vx = abs(poisson.Vx)
        elif poisson.x > 10:
            poisson.x = 10
            poisson.Vx = -abs(poisson.Vx)
            
        if poisson.y < 0:
            poisson.y = 0
            poisson.Vy = abs(poisson.Vy)
        elif poisson.y > 10:
            poisson.y = 10
            poisson.Vy = -abs(poisson.Vy)
    
    # Mise à jour des positions dans le graphique
    positions = np.array([[p.x, p.y] for p in poissons])
    velocities_x = np.array([p.Vx for p in poissons])
    velocities_y = np.array([p.Vy for p in poissons])
    speeds = np.sqrt(velocities_x**2 + velocities_y**2)
    
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
