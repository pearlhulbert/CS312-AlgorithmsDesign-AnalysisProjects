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

		
	def branchAndBound( self, time_allowance=60.0 ):
		bssf = self.defaultRandomTour(time_allowance)

		init_mat_state = MatrixState(self, city_matrix=self._scenario.getCities(), first_city=self._scenario.getCities()[0])

		init_city = self._scenario.getCities()[0]
		state_list = [init_mat_state]

		solutions = []

		start_time = time.time()
		while state_list and time.time() - start_time < time_allowance:
			state = state_list.pop()

			if not state.not_visited(self._scenario.getCities()):
				if state.to_place.costTo(init_city) < np.inf:
					bssf['count'] += 1

					state_visited = state.visited
					curr_solution = TSPSolution(state_visited)

					results = {
						'cost': state.curr_cost + state.to_place.costTo(init_city),
						'count': bssf['count'],
						'soln': curr_solution,
						'max': None,
						'total': None,
						'pruned': None
					}

					solutions.append(results)

			temp = []
			for c in state.not_visited(self._scenario.getCities()):
				if state.curr_place.costTo(c) < np.inf:
					next_state = MatrixState(state=state, from_place=state.from_place, to_place=c)

					temp.append(next_state)


			total_len = len(temp)
			prune_amt = math.ceil(total_len * 0.5)
			temp = heapq.nsmallest(total_len - prune_amt, temp, key=lambda x: x.curr_cost)
			state_list.extend(temp)


		end_time = time.time()

		best = solutions[0]
		for sol in solutions:
			best = sol if sol['cost'] < best['cost'] else best

		final_result = {}
		final_result['cost'] = best['cost']
		final_result['time'] = end_time - start_time
		final_result['count'] = len(solutions)
		final_result['soln'] = best['soln']
		final_result['max'] = None
		final_result['total'] = None
		final_result['pruned'] = None
		return final_result



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
		



