import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from poisson_3D import Poisson3D

""" Partie 3 : Règles Comportementales de Aoki en 3D

Simulation d'un banc de poissons 3D avec les règles d'Aoki (répulsion, alignement, attraction).

Chaque poisson est représenté par une position et une vitesse en 3D, et ajuste son comportement
selon les trois règles fondamentales :
- Répulsion : les poissons s'éloignent les uns des autres quand ils sont trop proches
- Alignement : les poissons s'alignent avec leurs voisins à distance moyenne
- Attraction : les poissons se rapprochent de leurs voisins éloignés
"""

# ---------------- Paramètres de simulation ---------------------
nombre_poissons = 50
largeur_bassin = 100  # xmax
hauteur_bassin = 100  # ymax
profondeur_bassin = 100  # zmax
xmin, xmax = 0, largeur_bassin
ymin, ymax = 0, hauteur_bassin
zmin, zmax = 0, profondeur_bassin
dt = 0.1

# Paramètres des rayons pour les règles d'Aoki (adaptés à l'échelle 3D)
rayon_repulsion = 30.0
rayon_alignement = 70.0
rayon_attraction = 200.0

# Coefficients de force pour chaque règle
k_repulsion = 0.05
k_alignement = 0.03
k_attraction = 0.01

# Vitesse maximale des poissons
vitesse_max = 20.0

# ---------------- Initialisation des poissons ---------------------
poissons = Poisson3D.creer_banc(nombre_poissons, xmin, xmax, ymin, ymax, zmin, zmax, Vmin=-15, Vmax=15)

# ----------------- Configuration du graphique -------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(zmin, zmax)
ax.set_title('Simulation des règles d\'Aoki en 3D')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Préparation des données pour l'affichage initial
positions = np.array([p.get_position() for p in poissons])

# Affichage des poissons en 3D
scatter = ax.scatter(
    positions[:, 0], positions[:, 1], positions[:, 2],
    c='blue', marker='o', s=50
)

# Texte d'information sur les règles d'Aoki
ax.text2D(0.05, 0.95, f'Répulsion: R < {rayon_repulsion}', transform=ax.transAxes, color='red')
ax.text2D(0.05, 0.92, f'Alignement: {rayon_repulsion} ≤ R < {rayon_alignement}', transform=ax.transAxes, color='green')
ax.text2D(0.05, 0.89, f'Attraction: {rayon_alignement} ≤ R < {rayon_attraction}', transform=ax.transAxes, color='blue')

# Fonction d'initialisation pour l'animation
def init():
    return scatter,

# Fonction de mise à jour pour l'animation
def update(frame):
    # Application des règles d'Aoki
    Poisson3D.appliquer_regles_aoki(poissons, rayon_repulsion, rayon_alignement, 
                                  rayon_attraction, k_repulsion, k_alignement, 
                                  k_attraction, vitesse_max)
    
    # Déplacement des poissons
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax, zmin, zmax)
    
    # Mise à jour des positions pour l'affichage
    positions = np.array([p.get_position() for p in poissons])
    
    # Mise à jour des données du scatter
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