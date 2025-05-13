import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poisson import Poisson
from scipy.spatial import KDTree

""" Partie 3 : Règles Comportementales de Aoki

Simulation d'un banc de poissons 2D avec les règles d'Aoki (répulsion, alignement, attraction).

Chaque poisson est représenté par une position et une vitesse, et ajuste son comportement
selon les trois règles fondamentales : répulsion, alignement et attraction.
"""

#---------------- Paramètres de simulation ---------------------
n = 50           # Nombre de poissons, augmenté pour mieux observer les comportements
xmin, xmax = 0, 10 
ymin, ymax = 0, 10
dt = 0.1

# Paramètres des rayons pour les règles d'Aoki
rayon_repulsion = 1.0
rayon_alignement = 2.5
rayon_attraction = 5.0

# Coefficients de force pour chaque règle
k_repulsion = 0.05
k_alignement = 0.03
k_attraction = 0.01

# Vitesse maximale des poissons
vitesse_max = 1.5

#---------------- Initialisation des poissons ---------------------
poissons = Poisson.creer_banc(n, xmin, xmax, ymin, ymax, -1, 1)

#----------------- Configuration du graphique -------------------
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(xmin-1, xmax+1)
ax.set_ylim(ymin-1, ymax+1)
ax.set_title('Simulation de banc de poissons avec les règles d\'Aoki')
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Données initiales
positions = np.array([[p.x, p.y] for p in poissons])
vitesses_x, vitesses_y = np.array([p.Vx for p in poissons]), np.array([p.Vy for p in poissons])
vitesses = np.sqrt(vitesses_x**2 + vitesses_y**2)

# Poisson de référence pour visualiser les rayons (on prend le premier)
poisson_ref_index = 0
c0 = (poissons[poisson_ref_index].x, poissons[poisson_ref_index].y)

# Affichage : points colorés selon la vitesse + flèches directionnelles
points = ax.scatter(positions[:, 0], positions[:, 1], c=vitesses, cmap='viridis', s=100, alpha=0.8)
fleches = ax.quiver(positions[:, 0], positions[:, 1], vitesses_x, vitesses_y, width=0.003, scale=40)

# Cercles de visualisation pour le poisson de référence
cercle_repulsion = plt.Circle(c0, rayon_repulsion, fill=False, color='r', linestyle='--', alpha=0.3)
cercle_alignement = plt.Circle(c0, rayon_alignement, fill=False, color='g', linestyle='--', alpha=0.3)
cercle_attraction = plt.Circle(c0, rayon_attraction, fill=False, color='b', linestyle='--', alpha=0.3)

ax.add_patch(cercle_repulsion)
ax.add_patch(cercle_alignement)
ax.add_patch(cercle_attraction)

# Légende personnalisée pour les rayons
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='r', linestyle='--', lw=1, label=f'Répulsion (R < {rayon_repulsion})'),
    Line2D([0], [0], color='g', linestyle='--', lw=1, label=f'Alignement ({rayon_repulsion} ≤ R < {rayon_alignement})'),
    Line2D([0], [0], color='b', linestyle='--', lw=1, label=f'Attraction ({rayon_alignement} ≤ R < {rayon_attraction})')
]
ax.legend(handles=legend_elements, loc='upper right')

def appliquer_regles_aoki():
    """Applique les règles d'Aoki à tous les poissons."""
    Poisson.appliquer_regles_aoki(poissons, rayon_repulsion, rayon_alignement, rayon_attraction, 
                                k_repulsion, k_alignement, k_attraction, vitesse_max)

def init():
    """Initialisation de l'animation."""
    return points, fleches, cercle_repulsion, cercle_alignement, cercle_attraction

def update(frame):
    """Mise à jour des positions, vitesses et affichage à chaque frame."""
    # Application des règles d'Aoki
    appliquer_regles_aoki()
    
    # Déplacement des poissons
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax)
    
    # Mise à jour des états des poissons
    positions = np.array([[p.x, p.y] for p in poissons])
    vitesses_x, vitesses_y = np.array([p.Vx for p in poissons]), np.array([p.Vy for p in poissons])
    vitesses = np.array([p.get_vitesse() for p in poissons])
    
    points.set_offsets(positions)
    points.set_array(vitesses)
    
    fleches.set_offsets(positions)
    fleches.set_UVC(vitesses_x, vitesses_y)
    
    # Mise à jour des cercles de visualisation pour suivre le poisson de référence
    poisson_ref = poissons[poisson_ref_index]
    centre_ref = (poisson_ref.x, poisson_ref.y)
    cercle_repulsion.center = centre_ref
    cercle_alignement.center = centre_ref
    cercle_attraction.center = centre_ref
    
    return points, fleches, cercle_repulsion, cercle_alignement, cercle_attraction

#------------------ Animation ------------------------------------
# Création de l'animation
ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=20)

# Ajout d'une barre de couleur pour montrer la vitesse
cbar = plt.colorbar(points)
cbar.set_label('Vitesse')

# Affichage
plt.show()