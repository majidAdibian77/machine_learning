import copy
import math
from random import randint

from Part2.genetic_algorithm import Genetic
from Part2.simulated_annealing import SimulatedAnnealing


class problem:
    def __init__(self, relation):
        self.relation = relation
        number_of_E = 0
        for r in relation:
            number_of_E += len(r)
        self.number_of_E = number_of_E
        # self.relation = [[2, 1, 8, 3, 7],  # 0: neighbours of Kerman
        #                  [8, 0],  # 1: neighbours of Sistan
        #                  [4, 1, 0, 7, 5, 6],  # 2: neighbours of Khorasan Jonoobi
        #                  [7, 0, 8, 18, 27, 6],  # 3: neighbours of Fars
        #                  [2, 6, 15],  # 4: neighbours of Khorasan Razavi
        #                  [6, 2, 7, 3, 27, 25, 15],  # 5: neighbours of Esfaha
        #                  [4, 2, 0, 3],  # 7: neighbours of Yazd *********
        #                  [0, 1, 18, 3],  # 8: neighbours of Hormozgan *********
        #                  [3, 8],  # 18: neighbours of Booshehr *********
        #                  ]

    """
        This def is for get first state by create random number
    """

    def first_state(self):
        new_state = []
        for j in range(31):
            new_state.append(randint(1, 4))
        return new_state

    """
        This def returns a directory that keys are id of a state of population and values are fitness of that state
    """

    def get_fitness(self, state):
        fitness = 0
        for province in range(len(self.relation)):
            for neighbour in self.relation[province]:
                if state[province] != state[neighbour]:
                    fitness += 1
        fitness = fitness / self.number_of_E
        return fitness

    """
        This def is for get next state by changing random place
    """

    def get_next_state(self, state):
        next_state = copy.deepcopy(state)
        value = next_state[randint(0, len(next_state) - 1)]
        # This while is for getting new value for this place not the same one
        while True:
            new_value = randint(1, 4)
            if new_value != value:
                break
        next_state[randint(0, len(next_state) - 1)] = new_value
        return next_state


relation = []
print("enter relations:")
state = input()
while len(state) != 0:
    neighbor_state = state.split(' ')
    neighbors = []
    for i in neighbor_state:
        neighbors.append(int(i))
    relation.append(neighbors)
    state = input()
problem = problem(relation)
print("witch algorithm: \n1) Genetic\n2) Simulated Annealing")
number_of_algorithm = int(input())
if number_of_algorithm == 1:
    # Genetic
    number_of_generations = int(input("enter number of generations:"))
    number_of_first_population = int(input("enter population size:"))
    tornument_size = int(input("enter tornument size:"))
    mutationRate = float(input("enter mutation rate:"))

    genetic = Genetic(problem, number_of_generations, number_of_first_population, tornument_size, mutationRate)
    genetic.run()

else:
    # SimulatedAnnealing
    number_of_function = int(input("enter number of function:"))
    if number_of_function == 1:
        func = lambda k, temperature0=1, alpha=0.85: temperature0 * (alpha ** k)
    elif number_of_function == 2:
        func = lambda k, temperature0=1, alpha=100: temperature0 / (1 + (alpha * math.log10(1 + k)))
    elif number_of_function == 3:
        func = lambda k, temperature0=1, alpha=1: temperature0 / (1 + (alpha * k))
    else:
        func = lambda k, temperature0=1, alpha=0.05: temperature0 / (1 + (alpha * k * k))
    simulate = SimulatedAnnealing(problem, func, number_of_function)
    simulate.run()
