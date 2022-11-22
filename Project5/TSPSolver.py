#!/usr/bin/python3
import csv

from PyQt5.QtCore import QLineF, QPointF
import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
from MatrixStates import *
from MinHeap import MinHeap



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
		results['max'] = 0
		results['total'] = 0
		results['pruned'] = 0
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
		pass
	
	
	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''

	# time: O(n^2), space: O(1)
	def branchAndBound( self, time_allowance=60.0 ):
		bssf = self.defaultRandomTour(time_allowance)

		init_mat_state = MatrixState(city_matrix=self._scenario.getCities(), first_city=self._scenario.getCities()[0])

		init_city = self._scenario.getCities()[0]
		heap = MinHeap()
		heap.insert(init_mat_state.priority(len(self._scenario.getCities())), init_mat_state)

		solutions = []

		start_time = time.time()
		# time: for loop is O(n), plus inner for loop is O(n^2)
		# space: O(1), same space is used every time
		# finished route, found a solution
		for state in heap:
			if time.time() - start_time > time_allowance:
				break
			if state is None:
				break

			# all operations in here are O(1)
			# finished route, found a solution
			if not state.not_visited(self._scenario.getCities()):
				if state.to_place.costTo(init_city) < np.inf:

					if state.curr_cost < bssf['cost']:
						bssf['cost'] = state.curr_cost + state.to_place.costTo(init_city)


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

			# time: for loop is O(n), insert is O(log(n))., so overall it's O(n)
			# go through every city that has not been visited yet
			for c in state.not_visited(self._scenario.getCities()):
				# create a new state if there is a path
				if state.curr_place.costTo(c) < np.inf:
					next_state = MatrixState(state=state, from_place=state.curr_place, to_place=c)
					bssf['total'] += 1

					# if the path is better than the bssf, insert that state into the heap
					if next_state.curr_cost < bssf['cost']:
						heap.insert(
							next_state.priority(len(self._scenario.getCities())),
							next_state
						)
					else:
						bssf['pruned'] += 1


		end_time = time.time()

		best = solutions[0]
		# time: O(n)
		for sol in solutions:
			best = sol if sol['cost'] < best['cost'] else best

		new_cost = 0
		# time: O(n) for loop
		for i in range(len(best['soln'].route)):
			new_cost += best['soln'].route[i].costTo(best['soln'].route[(i + 1) % len(best['soln'].route)])

		final_result = {}
		final_result['cost'] = new_cost
		final_result['time'] = end_time - start_time
		final_result['count'] = len(solutions)
		final_result['soln'] = best['soln']
		final_result['max'] = heap.max_length
		final_result['total'] = bssf['total']
		final_result['pruned'] = bssf['pruned']

		with open("results.csv", 'a') as f:
			csv_result = {
				'# Cities': len(self._scenario.getCities()),
				'Seed': 20,
				'Running time (sec.)': end_time - start_time,
				'Cost of best tour found': new_cost,
				'Max # of stored states at a given time': heap.max_length,
				'count': len(solutions),
				'# of BSSF updates': bssf['count'],
				'Total # of states created': bssf['total'],
				'Total # of states pruned': bssf['pruned']}

			w = csv.DictWriter(f, csv_result.keys())
			w.writerow(csv_result)

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
		



