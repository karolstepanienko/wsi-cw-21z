# Autor: Karol Stepanienko


from Constants import Constants
from Functions import f
from pprint import pprint

class Individual:
    def __init__(self, data, constants=None):
        if constants is None:
            self.c = Constants()
        else:
            self.c = constants
        self.data = self.check_data_values(data)
        self.bin_data = self.get_binary_data_representation(self.data)
        self.bin_vec = self.get_binary_vector_data_representation()

    def check_data_values(self, data):
        if self.c.ARG_MAX is not None and self.c.ARG_MIN is not None:
            return self.check_data_values_integers(data)
        else:
            return self.check_data_values_abstract(data)

    def check_data_values_integers(self, data):
        for element in data:
            if element > self.c.ARG_MAX or element < self.c.ARG_MIN:
                print("Bad value:", element)
                exit()
        return data

    def check_data_values_abstract(self, data):
        # Można nadpisać tą funkcję jeżeli używamy abstrakcyjnego typu danych
        return data

    def get_binary_data_representation(self, data):
        bin_data = []
        for element in data:
            bin_data.append(self.c.element_to_bin[element])
        return bin_data

    def get_binary_vector_data_representation(self):
        # Zwraca zmienną string z zapisem binarnym elementów osobnika
        bin_data = self.get_binary_data_representation(self.data)
        bin_vec = []
        for element in bin_data:
            for number in element:
                bin_vec.append(number)
        self.bin_vec = bin_vec
        return self.bin_vec

    def check_if_exists(self, bin_vec):
        bin_data = self.slice_list(bin_vec, self.c.n)
        for bin_element in bin_data:
            if bin_element not in self.c.element_to_bin.values():
                return False
        return True

    def update_after_binary_change(self):
        self.get_new_bin_data()
        self.get_new_data()

    def slice_list(self, data_list, n):
        # Tnie listę na podane n elementów
        return [data_list[i:i + self.c.NUMBER_OF_BITS] for i in range(0, len(data_list), self.c.NUMBER_OF_BITS)]

    def get_element_with_bin_element(self, bin_element):
        return list(self.c.element_to_bin.keys())[list(self.c.element_to_bin.values()).index(bin_element)]

    def get_new_bin_data(self):
        self.bin_data = self.slice_list(self.bin_vec, self.c.n)
        return self.bin_data

    def get_new_data(self):
        new_data = []
        for bin_element in self.bin_data:
            new_data.append(self.get_element_with_bin_element(bin_element))
        self.data = new_data
        return self.data

    def to_string(self):
        return "Współrzędne: " + str(self.data) +  " Wartość: " + str(f(self.data)) + " \n"

    def to_dict(self):
        data_dict = dict({
            "x1": self.data[0],
            "x2": self.data[1],
            "x3": self.data[2],
            "x4": self.data[3]
        })
        return dict({
            "data": data_dict,
            "value": f(self.data)
        })

    def invert_bit_in_bit_vector(self, index):
        if self.bin_vec[index] == 0:
            self.bin_vec[index] = 1
        else:
            self.bin_vec[index] = 0

    def compare(self, individual):
        return self.data == individual.data

    # Getter
    def get_bin_vector(self):
        return self.bin_vec

    # Setter
    def set_bin_vector(self, bin_vec):
        self.bin_vec = bin_vec


if __name__=="__main__":
    ind = Individual([1, 2, -0, 3])
    tmp = []
    individual_list = []
    for i in range(-16, 16):
        individual_list.append(Individual([i, i , i, i]))

    for i in individual_list:
        before = i.data
        i.invert_bit_in_bit_vector(4)
        # if i.bin_vec[4] == 0:
        #     i.bin_vec[4] = 1
        # else:
        #     i.bin_vec[4] = 0
        i.update_after_binary_change()
        tmp.append([before, i.data ])

    pprint(tmp)