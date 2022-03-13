# Autor: Karol Stepanienko


from sklearn.metrics import classification_report

from TestID3 import TestID3


class Statistics:
    def __init__(self):
        self.testID3 = TestID3()

    def get_data(self, test_or_validate):
        good_fits_list = []
        for i in range(1, self.testID3.id3.c.n + 1):
            if i % 10 == 0 and test_or_validate != self.testID3.id3.c.valiadate_str:
                print("Run: ", i)
            good_fits_list.append(self.testID3.run(test_or_validate))
        return good_fits_list

    def calc_average_fit(self, test_or_validate):
        good_fits_list = self.get_data(test_or_validate)
        average_fit = sum(good_fits_list) / len(good_fits_list)
        return average_fit

    def run(self, test_or_validate):
        """ Runs algorithm self.Constants.n times, calculates and returns average fit. """
        return self.calc_average_fit(test_or_validate)

    def run_and_print(self):
        calc_average_fit = self.calc_average_fit("test")
        print("Algorithm was run ", self.testID3.id3.c.n, " times.")
        print("Average fit:", calc_average_fit)
        print("Average fit percentage:", calc_average_fit / self.testID3.id3.c.test_size * 100, "%")


if __name__ == "__main__":
    s = Statistics()
    s.run_and_print()
