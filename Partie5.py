import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poisson import Poisson

""" Partie 5 : Réseau d'Influence

Simulation d'un banc de poissons 2D avec un réseau d'influence basé sur les connexions visuelles.

"""

#---------------- Paramètres de simulation ---------------------
n = 30          # Nombre de poissons
xmin, xmax = 0, 20 
ymin, ymax = 0, 20
dt = 0.05

# Angle du cône de vision (en degrés)
angle_cone = 60

# Coefficients de force pour chaque règle
k_repulsion = 0.05
k_alignement = 0.09
k_attraction = 0.01

# Rayons d'influence pour chaque règle
R_repulsion = 1.0
R_alignement = 2.5
R_attraction = 5.0

vitesse_max = 1.5
#---------------- Initialisation des poissons ---------------------
poissons = Poisson.creer_banc(n, xmin, xmax, ymin, ymax, -1.5, 1.5)

#----------------- Configuration du graphique -------------------
# Initialisation du graphique
positions = np.array([[p.x, p.y] for p in poissons])
vitesses_x = np.array([p.Vx for p in poissons])
vitesses_y = np.array([p.Vy for p in poissons])
normes = np.sqrt(vitesses_x**2 + vitesses_y**2)
normes[normes == 0] = 1
vitesses_x_norm = vitesses_x / normes
vitesses_y_norm = vitesses_y / normes

fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_title('Réseau d\'influence visuelle')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_facecolor('white')
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')

fleches = ax.quiver(positions[:, 0], positions[:, 1], vitesses_x_norm, vitesses_y_norm,
                   color='blue', width=0.005, scale=30, pivot='mid')

#----------------- Fonctions pour l'animation ----------------------

def init():
    return (fleches,)

def update(frame):
    # Application des règles d'influence visuelle
    Poisson.appliquer_regles_influence_visuelle(
        poissons,
        vision_angle=angle_cone,
        rayon_repulsion=R_repulsion,
        rayon_alignement=R_alignement,
        rayon_attraction=R_attraction,
        k_repulsion=k_repulsion,
        k_alignement=k_alignement,
        k_attraction=k_attraction,
        Vmax=vitesse_max
    )
    # Déplacement et rebond
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax)
    # Mise à jour de l'affichage
    positions = np.array([[p.x, p.y] for p in poissons])
    vitesses_x = np.array([p.Vx for p in poissons])
    vitesses_y = np.array([p.Vy for p in poissons])
    normes = np.sqrt(vitesses_x**2 + vitesses_y**2)
    normes[normes == 0] = 1
    vitesses_x_norm = vitesses_x / normes
    vitesses_y_norm = vitesses_y / normes
    fleches.set_offsets(positions)
    fleches.set_UVC(vitesses_x_norm, vitesses_y_norm)
    return (fleches,)

#------------------ Animation ------------------------------------
# Création de l'animation
ani = FuncAnimation(fig, update, frames=500, blit=True, interval=20)

# Affichage
plt.show()