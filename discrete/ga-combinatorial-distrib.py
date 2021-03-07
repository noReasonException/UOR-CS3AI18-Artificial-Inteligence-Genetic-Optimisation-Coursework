
import random
import sys
import numpy
#Reasonable Defaults
CROSSOVERRATE=0.8               #Probability of each individual to mate
MUTATIONRATE=0.2                #Probability of each gene to be mutated
POPULATION_SIZE=100



GENES_PER_INDIVIDUAL=4  #Warning, always must be divisible by 2


RUN_TIMES_AVG=1
#Supported functions
functions=[
    ("sum1min","Sum of ones",[0,1],lambda X: len(filter(lambda i:i==1,X)),lambda n:[0]*n),
    ("sum1max", "Sum of ones", [0, 1], lambda X: len(filter(lambda i: i == 1, X)), lambda n: [1] * n)
]
#Positions on supported functions
FCODE=0
FDESCRIPTOR=1
FSYMBOLS=2
FFUNCTION=3
FGENERATETARGET=4


"""
    Creates a list with n numbers using the symbol list of the choosen function
    This is called an 'Individual'
"""
def createIndividual(symbols):
    return [symbols[random.randint(0,len(symbols)-1)] for _ in range(GENES_PER_INDIVIDUAL)]
"""
    Creates a list with Individuals
    this is called a 'Population'
"""
def createPopulation(populationSize,functionDescriptor):
    return [createIndividual(functionDescriptor[FSYMBOLS]) for _ in range(populationSize)]
"""
    How well the Individual fits within the given function?
    
    This produces a score, we use this score to calculate the relative fitness and determine selection
"""


def fitIndividual(individual,functionDescriptor):
    target=functionDescriptor[FGENERATETARGET](GENES_PER_INDIVIDUAL)
    score=sum(map(lambda x:1 if x[0]==x[1] else 0 ,zip(target,individual)))
    return score

def diffsFromTarget(individual,functionDescriptor):
    target=functionDescriptor[FGENERATETARGET](GENES_PER_INDIVIDUAL)
    score=sum(map(lambda x:1 if x[0]!=x[1] else 0 ,zip(target,individual)))
    return score

def sortByFitness(population,functionDescriptor):
    fitness = [(fitIndividual(i,functionDescriptor), i) for i in population]        #Fitness,individual pair
    fitMax = sum(map(lambda x: abs(x[0]), fitness))                                 #Fitness max score
    fitness = map(lambda x: (abs(x[0]) / float(fitMax), x[1]), fitness)             #Percentage based on max score
    best = sorted(fitness, key=lambda x: x[0], reverse=True)                        #Sort for max or min
    return best
def sortByDiffsFromTarget(population,functionDescriptor):
    fitness = [(diffsFromTarget(i,functionDescriptor), i) for i in population]          #Fitness,individual pair
    best = sorted(fitness, key=lambda x: x[0])                            #Sort for max or min
    return best
"""
    Mutates a given gene with a probability determined by its second parameter, picking a random symbol from the pre-defined 
    symbol list
"""
def mutateGeneRandom(gene, mutationRate,functionDescriptor):
    prob=random.random()
    choosen=random.randint(0,len(functionDescriptor[FSYMBOLS])-1)
    if(prob<=mutationRate):
        return choosen
    return gene
"""
    Mutates all the genes(the numbers) of an individual (list of numbers) with a given mutationRate
"""
def mutateIndividual(individual,mutationRate,functionDescriptor):
    return [mutateGeneRandom(gene, mutationRate,functionDescriptor) for gene in individual]

"""
    Applies the mutation to the whole population, returning the combined 2N population(parents and children)
"""
def mutatePopulaton(population,mutationRate,functioDescriptor):
    return [mutateIndividual(individual,mutationRate,functionDescriptor) for individual in population]
"""
    Sorts the given population by the fitness, and chooses the N best of them 
"""
def survive(population,functionDescriptor):
    sortedPopulation = map(
        lambda x: x[1],                         #Discard the fitness percentage, we only want the individuals
        sortByDiffsFromTarget(population,functionDescriptor)
    )
    return sortedPopulation[:POPULATION_SIZE]   #Survive the N Best individuals


"""
    Performs Wheel Selection without balanced probability, this will just perform wheel selection based on fitness score
    This is expected to undermine the algorithms performance

"""
def elitisticSelect(population, functionDescriptor):
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

    sortedPopulation = sortByFitness(population, functionDescriptor)  # Sorted population-fitness pairs
    sortedPopulationWithDensities = _densityFitnessList(
        sortedPopulation)  # fitness part now has the density up to this point (PDF)
    selectedToReproduce = map(  # Selected individuals to reproduce
        lambda x: x[1],
        filter(lambda x: x[0] < CROSSOVERRATE, sortedPopulationWithDensities))
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
    assert len(children)!=0
    return children
def main(debug,present,functionDescriptor,runIndex,maxGen=250000):
    print('complete code for a discrete optimization problem:')


    population= createPopulation(POPULATION_SIZE,functionDescriptor)
    curr_generation=0
    found=False



    while not found and curr_generation<maxGen:
        #Evaluation
        so=map(lambda x:x[1],sortByFitness(population,functionDescriptor))
        if(diffsFromTarget(so[0],functionDescriptor)==0): #Perfect fit
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
            print "[" + str(runIndex) + "]Generation " + str(curr_generation) + " Best With fit " + str(diffsFromTarget(so[0],functionDescriptor)) + " - " + str(so[0])
    return curr_generation

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
    functionDescriptor=functions[0] #Default is sum of ones
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

    if("-fn" in sys.argv):
        choice=filter(lambda x:x[0]==sys.argv[sys.argv.index("-fn")+1],functions)
        assert len(choice)==1, "No support for this type of function"
        functionDescriptor=choice[0]
    if("-dim" in sys.argv):
        GENES_PER_INDIVIDUAL=int(sys.argv[sys.argv.index("-dim") + 1])
    if ("-rt" in sys.argv):
        RUN_TIMES_AVG = int(sys.argv[sys.argv.index("-rt") + 1])
        assert RUN_TIMES_AVG>0


    print "AVG("+str(RUN_TIMES_AVG)+")="+str(sum([main(debug,present,functionDescriptor,i) for i in range(RUN_TIMES_AVG)])/RUN_TIMES_AVG)