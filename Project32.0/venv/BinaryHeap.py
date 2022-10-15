class BinaryHeap:

    def __init__(self):
        #values: distances
        self.dist = {}
        self.prev = {}
        self.index = {}
        self.tree_heap = []

    def decrease_key(self, curr_node, new_d, new_p):
        self.dist[curr_node] = new_d
        self.prev[curr_node] = new_p

        self.bubble_up(curr_node)

    def bubble_up(self, curr_node):
        parent = self.get_parent(curr_node)

        while parent is not None and dist[curr_node] < dist[parent]:
            self.swap(curr_node, parent)
            parent = curr_node.get_parent(curr_node)

    def swap(self, a, b):
        a_index = index[a]
        b_index = index[b]

        self.index[b_index] = a
        self.index[a_index] = b

        self.tree[b_index] = a
        self.tree[a_index] = b

    def get_parent(self, child):
        child_index = self.index[child]
        if child_index == 0:
            return None
        else:
            parent_index = (child_index - 1) // 2
            return self.tree[parent_index]


    def make_queue(self, node_list):
        for node in node_list:
            self.tree.append(node)
