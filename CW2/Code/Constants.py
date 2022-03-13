# Autor: Karol Stepanienko


import numpy as np


class Constants:
    def __init__(self):
        self.table = Table()

        # Dla problemu wymagającego zakodowania liczb całkowitych:
        self.ABSTRACT = False

        # Minimalna wartość jaką może przyjąć zmienna włącznie z tą wartością
        self.ARG_MIN = -16
        # Maksymalna wartość jaką może przyjąć zmienna włącznie z tą wartością
        self.ARG_MAX = 15
        # self.ARG_MAX = 10
        # Zbiór wszystkich możliwych wartości genów
        self.ELEMENTS = [i for i in range(self.ARG_MIN, self.ARG_MAX + 1)]
        self.NUMBER_OF_ELEMENTS = len(self.ELEMENTS)
        # Liczba bitów potrzebna do reprezentowania zbioru wszystkich wartości genów
        self.NUMBER_OF_BITS = self.table.get_number_of_bits_integers(self.ARG_MIN, self.ARG_MAX)
        # Liczba elementów (tutaj liczb całkowitych lub elementów abstrakcyjnych) (genów) jednego osobnika
        self.n = 4

        
        # # ODKOMENTOWAĆ dla przykładu alternatywnego problemu
        # # Dla problemu wymagającego zakodowania abstrakcyjnych obiektów:
        # self.ABSTRACT = True
        # self.ARG_MIN = None
        # self.ARG_MAX = None
        # # Lista wszystkich elementów abstrakcyjnych
        # self.ELEMENTS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        # # Liczba wszystkich elementów abstrakcyjnych
        # self.NUMBER_OF_ELEMENTS = len(self.ELEMENTS)
        # self.NUMBER_OF_BITS = self.table.get_number_of_bits_abstract(self.NUMBER_OF_ELEMENTS)
        # # Problem tego typu wymaga definicji odpowiedniej funkcji celu zwracajacej liczbę rzeczywistą
        # # na podstawie wektora self.n genów w postaci wspomnianych obiektów
        # # Liczba elementów (tutaj liczb całkowitych lub elementów abstrakcyjnych) (genów) jednego osobnika
        # self.n = 1

        
        # Dla obu typów problemów:
    
        # Prawda gdy liczba elementów jest potęgą dwójki
        # Pogarsza wydajność
        self.NUMBER_OF_ELEMENTS_POWER_OF_TWO = self.table.check_if_power_of_two(self.NUMBER_OF_ELEMENTS)

        # Słowniki przechowujace powiązanie element <=> kod greya
        self.element_to_bin = self.table.get_dictionaries(self.ELEMENTS)
        
        # Parametry algorytmu genetycznego
        # u - Liczba osobników w populacji
        self.u = 300
        # pc - prawdopodobieństwo krzyżowania
        self.pc = 0.95
        # pm - prawdopodobieństwo mutacji
        self.pm = 0.05
        # t_max - maksymalna liczba iteracji (pokoleń)
        self.t_max = 300

        # Liczba uruchomień algorytmu w trakcie zbierania danych statystycznych
        # w postaci listy najlepszych osobników
        self.n_stat = 25
        # self.n_stat = 5

    def print_params(self):
        print('Parametry algorytmu genetycznego: ')
        print('Rozmiar populacji: ', self.u)
        print('Prawdopodobieństwo mutacji: ', self.pm)
        print('Prawdopodobieństwo krzyżowania: ', self.pc)
        print('Liczba pokoleń: ', self.t_max)


class Table:
    def check_if_power_of_two(self, num_of_elements):
        i = 0
        while (2 ** i < num_of_elements):
            i = i + 1
        return 2 ** i == num_of_elements

    def get_number_of_elements_integers(self, ARG_MIN, ARG_MAX):
        # Zwraca liczbę elementów w podanym zbiorze możliwych dyskretnych wartości współrzędnych punktów
        return abs(ARG_MAX - ARG_MIN) + 1

    def get_number_of_bits_integers(self, ARG_MIN, ARG_MAX):
        # Określa jak wiele bitów potrzeba do reprezentacji podanej ilości danych dyskretnych
        number_of_elements = self.get_number_of_elements_integers(ARG_MIN, ARG_MAX)
        return self.get_number_of_bits(number_of_elements)

    def get_number_of_bits_abstract(self, number_of_elements):
        return self.get_number_of_bits(number_of_elements)

    def get_number_of_bits(self, number_of_elements):
        number_of_bits = 1
        while 2**number_of_bits < number_of_elements:
            number_of_bits = number_of_bits + 1
        return number_of_bits

    def generate_grey_code_vectors(self, n):
        # Tworzy listę n kolejnych liczb naturalnych w kodzie greya
        number_of_bits = self.get_number_of_bits(n)
        grey_codes = []
        for i in range(n):
            grey_code_i = i ^ (i >> 1)
            # Uzupełnia zerami z przodu w miarę potrzeby
            string = bin(grey_code_i).split('b')[1].zfill(number_of_bits)
            grey_codes.append(self.string_to_array(string))
        return grey_codes

    def string_to_array(self, string):
        arr = []
        for char in string:
            arr.append(int(char))
        return arr


    def get_dictionaries(self, elements):
        # Tworzy słowniki przechowujace powiązanie element <=> kod greya
        grey_codes = self.generate_grey_code_vectors(len(elements))
        bin_to_element = dict()
        element_to_bin = dict()
        for element, grey_code in zip(elements, grey_codes):
            element_to_bin[element] = grey_code
        return element_to_bin
