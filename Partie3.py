import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from poisson import Poisson

""" Partie 3 : Règles Comportementales de Aoki

Simulation d'un banc de poissons 2D avec les règles d'Aoki (répulsion, alignement, attraction).

"""

#---------------- Paramètres de simulation ---------------------
n = 50          
xmin, xmax = 0, 100 
ymin, ymax = 0, 100
dt = 0.05

# Paramètres des rayons pour les règles d'Aoki
rayon_repulsion = 1.5
rayon_alignement = 3.5
rayon_attraction = 5.0

# Coefficients de force pour chaque règle
k_repulsion = 0.05
k_alignement = 0.03
k_attraction = 0.01

# Vitesse maximale des poissons
vitesse_max = 1.5

#---------------- Initialisation des poissons ---------------------
poissons = Poisson.creer_banc(n, xmin, xmax, ymin, ymax, -0.5, 0.5)

#----------------- Configuration du graphique -------------------
fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_title('Simulation des règles d\'Aoki')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_facecolor('white')
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')

# Données initiales
positions = np.array([[p.x, p.y] for p in poissons])
directions_x, directions_y = [], []

#flèches
for p in poissons:
    vx, vy = p.Vx, p.Vy
    norme = np.sqrt(vx**2 + vy**2)
    if norme == 0:
        norme = 1  
    directions_x.append(vx / norme)
    directions_y.append(vy / norme)

# Affichage des flèches (poissons)
fleches = ax.quiver(positions[:, 0], positions[:, 1], directions_x, directions_y, 
                   color='blue', width=0.005, scale=30, pivot='mid')

# Légende pour les règles d'Aoki
ax.text(0.05, 0.95, f'Répulsion: R < {rayon_repulsion}', transform=ax.transAxes, color='red')
ax.text(0.05, 0.92, f'Alignement: {rayon_repulsion} ≤ R < {rayon_alignement}', transform=ax.transAxes, color='green')
ax.text(0.05, 0.89, f'Attraction: {rayon_alignement} ≤ R < {rayon_attraction}', transform=ax.transAxes, color='blue')

#----------------- Fonctions pour l'animation ----------------------
def init():
    return (fleches,)

def update(frame):
    """Mise à jour des positions, vitesses et affichage à chaque frame."""
    
    # Application des règles d'Aoki
    Poisson.appliquer_regles_aoki(poissons, rayon_repulsion, rayon_alignement, 
                                 rayon_attraction, k_repulsion, k_alignement, 
                                 k_attraction, vitesse_max)
    
    # Déplacement des poissons
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax)
    
    # Mise à jour des positions dans le graphique
    positions = np.array([[p.x, p.y] for p in poissons])
    vitesses_x = np.array([p.Vx for p in poissons])
    vitesses_y = np.array([p.Vy for p in poissons])
    
    # Normaliser les vecteurs de vitesse pour avoir des flèches de taille uniforme
    normes = np.sqrt(vitesses_x**2 + vitesses_y**2)
    normes[normes == 0] = 1  # Éviter la division par zéro
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