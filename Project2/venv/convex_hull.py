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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25


#
# This is the class you have to complete.
#

class Hull:

    def __init__(self, circle_linked_list):
        self.list = circle_linked_list

    def size(self):
        return self.list.get_size()

    def right_side(self):
        return self.list.tail

    def left_side(self):
        return self.list.head

# Time complexity: O(1), only adds and subtracts, divides
def calculate_slope(left_node, right_node):
    x_1 = left_node.value.x()
    y_1 = left_node.value.y()

    x_2 = right_node.value.x()
    y_2 = right_node.value.y()

    slope = (y_2 - y_1) / (x_2 - x_1)

    return slope

#Time and space complexity: O(n), iterates for the number of points we have, stores points
def upper_tangent(left_right_most, right_left_most, left_half, right_half):
    left_guess = left_right_most
    right_guess = right_left_most

    curr_left = left_right_most
    curr_right = right_left_most

    guess_slope = calculate_slope(curr_left, curr_right)

    found = False

    while not found:
        negative = False
        positive = False
        #Look through left half, then right
        for i in range(left_half.size()):
            #Look at node to left (counter clockwise)
            curr_left = curr_left.prev
            #find slope with right
            new_slope = calculate_slope(curr_left, right_guess)
            #Look for a negative change, update if found
            if new_slope < guess_slope:
                left_guess = curr_left
                negative = True
                guess_slope = new_slope
        for i in range(right_half.size()):
            #Look at node to right (clockwise)
            curr_right = curr_right.next
            #find slope with left
            new_slope = calculate_slope(left_guess, curr_right)
            #Check for positive change, update
            if new_slope > guess_slope:
                right_guess = curr_right
                positive = True
                guess_slope = new_slope
        #Continue until no change
        if not negative and not positive:
            found = True

    # Return right and left points we found
    return left_guess, right_guess

#Time and space complexity: O(n), iterates for the number of points we have, stores points
def lower_tangent(left_right_most, right_left_most, left_half, right_half):
    left_guess = left_right_most
    right_guess = right_left_most

    curr_left = left_right_most
    curr_right = right_left_most

    guess_slope = calculate_slope(curr_left, curr_right)

    found = False

    while not found:
        negative = False
        positive = False
        #Check left half, then right
        for i in range(left_half.size()):
            curr_left = curr_left.next
            #Check slope with right
            new_slope = calculate_slope(curr_left, right_guess)
            #Check for negative change
            if new_slope > guess_slope:
                left_guess = curr_left
                negative = True
                guess_slope = new_slope
        for i in range(right_half.size()):
            curr_right = curr_right.prev
            #Check slope with left
            new_slope = calculate_slope(left_guess, curr_right)
            #Check for positive change
            if new_slope < guess_slope:
                right_guess = curr_right
                positive = True
                guess_slope = new_slope
        #Keep going until no change
        if not negative and not positive:
            found = True

    #Return right and left points we found
    return left_guess, right_guess

#Time and space complexity: O(n) because of upper and lower tangent
def combine_hulls(left_half, right_half):
    left_right_most = left_half.right_side()
    right_left_most = right_half.left_side()

    #Find upper and lower tangent lines
    upper_tangent_result = upper_tangent(left_right_most, right_left_most, left_half, right_half)
    lower_tangent_result = lower_tangent(left_right_most, right_left_most, left_half, right_half)

    left_upper_tangent, right_upper_tangent = upper_tangent_result
    left_lower_tangent, right_lower_tangent = lower_tangent_result

    #Connect left to right for each
    left_upper_tangent.next = right_upper_tangent
    right_upper_tangent.prev = left_upper_tangent

    right_lower_tangent.next = left_lower_tangent
    left_lower_tangent.prev = right_lower_tangent

    merge_list = CircleDoubleLinkedList()

    #Put upper start and end points in circle
    merge_list.head = right_upper_tangent
    merge_list.tail = left_upper_tangent

    new_hull = Hull(merge_list)
    return new_hull


class ConvexHullSolver(QObject):
    # Class constructor
    def __init__(self):
        super().__init__()
        self.pause = False

    # Some helper methods that make calls to the GUI, allowing us to send updates
    # to be displayed.

    def showTangent(self, line, color):
        self.view.addLines(line, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseTangent(self, line):
        self.view.clearLines(line)

    def blinkTangent(self, line, color):
        self.showTangent(line, color)
        self.eraseTangent(line)

    def showHull(self, polygon, color):
        self.view.addLines(polygon, color)
        if self.pause:
            time.sleep(PAUSE)

    def eraseHull(self, polygon):
        self.view.clearLines(polygon)

    def showText(self, text):
        self.view.displayStatusText(text)

    #Time complexity: O(nlog(n)) according to the Master's Theorem
    #Space complexity: O(n): still only ever need to store points
    def divide_and_conquer(self, points):
        if len(points) <= 1:
            linked_list_points = CircleDoubleLinkedList()
            linked_list_points.insert_tail(points[0])
            curr_hull = Hull(linked_list_points)
            return curr_hull

        middle_val = len(points) // 2
        left_half = points[:middle_val]
        right_half = points[middle_val:]

        left_hull = self.divide_and_conquer(left_half)
        right_hull = self.divide_and_conquer(right_half)

        combined = combine_hulls(left_hull, right_hull)
        return combined

    # This is the method that gets called by the GUI and actually executes
    # the finding of the hull
    #Time complexity: O(nlog(n))
    #Space Complexity: O(n)
    def compute_hull(self, points, pause, view):
        self.pause = pause
        self.view = view
        assert (type(points) == list and type(points[0]) == QPointF)

        t1 = time.time()
        points = sorted(points, key=lambda point: point.x())
        t2 = time.time()

        t3 = time.time()
        # this is a dummy polygon of the first 3 unsorted points
        final_hull = self.divide_and_conquer(points)
        polygon = []

        #Polygon should be an array. so we need to populate it with linked list values before we draw it
        linked_list_hull = final_hull.list
        for val in linked_list_hull:
            next_node = val.next
            polygon.append(QLineF(val.value.x(), val.value.y(), next_node.value.x(), next_node.value.y()))

        t4 = time.time()

        # when passing lines to the display, pass a list of QLineF objects.  Each QLineF
        # object can be created with two QPointF objects corresponding to the endpoints
        self.showHull(polygon, RED)
        self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4 - t3))
