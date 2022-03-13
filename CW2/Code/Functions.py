# Autor: Karol Stepanienko


import numpy as np
from numpy import sin

from Constants import Constants

"""
Functions.py
    Zawiera definicję dunkcji celu.
    Implementacja funkcji może zostać łatwo zmieniona, niezależnie od algorytmu.
"""

def f(X):
    if type(X[0]) is int or \
        type(X[0]) is np.int16 or \
        type(X[0]) is np.int32 or \
        type(X[0]) is np.int64:
        return f_single_specimen(X)
    elif type(X[0]) is list:
        return f_vector(X)
    else:
        return f_abstract(X)

# Liczy wartość funkcji celu dla podanego wektora argumentów
def f_single_specimen(X):
    # X1 = X[0]
    # X2 = X[1]
    # X3 = X[2]
    # X4 = X[3]

    comp_1 = (X[0] + 2 * X[1] - 7)**2
    comp_2 = (2 * X[0] + X[1] - 5)**2
    comp_3 = (sin(1.5 * X[2]))**3
    comp_4 = ((X[2] - 1)**2) * (1 + (sin(1.5 * X[3]))**2)
    comp_5 = ((X[3] - 1)**2) * (1 + (sin(X[3]))**2)

    return comp_1 + comp_2 + comp_3 + comp_4 + comp_5

def f_vector(X_vector):
    results = []
    for X in X_vector:
        results.append(f_single_specimen(X))
    return results

# Przykład funkcji dla innego problemu dyskretnego
# Ta funckja musi nadpisywać funkcję f dla potrzeb innego problemu
def f_abstract(X):
    value = 10
    if X[0] == 'a':
        value = -1
    elif X[0] == 'b':
        value = 2
    elif X[0] == 'c':
        value = 3
    elif X[0] == 'd':
        value = 4
    elif X[0] == 'e':
        value = 5
    elif X[0] == 'f':
        value = 6
    elif X[0] == 'g':
        value = 7
    elif X[0] == 'h':
        value = 8
    else:
        value = 10
    return value
