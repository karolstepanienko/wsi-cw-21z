# Autor: Karol Stepanienko


import sklearn
import yaml
from sklearn.preprocessing import KBinsDiscretizer
import numpy as np


class Constants:
    def __init__(self):
        # Load data
        self.iris_data_full = Constants.load()
        # print(self.iris_data_full.target_names)

        # Number of discretisation values
        # Shouldn't be lower than 15
        self. discretisation_bins = 15
        # Attributes to integers
        self.iris_data_full.data = self.discretisation_KBinsDiscretizer(self.iris_data_full.data)
        # self.iris_data_full.data = ID3.x_to_integers(self.iris_data_full.data, multiplier=10)

        # How many time to run the simulation
        self.n = 100

        # Defines maximum tree depth created by ID3 algorithm
        # If depth is to be exceeded, the most common function will be returned
        # instead of deeper tree
        # Should be equal to 1 or higher
        self.max_ID3_tree_depth = 4

        # Constant strings used as options in methods
        self.test_str = "test"
        self.valiadate_str = "validate"

        # Number of data points
        self.dataset_length = len(self.iris_data_full.data)

        # Number of values in every x_vector
        self.data_vector_length = len(self.iris_data_full.data[0])

        # All possible (and reasonable) tree depths
        # Tree can have much larger depth but,
        # it will never be used if it will be larger than number of elements in x_vector
        self.possible_tree_depths = Constants.get_possible_tree_depths(self.data_vector_length)

        # Displays warnings if max depth of the tree was set improperly
        Constants.check_max_depth(self.max_ID3_tree_depth, self.possible_tree_depths)

        # Define train, validate, test datasets sizes
        # Methods used bellow give the same results
        # self.train_size, self.validate_size,  self.test_size = self.automatic_size(train_size_scale=0.8)
        self.train_size, self.validate_size,  self.test_size = self.manual_size(0.8, 0.1, 0.1)

    def manual_size(self, train_size_scale, validate_size_scale, test_size_scale):
        """ Allows for setting collection sizes manually. Parameter values should add up to 1. """
        train_size = int(train_size_scale * self.dataset_length)
        validate_size = int(validate_size_scale * self.dataset_length)
        test_size = int(test_size_scale * self.dataset_length)
        return train_size, validate_size, test_size

    def automatic_size(self, train_size_scale):
        """ Sets collection sizes automatically, based on training set to full dataset length ratio. """
        train_size = int(train_size_scale * self.dataset_length)
        validate_size = int((self.dataset_length - train_size) / 2)
        test_size = int((self.dataset_length - train_size) / 2)
        return train_size, validate_size, test_size

    @staticmethod
    def save(data):
        with open("../data/iris.yaml", 'a+') as file:
            yaml.dump(data, file)

    @staticmethod
    def load() -> sklearn.utils.Bunch:
        """ Returns exactly the same as datasets.load_iris(). """
        with open("../data/iris.yaml") as file :
            loaded = yaml.load(file, Loader=yaml.Loader)
        return loaded

    @staticmethod
    def get_possible_tree_depths(data_vector_length):
        return list(range(1, data_vector_length + 1))

    @staticmethod
    def check_max_depth(max_depth, possible_depths):
        if max_depth < min(possible_depths):
            print("ERROR:")
            print("Depth value must be 1 or larger.")
            exit()
        elif max_depth > max(possible_depths):
            print("WARNING:")
            print("Unreasonably large depth value:", max_depth)
            print("It shouldn't be larger than:", possible_depths[len(possible_depths) - 1])

    def discretisation_KBinsDiscretizer(self, x_data):
        est = KBinsDiscretizer(n_bins=self.discretisation_bins, encode='ordinal', strategy='uniform')
        est.fit(x_data)
        x_data_t = est.transform(x_data)
        return x_data_t

    @staticmethod
    def x_to_integers(x_data, multiplier):
        for vector in x_data:
            for i, element in enumerate(vector):
                vector[i] = vector[i] * multiplier
        # Convert to integers
        data = np.int64(x_data)
        return data