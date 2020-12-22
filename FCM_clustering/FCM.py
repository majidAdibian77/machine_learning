import csv
import math
import random
import matplotlib.pyplot as plt

class FCM:
    def __init__(self, file_path, number_of_cluster, m):
        self.number_of_cluster = number_of_cluster
        self.file_path = file_path
        self.m = m
        self.points = []
        self.centers = []
        self.U = []
        self.diff_centers = 100

    def read_file(self):
        """
        This def is for reading info from file and save in a list
        """
        file = open(self.file_path, 'r')
        lines = file.readlines()
        points = []
        for line in lines[1:]:
            point = line.split(',')
            p = [float(xi) for xi in point]
            points.append(p)
        self.points = points

    def show_points(self):
        points = self.points
        centers = self.centers
        fig, diagram = plt.subplots(1, 1)
        diagram.scatter([X[0] for X in points], [X[1] for X in points], color='r', Label='all points')
        diagram.scatter([X[0] for X in centers], [X[1] for X in centers], color='b', label='centers')
        diagram.set_xlabel('X0')
        diagram.set_ylabel('X1')
        diagram.set_title('all points and center of each cluster')
        diagram.legend()
        plt.show()

    def show_ares(self):
        """
        This def shows area of all clusters
        """
        points = []
        for x in range(0, 100):
            for y in range(0, 100):
                points.append([x/100, y/100])
        U = self.compute_U(points)
        for i in range(len(points)):
            min = math.inf
            points[i].append(0)
            for c in range(len(self.centers)):
                if U[i][c] < min:
                    points[i][2] = c
                    min = U[i][c]

        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white', 'blue', 'green', 'red']
        fig, diagram = plt.subplots(1, 1)
        for i in range(self.number_of_cluster):
            x_points_of_this_cluster = [[point[0] for point in points if point[2]==i]]
            y_points_of_this_cluster = [[point[1] for point in points if point[2]==i]]
            diagram.scatter(x_points_of_this_cluster, y_points_of_this_cluster, color=colors[i])
        diagram.set_xlabel('X0')
        diagram.set_ylabel('X1')
        diagram.set_title('area of clusters')
        plt.show()

    def compute_entropy(self):
        """
        This def calculates entropy of this state
        This is used for finding best number of clusters
        :return: entropy
        """
        ent = 0
        U = self.U
        for i in range(len(self.points)):
            for c in range(len(self.centers)):
                ent += (U[i][c] * math.log2(U[i][c]))
        ent = -ent
        return ent

    def compute_reconstruction_error(self):
        """
        This def calculates reconstruction error of this state
        This is used for finding best number of clusters
        :return: reconstruction error
        """
        reconstruction_error = 0
        U = self.U
        centers = self.centers
        points = self.points
        for i in range(len(points)):
            uv = [0 for i in range(len(centers[0]))]
            for c in range(len(centers)):
                for k in range(len(centers[0])):
                    uv[k] += (U[i][c] * centers[c][k])
            reconstruction_error += (1/self.compute_distance_to_one_center(points[i], uv, 3))
        return reconstruction_error

    def select_random_centers(self):
        """
        This def choice center of clusters randomly
        It is used in start of algorithm
        """
        centers = random.choices(self.points, k=self.number_of_cluster)
        self.centers = centers

    def compute_distance_to_one_center(self, point, center, m):
        """
        This def computes the numerator of computation of U.
        For that, this def computes distance of one point to one center
        :param point: a list of float numbers that shows place of point
        :param center: a list of float numbers that shows place of center point
        :param m: is used in numerator of computation of U.
        """
        d = 0
        for i in range(len(point)):
            d = d + ((point[i] - center[i]) ** 2)
        if d == 0:
            return 0
        d = (1/math.sqrt(d)) ** (2/(m-1))
        return d

    def compute_distance_to_all_centers(self, point, m):
        """
        This def computes the denominator of computation of U.
        For that, this def computes distance of one point to all centers of clusters
        :param point: a list of float numbers that shows place of point
        :param m: is used in denominator of computation of U.
        """
        d = 0
        centers = self.centers
        for c in range(len(centers)):
            d += self.compute_distance_to_one_center(point, centers[c], m)
        return d

    def compute_U(self, points):
        """
        This def computes U_ic for all points and centers of clusters.
        :returns: U
        """
        points = points
        centers = self.centers
        m = self.m
        U = []
        for i in range(len(points)):
            Ui = []
            for c in range(len(centers)):
                # print(str(points[i])+ '  ' +str(centers[c]))
                # print(self.compute_distance_to_one_center(points[i], centers[c], m))
                # print(self.compute_distance_to_all_centers(points[i], m))
                # print("##########\n")

                Uik = self.compute_distance_to_one_center(points[i], centers[c], m) / self.compute_distance_to_all_centers(points[i], m)
                Ui.append(Uik)
            U.append(Ui)
        return U

    def compute_centers(self):
        """
        This def computes centers of clusters.
        """
        points = self.points
        centers = self.centers
        U = self.U
        m = self.m
        new_centers = []
        diff_centers = 0   # This variable is used to the difference between the old and new centers has been calculated
        for c in range(len(centers)):
            sum_UX = [0 for i in points[0]]
            sum_U = 0
            for i in range(len(points)):
                for k in range(len(sum_UX)):
                    sum_UX[k] += (U[i][c] ** m) * points[i][k]
                sum_U += U[i][c] ** m
            Vc = [n / sum_U for n in sum_UX]
            new_centers.append(Vc)
            diff_centers += 1/self.compute_distance_to_one_center(Vc, centers[c], 3)
        self.centers = new_centers
        self.diff_centers = diff_centers

    def compute_cost(self):
        """
        This def compute cost of this state
        :return: cost
        """
        points = self.points
        centers = self.centers
        U = self.U
        cost = 0
        for i in range(len(points)):
            for c in range(len(centers)):
                cost = cost + U[i][c] * (1/self.compute_distance_to_one_center(points[i], centers[c], m=3))
        return cost

    def run(self, show_plots=True):
        """
        This def uses other def of class to run FCM algorithm
        :return: a list that is centers of all clusters
        """
        self.read_file()
        self.select_random_centers()
        while self.diff_centers > 0.0001:
            U = self.compute_U(self.points)
            self.U = U
            self.compute_centers()
        if show_plots:
            self.show_points()
            self.show_ares()

        return self.centers
