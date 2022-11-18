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
import math
import heapq
import itertools



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

	# 	start at the first city
	# 	take the shortest path
	# 	keep taking the shortest path until you make it back or can't go anywhere
	# 	How do you get back to the start? DONE
	# 	How do you know if the path won't work? DONE
	# 	What do you do when the path doesn't work? DONE
	def greedy(self, time_allowance=60.0):
		cities = self._scenario.getCities()
		bssf = None
		count = 0
		results = {}
		start_time = time.time()
		for startIndex in range(len(cities)):
			if time.time() - start_time < time_allowance:
				currRoute = None
				path = []
				cost = 0
				startCity = cities[startIndex]
				path.append(startCity)
				nextCityIndex = -1
				while nextCityIndex != startIndex:
					lowestCost = math.inf
					for i in range(len(cities)):
						if not path.__contains__(cities[i]):
							newCost = startCity.costTo(cities[i])
							if newCost < lowestCost:
								lowestCost = newCost
								nextCityIndex = i
						elif len(path) == len(cities):
							returnCost = path[-1].costTo(path[0])
							if returnCost != math.inf:
								cost += returnCost
							break

					if len(path) == len(cities):
						currRoute = TSPSolution(path)
						nextCityIndex = startIndex
						if currRoute.cost != math.inf:
							count += 1
					elif lowestCost == math.inf:
						nextCityIndex = startIndex
					else:
						startCity = cities[nextCityIndex]
						path.append(startCity)
						cost += lowestCost

				if currRoute is not None and (bssf is None or currRoute.cost < bssf.cost):
					bssf = currRoute
			else:
				break

		end_time = time.time()
		results['cost'] = math.inf if bssf is None else bssf.cost
		results['time'] = end_time - start_time
		results['count'] = count
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

		pass



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


	def initializeParentMatrix(self):
		cities = self._scenario.getCities()
		parentMatrix = np.empty([len(cities), len(cities)])
		for i in range(len(cities)):
			for j in range(len(cities)):
				cost = cities[i].costTo(cities[j])
				parentMatrix[i, j] = cost


class Path:
	def __init__(self, parentMatrix, parentPath):
		self.costMatrix = parentMatrix
		self.lowerBound = self.findLowerBound(-1, -1)
		self.path = parentPath

	def findLowerBound(self, newCityIndex, currCityIndex):
		lowerBound = 0
		if newCityIndex >= 0 and currCityIndex >= 0:
			lowerBound += self.costMatrix[currCityIndex, newCityIndex]
			for i in range(np.shape(self.costMatrix)[0]):
				self.costMatrix[currCityIndex, i] = np.inf

			for i in range(np.shape(self.costMatrix)[0]):
				self.costMatrix[i, newCityIndex] = np.inf

			self.costMatrix[newCityIndex, currCityIndex] = np.inf

		for i in range(np.shape(self.costMatrix)[0]):
			minValue = min(self.costMatrix[i])
			lowerBound += minValue
			for j in range(np.shape(self.costMatrix)[1]):
				self.costMatrix[i, j] = self.costMatrix - minValue

		for j in range(np.shape(self.costMatrix)[1]):
			minValue = min(self.costMatrix[j])
			lowerBound += minValue
			for i in range(np.shape(self.costMatrix)[0]):
				self.costMatrix[i, j] = self.costMatrix - minValue

		return lowerBound

	def updatePath(self, newCityIndex):
		self.path.append(newCityIndex)
		



