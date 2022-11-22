import numpy as np


class MatrixState:

    def __init__(self, state=None, to_place=None, from_place=None, city_matrix=None, first_city=None):
        self.dist = []
        self.curr_cost = 0
        self.visited = []

        self.from_place = from_place
        self.to_place = to_place

        self.curr_place = first_city if first_city is not None else to_place

        if state is not None:
            self.dist = np.copy(state.dist)
            self.visited = state.visited.copy()
            self.visited.append(to_place)
            self.curr_cost = state.curr_cost + state.curr_place.costTo(to_place)

        elif city_matrix is not None:
            self.visited.append(first_city)
            self.dist = np.zeros((len(city_matrix), len(city_matrix)))
            for i in range(len(city_matrix)):
                for j in range(len(city_matrix)):
                    self.dist[i][j] = city_matrix[i].costTo(city_matrix[j])

        if from_place is not None and to_place is not None:
            self.restrict_matrix()
        self.min_cost_matrix()

    def min_cost_matrix(self):
        for i in range(len(self.dist)):
            curr_min = np.min(self.dist[i])
            if curr_min != np.inf:
                self.curr_cost += np.min(self.dist[i])
                self.dist[i] -= np.min(self.dist[i])

        for i in range(len(self.dist)):
            curr_min = np.min(self.dist[:, i])
            if curr_min != np.inf:
                self.curr_cost += np.min(self.dist[:, i])
                self.dist[:, i] -= np.min(self.dist[:, i])

    def restrict_matrix(self):
        self.dist[self.from_place._index] = np.full(len(self.dist), np.inf)
        self.dist[:, self.to_place._index] = np.full(len(self.dist), np.inf)

        self.dist[self.to_place._index][self.from_place._index] = np.inf

    def not_visited(self, cities_list):
        not_visited = []
        for c in cities_list:
            if c not in self.visited:
                not_visited.append(c)
        return not_visited

    def priority(self, total: int) -> float:
        return (total - len(self.visited)) * self.curr_cost
