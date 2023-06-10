import random
import scipy as sc
from stocastic_hc import SHC
from simulated_annealing import SA
import numpy as np
import visualize_tsp

def read_coords(path):
    coords = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = [float(x.replace("\n", "")) for x in line.split(" ")]
            coords.append(line)
    return coords


def generate_random_coords(num_nodes):
    return [[random.uniform(-1000, 1000), random.uniform(-1000, 1000)] for i in range(num_nodes)]

seeds = [
31, 76, 344, 359, 460, 662, 729, 741, 907, 967, 1035, 1091, 1113, 1315, 1318, 1412, 1529, 1826, 1839, 1925, 1969, 2249, 2267, 2324, 2470, 2506, 2650, 2701, 2833, 2847, 2875, 3129, 3144, 3145, 3179, 3186, 3272, 3392, 3609, 3980, 3987, 3992, 4048, 4102, 4257, 4485, 4557, 4911, 4926, 5027, 5190, 5263, 5311, 5589, 5607, 5678, 5728, 5793, 5816, 5881, 5892, 6047, 6094, 6248, 6581, 6592, 6684, 6769, 6845, 6952, 6974, 7061, 7131, 7351, 7359, 7365, 7543, 7546, 7727, 7751, 7902, 7913, 8025, 8076, 8830, 9026, 9133, 9194, 9235, 9256, 9270, 9284, 9373, 9423, 9715, 9755, 9777, 9791, 9951, 9972
]

if __name__ == "__main__":

    sa_fitness = []
    hc_fitness = []

    sa_solutions = []
    hc_solutions = []
    coords = []

    random.seed(1234)
    # usane 200
    coords = generate_random_coords(100)


    # prova vari parametri
    for seed in seeds[:50]:

        random.seed(seed)
        sa = SA(coords, stopping_iter=4000, alpha=0.995)
        sa.annealing()
        #sa.visualize_routes(algorithm="Simulated Annealing")
        #sa.plot_learning(algorithm="Simulated Annealing")

        random.seed(seed)
        hc = SHC(coords, stopping_iter=4000)
        hc.hill_climbing()
        #hc.visualize_routes(algorithm="Hill Climbing")
        #hc.plot_learning(algorithm="Hill Climbing")

        sa_fitness.append(sa.best_fitness)
        hc_fitness.append(hc.best_fitness)

        sa_solutions.append(sa.best_solution)
        hc_solutions.append(hc.best_solution)

    stats, p = sc.stats.mannwhitneyu(sa_fitness, hc_fitness, alternative='less')

    print("SA mean:", sc.stats.tmean(sa_fitness))
    print("SA std:", sc.stats.tstd(sa_fitness))

    print("HC mean:", sc.stats.tmean(hc_fitness))
    print("HC std:", sc.stats.tstd(hc_fitness))

    sa_best_sol = sa_solutions[np.argmin(sa_fitness)]
    hc_best_sol = hc_solutions[np.argmin(hc_fitness)]

    print("SA fitness min:", np.min(sa_fitness))
    print("HC fitness min:", np.min(hc_fitness))

    visualize_tsp.plotTSP([sa_best_sol], coords, "SA")
    visualize_tsp.plotTSP([hc_best_sol], coords, "HC")

    alpha = 0.05
    if p > alpha:
        print('Same distribution (fail to reject H0)')
    else:
        print('Different distribution (reject H0)')
