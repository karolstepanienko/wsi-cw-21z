# Autor: Karol Stepanienko


from Functions import f
from Constants import Constants


# Funkcje liczące wartości średnie i odchylenie standardowe
class Averages:
    def __init__(self, constants=None):
        if constants is None:
            self.c = Constants()
        else:
            self.c = constants

    def get_average(self, values):
        value_sum = 0
        for value in values:
            value_sum = value_sum + value
        return value_sum / len(values)

    def round_list(self, values):
        for i, value in enumerate(values):
            values[i] = round(value, 2)
        return values

    def get_standard_deviation(self, values):
        average = self.get_average(values)
        sum_square = 0
        for value in values:
            sum_square = sum_square + (value - average)**2
        return pow(sum_square / len(values), 0.5)

    # Zwraca wszystkie wartości danego genu w wektorzacch pionowych
    def get_values_vectors(self, values, num_of_elements):
        gene_values_vectors = num_of_elements * [len(values) * [0]]
        for gene_num in range(num_of_elements):
            for value_num, value in enumerate(values):
                gene_values_vectors[gene_num][value_num] = value[gene_num]
        return gene_values_vectors

    def get_average_vectors(self, values, num_of_elements):
        gene_values_vectors = self.get_values_vectors(values, num_of_elements)

        averages = []      
        for gene_num in range(num_of_elements):
            averages.append(self.get_average(gene_values_vectors[gene_num]))
        return averages

    def get_standard_deviation_vectors(self, values, num_of_elements):
        gene_values_vectors = self.get_values_vectors(values, num_of_elements)

        standard_deviations = []
        for gene_num in range(num_of_elements):
            standard_deviations.append(self.get_standard_deviation(gene_values_vectors[gene_num]))
        return standard_deviations

    # Średnia wartości funkcji
    def get_average_function_value(self, individuals):
        value_sum = 0
        for individual in individuals:
            value_sum = value_sum + f(individual.data)
        return value_sum / len(individuals)

    # Średnie wartości genów osobnika
    def get_average_individual(self, individuals):
        gene_sum = self.c.n * [0]
        for individual in individuals:
            for gene_num in range(self.c.n):
                gene_sum[gene_num] = gene_sum[gene_num] + individual.data[gene_num]
        
        average_genes = self.c.n * [0]
        for gene_num in range(self.c.n):
            average_genes[gene_num] = gene_sum[gene_num] / len(individuals)

        return average_genes

    # Odchylenie standardowe wartości funkcji
    def get_standard_deviation_function_value(self, individuals, average):
        sum_square = 0
        for individual in individuals:
            sum_square = sum_square + (f(individual.data) - average)**2
        return pow(sum_square / len(individuals), 0.5)

    # Odchylenia standardowe genów osobnika
    def get_standard_deviation_individual(self, individuals, average_individual_values):
        sum_squares = self.c.n * [0]
        for individual in individuals:
            for gene_num in range(self.c.n):
                sum_squares[gene_num] = sum_squares[gene_num] + \
                    (individual.data[gene_num] - average_individual_values[gene_num])**2
        
        standard_deviations = self.c.n * [0]
        for gene_num in range(self.c.n):
            standard_deviations[gene_num] = pow(sum_squares[gene_num] / len(individuals), 0.5)

        return standard_deviations