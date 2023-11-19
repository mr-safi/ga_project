from dic import *
import numpy as np


# ..................................................
POPULATION_SIZE = 200
population = []

#  feedback from mode
#  0  is benign payload 
#  except of modle , multuple paramater must effecct to fittness
def fittness_calc(payload):
    score = random.uniform(0 , 1)
    return score


# Genetic Algorithm flow:
def ga_algo():
    gram = grammer()

    # create initial population (generation 0):
    for i in range(POPULATION_SIZE):
        population.append(gram.get_simple_payload())
        # print(i)
    # print (population)

    # fittness calc
    for i in population:
        print(fittness_calc(i))

# test
# print(tags)
if __name__ == '__main__':
    ga_algo()

print(fittness_calc("s"))