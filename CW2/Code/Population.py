# Autor: Karol Stepanienko


import random

import numpy as np
from numpy import maximum, minimum

from Functions import f
from Individual import Individual
from Constants import Constants


class Population:
    def __init__(self, population=None, constants=None):
        if constants is None:
            self.c = Constants()
        else:
            self.c = constants
        if population is None:
            self.population = self.generate_starting_population()
        else:
            self.population = population

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
            # data_vector = []
            # # Każdy osobnik ma n współrzędnych
            # for i in range(self.c.n):
            #     data_vector.append(random.randint(self.c.ARG_MIN, self.c.ARG_MAX))
            individuals.append(Individual(data_vector, constants=self.c))
        
        return individuals

    """
    def generate_starting_population_integers(self):
        individuals = []
        # Generuj u osobników
        for i in range(self.c.u):
            individual_vector = []
            # Każdy osobnik ma n współrzędnych
            for i in range(self.c.n):
                individual_vector.append(random.randint(self.c.ARG_MIN, self.c.ARG_MAX))
            individuals.append(Individual(individual_vector, constants=self.c))
        
        return individuals
    """
    
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
        best_individual = None
        for individual in population:
            if best_individual is None or f(individual.data) < f(best_individual.data):
                best_individual = individual
        return best_individual

    def get_value_sum(self, population):
        value_sum = 0
        for individual in population:
            value_sum = value_sum + f(individual.data)
        return value_sum

    def get_selection_probability(self, individual, value_sum):
        # Reprodukcja ruletkowa
        return 1 - (f(individual.data) / value_sum)

    def get_selection_probabilities(self, population):
        return self.get_selection_probabilities_inv(population)

    def get_selection_probabilities_inv(self, population):
        probabilities = []
        for i in population:
            probabilities.append(1/f(i.data))
        return probabilities

    def get_selection_probabilities_normalised(self, population):
        probabilities = []
        value_sum = self.get_value_sum(population)
        values = [f(individual.data) for individual in population]
        maximum = max(values)
        minimum = min(values)
        if minimum == maximum:
            return [1 for _ in values]
        values = [1 - (v - minimum) / (maximum - minimum) for v in values]
        return values
        # for individual in population:
        #     probabilities.append(self.get_selection_probability(individual, value_sum))
        # return probabilities
