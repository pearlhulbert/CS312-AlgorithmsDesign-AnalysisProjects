import numpy as np


class MatrixState:

    def __init__(self, state=None, to_place=None, from_place=None, city_matrix=None, first_city=None):
        self.dist = []
        self.min = 0
        self.visited = []

        if to_place is not None and from_place is not None:
            self.to_place = to_place
            self.from_place = from_place
        else:
            self.to_place = None
            self.from_place = None

        if state is not None:
            self.dist = np.copy(state.dist)
            self.visited = state.visited.copy
            self.visited.append(to_place)

        elif city_matrix is not None:
            self.visited.append(first_city)
            self.dist = np.zeros(len(city_matrix), len(city_matrix))
            for i in range(len(city_matrix)):
                for j in range(len(city_matrix)):
                    self.dist[i][j] = city_matrix[i].costTo(city_matrix[j])

        #if statement here
        self.restrict_matrix()
        self.min_cost_matrix()


    def min_cost_matrix(self):
        for i in range(len(self.dist)):
            curr_min = np.min(self.dist[i])
            if curr_min != np.inf:
                self.min += min(self.dist[i])
                self.dist[i] -= min(self.dist[i])

        for i in range(len(self.dist)):
            curr_min = np.min(self.dist[:, i])
            if curr_min != np.inf:
                self.min += min(self.dist[:, i])
                self.dist[i] -= min(self.dist[:, i])

    def restrict_matrix(self):
        self.dist[self.from_place._index] = np.full(np.inf)
        self.dist[self.to_place._index] = np.full(np.inf)

        self.dist[self.to_place._index][self.from_place._index] = np.inf

    def not_visited(self, cities_list):
        not_visited = []
        for c in cities_list:
            if c._index not in self.visited:
                not_visited.append(c)

        return not_visited