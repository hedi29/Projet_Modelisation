# Simulation de Banc de Poissons en Temps Réel

Ce projet permet de visualiser un groupe de poissons se déplaçant en temps réel dans un espace 2D, avec trois modes de simulation :  
- **Partie 1** : Mouvement aléatoire avec rebond sur les bords  
- **Partie 2** : Propagation d'une contamination entre poissons
- **Partie 3** : Règles comportementales d'Aoki (répulsion, alignement, attraction)

## Prérequis

Pour exécuter cette simulation, vous aurez besoin de Python avec les bibliothèques suivantes :
- numpy
- matplotlib
- scipy

Vous pouvez les installer avec la commande :
```
pip install numpy matplotlib scipy
```

## Exécution

Pour lancer la **Partie 1** (mouvement aléatoire) :
```
python Partie1.py
```

Pour lancer la **Partie 2** (propagation de contamination) :
```
python Partie2.py
```

Pour lancer la **Partie 3** (règles d'Aoki) :
```
python Partie3.py
```

## Fonctionnalités

### Partie 1 : Mouvement Aléatoire
- Visualisation en temps réel de 20 poissons
- Couleurs des poissons basées sur leur vitesse
- Flèches indiquant la direction de déplacement
- Rebond sur les bords de l'espace de simulation

### Partie 2 : Propagation de Contamination
- Sélection d'un poisson "leader" qui transmet son comportement
- Propagation de la contamination entre poissons proches
- Visualisation par couleur de l'état de contamination
- Modification de la vitesse des poissons contaminés

### Partie 3 : Règles d'Aoki
- Simulation avec 50 poissons pour observer les comportements collectifs
- Visualisation des trois règles comportementales d'Aoki :
  - **Répulsion** (zone rouge) : les poissons trop proches s'éloignent les uns des autres
  - **Alignement** (zone verte) : les poissons à distance moyenne s'alignent dans la même direction
  - **Attraction** (zone bleue) : les poissons éloignés sont attirés vers le groupe

## Structure du Projet

- `poisson.py` : Contient la classe Poisson qui définit le comportement individuel et collectif des poissons
- `Partie1.py` : Mouvement aléatoire des poissons
- `Partie2.py` : Propagation de la contamination dans le banc de poissons
- `Partie3.py` : Simulation avec les règles comportementales d'Aoki

## Paramètres Ajustables (Partie 3)

Dans la **Partie 3**, vous pouvez ajuster plusieurs paramètres pour modifier le comportement du banc :

- **Nombre de poissons** : variable `n`
- **Rayons des zones** : variables `rayon_repulsion`, `rayon_alignement`, `rayon_attraction`
- **Coefficients de force** : variables `k_repulsion`, `k_alignement`, `k_attraction`
- **Vitesse maximale** : variable `vitesse_max`

Ces paramètres peuvent être modifiés directement dans le code pour observer différents comportements collectifs.
