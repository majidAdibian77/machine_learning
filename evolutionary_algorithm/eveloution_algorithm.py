import numpy as np
import random


class EvolutionaryAlgorithm:
    def __init__(self,
                 initial_population,
                 parent_selection,
                 mutation,
                 cross_over,
                 remaining_population_selection,
                 evaluator,
                 stop_condition,
                 number_of_children = 50,
                ):
        self.number_of_children = number_of_children
        self.generation_counter = 0
        self.evaluation_counter =  0
        self.population = []
        self.initial_population = initial_population[0]
        self.initial_population_param = initial_population[1]
        self.cross_over = cross_over[0]
        self.cross_over_params = cross_over[1]
        self.mutation = mutation[0]
        self.mutation_params = mutation[1]
        self.remaining_population_selection = remaining_population_selection[0]
        self.remaining_population_selection_params = remaining_population_selection[1]
        self.parent_selection = parent_selection[0]
        self.parent_selection_params = parent_selection[1]
        self.evaluator = evaluator[0]
        self.evaluator_parameter = evaluator[1]
        self.stop_condition = stop_condition[0]
        self.stop_condition_param = stop_condition[1]
        self.result = None
    
    def create_new_children(self, parents):
        """
            This def is for creating new children using crossover and mutation
        """
        children = []
        random.shuffle(parents)
        for i in range(self.number_of_children):
            index1 = i % len(parents)
            index2 = (i+1) % len(parents)
            child = self.cross_over(parents[index1], parents[index2], self.cross_over_params)
            child = self.mutation(child, self.mutation_params)
            child = self.evaluator(child, self.evaluator_parameter)
            self.evaluation_counter += 1
            children.append(child)
        return children


    def run_algorithm(self):
        """
            This def is for run algorithm for input functions and parameter
        """
        self.population = self.initial_population(self.initial_population_param)
        for chromosome in self.population:
            chromosome = self.evaluator(chromosome, self.evaluator_parameter)
        self.generation_counter = 1
        while not self.stop_condition(self.generation_counter,self.evaluation_counter, self.stop_condition_param):
            parents = self.parent_selection(self.population, self.parent_selection_params)
            children = self.create_new_children(parents)
            self.population = self.remaining_population_selection(self.population, children, self.remaining_population_selection_params)
            self.generation_counter += 1
        return self.population






