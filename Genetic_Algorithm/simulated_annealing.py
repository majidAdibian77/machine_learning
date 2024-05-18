import math
import random
import matplotlib.pyplot as plt


class SimulatedAnnealing:
    def __init__(self, problem, map_to_temperature, number_of_function):
        self.number_of_function = number_of_function
        self.problem = problem
        self.map_to_temperature = map_to_temperature
        self.current_state = problem.first_state()
        self.fitness = []

    def run(self):
        time = 1
        while time < 10000:
            temperature = self.map_to_temperature(time)
            if temperature == 0:
                break
            next_state = self.problem.get_next_state(self.current_state)
            current_fitness = self.problem.get_fitness(self.current_state)
            next_fitness = self.problem.get_fitness(next_state)
            self.fitness.append(current_fitness)
            difference_fitness = next_fitness - current_fitness
            if difference_fitness > 0:
                self.current_state = next_state
            else:
                probability = math.exp(difference_fitness/temperature)
                if random.random() < probability:
                    self.current_state = next_state
            time += 1
            print("temperature: " + str(temperature))
            print("state: " + str(self.current_state))
            print("fitness: " + str(current_fitness))
            print("time: " + str(time))

        plt.plot(range(len(self.fitness)), self.fitness)
        plt.title("function " + str(self.number_of_function))
        plt.xlabel('time')
        plt.ylabel('fitness')

        plt.show()
