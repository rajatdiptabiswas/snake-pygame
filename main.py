from geneetiline_algoritm import *
from Snake_Game import *
import matplotlib.pyplot as plt
import time

# n_x -> no. of input units
# n_h -> no. of units in hidden layer 1
# n_h2 -> no. of units in hidden layer 2
# n_y -> no. of output units

# hyperparameters
# The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
sol_per_pop = 25
generatsioonide_arv = 100
crossover_protsent = 0.2
mutatsiooni_intensiivsus = 0.05

datetimeCurr = str(time.strftime("%Y%m%d-%H%M%S"))

sigimis_vanemate_arv = (int)(crossover_protsent * sol_per_pop)  # has to be even
kaalude_arv = n_x * n_h + n_h * n_h2 + n_h2 * n_y
max_fitness = []

# Defining the population size.
pop_size = (sol_per_pop, kaalude_arv)
# Creating the initial population.
uus_populatsioon = np.random.choice(np.arange(-1, 1, step=0.01), size=pop_size, replace=True)


for generation in range(generatsioonide_arv):
    print('##############        GENERATSIOON ' + str(generation)+ '  ###############' )

    # Measuring the fitness of each chromosome in the population.
    fitness = arvuta_populatsiooni_fitness(uus_populatsioon)
    max_fitness.append(np.max(fitness))
    print('#######  parimal kromosoomil generatsioonis ' + str(generation) + ' on fitness väärtus:  ', np.max(fitness))

    # Selecting the best parents in the population for mating.
    vanemad = vali_sigimis_hulk(uus_populatsioon, fitness, sigimis_vanemate_arv)
    # Generating next generation using crossover.
    jarglaste_crossover = crossover(vanemad, jarglase_suurus=(pop_size[0] - vanemad.shape[0], kaalude_arv))
    # Adding some variations to the offsrping using mutation.
    jarglaste_mutatsioon = mutatsioon(jarglaste_crossover, mutatsiooni_intensiivsus)
    # Creating the new population based on the parents and offspring.
    uus_populatsioon[0:vanemad.shape[0], :] = vanemad
    uus_populatsioon[vanemad.shape[0]:, :] = jarglaste_mutatsioon

gen_count = list(range(1, generatsioonide_arv + 1))