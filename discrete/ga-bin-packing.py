
import random
import sys
import numpy
import math
import itertools

#Reasonable Defaults
CROSSOVERRATE=0.8               #Probability of each individual to mate
MUTATIONRATE=0.2                #Probability of each gene to be mutated
POPULATION_SIZE=10



GENES_PER_INDIVIDUAL=20  #Warning, always must be divisible by 2


RUN_TIMES_AVG=1

class Bin:
    def __init__(self,capacity):
        self.contains=[]
        self.capacity=capacity
    def addItem(self,item):
        self.contains.append(item)
        return self
    def isValid(self):
        return sum(self.contains)<=self.capacity
    def __str__(self):
        return "Bin(capacity="+str(self.capacity)+","+str(self.contains)+")"

"""
    The initial state is the worst state possible, every item in seperate bin
"""
def createInitialIndividual(binCapacity,weights):
    assert sum([0 if everyItem<binCapacity else 1 for everyItem in weights])==0,"Assume Every item is smaller than the bin capacity"
    return map(lambda everyItem:Bin(binCapacity).addItem(everyItem),weights)
"""
    Creates the worst possible initial population
"""
def createInitialPopulation(n,binCapacity,weights):
    return [createInitialIndividual(binCapacity,weights) for _ in range(n)]

"""
The following two functions are utills for debugging
"""
def individualStr(individual):
    return [str(everyGene) for everyGene in individual]
def populationStr(population):
    return [individualStr(individual) for individual in population]


def main(debug,present,runIndex,maxGen=250000):
    print('complete code for a discrete optimization problem:')



    a=createInitialPopulation(2,10,[4,8,1,4,2,1])
    print populationStr(a)
    return 0

    """
    population= createPopulation(POPULATION_SIZE,functionDescriptor)
    curr_generation=0
    found=False
    while not found and curr_generation<maxGen:
        #Evaluation
        so=map(lambda x:x[1],sortByFitness(population,functionDescriptor))
        if(fitIndividualToTarget(so[0],functionDescriptor)==0): #Perfect fit
            found=True
            if(present):
                presentResults(curr_generation,so[0],functionDescriptor)
            return curr_generation
        #Select
        selected = elitisticSelect(population, functionDescriptor)
        #Mate
        children=crossover(selected)
        #Mutate
        mutatedPopulation = mutatePopulaton(children, MUTATIONRATE,functionDescriptor)
        #Survive
        combined=mutatedPopulation+population
        population=survive(combined,functionDescriptor)
        curr_generation+=1
        if (debug):
            print "[" + str(runIndex) + "]Generation " + str(curr_generation) + " Best With fit " + str(fitIndividualToTarget(so[0],functionDescriptor)) + " - " + str(so[0])
    return curr_generation
    """


def presentResults(generations,optimal,functionDescriptor):
    print "Optimal:"\
          +str(optimal)+\
          " after "\
          +str(generations)+\
          " Generations"\
          +" with MR="\
          +str(MUTATIONRATE)\
          +", CR="\
          +str(CROSSOVERRATE)\
          +", POPULATION="\
          +str(POPULATION_SIZE)\
          +", Function="\
          +str(functionDescriptor[0])\
          +", N="\
          +str(GENES_PER_INDIVIDUAL)\

if __name__ == '__main__':
    debug=False
    present=False
    if("-d" in sys.argv):
        debug=True
    if("-r" in sys.argv):
        present=True
    if("-mr" in sys.argv):
        MUTATIONRATE=float(sys.argv[sys.argv.index("-mr")+1])
        assert 0<=MUTATIONRATE<=1,"Probability of crossover cannot be outsize of bounds [0(0% crossover) - 1(100% crossover)]"
    if ("-cr" in sys.argv):
        CROSSOVERRATE = float(sys.argv[sys.argv.index("-cr") + 1])
        assert 0 <= CROSSOVERRATE <= 1,"Probability of crossover cannot be outsize of bounds [0(0% crossover) - 1(100% crossover)]"
    if ("-po" in sys.argv):
        POPULATION_SIZE = int(sys.argv[sys.argv.index("-po") + 1])
        assert POPULATION_SIZE>=10 ,"Population size cannot be < 10"
    if("-dim" in sys.argv):
        GENES_PER_INDIVIDUAL=int(sys.argv[sys.argv.index("-dim") + 1])
    if ("-rt" in sys.argv):
        RUN_TIMES_AVG = int(sys.argv[sys.argv.index("-rt") + 1])
        assert RUN_TIMES_AVG>0


    print "AVG("+str(RUN_TIMES_AVG)+")="+str(sum([main(debug,present,i) for i in range(RUN_TIMES_AVG)])/RUN_TIMES_AVG)