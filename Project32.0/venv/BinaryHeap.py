class BinaryHeap:

    def __init__(self, nodes):
        #values: distances
        self.dist = {}
        self.prev = {}
        self.index = {}
        self.tree_heap = []
        for node in nodes:
            self.tree_heap.append(node)

    #Time: O(log(n))
    def decrease_key(self, curr_node, new_d, new_p):
        self.dist[curr_node] = new_d
        self.prev[curr_node] = new_p

        self.bubble_up(curr_node)

    #O(log(n))
    def bubble_up(self, curr_node):
        parent = self.get_parent(curr_node)

        while parent is not None and self.dist[curr_node] < self.dist[parent]:
            self.swap(curr_node, parent)
            parent = self.get_parent(curr_node)

    #Time: O(1)
    def swap(self, a, b):
        a_index = self.index[a]
        b_index = self.index[b]

        temp = a_index
        a_index = b_index
        b_index = temp

        self.index[a] = a_index
        self.index[b] = b_index

        self.tree_heap[b_index] = b
        self.tree_heap[a_index] = a

    #Time: O(1)
    def get_parent(self, child):
        child_index = self.index[child]
        if child_index == 0:
            return None
        else:
            parent_index = (child_index - 1) // 2
            return self.tree_heap[parent_index]

    #O(log(n))
    def delete_min(self):
        retVal = self.tree_heap[0]
        if len(self.tree_heap) == 1:
            del self.tree_heap[0]
            return retVal
        self.tree_heap[0] = self.tree_heap[-1]
        del self.index[self.tree_heap[-1]]
        del self.tree_heap[-1]
        self.index[self.tree_heap[0]] = 0
        self.sift_down(self.tree_heap[0])
        return retVal

    #O(1)
    def min_child(self, curr):
        parent_index = self.index[curr]

        if 2 * parent_index > len(self.tree_heap):
            return None

        if len(self.tree_heap) == 2:
            child_index = (2 * parent_index) + 1
            if child_index > len(self.tree_heap) - 1:
                child_index = len(self.tree_heap) - 1
            child_node = self.tree_heap[child_index]
            return child_node
        else:
            left_index = (2 * parent_index) + 1
            right_index = (2 * parent_index) + 2

            if left_index > len(self.tree_heap) - 1:
                left_index = len(self.tree_heap) - 2
            if right_index > len(self.tree_heap) - 1:
                right_index = len(self.tree_heap) - 1

            left_dist = self.dist[self.tree_heap[left_index]]
            right_dist = self.dist[self.tree_heap[right_index]]

            if left_dist < right_dist:
                return self.tree_heap[left_index]
            else:
                return self.tree_heap[right_index]

    #O(log(n))
    def sift_down(self, parent):
        min = self.min_child(parent)
        while min is not None and self.dist[min] < self.dist[parent]:
            self.swap(min, parent)
            min = self.min_child(parent)

    #Put source at beginning, set dist to 0
    def setup_start_tree(self, srcIndex):
        src = self.tree_heap[srcIndex]
        self.dist[src] = 0
        beginning = self.tree_heap[0]
        self.swap(src, beginning)

    
