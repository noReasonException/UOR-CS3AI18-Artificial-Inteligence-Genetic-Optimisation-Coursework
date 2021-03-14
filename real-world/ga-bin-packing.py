
import random
import sys
import numpy
import math
import itertools
from functools import reduce
import statistics
#Reasonable Defaults
MUTATIONRATE=0.2                #Probability of each gene to be mutated
POPULATION_SIZE=10

MAX_MUTATION_ATTEMPTS=3

WEIGHTS=[4, 8, 1, 4, 2, 1]
CAPACITY=10

RUN_TIMES_AVG=5

"""
    The initial state is the worst state possible, every item in seperate bin
"""
def createInitialIndividual():
    we=list(WEIGHTS)
    random.shuffle(we)
    mid=map(lambda x:[x,0],we)
    return [j for i in mid for j in i]
"""
    The initial state is the worst state possible, every item in seperate bin
"""
def createInitialPopulation(n):
    return [createInitialIndividual() for _ in range(n)]
"""
    gives a greater fitness score in case a solution has a completely full bin
"""
def priotityIfCompletedBin(individual):
    PRIORITY_OFFSET=0.5
    return len(filter(lambda x:x==CAPACITY,binsSum(individual)))*PRIORITY_OFFSET

"""
    The 0s are the separators between bins, so len(0's)==bins
    gives a priority score in case a solution has a full bin
"""
def fitByBinsUsed(individual):
    return float(minimumBins())/len(filter(lambda x:x==0,individual)) + priotityIfCompletedBin(individual)

"""
    Return the number of full bins in an individual
"""
def getCompletedBins(individual):
    return len(filter(lambda x: x == CAPACITY, binsSum(individual)))

"""
    Theoretical minimum of bins
"""
def minimumBins():
    return math.ceil(sum(WEIGHTS)/CAPACITY)
"""
    Sorts by fitness, uses the fitByBinsUsed criterion defined above
"""
def sortByFitness(population):
    fit=map(lambda x:(float(fitByBinsUsed(x)), x), population)
    best=sorted(fit,key=lambda x:x[0],reverse=True)
    return map(lambda x:x[1],best)
"""
    Validates a mutation as valid or not
"""
def validIndividual(individual):
    binsWeight=reduce(lambda a,b:(a[0]+[a[1]],0) if b==0 else (a[0],a[1]+b),individual,([],0))[0]
    overweightBins=sum(map(lambda x:0 if x<=CAPACITY else 1,binsWeight))
    emptyBins=sum(map(lambda x:0 if x!=0 else 1,binsWeight))
    return len(binsWeight)>0 and individual[len(individual)-1]==0 and individual[0]!=0 and overweightBins==0 and emptyBins==0

"""
    Returns True if the given individual contains empty bins
"""
def containsEmptyBins(individual):
    binsWeight = reduce(lambda a, b: (a[0] + [a[1]], 0) if b == 0 else (a[0], a[1] + b), individual, ([], 0))[0]
    emptyBins = sum(map(lambda x: 1 if x == 0 else 0, binsWeight))
    return emptyBins!=0
"""
    Removes the empty bins from the given individual
"""
def removeEmptyBins(individual):
    def removeEmptyBinsOnce(individual):
        if (individual[0] == 0): individual = individual[1:]
        return reduce(lambda a, b: a if b == 0 and len(a) > 0 and a[len(a) - 1] == 0 else a + [b], individual, [])
    while containsEmptyBins(individual)==True:
        individual=removeEmptyBinsOnce(individual)
    return individual

"""
    Returns a list with the sum of the weights inside each bin.
"""
def binsSum(individual):
    bins=map(lambda x:sum(x),getBins(individual))
    return bins
"""
    Mutates a given individual by swapping random genes, and then validating if the swap was a valid move, up to 150 times(modifiable).
"""
def mutateIndividual(individual,maxTries=150):
    prob=random.random()
    assert validIndividual(individual)==True
    if(prob<=MUTATIONRATE):
        while maxTries>0:
            mutated=list(individual)
            a=random.randint(0,len(mutated)-1)
            b=random.randint(0,len(mutated)-1)
            alem=mutated[a]
            belem=mutated[b]
            mutated[a]=belem
            mutated[b]=alem
            maxTries-=1
            mutated=removeEmptyBins(mutated)
            assert containsEmptyBins(mutated)==False
            if(validIndividual(mutated)):
                return mutated
    assert validIndividual(individual) == True
    return individual
"""
    Mutates given population
"""
def mutatePopulation(p):
    return [mutateIndividual(every) for every in p]
"""
    Returns a list of lists, each list representing the contents of each bin
"""
def getBins(individual):
    def append(x, y):
        x.append(y)
        return x
    return reduce(lambda a, b: (append(a[0],a[1]), []) if b == 0 else (a[0],append(a[1],b)), individual, ([], []))[0]

"""
    Returns the best POPULATION_SIZE individuals
"""
def survive(combined):
    sort=sortByFitness(combined)
    return sort[:POPULATION_SIZE]

def main(debug,present,runIndex,maxGen=2500):
    print('complete code for a discrete optimization problem:')

    population=createInitialPopulation(POPULATION_SIZE)

    curr_generation=0
    found=False

    while not found and curr_generation<maxGen:
        #Evaluation
        so=sortByFitness(population)
        if(getCompletedBins(so[0])==minimumBins()): #if 1 then bins/min=1 and that mean bins=min. Perfect fit
            found=True
            if(present):
                presentResults("Optimal: ",curr_generation,so[0])
            return curr_generation
        mutated=mutatePopulation(population)
        combined=mutated+population
        population=survive(combined)
        if (debug):
            print "[" + str(runIndex) + "]Generation " + str(curr_generation) + " Best With fit " + str(
                fitByBinsUsed(so[0])) + " - " + str((getBins(so[0])))
        curr_generation+=1
    if (present):
        presentResults("Best found: ", curr_generation, so[0])
    return curr_generation



def presentResults(typeof,generations,optimal):
    print typeof\
          +str(getBins(optimal))+\
          " after "\
          +str(generations)+\
          " Generations"\
          +" with MR="\
          +str(MUTATIONRATE)\
          +", POPULATION="\
          +str(POPULATION_SIZE)\
          +", CAPACITY="\
          +str(CAPACITY)\
          +", WEIGHTS="\
          +str(WEIGHTS)

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
    if ("-po" in sys.argv):
        POPULATION_SIZE = int(sys.argv[sys.argv.index("-po") + 1])
        assert POPULATION_SIZE>=10 ,"Population size cannot be < 10"
    if("-dim" in sys.argv):
        GENES_PER_INDIVIDUAL=int(sys.argv[sys.argv.index("-dim") + 1])
    if ("-rt" in sys.argv):
        RUN_TIMES_AVG = int(sys.argv[sys.argv.index("-rt") + 1])
        assert RUN_TIMES_AVG>0
    if ("-bc" in sys.argv):
        CAPACITY = int(sys.argv[sys.argv.index("-bc") + 1])
        assert RUN_TIMES_AVG>0
    if ("-we" in sys.argv):
        WEIGHTS = list(map(lambda x:int(x),sys.argv[sys.argv.index("-we") + 1].split(",")))
        assert RUN_TIMES_AVG>0


    print "AVG("+str(RUN_TIMES_AVG)+")="+str(sum([main(debug,present,i) for i in range(RUN_TIMES_AVG)])/RUN_TIMES_AVG)