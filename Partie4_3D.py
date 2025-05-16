import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from poisson_3D import Poisson3D

""" Partie 4 : Influence de la Densité en 3D

Simulation d'un banc de poissons 3D avec les règles d'Aoki limitées aux 6 plus proches voisins.


"""

# ---------------- Paramètres de simulation ---------------------
nombre_poissons = 50
largeur_bassin = 200  # xmax
hauteur_bassin = 200  # ymax
profondeur_bassin = 200  # zmax
xmin, xmax = 0, largeur_bassin
ymin, ymax = 0, hauteur_bassin
zmin, zmax = 0, profondeur_bassin
dt = 0.1

# Coefficients de force pour chaque règle
k_repulsion = 0.05
k_alignement = 0.03
k_attraction = 0.01

# Vitesse maximale des poissons
vitesse_max = 15.0

# ---------------- Initialisation des poissons ---------------------
poissons = Poisson3D.creer_banc(nombre_poissons, xmin, xmax, ymin, ymax, zmin, zmax, Vmin=-5, Vmax=5)

# ----------------- Configuration du graphique -------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(zmin, zmax)
ax.set_title('Simulation avec 6 voisins les plus proches en 3D')
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

# Information sur le modèle
info_text = ax.text2D(0.05, 0.95, 'Modèle: 6 voisins les plus proches uniquement', transform=ax.transAxes, fontsize=10)

# Fonction d'initialisation pour l'animation
def init():
    return scatter, info_text

# Fonction de mise à jour pour l'animation
def update(frame):
    # Application des règles d'Aoki avec seulement les 6 plus proches voisins
    Poisson3D.appliquer_regles_aoki_six_voisins(poissons, k_repulsion, k_alignement, 
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
    
    return scatter, info_text

# Création de l'animation avec blit=False pour les animations 3D
ani = animation.FuncAnimation(fig, update, frames=200, 
                             init_func=init, interval=50, 
                             blit=False)

# Affichage
plt.show() 