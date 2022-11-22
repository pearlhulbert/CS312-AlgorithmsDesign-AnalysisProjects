import numpy as np


class MatrixState:

    # time and space: O(n^2)
    def __init__(self, state=None, to_place=None, from_place=None, city_matrix=None, first_city=None):
        self.dist = []
        self.curr_cost = 0
        self.visited = []

        self.from_place = from_place
        self.to_place = to_place

        self.curr_place = first_city if first_city is not None else to_place

        if state is not None:
            self.dist = np.copy(state.dist)
            # time: O(n^2) for copy
            self.visited = state.visited.copy()
            self.visited.append(to_place)
            self.curr_cost = state.curr_cost + state.curr_place.costTo(to_place)

        elif city_matrix is not None:
            self.visited.append(first_city)
            # space: O(n^2) for matrix
            self.dist = np.zeros((len(city_matrix), len(city_matrix)))
            for i in range(len(city_matrix)):
                for j in range(len(city_matrix)):
                    self.dist[i][j] = city_matrix[i].costTo(city_matrix[j])

        if from_place is not None and to_place is not None:
            self.restrict_matrix()
        self.min_cost_matrix()

    # time: O(n^2), space: O(1)
    def min_cost_matrix(self):
        # for loop is O(n)
        for i in range(len(self.dist)):
            # min is O(n)
            curr_min = np.min(self.dist[i])
            if curr_min != np.inf:
                self.curr_cost += np.min(self.dist[i])
                self.dist[i] -= np.min(self.dist[i])

        for i in range(len(self.dist)):
            curr_min = np.min(self.dist[:, i])
            if curr_min != np.inf:
                self.curr_cost += np.min(self.dist[:, i])
                self.dist[:, i] -= np.min(self.dist[:, i])

    # time: O(n), space: O(1)
    def restrict_matrix(self):
        # time: O(n) for full
        # space: O(1) not anything extra allocated
        self.dist[self.from_place._index] = np.full(len(self.dist), np.inf)
        self.dist[:, self.to_place._index] = np.full(len(self.dist), np.inf)

        self.dist[self.to_place._index][self.from_place._index] = np.inf

    # time and space: O(n)
    def not_visited(self, cities_list):
        not_visited = []
        # time: O(n) for for loop
        for c in cities_list:
            if c not in self.visited:
                # space: O(n), adding n elements to not_visited
                not_visited.append(c)
        return not_visited

    # time and space: O(1)
    def priority(self, total: int) -> float:
        # sort of a hash to find priority
        return (total - len(self.visited)) * self.curr_cost
