import random
import matplotlib.pyplot as plt
from Player import Player
from Field import Field

from threading import Thread
from queue import Queue

# Константы задачи
HROMO_LENGTH = 109
SIZE_FIELD = 8

# Константы алгоритма
POPULATION_SIZE = 100
MAX_WEIGHT = 30

P_TOURNAMENT = 0.5

P_CROSSOVER = 0.9
COUNT_CROSSOVER = 8

P_MUTATION = 0.3
COUNT_MUTATION = 10
FORCE_MUTATION = 0.7

MAX_GENERATIONS = 30

RANDOM_SEED = 777
random.seed(RANDOM_SEED)

class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = 0

def individualCreator():
    return Individual([random.randint(0, MAX_WEIGHT) for _ in range(HROMO_LENGTH)])

def populationCreator():
    return list([individualCreator() for _ in range(POPULATION_SIZE)])



def get_win_index(population:list[list[int]], i:int, j:int, queue:Queue):
    field = Field()
    player1 = Player(Player.ZERO, SIZE_FIELD, population[i])
    player2 = Player(Player.CROSS, SIZE_FIELD, population[j])
    
    while field.game_is_over() == False:
        row, col = player1.get_move(field.get_last_move())
        if field._set_sign(Player.ZERO, row, col):
            return

        row, col = player2.get_move(field.get_last_move())
        if field._set_sign(Player.CROSS, row, col):
            return

    if (field.get_win_sign() == Player.ZERO):
        queue.put(i)
        return
    queue.put(j)

def getPopulationFitness(population: list[list[int]]):
    fitnesses = [0] * POPULATION_SIZE

    for i in range(POPULATION_SIZE):
        queue = Queue()
        threadings = []

        opponents = list(range(0, POPULATION_SIZE))
        opponents.remove(i)
        random.shuffle(opponents)
        opponents = set(opponents[:int((POPULATION_SIZE-1) * P_TOURNAMENT)])

        for j in range(POPULATION_SIZE):
            if j not in opponents:
                continue

            thread = Thread(target=get_win_index, args=(population, i, j, queue))
            thread.start()
            threadings.append(thread)

        for thread in threadings:
            thread.join()

        while not queue.empty():
            fitnesses[queue.get()] += 1

    return fitnesses

population = populationCreator()
generationCounter = 0

fitnessValues = getPopulationFitness(population)
for fitnessValue, individ in zip(fitnessValues, population):
    individ.fitness = fitnessValue

print("First Fitness End")

maxFitnessValues = []
meanFitnessValues = []

def clone(value:Individual):
    individ = Individual(value[:])
    individ.fitness.value = value.fitness.value
    return individ

def tournament(population, length):
    offspring = []
    for _ in range(length):
        i1 = i2 = i3 = 0
        while (i1 == i2) or (i2 == i3) or (i1 == i3):
            i1, i2, i3 = random.randint(0, length - 1), random.randint(0, length - 1), random.randint(0, length - 1)

        offspring.append(max([population[i1], population[i2], population[i3]], key=lambda ind: ind.fitness.value))

    return offspring

def crossover(parent1, parent2, start=0, count=0):
    if (start >= HROMO_LENGTH - 2 or count == COUNT_CROSSOVER):
        return
    
    s = random.randint(start + 1, len(parent1) - 2)
    parent1[s:], parent2[s:] = parent2[s:], parent1[s:]
    crossover(parent1, parent2, s, count + 1)


def mutation(individ, mutationRate=0.01):
    max_mut = int(FORCE_MUTATION * MAX_WEIGHT)
    for i in range(len(individ)):
        if random.random() < mutationRate:
            individ[i] = (random.randint(0, max_mut) - max_mut//2)
            individ[i] = abs(individ[i])


while generationCounter < MAX_GENERATIONS:
    generationCounter += 1
    offspring = tournament(population, len(population))
    offspring = list(map(clone, offspring))

    for parent1, parent2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            crossover(parent1, parent2)

    for individ in offspring:
        if random.random() < P_MUTATION:
            mutation(individ, (float(COUNT_MUTATION) / HROMO_LENGTH))

    freshFitnessValues = getPopulationFitness(offspring)

    for individual, fitnessValue in zip(offspring, freshFitnessValues):
        individual.fitness.value = fitnessValue

    population = offspring[:]

    fitnessValues = [individ.fitness.value for individ in population]

    
    maxFintess = max(fitnessValues)
    meanFitness = sum(fitnessValues) / len(fitnessValues)
    maxFitnessValues.append(maxFintess)
    meanFitnessValues.append(meanFitness)
    print(f"Поколение: {generationCounter}. Макс. приспособ: {maxFintess}. Средняя приспособ: {meanFitness}.")

    bestIndex = fitnessValues.index(maxFintess)
    print("Лучший индивид:", *population[bestIndex], "\n")
    


plt.plot(maxFitnessValues, color="red")
plt.plot(meanFitnessValues, color="blue")
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя приспособленность')
plt.savefig("fig.png")
