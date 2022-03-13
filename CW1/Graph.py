# Autor: Karol Stepanienko


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from Functions import Functions
from Constants import Constants


class Graph_commons:
    def __init__(self):
        self.lw_continuous = 4
        self.lw_track = 3
        self.ms_point = 10
        self.c = Constants()

    def get_graph_lim(self, X):
        track_width = abs(X[0] - X[len(X) - 1])
        if X[0] < X[len(X) - 1]:
            left = X[0]
            right = X[len(X) - 1]
        else:
            left = X[len(X) - 1]
            right = X[0]
        r_bound = right + track_width / 2
        l_bound = left - track_width / 2
        return l_bound, r_bound

    def to_single_vectors(self, X1X2):
        X1 = []
        X2 = []
        for x1x2 in X1X2:
            X1.append(x1x2[0])
            X2.append(x1x2[1])
        return X1, X2

    def set_graph_size(self):
        # return plt.figure(figsize=(20.8, 11.7))
        # return plt.figure(figsize=(16, 9))
        # return plt.figure(figsize=(12.8, 7.2))
        return plt.figure(figsize=(9.6, 5.4))


class Graph2D(Graph_commons):
    def __init__(self, X, i):
        super(Graph2D, self).__init__()
        self.f = Functions()
        self.X = X
        self.i = i
        self.Y = [self.f.g(i) for i in self.X]
        self.X_continuous = [i for i in np.arange(self.get_graph_lim(
            self.X)[0], self.get_graph_lim(self.X)[1], 0.01)]
        self.Y_continuous = [self.f.g(i) for i in self.X_continuous]

    def plot(self):
        self.set_graph_size()

        # Plot reference line
        plt.plot(
            self.X_continuous,
            self.Y_continuous,
            color=[0, 0.4470, 0.7410],
            linewidth=self.lw_continuous,
            label="Referencyjny wykres funkcji",
            zorder=0
        )

        # Plot track created by the algorithm
        plt.scatter(
            self.X,
            self.Y,
            color=[0.8500, 0.3250, 0.0980],
            linewidth=self.lw_track,
            label="Ścieżka wygenerowana przez algorytm gradientowy",
            zorder=1
        )

        # Mark start point
        start_point = plt.plot(self.X[0],
                               self.Y[0],
                               color=[0.6350, 0.0780, 0.1840],
                               marker='o',
                               markersize=self.ms_point,
                               label="Punkt startowy",
                               zorder=2
                               )
        plt.annotate(
            "(" + str(round(self.X[0], 2)) +
            ", " + str(round(self.Y[0], 2)) + ")",
            [self.X[0] + 0.01, self.Y[0]])

        # Mark end point
        end_point = plt.plot(self.X[len(self.X) - 1],
                             self.Y[len(self.Y) - 1],
                             color=[0.4660, 0.6740, 0.1880],
                             marker='o',
                             markersize=self.ms_point,
                             label="Punkt końcowy"
                             )
        plt.annotate(
            "(" + str(round(self.X[len(self.X) - 1], 2)) +
            ", " + str(round(self.Y[len(self.Y) - 1], 2)) + ")",
            [self.X[len(self.X) - 1] - 0.01, self.Y[len(self.Y) - 1] + 0.2])

        # Add axes
        # plt.axvline(x=0, color="black", linewidth=0.4)
        # plt.axhline(y=0, color="black", linewidth=0.4)

        # Add a legend and choose it's localisation
        plt.legend(loc=2)

        # Set graph labels
        self.add_graph_labels()

        # Set plot margins
        plt.margins(x=0)

        # Save the plot in a vector graphics file
        # plt.savefig("./sprawozdanie/2D.svg")
        plt.show()

    def add_graph_labels(self):
        plt.title("Algorytm gradientu prostego dla funkcji g(x). Liczba iteracji: " +
                  str(self.i) + ". Punkt startowy: " + str(self.c.X_START))
        plt.xlabel("x")
        plt.ylabel("y")


class Graph3D(Graph_commons):
    def __init__(self, X1X2, i):
        super(Graph3D, self).__init__()

        self.f = Functions()
        self.X1, self.X2 = self.to_single_vectors(X1X2)
        self.Y = [self.f.f_element(x1, x2) for x1, x2 in zip(self.X1, self.X2)]
        self.X1_coordinates, self.X2_coordinates = np.meshgrid(
            self.X1, self.X2)
        self.Y_coordinates = self.f.f_element(
            self.X1_coordinates, self.X2_coordinates)

        # Manual 3D graph limits setting
        bound = 3
        X1_lbound = -bound * 0.5
        X1_rbound = bound * 0.2
        X2_lbound = -bound * 0.5
        X2_rbound = bound * 0.2

        # Plane of function for reference purposes
        self.X1_continuous_coordinates, self.X2_continuous_coordinates = np.meshgrid(
            np.arange(2 * X1_lbound, 2 * X1_rbound, 0.5), np.arange(2 * X2_lbound, 2 * X2_rbound, 0.5))

        self.Y_continuous_coordinates = self.f.f_element(
            self.X1_continuous_coordinates, self.X2_continuous_coordinates)

    def add_graph_labels(self, ax):
        ax.set_xlabel(r'$x_1$')
        ax.set_ylabel(r'$x_2$')
        ax.set_zlabel(r'$f(x_1, x_2)$')

    def plot(self):
        fig = self.set_graph_size()

        ax = Axes3D(fig, auto_add_to_figure=False, title="lol")
        self.add_graph_labels(ax)
        fig.add_axes(ax)

        # Reference function plotting
        ax.plot_wireframe(
            self.X1_continuous_coordinates,
            self.X2_continuous_coordinates,
            self.Y_continuous_coordinates,
            color='#0072BD',
            linewidth=2
        )

        # Plot track created by the algorithm
        ax.scatter(
            self.X1,
            self.X2,
            self.Y,
            color=[0.8500, 0.3250, 0.0980],
            linewidth=self.lw_track + 2
        )

        # plt.savefig("CW1/sprawozdanie/3D.svg")
        plt.show()
