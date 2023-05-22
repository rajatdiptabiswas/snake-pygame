from jooksuta_mang import *
from random import choice, randint

def arvuta_populatsiooni_fitness(pop): # pop - populatsioon
    fitness = []
    for i in range(pop.shape[0]):
        fit = jooksuta_mang_AI(game_window, fps_controller, pop[i])
        print('Kromosoomi fitness väärtus ' + str(i) + ' :  ', fit)
        fitness.append(fit)
    return np.array(fitness)

def vali_sigimis_hulk(pop, fitness, arv_vanemaid):
    vanemad = np.empty((arv_vanemaid, pop.shape[1]))
    for vanema_nr in range(arv_vanemaid):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        vanemad[vanema_nr, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999
    return vanemad

def crossover(vanemad, jarglase_suurus):
    jarglased = np.empty(jarglase_suurus)

    for k in range(jarglase_suurus[0]):

        while True:
            parent1_idx = random.randint(0, vanemad.shape[0] - 1)
            parent2_idx = random.randint(0, vanemad.shape[0] - 1)
            # produce offspring from two parents if they are different
            if parent1_idx != parent2_idx:
                for j in range(jarglase_suurus[1]):
                    if random.uniform(0, 1) < 0.5:
                        jarglased[k, j] = vanemad[parent1_idx, j]
                    else:
                        jarglased[k, j] = vanemad[parent2_idx, j]
                break
    return jarglased

def mutatsioon(jarglaste_crossover, mutatsiooni_intensiivsus):
    for idx in range(jarglaste_crossover.shape[0]):
        for i in range(jarglaste_crossover.shape[1]):
            if random.uniform(0, 1) < mutatsiooni_intensiivsus:
                random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
                jarglaste_crossover[idx, i] = jarglaste_crossover[idx, i] + random_value
    return jarglaste_crossover