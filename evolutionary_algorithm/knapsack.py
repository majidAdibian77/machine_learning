import numpy as np
import random
import math
from eveloution_algorithm import EvolutionaryAlgorithm

class KnapsackProblem:
    def __init__(self, file_path):
        self.file_path = file_path  
        self.number_of_population = 200
        self.first_info = [] 
        self.items_value_wight = []
        self.best_chromosome = {'chromosome':[], 'fitness':-math.inf}

    def read_file(self):
        """
        This def is for reading info from file and save in a list
        """
        file = open(self.file_path, 'r')
        lines = file.readlines()
        items_value_wight = []
        a = lines[0].split(' ')
        first_info = [int(a[0]), int(a[1][:-1])]  # first number of it is number of items and second of it is weight of knapsack
        for line in lines[1:-1]:
            a = line.split(' ')
            items_value_wight.append([int(a[0]), int(a[1][:-1])])
            
        a = lines[-1].split(' ')
        items_value_wight.append([int(a[0]), int(a[1])])
        return first_info, items_value_wight
    

    def initial_population(self, parameter):
        """
            This def is for creating first population of algorithm
        """
        all_chromosome = []
        for i in range(parameter['number_of_population']):
            chromosome = []
            for i in range(parameter['number_of_gens']):
                if random.random() < parameter['prob']:
                    chromosome.append(1)
                else:
                    chromosome.append(0)
            all_chromosome.append({'chromosome': chromosome, 'fitness': -math.inf})
        return all_chromosome
    

    def mutation(self, chromosome_fitness, parameter={'prob': 0.001}):
        """
            This def is for mutatation in a chromosome
        """
        chromosome = chromosome_fitness['chromosome']
        for i in range(len(chromosome)):
            if random.random() < parameter['prob']:
                chromosome[i] = 1 - chromosome[i] # this line toggles the gen: 1->0 and 0->1
        chromosome_fitness['chromosome'] = chromosome
        return chromosome_fitness
    
    def cross_over(self, parent1, parent2, parameter={'place_of_division':0.5 ,'prob': 0.5}):
        """
            This def is for crossover two chromosom 
        """
        p1 = parent1['chromosome']
        p2 = parent2['chromosome']
        index = int(parameter['place_of_division'] * len(p1))
        if random.random() < parameter['prob']:
            child = p1[:index] + p2[index:]
        else:
            child = p2[:index] + p1[index:]
        child_fitness = {'chromosome': child, 'fitness': -math.inf}
        return child_fitness

    def evaluator(self, chromosome_fitness, parameter):
        """
            This def is for evaluating of chromosom and calculating fitness for it
        """
        chromosome = chromosome_fitness['chromosome']
        items_value_wight = parameter['items_value_wight']
        sum_selected_value = 0
        sum_selected_weight = 0
        for i in range(len(chromosome)):
            sum_selected_value += chromosome[i] * items_value_wight[i][0]
            sum_selected_weight += chromosome[i] * items_value_wight[i][1]
        if parameter['knapsack_weight'] > sum_selected_weight:
            fitness = sum_selected_value + (parameter['arg1'] * (parameter['knapsack_weight'] - sum_selected_weight))
        else:
            fitness = sum_selected_value + (parameter['arg2'] * (sum_selected_weight - parameter['knapsack_weight']))
        chromosome_fitness['fitness'] = fitness
        return chromosome_fitness

    def rank_selection(self, papulation, parameter = {'number_of_parents':10}):
        """
        This def is for selcting some chromosom from population via rank selection approach
        """
        fitnesses = [c['fitness'] for c in papulation]
        arg_sort = np.argsort(fitnesses)
        sorted_items = []
        for index in arg_sort:
            sorted_items.append(papulation[index])
        parents = sorted_items[:-(parameter['number_of_parents']+1):-1]
        return parents
    

    def random_parent_selection(self, papulation, parameter = {'number_of_parents':10}):
        """
            This def is for selecting parents from population randomly
        """
        parents = []
        for i in range(parameter['number_of_parents']):
            rand = random.randint(0, len(papulation)-1)
            parents.append(papulation[rand])
        return parents


    def Q_tornoment(self, population, children, parameter = {'size':5, 'number_of_selection': 100}):
        """
            This def is for selecting from population via Q_tornoment approach
        """
        all_population = population + children
        selected_population = []
        for i in range(parameter['number_of_selection']):
            fitness = -math.inf
            for j in range(parameter['size']):
                rand = random.randint(0, len(all_population)-1)
                if all_population[rand]['fitness'] >= fitness:
                    selected = all_population[rand]
                    fitness = selected['fitness']
            selected_population.append(selected)
        return selected_population

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
        self.first_info, self.items_value_wight = self.read_file()

        initial_population_parameter={'number_of_population': self.number_of_population, 'number_of_gens': self.first_info[0], 'prob': 0.3}
        if self.file_path == 'knapsack_1.txt':
            arg1 = 5
            arg2 = -15
        else:
            arg1 = 0
            arg2 = -15
        evaluator_parameter = {'items_value_wight': self.items_value_wight, 'arg1': arg1, 'arg2': arg2, 'knapsack_weight': self.first_info[1]}
        parent_selection_parameter = {'number_of_parents': 20}
        cross_over_parameter={'place_of_division':0.5 ,'prob': 0.5}
        mutation_parameter={'prob':0.0005}
        remaining_population_selection = {'size':5, 'number_of_selection': self.number_of_population}
        stop_condition_parameter = {'max_number_of_evaluation': 1000000, 'max_number_of_generation': 20000}
        evolution = EvolutionaryAlgorithm([self.initial_population, initial_population_parameter],
                              [self.rank_selection, parent_selection_parameter],
                              [self.mutation, mutation_parameter],
                              [self.cross_over, cross_over_parameter],
                              [self.Q_tornoment, remaining_population_selection],
                              [self.evaluator, evaluator_parameter],
                              [self.stop_condition, stop_condition_parameter], 20
                              )

        last_population = evolution.run_algorithm()
        result = {'chromosome':[], 'fitness': -math.inf}
        for chromosome in last_population:
            if chromosome['fitness'] > result['fitness']:
                result = chromosome
        self.best_chromosome = result
        return result, self.items_value_wight


