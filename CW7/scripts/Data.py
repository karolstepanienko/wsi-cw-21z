# Autor: Karol Stepanienko


import yaml
import numpy as np

import sklearn
from sklearn import datasets
from sklearn.model_selection import train_test_split

from Constants import Constants
from Pair import Pair


class Data:
    """
    Prepares data for use in Bayes algorithm.
    Creates pairs of attribute (x) and class (y) values.
    """
    def __init__(self):
        self.dataset_raw = Data.load_offline()

        # Init empty data sets
        self.x_train = np.empty(0)
        self.y_train = np.empty(0)
        self.x_test = np.empty(0)
        self.y_test = np.empty(0)

        # Init empty pairs
        self.pairs_train = []
        self.pairs_test = []

        # Sliced data for cross validation algorithm
        self.sliced_data = []

        # Dictionary
        # key - class
        # value - list of all attribute vectors that have this class
        self.class_and_data = dict()

        # Initialisation of all declared variables
        self.init_all()

        # Init set of classes
        Constants.CLASSES = self.get_classes(self.dataset_raw)
        # Init number of attributes
        Constants.NUMBER_OF_ATTRIBUTES = len(self.pairs_train[0].x)

    def init_all(self):
        """ Allows for initialisation and reinitialisation of all declared variables. """
        # Overwrite set sizes
        Constants.TRAIN_SIZE, Constants.TEST_SIZE = self.get_sizes()
        self.get_training_and_test_sets()
        self.init_pairs()
        # self.class_and_data = self.get_class_and_data(self.pairs_train)
        # self.sliced_data = self.get_cross_validation_split(Constants.n)

    def init_pairs(self):
        """ Creates pairs from divided datasets. """
        self.pairs_train = Data.get_pairs(self.x_train, self.y_train)
        self.pairs_test = Data.get_pairs(self.x_test, self.y_test)
        return self.pairs_train, self.pairs_test

    def get_cross_validation_split(self, k):
        """ Runs cross validation splitting of data into k sub-arrays. """
        all_pairs = self.pairs_train + self.pairs_test
        sliced_data = np.array_split(all_pairs, k)
        for i, data in enumerate(sliced_data):
            sliced_data[i] = list(data)
        return sliced_data

    def get_sizes(self):
        """ Returns TRAIN_SIZE and TEST_SIZE based on n value for cross_validation algorithm. """
        return 1 - 1/Constants.n, 1/Constants.n,

    @staticmethod
    def get_pairs(x_vector, y_vector):
        pairs = []
        for i in range(0, len(x_vector)):
            pairs.append(Pair(x_vector[i], y_vector[i]))
        return pairs

    def get_training_and_test_sets(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            self.dataset_raw.data,
            self.dataset_raw.target,
            train_size=Constants.TRAIN_SIZE, test_size=Constants.TEST_SIZE)

    @staticmethod
    def get_class_and_data(pairs):
        """ Creates a dictionary where all attribute vectors are assigned to their class. """
        class_and_data = dict()
        for pair in pairs:
            if pair.y not in list(class_and_data.keys()):
                class_and_data[pair.y] = [pair.x]
            else:
                class_and_data[pair.y].append(pair.x)
        return class_and_data

    @staticmethod
    def get_classes(dataset_raw):
        return set(dataset_raw['target'])

    @staticmethod
    def save_data_from_online():
        # Saving data for offline use
        Data.save(datasets.load_wine())

    @staticmethod
    def save(data_to_save):
        with open("../data/" + Constants.DATASET_NAME + ".yaml", 'a+') as file:
            yaml.dump(data_to_save, file)

    @staticmethod
    def load_offline() -> sklearn.utils.Bunch:
        """ Returns exactly the same as datasets.load_wine(). """
        with open("../data/" + Constants.DATASET_NAME + ".yaml") as file :
            loaded = yaml.load(file, Loader=yaml.Loader)
        return loaded

    @staticmethod
    def load_online() -> sklearn.utils.Bunch:
        return datasets.load_wine()


if __name__ == "__main__":
    # Data.save_data_from_online()
    data = Data()
    print(data.dataset_raw.keys())
    # print(data.dataset_raw['DESCR'])
    # print(data.dataset_raw['data'])
    # print(data.dataset_raw['feature_names'])
    # print(data.dataset_raw['frame'])
    # print(data.dataset_raw['target'])
    # print(data.dataset_raw['target_names'])
    data.init_all()
    data.cross_validation_split(2)
