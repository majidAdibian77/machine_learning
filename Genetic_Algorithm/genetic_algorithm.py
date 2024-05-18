from random import randint
import matplotlib.pyplot as plt


class Genetic:
    def __init__(self, problem, number_of_generations, population_size, tornument_size, mutation_rate):
        self.problem = problem
        self.number_of_generations = number_of_generations
        self.population_size = population_size
        self.tornument_size = tornument_size
        self.mutation_rate = mutation_rate
        self.parents = []
        self.children = []
        first_population = []
        """
            creating first population. 
            In any coloring of map: 1->red, 2->blue, 3->yellow, 4->green
        """
        for i in range(population_size):
            first_population.append(problem.first_state())
        self.population = first_population
        self.min_fitness = []
        self.max_fitness = []
        self.avg_fitness = []
        self.relation = problem.relation

    def get_fitness(self):
        fitness = {}
        for i in range(len(self.population)):
            fitness[id(self.population[i])] = self.problem.get_fitness(self.population[i])
        return fitness

    """
        This def select parents from population: selecting k random state and selecting best of them
         and doing it to the length of the population and then we have parents as many as population
    """

    def select_parent(self, fitness):
        parents = []
        number_of_population = len(self.population)
        number_of_parent = int(len(self.population) / self.tornument_size)
        for torment in range(number_of_parent):
            k_selected = []
            for k in range(self.tornument_size):
                k_selected.append(self.population[randint(0, number_of_population - 1)])
            max = 0
            max_state = None
            for selected in k_selected:
                if fitness[id(selected)] > max:
                    max = fitness[id(selected)]
                    max_state = selected
            parents.append(max_state)
        self.parents = parents

    """
        This def generates children: selecting tow parents randomly and crossover them
    """

    def children_by_crossover(self):
        children = []
        parents_size = len(self.parents)
        for i in range(len(self.population)):
            crossover_x = self.parents[randint(0, parents_size - 1)]
            crossover_y = self.parents[randint(0, parents_size - 1)]
            crossover_index = int(len(crossover_x) / 2)
            child = crossover_x[:crossover_index]
            child.extend(crossover_y[crossover_index:])
            children.append(child)
        self.children = children

    """
        This def changes some node of all population
    """

    def mutation(self):
        population_size = len(self.population)
        number_of_node = len(self.population[0])
        mutated_genomes = population_size * number_of_node * self.mutation_rate
        for i in range(int(mutated_genomes)):
            state_index = randint(0, population_size - 1)
            node_index = randint(0, number_of_node - 1)
            self.children[state_index][node_index] = randint(1, 4)

    """
        This def changes population and assigns children to population
    """

    def change_population(self):
        self.population = self.children

    def run(self):

        for i in range(self.number_of_generations):
            fitness = self.get_fitness()
            max_fitness = 0
            min_fitness = 100000000
            sum_fitness = 0
            for key in fitness.keys():
                f = fitness[key]
                if max_fitness < f:
                    max_fitness = f
                elif min_fitness > f:
                    min_fitness = f
                sum_fitness += f
            avg_fitness = sum_fitness / len(self.population)
            self.min_fitness.append(min_fitness)
            self.max_fitness.append(max_fitness)
            self.avg_fitness.append(avg_fitness)
            # print(fitness)
            self.select_parent(fitness)
            self.children_by_crossover()
            self.mutation()
            self.change_population()
            # for state in self.population:
            #     print(state)

        plt.plot(range(self.number_of_generations), self.max_fitness, range(self.number_of_generations),
                 self.min_fitness, range(self.number_of_generations), self.avg_fitness)
        plt.title(
            "populationSize: " + str(
                self.population_size) + ", tornumentSize: " + str(self.tornument_size) + ", mutationRate: " + str(
                self.mutation_rate))
        plt.xlabel('numberOfGenerations')
        plt.ylabel('fitness')
        plt.show()
        print("result:")
        # for state in self.population:
        #     print(state)
        print(self.population[0])
        print("max fitness:")
        print(self.max_fitness)
        print("min fitness:")
        print(self.min_fitness)
        print("average fitness:")
        print(self.avg_fitness)
