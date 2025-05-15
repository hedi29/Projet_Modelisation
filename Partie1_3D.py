import numpy as np
import plotly.graph_objects as go
from poisson_3D import Poisson_3D
import plotly.io as pio

# Configurer Plotly pour ouvrir la visualisation dans un navigateur
pio.renderers.default = "browser"

""" Partie 1 3D : Mouvement Aléatoire

Simulation d'un banc de poissons 3D avec rebond sur les bords d'un cube.

Chaque poisson est représenté par une position 3D et une vitesse 3D.
La simulation est animée à l'aide de Plotly qui crée une visualisation interactive dans le navigateur.
"""
#---------------- Paramètres de simulation ---------------------
n = 50           # Nombre de poissons
xmin, xmax = -100, 100 
ymin, ymax = -100, 100
zmin, zmax = -100, 100
dt = 0.1
nb_frames = 100  # Nombre de frames pour l'animation

#---------------- Initialisation des poissons ---------------------
poissons = Poisson_3D.creer_banc(n, xmin, xmax, ymin, ymax, zmin, zmax, -0.5, 0.5)

#---------------- Préparation des données pour l'animation ---------------------
# Stockage de toutes les positions pour l'animation
all_positions = []
all_directions = []

# Calculer toutes les positions pour toutes les frames
for frame in range(nb_frames):
    # Déplacer tous les poissons
    for poisson in poissons:
        poisson.deplacer(dt)
        poisson.verifier_bords(xmin, xmax, ymin, ymax, zmin, zmax)
    
    # Récupérer les positions et directions actuelles
    positions = np.array([[p.x, p.y, p.z] for p in poissons])
    vitesses = np.array([[p.Vx, p.Vy, p.Vz] for p in poissons])
    
    # Normaliser les vecteurs de vitesse
    normes = np.linalg.norm(vitesses, axis=1)
    normes[normes == 0] = 1  # Éviter la division par zéro
    directions = vitesses / normes.reshape(-1, 1)
    
    # Stocker les positions et directions pour cette frame
    all_positions.append(positions.copy())
    all_directions.append(directions.copy())

#---------------- Création de l'animation ---------------------
# Créer une figure Plotly vide
fig = go.Figure()

# Définir les limites du graphique
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[xmin, xmax], title="X"),
        yaxis=dict(range=[ymin, ymax], title="Y"),
        zaxis=dict(range=[zmin, zmax], title="Z"),
        aspectmode='cube'  # Garder les dimensions proportionnelles
    ),
    title="Simulation 3D de poissons",
    template="plotly_white",
    margin=dict(l=0, r=0, b=0, t=30)
)

# Ajouter les données pour la première frame
positions = all_positions[0]
directions = all_directions[0]
arrow_length = 5  # Longueur des flèches
arrow_ends = positions + directions * arrow_length

# Ajouter les points (positions des poissons)
fig.add_trace(go.Scatter3d(
    x=positions[:, 0],
    y=positions[:, 1],
    z=positions[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color='blue',
        opacity=0.7
    ),
    name='Poissons'
))

# Créer des lignes pour représenter les directions
for i in range(n):
    fig.add_trace(go.Scatter3d(
        x=[positions[i, 0], arrow_ends[i, 0]],
        y=[positions[i, 1], arrow_ends[i, 1]],
        z=[positions[i, 2], arrow_ends[i, 2]],
        mode='lines',
        line=dict(color='blue', width=2),
        showlegend=False
    ))

# Ajouter des frames pour l'animation
frames = []
for i in range(nb_frames):
    positions = all_positions[i]
    directions = all_directions[i]
    arrow_ends = positions + directions * arrow_length
    
    frame_data = []
    
    # Mise à jour des positions des poissons (premier trace - les marqueurs)
    frame_data.append(
        go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2],
            mode='markers',
            marker=dict(
                size=5,
                color='blue',
                opacity=0.7
            )
        )
    )
    
    # Ajouter les lignes de direction pour chaque poisson
    for j in range(n):
        frame_data.append(
            go.Scatter3d(
                x=[positions[j, 0], arrow_ends[j, 0]],
                y=[positions[j, 1], arrow_ends[j, 1]],
                z=[positions[j, 2], arrow_ends[j, 2]],
                mode='lines',
                line=dict(color='blue', width=2)
            )
        )
    
    frames.append(go.Frame(data=frame_data, name=f'frame{i}'))

fig.frames = frames

# Ajouter un slider et des boutons de lecture
fig.update_layout(
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'buttons': [{
            'label': 'Play',
            'method': 'animate',
            'args': [None, {'frame': {'duration': 50, 'redraw': True}, 'fromcurrent': True}]
        }, {
            'label': 'Pause',
            'method': 'animate',
            'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}]
        }]
    }],
    sliders=[{
        'active': 0,
        'steps': [{'args': [[f'frame{i}'], 
                           {'frame': {'duration': 50, 'redraw': True}, 'mode': 'immediate'}],
                 'label': str(i),
                 'method': 'animate'} for i in range(nb_frames)]
    }]
)

# Afficher la figure interactive dans le navigateur
fig.show()

# En option: sauvegarder l'animation dans un fichier HTML
pio.write_html(fig, file='animation_poissons_3D.html', auto_open=True) 