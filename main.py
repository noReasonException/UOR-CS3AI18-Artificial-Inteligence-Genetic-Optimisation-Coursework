
found=False
import random
fun=lambda X:sum([(i+1)*pow(X[i],2) for i in range(len(X))])


CROSSOVERRATE=0.8               #Probability of each individual to mate
MUTATIONRATE=0.2                #Probability of each gene to be mutated
POPULATION_SIZE=1000

LB=0
UB=10
GENES_PER_INDIVIDUAL=4  #Warning, always must be divisible by 2
MUTATION_STEP_RANGE=0.05


"""
    Creates a list with GENES_PER_INDIVIDUAL numbers on range [LB,UB]
    This is called an 'Individual'
"""
def createIndividual(lb,ub,n):
    return [random.randint(lb,ub) for i in range(n)]
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
    Mutates a given gene with a probability determined by its second parameter
"""
def mutateGene(gene,mutationRate):
    prob=random.random()
    if(prob<=mutationRate):
        gene+=random.uniform(-MUTATION_STEP_RANGE,MUTATION_STEP_RANGE)
    return max(min(gene,UB),LB)
"""
    Mutates all the genes(the numbers) of an individual (list of numbers) with a given mutationRate
"""
def mutateIndividual(individual,mutationRate):
    return [mutateGene(gene,mutationRate) for gene in individual]

"""
    Applies the mutation to the whole population, returning the combined 2N population(parents and children)
"""
def mutatePopulaton(population,mutationRate):
    return [mutateIndividual(individual,mutationRate) for individual in population]
"""
    Sorts the given population by the fitness, and chooses the N best of them 
"""
def survive(population):
    sortedPopulation = map(
        lambda x: x[1],                         #Discard the fitness percentage, we only want the individuals
        sortByFitness(population)
    )
    return sortedPopulation[:POPULATION_SIZE]   #Survive the N Best individuals
"""
    Returns a pair of (FITNESS_PERCENTAGE,INDIVIDUAL_VECTOR) sorted by the first key
"""
def sortByFitness(population):
    fitness = [(fitIndividual(i, fun), i) for i in population]      # Fitness,individual pair
    fitSum = sum(map(lambda x: x[0], fitness))                      # Fitness sum
    fitness = map(lambda x: (1 - x[0] / fitSum, x[1]), fitness)     # Reversed Percentage
    revSum = sum(map(lambda x: x[0], fitness))                      # Reversed Percentage sum(to be normalized)
    fitness = map(lambda x: (x[0] / revSum, x[1]), fitness)         # Normalized Reversed Percentage
    best = sorted(fitness, key=lambda x: x[0], reverse=True)        # Sort most fitted first

    return best



def select(population):
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

    sortedPopulation=sortByFitness(population)                                                              #Sorted population-fitness pairs
    sortedPopulationWithDensities=_densityFitnessList(sortedPopulation)                                     #fitness part now has the density up to this point (PDF)
    sortedWithDensitiesAndCrossovers=_individualCrossoverProbabilityList(sortedPopulationWithDensities)     #now we have the individual crossover rates as well
    selectedToReproduce=map(                                                                                #Selected individuals to reproduce
        lambda x:x[2],
        filter(lambda x:x[1]<CROSSOVERRATE,sortedWithDensitiesAndCrossovers))
    return selectedToReproduce

def crossover(selectedParents):



    def _mate(male,female):
        assert GENES_PER_INDIVIDUAL%2==0
        return [male[:len(male)]+female[len(female):],male[len(male):]+female[:len(female)]]


    if(len(selectedParents)%2!=0):selectedParents=selectedParents[:len(selectedParents)-1]          #Someone will get lonely
    random.shuffle(selectedParents)
    males = selectedParents[:int(len(selectedParents)/2)]                                           #Arbitary split half of them as males
    females = selectedParents[int(len(selectedParents)/2):]                                         #And half of them as females
    children=[]

    for male,female in zip(males,females):
        children.extend(_mate(male,female))

    return children

population= createPopulation(POPULATION_SIZE,LB,UB,GENES_PER_INDIVIDUAL)
curr_generation=0
while not found:
    #Evaluation
    so=sorted(population)
    if(fitIndividual(so[0],fun)==0):
        found=True
        break
    #Select
    selected=select(population)

    #Crossover?
    children=crossover(selected)



    #Mutate
    mutatedPopulation = mutatePopulaton(children, MUTATIONRATE)
    #Survive
    population=survive(mutatedPopulation+population)

    curr_generation+=1
    print "Generation "+str(curr_generation)+" Best With fit "+str(fitIndividual(so[0],fun))


