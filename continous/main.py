
import random
import sys
import numpy
#Reasonable Defaults
CROSSOVERRATE=0.8               #Probability of each individual to mate
MUTATIONRATE=0.2                #Probability of each gene to be mutated
POPULATION_SIZE=1000
LB=0
UB=10
GENES_PER_INDIVIDUAL=4  #Warning, always must be divisible by 2
MUTATION_STEP_RANGE=1
RUN_TIMES_AVG=10
#List of supported functions
import math
functions=[
    ("mse","Mean Square Error",lambda X: sum([(i + 1) * pow(X[i], 2) for i in range(len(X))])),
    ("sph","Sphere",lambda X: sum([pow(X[i], 2) for i in range(len(X))])),
    ("lin","Linear",lambda X: sum(X[i] for i in range(len(X)))),
    ("sin","Sinusoidal",lambda X: sum(math.sin(X[i]) for i in range(len(X)))),
    ("abs","Absolute",lambda X: sum(abs(X[i]) for i in range(len(X)))),
    ("ras","Rastrigin function",lambda X: len(X)*10+sum(pow(X[i],2)-10*math.cos(2*math.pi*X[i]) for i in range(len(X))))
]


"""
    Creates a list with GENES_PER_INDIVIDUAL numbers on range [LB,UB]
    This is called an 'Individual'
"""
def createIndividual(lb,ub,n):
    return [random.randint(lb,ub) for _ in range(n)]
"""
    Creates a list with Individuals
    this is called a 'Population'
"""
def createPopulation(populationSize,lb,ub,n):
    return [createIndividual(lb,ub,n) for _ in range(populationSize)]
"""
    How well the Individual fits within the given function?
    We just apply the vector to the function defined
    This produces a score, we use this score to calculate the relative fitness and determine selection"""
def fitIndividual(individual,fun):
    return fun(individual)


"""
    Mutates a given gene with a probability determined by its second parameter, with a standard normal distribution
"""
def mutateGeneStandardNormal(gene, mutationRate):
    prob=random.random()
    if(prob<=mutationRate):
        gene+=numpy.random.normal()#(-MUTATION_STEP_RANGE,MUTATION_STEP_RANGE)
    return max(min(gene,UB),LB)
"""
    Mutates a given gene with a probability determined by its second parameter, with a uniform distribution, this
    is expected to worsen the algorithms performance for very simple functions
"""
def mutateGeneUniform(gene, mutationRate):
    prob=random.random()
    if(prob<=mutationRate):
        gene+=random.uniform(-MUTATION_STEP_RANGE,MUTATION_STEP_RANGE)
    return max(min(gene,UB),LB)
"""
    Mutates all the genes(the numbers) of an individual (list of numbers) with a given mutationRate
"""
def mutateIndividual(individual,mutationRate):
    return [round(mutateGeneUniform(gene, mutationRate), 3) for gene in individual]

"""
    Applies the mutation to the whole population, returning the combined 2N population(parents and children)
"""
def mutatePopulaton(population,mutationRate):
    return [mutateIndividual(individual,mutationRate) for individual in population]
"""
    Sorts the given population by the fitness, and chooses the N best of them 
"""
def survive(population,fun):
    sortedPopulation = map(
        lambda x: x[1],                         #Discard the fitness percentage, we only want the individuals
        sortByFitness(population,fun)
    )
    return sortedPopulation[:POPULATION_SIZE]   #Survive the N Best individuals
"""
    Returns a pair of (FITNESS_PERCENTAGE,INDIVIDUAL_VECTOR) sorted by the first key
"""
def sortByFitness(population,fun):
    fitness = [(fitIndividual(i, fun), i) for i in population]      # Fitness,individual pair
    fitSum = sum(map(lambda x: abs(x[0]), fitness))                      # Fitness sum
    fitness = map(lambda x: (1 - abs(x[0]) / fitSum, x[1]), fitness)     # Reversed Percentage
    revSum = sum(map(lambda x: abs(x[0]), fitness))                      # Reversed Percentage sum(to be normalized)
    fitness = map(lambda x: (abs(x[0] / revSum), x[1]), fitness)         # Normalized Reversed Percentage
    best = sorted(fitness, key=lambda x: x[0], reverse=True)        # Sort most fitted first

    return best


"""
    Performs Wheel Selection with balance probability, this will exclude some individuals with high fitness score to allow 
    non-so-good ones to reproduce. This mechanism will help the algorithm to avoid stucking in local minima for too long
"""
def balancedSelect(population, fun):
    """
        Takes a list of pairs (FITNESS_PERCENTAGE,INDIVIDUAL_VECTOR) and returns
                                        (FITNESS_PERCENTAGE_SO_FAR,INDIVIDUAL_VECTOR)
        for example
            [(0.5,[...]),(0.2,[...]),(0.3,[...])] -> [(0.5,[...]),(0.7,[...]),(1.0,[...])]
    """
    def _densityFitnessList(populationDensityPair):
        acc = 0
        for i in range(len(populationDensityPair)):
            acc += populationDensityPair[i][0]
            populationDensityPair[i] = (acc, populationDensityPair[i][1])
        return populationDensityPair

    """
        Takes a list of pairs (FITNESS_PERCENTAGE_SO_FAR,INDIVIDUAL_VECTOR) and returns
                                        (FITNESS_PERCENTAGE_SO_FAR,INDIVIDUALS_CROSSOVER_RATE,INDIVIDUAL_VECTOR)
    """
    def _individualCrossoverProbabilityList(populationDensityPair):
        return map(lambda x:(x[0],random.uniform(0,1),x[1]),populationDensityPair)
    sortedPopulation=sortByFitness(population,fun)                                                          #Sorted population-fitness pairs
    sortedPopulationWithDensities=_densityFitnessList(sortedPopulation)                                     #fitness part now has the density up to this point (PDF)
    sortedWithDensitiesAndCrossovers=_individualCrossoverProbabilityList(sortedPopulationWithDensities)     #now we have the individual crossover rates as well
    selectedToReproduce=map(                                                                                #Selected individuals to reproduce
        lambda x:x[2],
        filter(lambda x:x[1]<CROSSOVERRATE,sortedWithDensitiesAndCrossovers))
    return selectedToReproduce
"""
    Performs Wheel Selection without balanced probability, this will just perform wheel selection based on fitness score
    This is expected to undermine the algorithms performance
    NOTESTED
"""
def elitisticSelect(population, fun):
    """
        Takes a list of pairs (FITNESS_PERCENTAGE,INDIVIDUAL_VECTOR) and returns
                                        (FITNESS_PERCENTAGE_SO_FAR,INDIVIDUAL_VECTOR)
        for example
            [(0.5,[...]),(0.2,[...]),(0.3,[...])] -> [(0.5,[...]),(0.7,[...]),(1.0,[...])]
    """
    def _densityFitnessList(populationDensityPair):
        acc = 0
        for i in range(len(populationDensityPair)):
            acc += populationDensityPair[i][0]
            populationDensityPair[i] = (acc, populationDensityPair[i][1])
        return populationDensityPair

    sortedPopulation=sortByFitness(population,fun)                                                          #Sorted population-fitness pairs
    sortedPopulationWithDensities=_densityFitnessList(sortedPopulation)                                     #fitness part now has the density up to this point (PDF)
    selectedToReproduce=map(                                                                                #Selected individuals to reproduce
        lambda x:x[1],
        filter(lambda x:x[0]<CROSSOVERRATE,sortedPopulationWithDensities))
    return selectedToReproduce
"""
    Performs mating on selected parents
"""
def crossover(selectedParents):



    def _mate(male,female):
        assert GENES_PER_INDIVIDUAL%2==0
        return [male[:len(male)]+female[len(female):],male[len(male):]+female[:len(female)]]


    if(len(selectedParents)%2!=0):selectedParents=selectedParents[:len(selectedParents)-1]          #Someone will get lonely, everyone must have pair
    random.shuffle(selectedParents)                                                                 #Shuffling avoids the best to be mated always with the best
    males = selectedParents[:int(len(selectedParents)/2)]                                           #Arbitary split half of them as males
    females = selectedParents[int(len(selectedParents)/2):]                                         #And half of them as females
    children=[]

    for male,female in zip(males,females):
        children.extend(_mate(male,female))

    return children

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
          +", UB="\
          +str(UB)\
          +", LB="\
          +str(LB)\
          +", Function="\
          +str(functionDescriptor[0])\
          +", N="\
          +str(GENES_PER_INDIVIDUAL)\


def main(debug,present,functionDescriptor,runIndex,maxGen=250000):
    #print('complete code for a continuous optimization problem:')
    population= createPopulation(POPULATION_SIZE,LB,UB,GENES_PER_INDIVIDUAL)
    curr_generation=0
    found=False
    while not found and curr_generation<maxGen:
        #Evaluation
        so=sorted(population)
        if(fitIndividual(so[0],functionDescriptor[2])==0):
            found=True
            if(present):
                presentResults(curr_generation,so[0],functionDescriptor)
            return curr_generation
        #Select
        selected=elitisticSelect(population, functionDescriptor[2])
        #Crossover
        children=crossover(selected)
        #Mutate
        mutatedPopulation = mutatePopulaton(children, MUTATIONRATE)
        #Survive
        population=survive(mutatedPopulation+population,functionDescriptor[2])
        curr_generation+=1
        if(debug):
            print "[" + str(runIndex) + "]Generation " + str(curr_generation) + " Best With fit " + str(fitIndividual(so[0], functionDescriptor[2])) + " - " + str(so[0])
    return curr_generation


if __name__ == '__main__':
    debug=False
    present=False
    functionDescriptor=functions[0] #Default is Mean Square Error
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
        assert POPULATION_SIZE>0 ,"Population size cannot be <= 0"
    if ("-ub" in sys.argv):
        UB = int(sys.argv[sys.argv.index("-ub") + 1])
    if ("-lb" in sys.argv):
        LB = int(sys.argv[sys.argv.index("-lb") + 1])
    if("-fn" in sys.argv):
        choice=filter(lambda x:x[0]==sys.argv[sys.argv.index("-fn")+1],functions)
        assert len(choice)==1, "No support for this type of function"
        functionDescriptor=choice[0]
    if("-dim" in sys.argv):
        GENES_PER_INDIVIDUAL=int(sys.argv[sys.argv.index("-dim") + 1])
    if ("-rt" in sys.argv):
        RUN_TIMES_AVG = int(sys.argv[sys.argv.index("-rt") + 1])
        assert RUN_TIMES_AVG>0



    assert LB<UB ,"Lower bound cant be bigger that upper bound"


    print "AVG("+str(RUN_TIMES_AVG)+")="+str(sum([main(debug,present,functionDescriptor,i) for i in range(RUN_TIMES_AVG)])/RUN_TIMES_AVG)


"""
if __name__ == '__main__':
#if(False):
    debug=False
    present=False
    functionDescriptor=functions[-1] #Default is sph
    UB = 5
    LB = -5



    MR=[0.2,0.4,0.6,0.8]
    CR=[0.2,0.4,0.6,0.8]
    POP=[10,20,30,40,50,60,70,80,90,100]
    import itertools
    for i in  itertools.product(MR,CR,POP):
        MUTATIONRATE=i[0]
        CROSSOVERRATE=i[1]
        POPULATION_SIZE=i[2]
        print "MR="+str(MUTATIONRATE)+" "\
                "CR="+str(CROSSOVERRATE)+" "\
                "POP="+str(POPULATION_SIZE)+" "\
                "AVG="+str(sum([main(debug,present,functionDescriptor,i) for i in range(10)])/10)
"""