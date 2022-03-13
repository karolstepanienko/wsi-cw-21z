# Autor: Karol Stepanienko


import numpy as np
from copy import deepcopy

from Constants import Constants
from Data import Data


class BayesClassifier:
    """
    Implementation of Bayes naive classifier.
    """
    def __init__(self):
        self.data = Data()
        # Model as a dictionary
        # key - class value
        # value - statistics for class
        self.model = dict()

    def re_init(self):
        self.data.init_all()
        self.model = dict()

    @staticmethod
    def get_class_probabilities(pairs):
        """
        Returns probability of attribute belonging to the class based on the amount of attributes
        assigned to that class.
        """
        class_probabilities = dict()
        # Sum
        for pair in pairs:
            if pair.y not in class_probabilities.keys():
                class_probabilities[pair.y] = 1
            else:
                class_probabilities[pair.y] += 1

        # Normalise sums
        for key, value in class_probabilities.items():
            class_probabilities[key] = value / len(pairs)
        return class_probabilities

    @staticmethod
    def get_attribute_probabilities(model, pair):
        attribute_probabilities = dict()
        for class_val, stats in model.items():
            attribute_probabilities[class_val] = 0  # Init as zeros
            means = model[class_val][Constants.ATTRIBUTES_MEANS]
            stds = model[class_val][Constants.STANDARD_DEVIATION]
            for i in range(len(pair.x)):
                # Attribute probabilities sum
                attribute_probabilities[class_val] += np.log(BayesClassifier.gauss_distribution(pair.x[i], means[i], stds[i]))
            # Class probability multiply
            attribute_probabilities[class_val] *= model[class_val][Constants.CLASS_PROBABILITY]
        return attribute_probabilities

    @staticmethod
    def get_prediction(model, pair):
        """ Predict class value of a given pair. """
        attribute_probabilities = BayesClassifier.get_attribute_probabilities(model, pair)
        predicted_class = max(attribute_probabilities, key=attribute_probabilities.get)
        return predicted_class

    @staticmethod
    def gauss_distribution(x, mean, standard_deviation):
        return 1 / (standard_deviation * np.sqrt(2 * np.pi)) * np.exp(-0.5 * pow((x - mean) / standard_deviation, 2))

    @staticmethod
    def get_stats(attribute_vectors):
        """ Calculates mean value for every attribute in vertical column. """
        attribute_stats = dict()
        attribute_stats[Constants.ATTRIBUTES_MEANS] = []
        attribute_stats[Constants.STANDARD_DEVIATION] = []
        attribute_stats[Constants.COL_LEN] = len(attribute_vectors)
        for column in zip(*attribute_vectors):
            attribute_stats[Constants.ATTRIBUTES_MEANS].append(np.mean(column))
            attribute_stats[Constants.STANDARD_DEVIATION].append(np.std(column))
        return attribute_stats

    def naive_bayes(self, pairs_train):
        """ Create model assuming that there is no correlation between the attributes (naive). """
        class_probabilities = BayesClassifier.get_class_probabilities(pairs_train)
        class_and_data = self.data.get_class_and_data(pairs_train)
        for class_val, attribute_vectors in class_and_data.items():
            self.model[class_val] = BayesClassifier.get_stats(attribute_vectors)
            self.model[class_val][Constants.CLASS_PROBABILITY] = class_probabilities[class_val]
        return self.model

    @staticmethod
    def get_prediction_percentage(model, pairs_to_test_against):
        """ Returns percentage of good predictions. """
        good_predictions = 0
        for pair in pairs_to_test_against:
            prediction = BayesClassifier.get_prediction(model, pair)
            if prediction == pair.y:
                # print("Predicted: ", prediction)
                # print("Real: ", pair.y)
                good_predictions += 1
        return good_predictions / len(pairs_to_test_against) * 100

    def run_cross_validation_once(self, pairs_train, pairs_test):
        """ Returns results in one run of cross validation algorithm. """
        self.re_init()
        model = self.naive_bayes(pairs_train)
        return self.get_prediction_percentage(model, pairs_test)

    def run_cross_validation(self, k):
        """ Runs cross validation algorithm k times and returns percentage results mean. """
        percentages = []
        sliced_data = self.data.get_cross_validation_split(k)
        unchanged_sliced_data = deepcopy(sliced_data)
        for i, pairs_test in enumerate(sliced_data):
            sliced_data = deepcopy(unchanged_sliced_data)

            # Create list of pairs for training set
            sliced_data.pop(i)

            # Create training set
            pairs_train = []
            for data in sliced_data:
                pairs_train += data

            percentages.append(self.run_cross_validation_once(pairs_train, pairs_test))
        # print(percentages)
        return np.mean(percentages)

    def run_cross_validation_online(self):
        percentages_mean = self.run_cross_validation(Constants.n)
        print("Cross validation results: ", percentages_mean, "% for", Constants.n, "data splits")

    def run_bayes_offline(self):
        self.re_init()
        self.naive_bayes(self.data.pairs_train)
        return self.get_prediction_percentage(self.model, self.data.pairs_test)

    def run_testing_online(self):
        """ Runs a classic learning and testing against testing set. """
        prediction_percentage = self.run_bayes_offline()
        print("Classical learning-testing results:", prediction_percentage,
              "%. Train size:", Constants.TRAIN_SIZE, " Test size:", Constants.TEST_SIZE)


if __name__ == "__main__":
    bayes_classifier = BayesClassifier()
    bayes_classifier.run_testing_online()
    bayes_classifier.run_cross_validation_online()
