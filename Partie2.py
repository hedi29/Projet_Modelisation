import matplotlib.pyplot as plt
import numpy as np
import random
import time
from poisson import Poisson 

""" Partie 2 : Propagation des Mouvements - L'effet Trafalgar

Simulation d'un banc de poissons 2D avec propagation d'une contamination.

Un poisson contaminé peut transmettre la contamination aux autres poissons proches.
Chaque poisson est représenté par une position, une vitesse et un état de contamination.
La simulation est animée à l'aide de matplotlib.
"""
#---------------- Paramètres de simulation ---------------------
n = 20           
xmin, xmax = 0, 10 
ymin, ymax = 0, 10
dt = 0.1
distance_contamination = 1.5
periode_propagation = 5
nb_iter = 500
dV = 0.5 
Vmin = -1
Vmax = 1

#-----------------  Simulation -------------------------------
def run_simulation():
    # Initialisation du banc de poisson
    banc_de_poissons = Poisson.creer_banc(n, xmin, xmax, ymin, ymax, Vmin, Vmax)
    
    #Choix du leader
    if banc_de_poissons:
        leader = random.choice(banc_de_poissons)
        leader.contaminer(dV) 
        
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 10))

    for iter in range(nb_iter):
        if iter % periode_propagation == 0:
            contamines_actuels = [p for p in banc_de_poissons if p.is_contaminated]
            if contamines_actuels: 
                for poisson_p in banc_de_poissons:
                    if not poisson_p.is_contaminated:
                        for poisson_c in contamines_actuels:
                            if Poisson.distance_euclidienne(poisson_p, poisson_c) < distance_contamination:
                                poisson_p.contaminer(dV)
                                break 

        for poisson in banc_de_poissons:
            poisson.deplacer(dt)
            poisson.verifier_bords(xmin, xmax, ymin, ymax)

        ax.clear()
        for poisson in banc_de_poissons:
            ax.plot(poisson.x, poisson.y, 'o', color=poisson.color, markersize=5)
        
        ax.set_xlim(xmin - 1, xmax + 1)
        ax.set_ylim(ymin - 1 , ymax + 1)
        ax.set_title(f"Étape: {iter + 1}/{nb_iter} - Contaminés: {sum(p.is_contaminated for p in banc_de_poissons)}")
        ax.set_xlabel("Position X")
        ax.set_ylabel("Position Y")
        ax.grid(True)
        
        plt.draw()
        plt.pause(0.01)

    plt.ioff() 
    plt.show() 

if __name__ == "__main__":
    run_simulation()
