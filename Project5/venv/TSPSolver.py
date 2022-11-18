#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
from MatrixStates import *



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results

	def lower_bound(self, city):
		pass


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	def greedy( self,time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		paths = self._scenario._edge_exists
		ncities = len(cities)
		current_city = cities[0]

		# visited = []
		solved_path = []
		solved_path.append(current_city)
		# visited.append(cities[0])
		# solved_path.append(cities[0])
		total_cost = 0
		start_time = time.time()

		# while time.time()-start_time < time_allowance:
		for i in range(ncities):
			current_paths = paths[cities.index(current_city)]
			shortest_path = float('inf')
			closest_city = None

			for j in range(ncities):
				if current_paths[j] == True:
					if cities[j] not in solved_path:
						distance = current_city.costTo(cities[j])
						if distance < shortest_path:
							shortest_path = distance
							closest_city = cities[j]

			if closest_city != None:
				# visited.append(closest_city)
				solved_path.append(closest_city)
				current_city = closest_city
				total_cost += shortest_path

		bssf = TSPSolution(solved_path)
		end_time = time.time()

		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = 1
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results
	
	
	
	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''

	def find_neighbors(self, city):
		cities = self._scenario.getCities
		city_neighbors = []

		for cit in cities:
			if city.costTo(cit):
				city_neighbors.append(cit)

		return city_neighbors

		
	def branchAndBound( self, time_allowance=60.0 ):

		init_mat_state = MatrixState(self, city_matrix=self._scenario.getCities(), first_city=self._scenario.getCities()[0])
		BSSF = self.defaultRandomTour(time_allowance)

		state_list = [init_mat_state]

		while True:
			curr_min_states = []
			curr_min_cost = 0

			for state in state_list:
				if state.min < curr_min_cost:
					curr_min_cost = state.min
					curr_min_states.clear()
					curr_min_states.append(state)
				elif state.min == curr_min_cost:
					curr_min_states.append(state)

			#clear layer

			for state in curr_min_states:
				for c in state.not_visited(self._scenario.getCities()):
					next_state = MatrixState(state=state, from_place=state.from_place, to_place=c)

					if next_state.min < BSSF['cost']:
						BSSF['cost'] = curr_min_cost

		# P_0 = self._scenario.getCities()[0]
		# stack = []
		# stack.append(P_0)
		# BSSF = self.defaultRandomTour(time_allowance)['cost']
		#
		# while len(stack) != 0:
		# 	P = stack.pop()
		# 	if lower_bound(P) < BSSF:
		# 		for P_i in P._scenario.getCities():
		# 			if P.cost(P_i) is not math.inf and P.costTo(P_i) < BSSF:
		# 				BSSF = P_i.costTo(P)
		# 			elif lower_bound(P) < BSSF:
		# 				stack.append(P)
		#
		# return BSSF




	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
		
	def fancy( self,time_allowance=60.0 ):
		pass
		



