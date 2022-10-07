
class PriorityQueueArray:

    def __init__(self, dist):
        #self.data = {}
        self.data = []
        self.dist = dist

    def insert(self, node):
        #self.data[value] = priority
        self.data.append(node)

    def decrease_key(self, new_min):
        return

    def make_queue(self, nodes):
        for node in nodes:
            self.data.insert(node)

    def delete_min(self):
        curr_min = None
        #for value, priority in self.data.items():
            #if curr_min is None or priority < self.data[curr_min]
                #curr_min = value

        #del self.data[curr_min]
        for i in range(len(self.dist)):
            if curr_min is None or curr_min > dist[i]:
                curr_min = i
        self.data.remove(data[curr_min])
        return curr_min




