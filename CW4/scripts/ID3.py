# Autor: Karol Stepanienko


import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split

import numpy as np

from Tree import Tree
from Pair import Pair
from Constants import Constants

# Dataset
# Data format 150x4 numpy.ndarray
# Iris - irys, kwiatek
# sepal - działka kielicha (kwiatu)
# petal - płatek (kwiatu)
# Rows are samples
# Columns are:
# Sepal Length - Długość działki kielicha
# Sepal Width - Szerokość działki kielicha
# Petal Length - Długość płatka
# Petal Width - Szerokość płatka
#
# iris_data_full.target - classes which give discrete type of flower


class ID3:
    def __init__(self):

        self.c = Constants()

        # Init empty data sets
        self.x_train = np.empty(0)
        self.y_train = np.empty(0)
        self.x_validate = np.empty(0)
        self.y_validate = np.empty(0)
        self.x_test = np.empty(0)
        self.y_test = np.empty(0)

        # Init empty ID3 variables
        self.Y = set()
        self.D = set()
        self.tree = {}

        # Init empty pairs
        self.pairs_train = []
        self.pairs_validate = []
        self.pairs_test = []

    # Y = self.classes - set of all classes
    # D - input attributes
    # U = pairs - collection of training pairs ie.: self.petal_train
    # d - <0;3> - index of attribute in x vector
    # d_j - value of the d attribute in vector
    def ID3(self, Y, D, U, current_depth=1):
        if ID3.check_all_pairs_one_class(U):
            # All the pairs have the same class, so return class of the first element
            return U[0].y
        if len(D) == 0 or current_depth > self.c.max_ID3_tree_depth:
            return ID3.get_most_common_class(U)

        d = ID3.get_d_max_InfGain(D, U)
        D.remove(d)

        d_j_list = ID3.get_all_attribute_values(d, U)
        U_j_list = ID3.get_pairs_with_attribute_values(d, d_j_list, U)

        children = []
        for U_j in U_j_list:
            children.append(self.ID3(Y, D, U_j, current_depth + 1))

        return Tree(d, d_j_list, children)

    # Informational gain
    @staticmethod
    def InfGain(d, U) -> int:
        return ID3.I(U) - ID3.Inf(d, U)

    # Entropy of collection of pairs divided by values of attribute on d index
    @staticmethod
    def Inf(d, U) -> int:
        d_j_list = ID3.get_all_attribute_values(d, U)
        entropy_of_divided_collection = 0
        for d_j in d_j_list:
            U_j = ID3.get_all_pairs_with_attribute_value(d, U, d_j)
            entropy_of_divided_collection += len(U_j)/len(U) * ID3.I(U_j)
        return entropy_of_divided_collection

    # Entropy of the collection of pairs U
    @staticmethod
    def I(U) -> int:
        class_amounts = ID3.get_classes_frequency(pairs=U)
        entropy = 0
        for frequency in class_amounts.values():
            entropy += frequency * np.log(frequency)
        return -entropy

    @staticmethod
    def get_d_max_InfGain(D, U):
        max_InfGain = 0
        d_max_InfGain = 0
        for d in D:
            infGain = ID3.InfGain(d, U)
            if max_InfGain == 0 or max_InfGain < infGain:
                d_max_InfGain = d
                max_InfGain = infGain
        return d_max_InfGain

    @staticmethod
    def get_pairs_with_attribute_values(d, d_j_list, U):
        U_j_list = []
        for d_j in d_j_list:
            U_j_list.append(ID3.get_all_pairs_with_attribute_value(d, U, d_j))
        return U_j_list

    @staticmethod
    def get_all_pairs_with_attribute_value(d, U, d_j):
        pairs_with_the_same_attribute = []
        for pair in U:
            if pair.x[d] == d_j:
                pairs_with_the_same_attribute.append(pair)
        return pairs_with_the_same_attribute

    @staticmethod
    def get_all_attribute_values(d, U):
        """ Returns set of all d attribute values. """
        attribute_values = set()
        for pair in U:
            if pair.x[d] not in attribute_values:
                attribute_values.add(pair.x[d])
        return attribute_values

    # WORKS
    @staticmethod
    def get_classes_frequency(pairs):
        # Dictionary where:
        # keys - classes
        # value - frequency of class (amount of pairs that belong to class)
        class_amounts = {}

        # Get all classes and add them to class_amounts.keys()
        for pair in pairs:
            if pair.y not in class_amounts.keys():
                class_amounts[pair.y] = 0

        # Count the classes
        for pair in pairs:
            for c in class_amounts.keys():
                if pair.y == c:
                    class_amounts[c] += 1

        return class_amounts

    # WORKS
    @staticmethod
    def get_most_common_class(pairs) -> int:
        class_amounts = ID3.get_classes_frequency(pairs)
        most_common_class = None

        # Find most common class
        max_value = max(class_amounts.values())
        for c, value in class_amounts.items():
            if value == max_value:
                most_common_class = c

        return most_common_class

    # WORKS
    @staticmethod
    def check_all_pairs_one_class(pairs) -> bool:
        """ Returns true if all pairs have the same class. """
        first_pair_class = pairs[0].y
        for pair in pairs:
            if pair.y != first_pair_class:
                return False
        return True

    @staticmethod
    def get_pairs(x_vector, y_vector):
        pairs = []
        for i in range(0, len(x_vector)):
            pairs.append(ID3.get_pair(x_vector[i], y_vector[i]))
        return pairs

    @staticmethod
    def get_pair(x, y):
        return Pair(x, y)

    @staticmethod
    def print_pairs(pairs) -> None:
        for pair in pairs:
            print(pair)

    @staticmethod
    def plot_x_y(x, y, c=None):
        plt.scatter(x, y)
        plt.show()

    @staticmethod
    def divide_data_sets(x, y, train_size, test_size):
        x_train, x_rem, y_train, y_rem = train_test_split(x, y, train_size=train_size)
        x_validate, x_test, y_validate, y_test = train_test_split(x_rem, y_rem, test_size=test_size)

        return x_train, y_train, x_validate, y_validate, x_test, y_test

    @staticmethod
    def present_data(full, first, second):
        for i in range(0, 3):
            print(full[i])
            print(first[i], ",", second[i])

    @staticmethod
    def save_data_from_online():
        # Saving data for offline use
        iris_data_full = datasets.load_iris()
        ID3.save(iris_data_full)

    def init_all(self):
        self.init_ID3_variables()
        self.new_data_sets()
        self.init_pairs()

    def init_ID3_variables(self):
        self.Y = set(self.c.iris_data_full.target)
        self.D = set(range(0, len(self.c.iris_data_full.data[0])))
        self.tree = {}

    def new_data_sets(self):
        """ Divide data set and initialise data sets. """
        # Divide dataset to train, validate and test
        self.x_train, self.y_train, self.x_validate, self.y_validate, self.x_test, self.y_test = \
            self.divide_data_sets(
                self.c.iris_data_full.data, self.c.iris_data_full.target, self.c.train_size, self.c.test_size)

        return self.x_train, self.y_train, self.x_validate, self.y_validate, self.x_test, self.y_test

    def init_pairs(self):
        """ Creates pairs from divided datasets. """
        self.pairs_train = ID3.get_pairs(self.x_train, self.y_train)
        self.pairs_validate = ID3.get_pairs(self.x_validate, self.y_validate)
        self.pairs_test = ID3.get_pairs(self.x_test, self.y_test)
        return self.pairs_train, self.pairs_validate, self.pairs_test

    def run(self):
        self.init_all()
        self.tree = self.ID3(self.Y, self.D, U=self.pairs_train)

    def run_and_print(self):
        self.init_all()
        self.tree = self.ID3(self.Y, self.D, U=self.pairs_train)
        self.tree.print_tree()


if __name__ == '__main__':
    id3 = ID3()
    id3.run_and_print()
