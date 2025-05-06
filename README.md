# Simulation de Poissons en Temps Réel

Ce projet permet de visualiser un groupe de poissons se déplaçant en temps réel dans un espace 2D.

## Prérequis

Pour exécuter cette simulation, vous aurez besoin de Python avec les bibliothèques suivantes :
- numpy
- matplotlib

Vous pouvez les installer avec la commande :
```
pip install numpy matplotlib
```

## Exécution

Pour lancer la simulation, exécutez simplement :
```
python main.py
```

## Fonctionnalités

- Visualisation en temps réel de 20 poissons
- Couleurs des poissons basées sur leur vitesse
- Flèches indiquant la direction de déplacement
- Rebond sur les bords de l'espace de simulation

## Structure du Projet

- `poisson.py` : Contient la classe Poisson qui définit le comportement d'un poisson
- `main.py` : Script principal pour la visualisation 