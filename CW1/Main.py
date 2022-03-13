# Autor: Karol Stepanienko


import sys
from Functions import Functions
from Graph import Graph2D, Graph3D
from Constants import Constants


class Gradient_descent_algorithm:
    def __init__(self):
        self.f = Functions()
        self.c = Constants()

    def find_minimum(self, X):
        # X - initialised point
        X = [X]
        i = 0  # Counts the number of rotations
        # Main loop
        while(self.check_stop_gradient(X) and i < self.c.MAX_ROTATIONS):
            X.append(self.get_new_point(X[len(X) - 1]))
            i = i + 1
        return X, i


class Gradient_descent_algorithm_one_variable(Gradient_descent_algorithm):

    def get_new_point(self, x):
        return x - self.c.SINGLE_ALFA * self.f.nabla_g(x)

    def check_stop_gradient(self, X):
        # Compare the derivative value (function speed of change) with constant
        return not (pow(self.f.nabla_g(X[len(X) - 1]), 2) <= self.c.EPSILON_GRADIENT)

    def cal_RMSE(self, X):
        return self.f.RMSE(X[len(X) - 1], self.c.X_IDEAL_POINT)

    def run(self):
        # X - point coordinates
        X, i = self.find_minimum(self.c.X_START)
        print("Number of iterations: " + str(i))
        print("Last calculated point: " + str(X[len(X) - 1]))
        print("Error RMSE value: " + str(self.cal_RMSE(X)))
        return X, i


class Gradient_descent_algorithm_two_variables(Gradient_descent_algorithm):

    def get_new_point(self, x1x2):
        tmp_list = []
        for x, i in zip(x1x2, range(len(x1x2))):
            tmp_list.append(x - self.c.DOUBLE_ALFA * self.f.nabla_f(x1x2)[i])
        return tmp_list

    def check_stop_gradient(self, X1X2):
        # Compare the derivative value (function speed of change) with constant
        [dx1, dx2] = self.f.nabla_f(X1X2[len(X1X2) - 1])
        return not (pow(pow(dx1, 2) + pow(dx2, 2), 1/2) <= self.c.EPSILON_GRADIENT)

    def cal_RMSE(self, X1X2):
        RMSE = 0
        for x, x_ideal in zip(X1X2[len(X1X2) - 1], self.c.X1X2_IDEAL_POINTS):
            RMSE = RMSE + self.f.RMSE(x, x_ideal)
        return RMSE

    def run(self):
        # X1X2 - point coordinates
        X1X2, i = self.find_minimum(self.c.X1X2_START)
        print("Number of iterations: " + str(i))
        print("Last calculated point: " + str(X1X2[len(X1X2) - 1]))
        print("Error RMSE value: " + str(self.cal_RMSE(X1X2)))
        return X1X2, i


class Main:
    """Runs requested algorithm."""

    def run(self):
        if len(sys.argv) == 1 or sys.argv[1] == 'f':
            # Runs the algorithm for function f
            gda2 = Gradient_descent_algorithm_two_variables()
            X1X2, i = gda2.run()

            graph3D = Graph3D(X1X2, i)
            graph3D.plot()
        elif sys.argv[1] == 'g':
            # Runs the algorithm for function g
            gda1 = Gradient_descent_algorithm_one_variable()
            X, i = gda1.run()

            graph2D = Graph2D(X, i)
            graph2D.plot()
        else:
            print(sys.argv[1])
            print("Niepoprawne argumenty.")


if __name__ == "__main__":
    main = Main()
    main.run()
