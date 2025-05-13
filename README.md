# Simulation de Poissons en Temps Réel

Ce projet permet de visualiser un groupe de poissons se déplaçant en temps réel dans un espace 2D, avec deux modes :  
- **Partie 1** : Mouvement aléatoire avec rebond sur les bords  
- **Partie 2** : Propagation d'une contamination entre poissons

## Prérequis

Pour exécuter cette simulation, vous aurez besoin de Python avec les bibliothèques suivantes :
- numpy
- matplotlib

Vous pouvez les installer avec la commande :
```
pip install numpy matplotlib
```

## Exécution

Pour lancer la **Partie 1** (mouvement aléatoire) :
```
python Partie1.py
```

Pour lancer la **Partie 2** (propagation de contamination) :
```
python Partie2.py
```

## Fonctionnalités

- Visualisation en temps réel de 20 poissons
- Couleurs des poissons basées sur leur vitesse (Partie 1) ou leur état de contamination (Partie 2)
- Flèches indiquant la direction de déplacement (Partie 1)
- Rebond sur les bords de l'espace de simulation
- Propagation d'une contamination entre poissons proches (Partie 2)

## Structure du Projet

- `poisson.py` : Contient la classe Poisson qui définit le comportement d'un poisson
- `Partie1.py` : Mouvement aléatoire des poissons
- `Partie2.py` : Propagation de la contamination dans le banc de poissons