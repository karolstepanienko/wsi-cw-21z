# Autor: Karol Stepanienko


from Statistics import Statistics


class ChooseDepth:
    def __init__(self):
        self.statistics = Statistics()
        # Dictionary where keys are fitness values and values are corresponding max depth settings
        self.average_fitness = dict()
        self.best_fitness = 0
        self.best_depth = 0

    def run_and_print(self):
        self.average_fitness = dict()
        for depth_val in self.statistics.testID3.id3.c.possible_tree_depths:
            # Set one of the possible depth values
            self.statistics.testID3.id3.c.max_ID3_tree_depth = depth_val
            fitness = self.statistics.run(test_or_validate=self.statistics.testID3.id3.c.valiadate_str)
            self.average_fitness[fitness] = depth_val
            self.print_loop_results(depth_val, fitness)
        self.print_end_results()

    def test_with_test_collection(self):
        # Set to best depth val
        self.statistics.testID3.id3.c.max_ID3_tree_depth = self.best_depth
        fitness = self.statistics.run(test_or_validate=self.statistics.testID3.id3.c.test_str)
        print("Testing with test collection for the best depth:", self.best_depth)
        print("Fitness was:", fitness, "which is", fitness / self.statistics.testID3.id3.c.test_size * 100, "%")

    def print_loop_results(self, depth_val, fitness):
        print("For depth:", depth_val, "Fitness was:", fitness)

    def print_end_results(self):
        self.best_fitness = max(self.average_fitness.keys())
        self.best_depth = self.average_fitness[self.best_fitness]

        print("Best depth:", self.best_depth, "Best fitness:", self.best_fitness,
              "which is", self.best_fitness / self.statistics.testID3.id3.c.validate_size * 100, "%")
        self.test_with_test_collection()


if __name__ == "__main__":
    choose_depth = ChooseDepth()
    choose_depth.run_and_print()