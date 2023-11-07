# https://github.com/cihatislamdede/genetic-algorithm-text-classification/blob/main/main.ipynb


def create_individual(word_count: int, vocab: list) -> list:
    """
    Creates an individual with a given word count and vocabulary.
    """
    individual = [[], []]
    for i in range(word_count // 2):
        individual[0].append(random.choice(vocab))
        individual[1].append(random.choice(vocab))
    return individual


def create_population(population_size: int, word_count: int, vocab: list) -> list:
    """
    Creates a population with a given size, word count, and vocabulary.
    """
    population = []
    for i in range(population_size):
        individual = create_individual(word_count, vocab)
        if individual not in population:
            population.append(individual)
    return population


def find_fitness(individual: list, first_label_words: pd.Series, second_label_words: pd.Series) -> int:
    """
    Finds the fitness of an individual.
    """
    fitness = 0
    for word in individual[0]:
        if word in first_label_words:
            fitness += first_label_words[word]
        if word in second_label_words:
            fitness -= second_label_words[word]
    for word in individual[1]:
        if word in second_label_words:
            fitness += second_label_words[word]
        if word in first_label_words:
            fitness -= first_label_words[word]
    return fitness


def find_population_fitness(
        population: list, first_label_words: pd.Series, second_label_words: pd.Series
) -> list:
    """
    Finds the fitness of each individual in a population.
    """
    population_fitness = []
    for individual in population:
        population_fitness.append(
            find_fitness(individual, first_label_words, second_label_words)
        )
    return population_fitness


def find_best(population: list, population_fitness: list) -> list:
    """
    Finds the best individual in a population.
    """
    best_index = population_fitness.index(max(population_fitness))
    return population[best_index]


def find_elites(population: list, population_fitness: list, elite_size: int) -> list:
    """
    Finds the elite individuals in a population.
    """
    elites = []
    for i in range(elite_size):
        best_index = population_fitness.index(max(population_fitness))
        elites.append(population[best_index])
        population_fitness[best_index]
    return elites


def crossover(parent1: list, parent2: list) -> list:
    """
    Creates a child from two parents.
    """
    child = [[], []]
    for i in range(len(parent1[0])):
        if random.random() > 0.5:
            child[0].append(parent1[0][i])
            child[1].append(parent2[1][i])
        else:
            child[0].append(parent2[0][i])
            child[1].append(parent1[1][i])
    return child


def mutate(individual: list, mutation_rate: float, vocab: list) -> list:
    """
    Mutates an individual.
    """
    for i in range(len(individual[0])):
        if random.random() < mutation_rate:
            individual[0][i] = random.choice(vocab)
        if random.random() < mutation_rate:
            individual[1][i] = random.choice(vocab)
    return individual


ef
check_if_unique(individual: list) -> bool:
"""
Checks if an individual is unique. Purpose is to avoid duplicates in a population.
"""
# Check if individual[0] and individual[1] is unique
if len(set(individual[0])) != len(individual[0]):
    return False
if len(set(individual[1])) != len(individual[1]):
    return False
return True


def evolve(
        population: list,
        population_fitness: list,
        elite_size: int,
        mutation_rate: float,
        vocab: list, ) -> list:
    """
    Evolves a population.
    """
    elites = find_elites(population, population_fitness, elite_size)
    next_generation = elites
    while len(next_generation) < len(population):
        parent1 = random.choice(next_generation)
        parent2 = random.choice(next_generation)
        child = crossover(parent1, parent2)
        child = mutate(child, mutation_rate, vocab)
        if child not in next_generation and check_if_unique(child):
            next_generation.append(child)
    return next_generation


def genetic_algorithm(
        population_size: int,
        elite_size: int,
        mutation_rate: float,
        generation_count: int,
        word_count: int,
        vocab: list,
        first_label_words: pd.Series,
        second_label_words: pd.Series, ) -> tuple:
    """
    Runs the genetic algorithm.
    """
    population = create_population(population_size, word_count, vocab)
    plot_data = {}
    for i in range(generation_count):
        population_fitness = find_population_fitness(
            population, first_label_words, second_label_words
        )
        population = evolve(
            population, population_fitness, elite_size, mutation_rate, vocab
        )
        plot_data[i] = {
            "max": max(population_fitness),
            "avg": sum(population_fitness) / len(population_fitness),
        }
    population_fitness = find_population_fitness(
        population, first_label_words, second_label_words
    )
    best = find_best(population, population_fitness)
    return best, population_fitness, plot_data