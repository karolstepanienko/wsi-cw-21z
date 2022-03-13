# Autor: Karol Stepanienko


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from FileManagement import Loading

class Graph:
    def __init__(self):
        self.loading = Loading('u_10_200.yaml')
        self.data = self.loading.loaded

    def get_runs(self):
        runs = []
        for ID in range(len(self.data.keys())):
            runs.append(self.data[ID])
        return runs

    def get_us(self):
        us = []
        for run in self.get_runs():
            us.append(run['u'])
        return us

    def get_standard_deviations(self):
        standard_deviations = []
        for run in self.get_runs():
            standard_deviations.append(run['standard_deviation'])
        return standard_deviations

    def string(self, old_list):
        new_list = []
        for element in old_list:
            new_list.append(str(element))
        return new_list

    def graph_histogram_standard_deviation(self):
        x_labels = self.get_us()
        data = self.get_standard_deviations()
        data_series = pd.Series(data)

        plt.figure(figsize=(12, 8))
        ax = data_series.plot(kind="bar")
        ax.set_title('Wartość odchylenia standardowego dla zmiennej liczby osobników w populacji')
        ax.set_xlabel("Liczba osobników w populacji")
        ax.set_ylabel("Wartość odchylenia standardowego")
        ax.set_xticklabels(x_labels)
        
        rects = ax.patches

        plt.show()


if __name__ == "__main__":
    graph = Graph()
    graph.graph_histogram_standard_deviation()

