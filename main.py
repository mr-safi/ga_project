from dic import *
import numpy as np
from htmlparser import Lexer

# lex = Lexer('<script src="/\%(jscript)s"></script>')
# lex.tokenise()
# toktype = lex.get_tokens_type()
# tokValue = lex.get_tokens_value()
# print(tokValue) 
# print(toktype)

# ..................................................
POPULATION_SIZE = 10
population = []
MAX_GENERATIONS = 100
MAX_FITTNESS = 1
array_payload_lexer_value =[]
array_payload_lexer_type =[]

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

    # ..............................create initial population (generation 0):
    for i in range(POPULATION_SIZE):
        p = gram.get_simple_payload()
        population.append(p)
        lx = Lexer(p)
        lx.tokenise()
        array_payload_lexer_type.append(lx.get_tokens_type())
        array_payload_lexer_value.append(lx.get_tokens_value())

    # test inital population 
    # print (*population,sep='\n')
    print(*array_payload_lexer_type , sep='\n')
    print(*array_payload_lexer_value , sep='\n')


    # fittness calc
    for fitscore in population:
        # print(fittness_calc(fitscore))#///...................... uncomment this
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
