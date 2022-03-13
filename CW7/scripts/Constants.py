# Autor: Karol Stepanienko


class Constants:
    """
    Contains constant values used by Bayes algorithm.
    """
    DATASET_NAME = "wine"

    # Has to be initialised externally
    NUMBER_OF_ATTRIBUTES = 0

    TRAIN_SIZE = 0.5
    TEST_SIZE = 0.5

    # Set of classes
    # Has to be initialised externally
    CLASSES = None

    # Stats dictionary keys
    ATTRIBUTES_MEANS = 0
    COL_LEN = 1
    STANDARD_DEVIATION = 2
    CLASS_PROBABILITY = 3

    # Cross validation parameter
    # Decides into how many sub-arrays data will be sliced
    n = 2

    # Enables running tests multiple times
    # for gathering statistical data
    n_stat = 25
