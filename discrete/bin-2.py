
import random
import sys
import numpy
import math
import itertools
from functools import reduce
#Reasonable Defaults
CROSSOVERRATE=0.8               #Probability of each individual to mate
MUTATIONRATE=1                #Probability of each gene to be mutated
POPULATION_SIZE=100000



GENES_PER_INDIVIDUAL=20  #Warning, always must be divisible by 2
MAX_MUTATION_ATTEMPTS=3

WEIGHTS=[4, 8, 1, 4, 2, 1]
CAPACITY=10

RUN_TIMES_AVG=1

"""
    The initial state is the worst state possible, every item in seperate bin
"""
def createInitialIndividual():
    we=list(WEIGHTS)
    random.shuffle(we)
    mid=map(lambda x:[x,0],we)
    return [j for i in mid for j in i]
def createInitialPopulation(n):
    return [createInitialIndividual() for _ in range(n)]
"""
    The 0s are the separators between bins, so len(0's)==bins
"""
def fitIndividual(individual):
    return float(minimumBins())/len(filter(lambda x:x==0,individual))

"""
    Theoretical minimum of bins
"""
def minimumBins():
    return math.ceil(sum(WEIGHTS)/CAPACITY)
"""
    
"""
def sortByFitness(population):
    fit=map(lambda x:(float(fitIndividual(x)),x),population)
    best=sorted(fit,key=lambda x:x[0],reverse=True)
    return map(lambda x:x[1],best)

def validIndividual(individual):
    binsWeight=reduce(lambda a,b:(a[0]+[a[1]],0) if b==0 else (a[0],a[1]+b),individual,([],0))[0]
    overweightBins=sum(map(lambda x:0 if x<CAPACITY else 1,binsWeight))
    emptyBins=sum(map(lambda x:0 if x!=0 else 1,binsWeight))
    return len(binsWeight)>0 and individual[len(individual)-1]==0 and individual[0]!=0 and overweightBins==0 and emptyBins==0


def removeEmptyBinsOnce(individual):
    if(individual[0]==0):individual=individual[1:]
    return reduce(lambda a,b:a if b==0 and len(a)>0 and a[len(a)-1]==0 else a+[b],individual,[])


def containsEmptyBins(individual):
    binsWeight = reduce(lambda a, b: (a[0] + [a[1]], 0) if b == 0 else (a[0], a[1] + b), individual, ([], 0))[0]
    emptyBins = sum(map(lambda x: 1 if x == 0 else 0, binsWeight))
    return emptyBins!=0

def removeEmptyBins(individual):
    while containsEmptyBins(individual)==True:
        individual=removeEmptyBinsOnce(individual)
    return individual


def mutateIndividual(individual,maxTries=150):
    prob=random.random()
    assert validIndividual(individual)==True
    if(True):
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


def getBins(individual):
    def append(x, y):
        x.append(y)
        return x
    return reduce(lambda a, b: (append(a[0],a[1]), []) if b == 0 else (a[0],append(a[1],b)), individual, ([], []))[0]



def mutatePopulation(p):
    return [mutateIndividual(every) for every in p]
def survive(combined):
    sort=sortByFitness(combined)
    return sort[:POPULATION_SIZE]
def main(debug,present,runIndex,maxGen=50):
    print('complete code for a discrete optimization problem:')

    population=createInitialPopulation(POPULATION_SIZE)

    curr_generation=0
    found=False

    while not found and curr_generation<maxGen:
        #Evaluation
        so=sortByFitness(population)
        if(fitIndividual(so[0])==1): #if 1 then bins/min=1 and that mean bins=min. Perfect fit
            found=True
            if(present):
                presentResults(curr_generation,so[0])
            return curr_generation
        mutated=mutatePopulation(population)
        combined=mutated+population
        population=survive(combined)
        if (debug):
            print "[" + str(runIndex) + "]Generation " + str(curr_generation) + " Best With fit " + str(
                fitIndividual(so[0])) + " - " + str((getBins(so[0])))+" - "+str(so[0])
        curr_generation+=1

    return curr_generation



def presentResults(generations,optimal):
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