import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import random
from poisson_3D import Poisson3D

""" Partie 2 : Propagation des Mouvements - L'effet Trafalgar en 3D

Simulation d'un banc de poissons 3D avec propagation d'une contamination.

Un poisson leader contamine les autres poissons à proximité.
Les poissons contaminés suivent la direction et la vitesse du leader.
"""
# ---------------- Paramètres de simulation ---------------------
nombre_poissons = 20
largeur_bassin = 100  # xmax
hauteur_bassin = 100  # ymax
profondeur_bassin = 100  # zmax
xmin, xmax = 0, largeur_bassin
ymin, ymax = 0, hauteur_bassin
zmin, zmax = 0, profondeur_bassin
dt = 0.1
distance_contamination = 25  # Distance à laquelle un poisson peut être contaminé
variation_norme = True  # Si True, la norme de la vitesse du poisson contaminé est modifiée sinon chaque composante de la vitesse est modifiée
pas_de_variation_norme = 0.05  # Variation de la norme ou de chaque composante de la vitesse

# ---------------- Initialisation des poissons ---------------------
poissons = Poisson3D.creer_banc(nombre_poissons, xmin, xmax, ymin, ymax, zmin, zmax, Vmin=-10, Vmax=10)

# Sélection aléatoire du leader
leader = random.choice(poissons)
leader.is_contaminated = True
leader.color = 'red'  # Le leader est rouge

# ----------------- Configuration du graphique -------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_zlim(zmin, zmax)
ax.set_title('Simulation de l\'effet Trafalgar en 3D')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Préparation des données pour l'affichage
positions = np.array([p.get_position() for p in poissons])
colors = ['red' if p is leader else 'blue' for p in poissons]

# Affichage des poissons en 3D
scatter = ax.scatter(
    positions[:, 0], positions[:, 1], positions[:, 2],
    c=colors, marker='o', s=50
)

# Texte d'information sur la contamination
contamination_text = ax.text2D(0.05, 0.95, 'Poissons contaminés: 1', transform=ax.transAxes)

# Fonction d'initialisation pour l'animation
def init():
    return scatter, contamination_text

# Fonction de mise à jour pour l'animation
def update(frame):
    global leader
    
    # Vérifier les contaminations
    for poisson in poissons:
        if not poisson.is_contaminated:
            # Vérifier si un poisson contaminé (leader ou autre) est à proximité
            for contaminateur in [p for p in poissons if p.is_contaminated]:
                if Poisson3D.distance_euclidienne(poisson, contaminateur) < distance_contamination:
                    # Contaminer avec la vitesse du contaminateur
                    poisson.contaminer(contaminateur.Vx, contaminateur.Vy, contaminateur.Vz, 
                                      dV=pas_de_variation_norme, norm=variation_norme)
                    break
    
    # Déplacer tous les poissons
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax, zmin, zmax)
    
    # Mise à jour des positions pour l'affichage
    positions = np.array([p.get_position() for p in poissons])
    
    # Mise à jour des couleurs
    colors = []
    for p in poissons:
        if p is leader:
            colors.append('red')
        elif p.is_contaminated:
            colors.append('green')
        else:
            colors.append('blue')
    
    # Mise à jour des données du scatter
    scatter._offsets3d = (positions[:, 0], positions[:, 1], positions[:, 2])
    scatter.set_color(colors)
    
    # Mise à jour du compteur de contamination
    nb_contamines = sum(p.is_contaminated for p in poissons)
    contamination_text.set_text(f'Poissons contaminés: {nb_contamines}/{len(poissons)}')
    
    # Forcer un rafraîchissement du graphique
    fig.canvas.draw_idle()
    
    return scatter, contamination_text

# Création de l'animation avec blit=False pour les animations 3D
ani = animation.FuncAnimation(fig, update, frames=200, 
                             init_func=init, interval=50, 
                             blit=False)

# Affichage
plt.show() 