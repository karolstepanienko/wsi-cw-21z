# Autor: Karol Stepanienko


import numpy as np

from ID3 import ID3
from Tree import Tree


class TestID3:
    def __init__(self):
        self.id3 = ID3()
        self.good_fits = 0
        # Dictionary where:
        # keys - pairs from test collection
        # values- predicted classes
        self.predictions = dict()

    def get_good_fits(self):
        return self.good_fits

    def predict_classes(self, full_tree, pairs_test):
        self.predictions = dict()
        for pair in pairs_test:
            predicted_class = TestID3.predict_class(pair, full_tree)
            self.predictions[pair] = predicted_class
        return self.predictions

    @staticmethod
    def predict_class(pair, current_tree):
        predicted_class = None
        # If the value of this tree parameter is in keys of the tree
        if pair.x[current_tree.node] in current_tree.children.keys():
            # Get class or tree assigned to that parameter value
            tree_or_class = current_tree.children[pair.x[current_tree.node]]
            if type(tree_or_class) is np.int32:
                # Type is int (class)
                predicted_class = tree_or_class
            else:
                # print(type(tree_or_class))
                # Type is tree
                tmp_tree = tree_or_class
                predicted_class = TestID3.predict_class(pair, tmp_tree)
        else:
            # Tree did not learn about this value for this parameter
            all_subtrees = TestID3.get_all_subtrees(current_tree)
            if len(all_subtrees) != 0:
                for tree in all_subtrees:
                    result = TestID3.predict_class_once(pair, tree)
                    if result is not None:
                        predicted_class = result

        if predicted_class is None:
            # Tree did not learn about this value for this parameter or
            # no other trees were found so return the most common class
            # If classes are equally common return first one in the dict
            predicted_class = TestID3.get_most_common_class(current_tree)
        return predicted_class

    @staticmethod
    def predict_class_once(pair, tree):
        if pair.x[tree.node] in tree.children.keys():
            return tree.children[pair.x[tree.node]]
        else:
            return None

    @staticmethod
    def get_all_subtrees(tree):
        subtrees = []
        for value in tree.children.values():
            if type(value) is Tree:
                subtrees.append(value)
                subtrees += TestID3.get_all_subtrees(value)
        return subtrees

    @staticmethod
    def get_most_common_class(current_tree):
        classes_and_trees = current_tree.children.values()
        classes = TestID3.remove_elements_with_type(classes_and_trees, Tree)
        return max(set(classes), key=classes.count)

    @staticmethod
    def remove_elements_with_type(list_of_elements, type_to_remove):
        new_list = []
        for element in list_of_elements:
            if type(element) is not type_to_remove:
                new_list.append(element)
        return new_list

    def calc_fit_error(self):
        """ Calculates the amount of good fits. """
        good_fits = 0
        for pair, predicted_class in self.predictions.items():
            if pair.y == predicted_class:
                good_fits += 1
        return good_fits

    def run(self, test_or_validate):
        self.id3.run()
        if test_or_validate == "test":
            self.predictions = self.predict_classes(self.id3.tree, self.id3.pairs_test)
        elif test_or_validate == "validate":
            self.predictions = self.predict_classes(self.id3.tree, self.id3.pairs_validate)
        self.good_fits = self.calc_fit_error()
        return self.good_fits

    def run_and_print(self):
        self.id3.run()
        self.predictions = self.predict_classes(self.id3.tree, self.id3.pairs_test)
        self.good_fits = self.calc_fit_error()
        print("Good fits: ", self.good_fits)
        print("Good fits percentage: ", self.good_fits / self.id3.c.test_size * 100, "%")


if __name__ == "__main__":
    testID3 = TestID3()
    testID3.run_and_print()
