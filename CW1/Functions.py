# Autor: Karol Stepanienko


import math


# Contains methods returning value of functions given in the task content
class Functions:
    def f(self, x1x2):
        return pow(x1x2[0], 2) + pow(x1x2[1], 2)

    def f_element(self, x1, x2):
        return pow(x1, 2) + pow(x2, 2)

    def nabla_f(self, x1x2):
        return [2 * x1x2[0], 2 * x1x2[1]]
    
    def g(self, x):
        return pow(x, 2) - 10 * math.cos(2 * math.pi * x) + 10
    
    def nabla_g(self, x):
        return 2*x + 20 * math.pi * math.sin(2 * math.pi * x)

    def RMSE(self, a, b):
        return pow(pow(a - b, 2), 0.5)

