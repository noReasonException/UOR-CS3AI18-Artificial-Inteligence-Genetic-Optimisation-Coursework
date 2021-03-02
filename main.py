
found=False
import random
fun=lambda X:sum([(i+1)*pow(X[i],2) for i in range(len(X))])

MUTATIONRATE=0.2
POPULATION_SIZE=1000
LB=0
UB=10
GENES_PER_INDIVIDUAL=4
MUTATION_STEP_RANGE=0.05

def createIndividual(lb,ub,n):
    return [random.randint(lb,ub) for i in range(n)]

def createPopulation(populationSize,lb,ub,n):
    return [createIndividual(lb,ub,n) for _ in range(populationSize)]

def fitIndividual(individual,fun):
    return fun(individual)

def mutateGene(gene,mutationRate):
    prob=random.random()
    if(prob<=mutationRate):
        gene+=random.uniform(-MUTATION_STEP_RANGE,MUTATION_STEP_RANGE)
    return max(min(gene,UB),LB)
def mutateIndividual(individual,mutationRate):
    return [mutateGene(gene,mutationRate) for gene in individual]

def survive(old_population,mutated_population):
    combined=old_population+mutated_population
    fitness = [(fitIndividual(i, fun),i) for i in combined]
    bestFit=sorted(fitness,key=lambda pair:pair[0])
    best=map(lambda x:x[1],bestFit)
    return best[:POPULATION_SIZE]

def fitAsPercentage(individual,fun):
    return 1-(fun(individual)/fun([UB for _ in range(GENES_PER_INDIVIDUAL)]))

def surviveWithWeelSelection(old_population,mutated_population):
    combined=old_population+mutated_population
    fitness=[(fitAsPercentage(i,fun),i) for i in combined]
    bestFit=sorted(fitness,key=lambda pair:pair[1])
    best=map(lambda x:x[1],bestFit)
    return best[:POPULATION_SIZE]


population= createPopulation(POPULATION_SIZE,LB,UB,GENES_PER_INDIVIDUAL)
curr_generation=0
while not found:
    mutatedPopulation=[mutateIndividual(individual,MUTATIONRATE) for individual in population]
    population=survive(population,mutatedPopulation)
    so=sorted(population)
    if(fitIndividual(so[0],fun)==0):found=True
    curr_generation+=1
    print str(curr_generation)+"Best-> "+str(so[0])+"With fit "+str(fitIndividual(so[0],fun)) +" -> "+str(fitAsPercentage(so[0],fun))


print population
