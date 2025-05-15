import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Wedge
from poisson import Poisson

""" Partie 5 : Réseau d'Influence

Dans cette partie, nous modélisons comment les comportements se propagent dans le banc 
de poissons en utilisant un réseau d'influence basé sur les connexions visuelles.
Chaque poisson est influencé par ceux qu'il peut voir, créant un réseau dynamique 
basé sur les connexions visuelles.
"""

#---------------- Paramètres de simulation ---------------------
n = 50           # Nombre de poissons
xmin, xmax = 0, 20 
ymin, ymax = 0, 20
dt = 0.05

# Angle du cône de vision des poissons (en degrés)
angle_vision = 60

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
poissons = Poisson.creer_banc(n, xmin, xmax, ymin, ymax, -0.5, 0.5)

# Sélection d'un poisson pour visualiser son cône de vision
poisson_focus_index = 0
poisson_focus = poissons[poisson_focus_index]

#----------------- Configuration du graphique -------------------
fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_title('Simulation avec réseau d\'influence visuelle')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_facecolor('white')
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('black')

# Données initiales
positions = np.array([[p.x, p.y] for p in poissons])
directions_x, directions_y = [], []

# Normaliser les vecteurs de direction pour avoir des flèches de taille uniforme
for p in poissons:
    vx, vy = p.Vx, p.Vy
    norme = np.sqrt(vx**2 + vy**2)
    if norme == 0:
        norme = 1  # Éviter la division par zéro
    directions_x.append(vx / norme)
    directions_y.append(vy / norme)

# Couleurs pour les poissons
colors = ['blue' for _ in poissons]
colors[poisson_focus_index] = 'red'  # Le poisson dont on visualise le champ de vision

# Affichage des flèches (poissons)
fleches = ax.quiver(positions[:, 0], positions[:, 1], directions_x, directions_y, 
                   color=colors, width=0.005, scale=30, pivot='mid')

# Créer un cône de vision pour le poisson focus (initialement vide)
angle_deg = np.degrees(np.arctan2(poisson_focus.Vy, poisson_focus.Vx))
cone_vision = Wedge((poisson_focus.x, poisson_focus.y), rayon_attraction, 
                   angle_deg - angle_vision/2, angle_deg + angle_vision/2,
                   alpha=0.2, color='green')
ax.add_patch(cone_vision)

# Connexions entre le poisson focus et ses voisins visibles (initialement vides)
lignes_visibles = []

# Information sur le modèle
info_text = ax.text(0.05, 0.95, f'Modèle: Cône de vision {angle_vision}°', 
                    transform=ax.transAxes, fontsize=10)
nbr_visible_text = ax.text(0.05, 0.92, 'Poissons visibles: 0', 
                         transform=ax.transAxes, fontsize=10)

#----------------- Fonctions pour l'animation ----------------------
def init():
    # Retourner tous les éléments qui seront mis à jour
    return (fleches, cone_vision, info_text, nbr_visible_text, *lignes_visibles)

def update(frame):
    """Mise à jour des positions, vitesses et affichage à chaque frame."""
    global lignes_visibles
    
    # Application des règles d'Aoki avec le cône de vision
    Poisson.appliquer_regles_aoki_vision(poissons, angle_vision, rayon_repulsion, 
                                       rayon_alignement, rayon_attraction, 
                                       k_repulsion, k_alignement, k_attraction, vitesse_max)
    
    # Déplacement des poissons
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax)
    
    # Mise à jour des positions et directions
    positions = np.array([[p.x, p.y] for p in poissons])
    vitesses_x, vitesses_y = [], []
    
    # Normaliser les vecteurs de vitesse
    for p in poissons:
        vx, vy = p.Vx, p.Vy
        norme = np.sqrt(vx**2 + vy**2)
        if norme == 0:
            norme = 1
        vitesses_x.append(vx / norme)
        vitesses_y.append(vy / norme)
    
    # Mise à jour des flèches
    fleches.set_offsets(positions)
    fleches.set_UVC(vitesses_x, vitesses_y)
    
    # Mise à jour du cône de vision pour le poisson focus
    poisson_focus = poissons[poisson_focus_index]
    angle_deg = np.degrees(np.arctan2(poisson_focus.Vy, poisson_focus.Vx))
    cone_vision.set_center((poisson_focus.x, poisson_focus.y))
    cone_vision.set_theta1(angle_deg - angle_vision/2)
    cone_vision.set_theta2(angle_deg + angle_vision/2)
    
    # Supprimer les anciennes lignes de connexion
    for ligne in lignes_visibles:
        ligne.remove()
    lignes_visibles = []
    
    # Déterminer les poissons visibles par le poisson focus
    poissons_visibles = []
    for i, p in enumerate(poissons):
        if i != poisson_focus_index and Poisson.est_visible(poisson_focus, p, angle_vision):
            poissons_visibles.append(p)
            # Créer une ligne entre le poisson focus et le poisson visible
            ligne = ax.plot([poisson_focus.x, p.x], [poisson_focus.y, p.y], 
                           'g-', alpha=0.3, linewidth=1)[0]
            lignes_visibles.append(ligne)
    
    # Mise à jour du texte d'information
    nbr_visible_text.set_text(f'Poissons visibles: {len(poissons_visibles)}')
    
    # Retourner tous les éléments qui ont été mis à jour
    return (fleches, cone_vision, info_text, nbr_visible_text, *lignes_visibles)

#------------------ Animation ------------------------------------
# Création de l'animation
ani = FuncAnimation(fig, update, frames=500, init_func=init, blit=True, interval=20)

# Affichage
plt.show()
