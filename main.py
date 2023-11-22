from dic import *
import numpy as np
from htmlparser import Lexer

lex = Lexer('"><img src=https://www.google.com onerror="javascript:alert(1)" ><script> alert(1)</script>"')
lex.tokenise()
toktype = lex.get_tokens_type()
tokValue = lex.get_tokens_value()
print(tokValue)
print(toktype)

# ..................................................
POPULATION_SIZE = 200
population = []
MAX_GENERATIONS = 100
MAX_FITTNESS = 1

# fitnessValues = [individual.fitness.values[0] for individual in population]
fitnessValues = []

#  feedback from model
#  0  is benign payload 
#  except of model , multiple paramater must effecct to fittness
#  for example number of nested tag 
#  and number of attributes
def fittness_calc(payload):
    score = random.uniform(0 , 1)
    return score


# Genetic Algorithm flow:
def ga_algo():
    gram = grammer()
    generationCounter = 0

    # create initial population (generation 0):
    for i in range(POPULATION_SIZE):
        population.append(gram.get_simple_payload())
        # print(i)
    # print (population)

    # fittness calc
    for fitscore in population:
        # print(fittness_calc(fitscore))////////////...................... uncomment this
        fitnessValues.append(fittness_calc(fitscore))


    
    # main evolutionary loop:
    # stop if max fitness value reached the known max value
    # OR if number of generations exceeded the preset value:
    while max(fitnessValues) < MAX_FITTNESS and generationCounter < MAX_GENERATIONS:
        generationCounter = generationCounter +1
    # print(max(fitnessValues))





# test
# print(tags)
if __name__ == '__main__':
    ga_algo()
