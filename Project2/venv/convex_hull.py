from linked_list import Node, CircleDoubleLinkedList
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#

class Hull:

	def __init__(self, cirle_linked_list):
		self.list = cirle_linked_list

	def size(self):
		return self.list.get_size()

	def right_side(self):
		return self.list.tail

	def left_side(self):
		return self.list.head



def calculate_slope(left_node, right_node):
	x_1 = left_node.value.x()
	y_2 = left_node.value.y()

	x_2 = right_node.value.x()
	y_2 = right_node.value.y()

	slope = (y_2 - y_1) / (x_2 - x_1)

	return slope

def list_in_half(circle_linked_list):
	list_size = circle_linked_list.get_size()
	middle = list_size // 2
	first_half = CircleDoubleLinkedList()
	last_half = CircleDoubleLinkedList()

	current = circle_linked_list.get_head()

	for i in range(list_size):
		if i < middle:
			first_half.insert_tail(current.value)
		else:
			last_half.insert_tail(current.value)
		current = current.next

	return first_half, last_half

def upper_tangent(left_right_most, right_left_most, left_half, right_half):
	best_left_guess = left_right_most
	best_right_guess = right_left_most

	curr_left = left_right_most
	curr_right = right_left_most

	best_guess_slope = calculate_slope(curr_left, curr_right)

	found = False

	while not found:
		negative = False
		positive = False
		for i in range(left_half.get_size()):
			curr_left = curr_left.prev
			new_slope = calculate_slope(curr_left, best_right_guess)
			if new_slope < best_guess_slope:
				best_left_guess = curr_left
				negative = True
				best_guess_slope = new_slope
		for i in range(right_half.get_size()):
			curr_node = curr_right.next
			new_slope = calculate_slope(best_left_guess, curr_right)
			if new_slope > best_guess_slope:
				best_right_guess = curr_node
				positive = True
				best_guess_slope = new_slope
		if not negative and not positive:
			found = True

	#This is the value we actually need for combining the hulls
	return best_right_guess


def lower_tangent(left_right_most, right_left_most, left_half, right_half):
	best_left_guess = left_right_most
	best_right_guess = right_left_most

	curr_left = left_right_most
	curr_right = right_left_most

	best_guess_slope = calculate_slope(curr_left, curr_right)

	found = False

	while not found:
		negative = False
		positive = False
		for i in range(left_half.get_size()):
			curr_left = curr_left.next
			new_slope = calculate_slope(curr_left, best_right_guess)
			if new_slope > best_guess_slope:
				best_left_guess = curr_left
				negative = True
				best_guess_slope = new_slope
		for i in range(0, right_half.get_size()):
			curr_right = curr_right.prev
			new_slope = calculate_slope(best_left_guess, curr_right)
			if new_slope < best_guess_slope:
				best_right_guess = curr_right
				positive = True
				best_guess_slope = new_slope
		if not negative and not positive:
			found = True

	# This is the value we actually need for combining the hulls
	return best_left_guess

def combine_hulls(self, left_half, right_half):

	left_right_most = left_half.right_side()
	right_left_most = right_half.left_side()

	upper_tangent_result = upper_tangent(left_right_most, right_left_most, left_half, right_half)
	lower_tangent_result = lower_tangent(left_right_most, right_left_most, left_half, right_half)

	best_left.next = upper_tangent_result
	best_right.next = lower_tangent_result

	merge_list = CircleDoubleLinkedList()

	curr_node = upper_tangent_result

	while curr_node.next != upper_tangent_result:
		merge_list.insert_tail(curr_node.value)
		curr_node = curr_node.next
	merge_list.insert_tail(curr_node.value)

	new_hull = Hull(merge_list)
	return new_hull

def divide_and_conquer(self, points_list):
	if points_list.get_size() <= 1:
		curr_hull = Hull(points_list)
		return curr_hull

	left_half, right_half = list_in_half(points_list)

	left_hull = self.divide_and_conquer(left_half)
	right_hull = self.divide_and_conquer(right_half)

	return self.combine_hulls(left_hull, right_hull)

def make_hull(self, points):
	linked_points = CircleDoubleLinkedList()

	for elem in points:
		linked_points.insert_tail(elem)

	final_hull = self.divide_and_conquer(self, points)
	return final_hull

class ConvexHullSolver(QObject):
# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)
		
	def showText(self,text):
		self.view.displayStatusText(text)
	

# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		points = sorted(points, key=lambda point: point.x())
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		final_hull = self.make_hull(points)
		polygon = []

		#populate polygon list with values from linked list
		linked_list_hull = final_hull.list
		for val in linked_list_hull:
			next = val.next
			polygon.append(QLineF(val.value.x(), val.value.y(), next.value.x(), next.value.y()))

		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))



