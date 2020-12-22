import numpy as np
import random
import math
from eveloution_algorithm import EvolutionaryAlgorithm

class TSP_Problem:
    def __init__(self, file_path):
        self.file_path = file_path
        self.number_of_generation = 100

    def read_file(self):
        """
        This def is for reading info from file and save in a list
        """
        file = open(self.file_path, 'r')
        lines = file.readlines()
        cities = []
        for line in lines[1:-1]:
            a = line.split(' ')
            cities.append([float(a[1]), float(a[2][:-1])])
        a = lines[-1].split(' ')
        cities.append([float(a[1]), float(a[2])])
        return cities
    
    def initial_population(self, parameter):
        """
            This def is for creating first population of algorithm
        """
        all_chromosome = []
        for i in range(parameter['number_of_population']):
            chromosome = random.sample(range(parameter['number_of_gens']), parameter['number_of_gens'])
            np.random.shuffle(chromosome)
            all_chromosome.append({'chromosome':chromosome, 'fitness': -1})
        return all_chromosome

    def evaluator(self, chromosome_fitness, parameter):
        """
            This def is for evaluating of chromosom and calculating fitness for it
        """
        cities = parameter['cities']
        distance = 0
        place1 = cities[chromosome_fitness['chromosome'][0]]
        for i in chromosome_fitness['chromosome'][1:]:
            place2 = cities[i]
            distance += math.sqrt((place1[0] - place2[0])**2 + (place1[1] - place2[1])**2)
            # print(str(place1) +'  '+ str(place2) +'  '+ str(distance))
            place1 = place2
        chromosome_fitness['fitness'] = 1000000000/distance
        return chromosome_fitness

    def rank_selection(self, papulation, parameter):
        """
        This def is for selcting some chromosom from population via rank selection approach
        """
        fitnesses = [c['fitness'] for c in papulation]
        arg_sort = np.argsort(fitnesses)
        sorted_items = []
        for index in arg_sort:
            sorted_items.append(papulation[index])
        parents = sorted_items[:-(parameter['number_of_selection']+1):-1]
        return parents
    
    def random_parent_selection(self, papulation, parameter):
        """
            This def is for selecting parents from population randomly
        """
        parents = []
        for i in range(parameter['number_of_selection']):
            rand = random.randint(0, len(papulation)-1)
            parents.append(papulation[rand])
        return parents

    def Q_tornoment(self, population, children, parameter):
        """
            This def is for selecting from population via Q_tornoment approach
        """
        all_population = population + children
        selected_population = []
        for i in range(parameter['number_of_selection']):
            fitness = -1
            for j in range(parameter['size']):
                rand = random.randint(0, len(all_population)-1)
                if all_population[rand]['fitness'] >= fitness:
                    selected = all_population[rand]
                    fitness = selected['fitness']
            selected_population.append(selected)
        return selected_population

    def edge_cross_over(self, parent1, parent2, parameter):
        """
            This def is for crossover two chromosom via edge approach
        """
        p1 = parent1['chromosome']
        p2 = parent2['chromosome']
        if p1[0] == p2[0]:
            neighbour = {p1[0]: [p1[1], p2[1]]}
        else:
            neighbour = {p1[0]: [p1[1]], p2[0]: [p2[1]]}

        for i in range(1, len(p1)-1):
            if p1[i] in neighbour.keys():
                neighbour[p1[i]].extend([p1[i+1], p1[i-1]])
            else:
                neighbour[p1[i]] = [p1[i+1], p1[i-1]]
            if p2[i] in neighbour.keys():
                neighbour[p2[i]].extend([p2[i+1], p2[i-1]])
            else:
                neighbour[p2[i]] = [p2[i+1], p2[i-1]]

        if p1[-1] in neighbour.keys():
            neighbour[p1[-1]].append(p1[-2])
        else:
            neighbour[p1[-1]] = [p1[-2]]
        if p2[i] in neighbour.keys():
            neighbour[p2[-1]].append(p2[-2])
        else:
            neighbour[p2[-1]] = [p2[-2]]

        result = [random.choice(p1)] # first gen is random
        while len(neighbour.keys()) > 1:
            lst = neighbour[result[-1]]
            next_gen = max(lst, key=lst.count) # getting neighbour with max occurrences
            neighbour.pop(result[-1])
            while next_gen not in neighbour.keys():
                lst.remove(next_gen)
                if lst == []:
                    next_gen = random.choice(list(neighbour.keys()))
                    break
                next_gen = max(lst, key=lst.count)
            result.append(next_gen)
        return {'chromosome': result, 'fitness': -1}
        
    def swap_mutation(self, chromosome_fitness, parameter):
        """
            This def is for mutatation in a chromosome via swap approach
        """
        chromosome = chromosome_fitness['chromosome']
        for i in range(len(chromosome)):
            if random.random() < parameter['prob']:
                temp = chromosome[i]
                other = random.randint(0, len(chromosome)-1)
                chromosome[i] = chromosome[other]
                chromosome[other] = temp
        chromosome_fitness['chromosome'] = chromosome
        return chromosome_fitness

    def stop_condition(self, number_of_generation, number_of_evaluation, parameter):
        """
            This def is for specify the end condition of the algorithm
        """
        if number_of_evaluation > parameter['max_number_of_evaluation'] or number_of_generation > parameter['max_number_of_generation']:
            return True
        return False

    def solve(self):
        """
            This def is as main function of this class and this def uses other function to solve the problem
        """
        # Reading from file
        cities = self.read_file()

        initial_population_parameter = {'number_of_population': self.number_of_generation, 'number_of_gens': len(cities)}
        evaluator_parameter = {'cities': cities}
        parent_selection_parameter = {'size':20, 'number_of_selection': 20}
        cross_over_parameter={}
        mutation_parameter={'prob':0.0005}
        remaining_population_selection = {'size':20, 'number_of_selection': len(cities)}
        stop_condition_parameter = {'max_number_of_evaluation': 500000, 'max_number_of_generation': 20000}
        evolution = EvolutionaryAlgorithm([self.initial_population, initial_population_parameter],
                              [self.rank_selection, parent_selection_parameter],
                              [self.swap_mutation, mutation_parameter],
                              [self.edge_cross_over, cross_over_parameter],
                              [self.Q_tornoment, remaining_population_selection],
                              [self.evaluator, evaluator_parameter],
                              [self.stop_condition, stop_condition_parameter], 20
                              )
        
        last_population = evolution.run_algorithm()
        result = {'chromosome':[], 'fitness': -1}
        for chromosome in last_population:
            if chromosome['fitness'] > result['fitness']:
                result = chromosome
        self.best_chromosome = result
        result['fitness'] = 1000000000/result['fitness']
        return result
