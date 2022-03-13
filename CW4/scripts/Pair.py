# Autor: Karol Stepanienko


# A pair of x_values - vector
# and y_value - class (defines the type of the object, described by x_values)
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: " + str(self.x) + "    " + "y: " + str(self.y)
