# Autor: Karol Stepanienko


import numpy as np

from Constants import Constants
from Bayes import BayesClassifier


class Statistics:
    """
    Runs statistical calculation and gathers data about bayes algorithm results.
    """
    def __init__(self):
        self.bayes_classifier = BayesClassifier()

    def run_testing(self):
        percentages = []
        for i in range(Constants.n_stat):
            # if i % 5 == 0:
            #     print("Run: ", i)
            percentages.append(self.bayes_classifier.run_bayes_offline())
        # print(percentages)
        print("Classical lerning-testing results: ", np.mean(percentages), "% in ", Constants.n_stat, "runs.")
        return np.mean(percentages)

    def run_cross_validation(self):
        percentages = []
        for i in range(Constants.n_stat):
            # if i % 5 == 0:
            #     print("Run: ", i)
            percentages.append(self.bayes_classifier.run_cross_validation(Constants.n))
        # print(percentages)
        print("Cross validation results: ", np.mean(percentages), "% in ", Constants.n_stat, "runs.")
        return np.mean(percentages)

    def rotate_over_n(self):
        parameter_value_list = [i for i in range(2, 21)]
        best_n = 0.0
        best_quality = 0.0
        data = dict()
        for n in parameter_value_list:
            print("----------")
            print("Current n value: ", n)
            Constants.n = n # Overwrite current n
            self.bayes_classifier.data.init_all()
            test_q = self.run_testing()
            cross_validate_q = self.run_cross_validation()
            data[n] = [test_q, cross_validate_q, Constants.TRAIN_SIZE, Constants.TEST_SIZE]
        Statistics.print_results_latex(data)

    @staticmethod
    def print_results_latex(data):
        print("Latex table format.")
        print("-------------------")
        for param, values in data.items():
            for i, val in enumerate(values):
                if type(val) is float or type(val) is np.float64:
                    values[i] = round(val, 2)

            print(param, "   &   ",
                  values[0], "   &   ",
                  values[1], "   &   ",
                  values[2], "   &   ",
                  values[3],
                  "  \\\\")


if __name__ == "__main__":
    statistics = Statistics()
    # statistics.run_testing()
    # statistics.run_cross_validation()
    statistics.rotate_over_n()
