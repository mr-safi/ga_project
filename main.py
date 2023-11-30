import random

from dic import *
import numpy as np
from htmlparser import Lexer
from individual import Individual
import matplotlib.pyplot as plt
import seaborn as sns

# lex = Lexer('<script src="/\%(jscript)s"></script>')
# lex.tokenise()
# toktype = lex.get_tokens_type()
# tokValue = lex.get_tokens_value()
# print(tokValue) 
# print(toktype)

# ..................................................
POPULATION_SIZE = 512
population = []
MAX_GENERATIONS = 256
MAX_FITTNESS = 1.0
maxFitnessValues = []
meanFitnessValues = []
OFFSPRING_POOL_SIZE=256

# fitnessValues = [individual.fitness.values[0] for individual in population]
fitnessValues = []


#  feedback from model
#  0  is benign payload 
#  except of model , multiple paramater must effecct to fittness
#  for example number of nested tag 
#  and number of attributes
#  xssCalssifer model: 0 is benign payload and 1 is xss
def fitness_calc(individual):

    payload = individual.get_payload()
    otherparam = individual.numtags + individual.numevent + individual.numxss
    modelFeedback = random.uniform(0.0 , 0.1)
    score = (1-modelFeedback)
    return score


def crossover(p1,p2):
    ghaleb =p2
    parent2=p1
    # if len(p1.elements) > len(p2.elements):
    #         ghaleb = p1
    #         parent2 = p2
    # else:
    #     ghaleb = p2
    #     parent2 = p1
    croossover_point = random.randint(2,3)
    child_Porder = parent2.puzzelorder[0:croossover_point]+ghaleb.puzzelorder[croossover_point:]
    child_elenmets = parent2.elements[0:croossover_point]+ghaleb.elements[croossover_point:]
    child = Individual(elment=child_elenmets , puzleorder=child_Porder)
    return child
    # print("----",child)

# Genetic Algorithm flow:
def ga_algo():
    gram = grammer()
    generationCounter = 0

    # ..............................create initial population (generation 0):
    for i in range(POPULATION_SIZE):
        p = gram.get_simple_payload()
        lx = Lexer(p)
        lx.tokenise()
        ind = Individual(elment=lx.get_tokens_value() , puzleorder=lx.get_tokens_type())
        population.append(ind)
 
    # test inital population 
    # print (*population,sep='\n')
    # ................................................


    # .....................................................fittness calc
    for ind in population:
        fitness = fitness_calc(ind)#///...................... uncomment this
        # print(fitness,ind.get_payload())
        ind.fitness = fitness
        #  is realy necessary this?yes
        fitnessValues.append(fitness)

    # print (*population,sep='\n')
    # ..............................................
    


    # =================.........============================.........=============================...main evolutionary loop:
    # stop if max fitness value reached the known max value
    # OR if number of generations exceeded the preset value:
    while generationCounter < MAX_GENERATIONS:
        maxFitness = max(fitnessValues)
        # meanFitness = sum(fitnessValues) / len(fitnessValues)
        # maxFitnessValues.append(maxFitness)
        # meanFitnessValues.append(meanFitness)

        if maxFitness >= MAX_FITTNESS:
            break

        # apply the selection operator, to select the next generation's individuals:
        #........select winners (8 offspring)
        #  sort by fittness
        population.sort(key=lambda x: x.fitness,reverse=True)
        newpopulation = population[:OFFSPRING_POOL_SIZE]
        population.clear()
        # fitnessValues.clear()


        #........ crossover
        # ... must set suitable cross point
        # ..positiopn 3 4 can be suitable
        parents = random.sample(newpopulation,OFFSPRING_POOL_SIZE)
        for i in range(0,len(parents)):
            if i == (len(parents)-1) :
                population.append(crossover(parents[i],parents[0]))
                break
            population.append(crossover(parents[i],parents[i+1]))
        
        parents.clear()
        for ind in population:
            fitness = fitness_calc(ind)#///...................... uncomment this
            ind.fitness = fitness
            fitnessValues.append(fitness)
            
        # .........mutation
          



        # notice: last way is encoding:(



        #.......calculate fitneess 
        # ......update population
        population.extend(newpopulation)
        print (*population,sep='\n')
        newpopulation.clear()

        generationCounter = generationCounter +1
        print("Generation {} : Max Fitness = {}".format(generationCounter, maxFitness))
    

    # print(len(fitnessValues))
    # sns.set_style("whitegrid")
    # plt.plot(maxFitnessValues, color='red')
    # plt.plot(meanFitnessValues, color='green')
    # plt.xlabel('Generation')
    # plt.ylabel('Max / Average Fitness')
    # plt.title('Max and Average Fitness over Generations')
    # plt.show()



# test
# print(tags)
if __name__ == '__main__':
    ga_algo()

# https://www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php#outline