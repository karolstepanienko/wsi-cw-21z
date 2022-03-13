# Autor: Karol Stepanienko


import random
import numpy as np
from copy import deepcopy
from pprint import pprint
from time import time

from Constants import Constants
from Functions import f
from Individual import Individual
from Averages import Averages


class GeneticAlgorithm:
    def __init__(self, constants=None):
        if constants is None:
            self.c = Constants()
        else:
            self.c = constants
        self.reproduction = Reproduction(self.c)
        self.crossover = Crossover(self.c)
        self.mutation = Mutatation(self.c)
        self.averages = Averages(self.c)

    def generate_starting_population(self):
        if self.c.ARG_MAX is not None and self.c.ARG_MIN is not None:
            return self.generate_starting_population_integers()
        else:
            return self.generate_starting_population_abstract()

    def generate_starting_population_integers(self):
        individuals = []
        # Generuj u osobników
        for i in range(self.c.u):
            data_vector = np.random.randint(low=self.c.ARG_MIN, high=self.c.ARG_MAX + 1, size=self.c.n)
            individuals.append(Individual(data_vector, constants=self.c))
        
        return individuals

    def generate_starting_population_abstract(self):
        individuals = []
        # Generuj u osobników
        for i in range(self.c.u):
            individual_vector = []
            # Każdy osobnik ma n współrzędnych
            for i in range(self.c.n):
                individual_vector.append(random.choice(self.c.ELEMENTS))
            individuals.append(Individual(individual_vector, constants=self.c))
        return individuals        

    def find_best_individual(self, population):
        best_i = None
        for i in population:
            if best_i is None or f(i.data) < f(best_i.data):
                best_i = i
        return best_i



    def run(self):
        population = self.generate_starting_population()

        best_individual = self.find_best_individual(population)
        
        t = 0
        while t < self.c.t_max:
            # Reprodukcja
            R = self.reproduction.reproduction(deepcopy(population))
            
            # Krzyżowanie
            C = self.crossover.crossover(deepcopy(R))

            # Mutacja
            M = self.mutation.mutation(deepcopy(C))
            
            best_individual_t = self.find_best_individual(M)

            if f(best_individual_t.data) < f(best_individual.data):
                best_individual = best_individual_t
            
            # Inkrementacja
            t = t + 1
        
        print(best_individual.to_string())
        if not self.c.ABSTRACT:
            end_population_function_average = self.averages.get_average_function_value(M)
            end_population_individual_average = self.averages.get_average_individual(M)
            return best_individual, end_population_function_average, end_population_individual_average
        else:
            return best_individual


class Reproduction:
    def __init__(self, constants=None):
        if constants is None:
            self.c = Constants()
        else:
            self.c = constants

    def reproduction(self, population):
        probabilities = self.get_selection_probabilities_normalised(population)
        new_population = []
        for _ in range(self.c.u):
            new_population.append(random.choices(population=population, weights=probabilities, k=1)[0])
        return new_population

    def get_value_sum(self, population):
        value_sum = 0
        for individual in population:
            value_sum = value_sum + f(individual.data)
        return value_sum

    # Wartości prawdopodobienstwa obliczone w ten sposób są bardzo blisko siebie
    # W konsekwencji nie udaje się odpowiednio wybrać lepszych i gorszych osobników
    def get_selection_probabilities_roulette(self, population):
        probabilities = []
        value_sum = self.get_value_sum(population)
        for i in population:
            probabilities.append(1 - (f(i.data) / value_sum))
        return probabilities

    def get_selection_probabilities_normalised(self, population):
        probabilities = []
        values = [f(i.data) for i in population]
        values = self.add_offset(values)
        
        maximum = max(values)
        minimum = min(values)
        
        if minimum == maximum:
            probabilities = [1 for _ in population]
        else:
            probabilities = [1 - ((v - minimum) / (maximum - minimum)) for v in values]
        return probabilities

    # Upewnia sie, ze nie ma ujemnych prawdopodobienstw
    def add_offset(self, values):
        min_value = min(values)
        if min_value < 0:
            offset = - min_value
            positive_values = []
            for value in values:
                positive_values.append(value + offset)
            return positive_values
        else:
            return values

    def get_selection_probabilities_inv(self, population):
        probabilities = []
        for i in population:
            probabilities.append(1/f(i.data))
        return probabilities


class Crossover:
    def __init__(self, constants=None):
        if constants is None:
            self.c = Constants()
        else:
            self.c = constants

    def get_pairs(self, population):
        pairs = []
        # Zwiększ liczbę elementów jeżeli jest nieparzysta dodając jeszcze raz ostatniego osobnika
        if self.c.u % 2 != 0:
            population.append(population[self.c.u - 1])
        
        for i in range(int(len(population)/2)):
            pairs.append([
                population[2*i],
                population[2*i + 1]
            ])
        
        return pairs

    def check_if_individuals_exist(self, individuals):
        for individual in individuals:
            if not individual.check_if_exists(individual.bin_vec):
                return False
        return True

    def crossover(self, population):
        new_population = []
        
        pairs = self.get_pairs(population)
        
        for pair in pairs:
            
            crossed_pair = self.cross_pair(pair)
            
            # Udopornienie na liczbę elementów niebędącą potęgą dwójki
            if not self.c.NUMBER_OF_ELEMENTS_POWER_OF_TWO:
                while not self.check_if_individuals_exist(crossed_pair):
                    crossed_pair = self.cross_pair(pair)

            for i in crossed_pair:
                new_population.append(i)
        
        # Naprawa długości populacji
        new_population = self.fix_population_len(new_population)
        
        # Aktualizacja wartości całkowitych osobnika
        for i in new_population:
            i.update_after_binary_change()
        return new_population

    def cross_pair(self, pair):
        crossover_point = np.random.randint(0, 20)
        tmp = [None, None]

        # print("before cross")
        # for i in pair:
        #     print(i.to_string())
        # print(crossover_point)
        if random.uniform(0, 1) < self.c.pc:
            # print(0)
            # Krzyżowanie pierwszej części
            tmp[0] = deepcopy(pair[0].bin_vec[:crossover_point])
            tmp[1] = deepcopy(pair[1].bin_vec[:crossover_point])
            
            pair[0].bin_vec[:crossover_point] = tmp[1]
            pair[1].bin_vec[:crossover_point] = tmp[0]
        
        elif random.uniform(0, 1) < self.c.pc:
            # print(1)
            # Krzyżowanie drugiej części
            tmp[0] = deepcopy(pair[0].bin_vec[crossover_point:])
            tmp[1] = deepcopy(pair[1].bin_vec[crossover_point:])

            pair[0].bin_vec[crossover_point:] = tmp[1]
            pair[1].bin_vec[crossover_point:] = tmp[0]

        # print("after cross")
        # for i in pair:
        #     print(i.to_string())

        return pair

    def fix_population_len(self, population):
        diff = len(population) - self.c.u
        if diff > 0:
            population = population[:-diff]
        return population


class Mutatation:
    def __init__(self, constants=None):
        if constants is None:
            self.c = Constants()
        else:
            self.c = constants

    def mutation(self, population):
        if not self.c.NUMBER_OF_ELEMENTS_POWER_OF_TWO:
            new_population = self.mutation_check_if_exists(population)
        else:
            new_population = self.mutation_basic(population)
        
        for i in new_population:
            i.update_after_binary_change()
        return new_population

    def mutate_one_individual(self, individual):
        # Dla każdego bitu
        for bit_index in range(self.c.NUMBER_OF_BITS * self.c.n):
            if random.uniform(0, 1) < self.c.pm:
                individual.invert_bit_in_bit_vector(index=bit_index)
        return individual

    def mutation_basic(self, population):
        # Dla każdego osobnika w populacji
        for individual_index in range(len(population)):
            population[individual_index] = self.mutate_one_individual(population[individual_index])
        return population

    def mutation_check_if_exists(self, population):
        # Dla każdego osobnika w populacji
        for individual_index in range(len(population)):
            new_i = self.mutate_one_individual(deepcopy(population[individual_index]))
            # Udopornienie na liczbę elementów niebędącą potęgą dwójki
            while not new_i.check_if_exists(new_i.bin_vec):
                new_i = self.mutate_one_individual(deepcopy(population[individual_index]))
            population[individual_index] = new_i
        return population


if __name__=="__main__":
    ga = GeneticAlgorithm()
    start = time()
    result = ga.run()
    end = time()
    if type(result) is tuple:
        print(result[0].to_string())
    else:
        print(result.to_string())
    
    # Czas wykonania
    print(end - start,'s')