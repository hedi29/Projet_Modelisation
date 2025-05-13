import matplotlib.pyplot as plt
import numpy as np
import random
import time
from poisson import Poisson # Assuming poisson.py is in the same directory

# Simulation Parameters
NOMBRE_POISSONS = 10
ZONE_LIMITE = 10  # The simulation area will be from -ZONE_LIMITE to +ZONE_LIMITE for x and y
DELTA_T = 0.1  # Time step
LIMITE_CONTAMINATION = 1.5  # Distance threshold for contamination
PROPAGATION_PERIOD = 5  # Contamination check every 5 iterations
TOTAL_STEPS = 500
SPEED_VARIATION_SCALE = 0.5 # Scale of random speed variation upon contamination
INITIAL_V_MIN = -1
INITIAL_V_MAX = 1

# Helper function for Euclidean distance in 2D
def distance_euclidienne(poisson1, poisson2):
    pos1 = poisson1.get_position()
    pos2 = poisson2.get_position()
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def run_simulation():
    # 1. Initialize fish
    banc_de_poissons = Poisson.creer_banc(NOMBRE_POISSONS, ZONE_LIMITE, INITIAL_V_MIN, INITIAL_V_MAX)

    # 2. Leader Selection and initial contamination
    if banc_de_poissons:
        leader = random.choice(banc_de_poissons)
        leader.contaminate(SPEED_VARIATION_SCALE) # Leader gets contaminated

    plt.ion() # Turn on interactive mode for matplotlib
    fig, ax = plt.subplots(figsize=(8, 8))

    for step in range(TOTAL_STEPS):
        # 3. Behavior Propagation (periodically)
        if step % PROPAGATION_PERIOD == 0:
            contamines_actuels = [p for p in banc_de_poissons if p.is_contaminated]
            if contamines_actuels: # Only propagate if there's someone contaminated
                for poisson_p in banc_de_poissons:
                    if not poisson_p.is_contaminated:
                        for poisson_c in contamines_actuels:
                            if distance_euclidienne(poisson_p, poisson_c) < LIMITE_CONTAMINATION:
                                poisson_p.contaminate(SPEED_VARIATION_SCALE)
                                break # Contaminated by the first one close enough

        # 4. Update fish positions and check boundaries
        for poisson in banc_de_poissons:
            poisson.move(DELTA_T)
            poisson.check_boundary(ZONE_LIMITE)

        # 5. Visualization
        ax.clear()
        for poisson in banc_de_poissons:
            ax.plot(poisson.x, poisson.y, 'o', color=poisson.color, markersize=5)
        
        ax.set_xlim(-ZONE_LIMITE -1, ZONE_LIMITE + 1)
        ax.set_ylim(-ZONE_LIMITE -1, ZONE_LIMITE + 1)
        ax.set_title(f"Étape: {step + 1}/{TOTAL_STEPS} - Contaminés: {sum(p.is_contaminated for p in banc_de_poissons)}")
        ax.set_xlabel("Position X")
        ax.set_ylabel("Position Y")
        ax.grid(True)
        
        plt.draw()
        plt.pause(0.01) # Pause to allow plot to update

    plt.ioff() # Turn off interactive mode
    plt.show() # Keep the final plot displayed

if __name__ == "__main__":
    run_simulation()
