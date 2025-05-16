import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from poisson_3D import Poisson3D

""" Partie 5 : Réseau d'Influence en 3D

Simulation d'un banc de poissons 3D avec un réseau d'influence basé sur les connexions visuelles.


"""

# ---------------- Paramètres de simulation ---------------------
nombre_poissons = 50
largeur_bassin = 50  # xmax
hauteur_bassin = 50  # ymax
profondeur_bassin = 50  # zmax
xmin, xmax = 0, largeur_bassin
ymin, ymax = 0, hauteur_bassin
zmin, zmax = 0, profondeur_bassin
dt = 0.1

# Angle du cône de vision (en degrés)
angle_cone = 60

# Paramètres des rayons pour les règles d'Aoki (adaptés à l'échelle 3D)
rayon_repulsion = 10.0
rayon_alignement = 25.0
rayon_attraction = 50.0

# Coefficients de force pour chaque règle
k_repulsion = 0.05
k_alignement = 0.10
k_attraction = 0.01

# Vitesse maximale des poissons
vitesse_max = 20.0

# ---------------- Initialisation des poissons ---------------------
poissons = Poisson3D.creer_banc(nombre_poissons, xmin, xmax, ymin, ymax, zmin, zmax, Vmin=-5, Vmax=5)

# ----------------- Configuration du graphique -------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(zmin, zmax)
ax.set_title('Réseau d\'influence visuelle en 3D')
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
info_text = ax.text2D(0.05, 0.95, f'Angle de vision: {angle_cone}°', transform=ax.transAxes, fontsize=10)

# Fonction d'initialisation pour l'animation
def init():
    return scatter, info_text

# Fonction de mise à jour pour l'animation
def update(frame):
    # Application des règles d'influence visuelle
    Poisson3D.appliquer_regles_influence_visuelle(
        poissons,
        vision_angle=angle_cone,
        rayon_repulsion=rayon_repulsion,
        rayon_alignement=rayon_alignement,
        rayon_attraction=rayon_attraction,
        k_repulsion=k_repulsion,
        k_alignement=k_alignement,
        k_attraction=k_attraction,
        Vmax=vitesse_max
    )
    
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