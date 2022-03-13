# Autor: Karol Stepanienko


import time
import random

from Functions import f
from Constants import Constants
from GeneticAlgorithm import GeneticAlgorithm
from Averages import Averages


class Stats:
    def __init__(self, constants=None):
        self.best_individuals = []
        self.end_population_function_averages = []
        self.end_population_individual_averages = []
        if constants is None:
            self.c = Constants()
        else:
            self.c = constants
        self.averages = Averages(constants=self.c)
        self.reset()

    # Resetuje algorytm genetyczny i losuje nową populację
    def reset(self):
        self.genetic_algorithm = GeneticAlgorithm(constants = self.c)

    def run_genetic_algorithms(self):
        random.seed()
        best_individuals = []
        end_population_function_averages = []
        end_population_individual_averages = []
        for i in range(self.c.n_stat):
            self.reset()
            best_individual, end_population_function_average, end_population_individual_average = \
                self.genetic_algorithm.run()

            best_individuals.append(best_individual)
            end_population_function_averages.append(end_population_function_average)
            end_population_individual_averages.append(end_population_individual_average)

            if (i+1) % 5 == 0:
                print('Run: ', i + 1)

        return best_individuals, end_population_function_averages, end_population_individual_averages

    def get_best_individual(self, individuals):
        best_individual = None
        for individual in individuals:
            if best_individual is None or f(individual.data) < f(best_individual.data):
                best_individual = individual
        return best_individual

    def run_offline(self):
        start_time = time.time()
        self.best_individuals, self.end_population_function_averages,\
             self.end_population_individual_averages = self.run_genetic_algorithms()
        average = self.get_average(self.best_individuals)
        standard_deviation = self.get_standard_deviation(self.best_individuals, average)

        return time.time() - start_time, best_individual, average, standard_deviation

    def run_online(self):
        start_time = time.time()
        self.best_individuals, self.end_population_function_averages,\
             self.end_population_individual_averages = self.run_genetic_algorithms()
        
        average_function_value = self.averages.get_average_function_value(self.best_individuals)
        average_individual_values = self.averages.get_average_individual(self.best_individuals)

        standard_deviation_function_value = self.averages.get_standard_deviation_function_value(self.best_individuals, average_function_value)
        standard_deviation_individual_values = self.averages.get_standard_deviation_individual(self.best_individuals, average_individual_values)
        
        # standard_deviation_end_population_function_value = self.averages.get_standard_deviation(self.end_population_function_averages)
        # standard_deviation_end_population_individual_averages = self.averages.get_standard_deviation_vectors(self.end_population_individual_averages, self.c.n)

        self.c.print_params()
        print()
        print('Wyniki:')
        
        print('Średnia wartość funkcji: ', round(average_function_value, 2))
        print('Odchylenie standardowe funkcji: ', round(standard_deviation_function_value, 2))
        
        print('Średnie wartości genów osobnika: ', self.averages.round_list(average_individual_values))
        print('Odchylenie standardowe wartości genów osobnika: ', self.averages.round_list(standard_deviation_individual_values))
        
    
        # print('Odchylenie standardowe średniej wartości funkcji w ostatniej populacji: ', round(standard_deviation_end_population_function_value, 2))
        # print('Odchylenie standardowe średniej wartości genów osobnika w ostatniej populacji: ', self.averages.round_list(standard_deviation_end_population_individual_averages))

        print('Najlepszy osobnik: ', self.genetic_algorithm.find_best_individual(self.best_individuals).to_string())
        print('Czas: ', time.time() - start_time, 's')


if __name__=="__main__":
    stats = Stats()
    stats.run_online()
