
class PriorityQueueArray:

    def __init__(self):
        self.data = {}

    #Time: O(1)
    def insert(self, value, weight):
        self.data[value] = weight

    #Time: O(1)
    def decrease_key(self, value, new_min):
        self.data[value] = new_min

    #Time: O(n)
    #Space: O(n)
    def delete_min(self):
        curr_min = None
        for value, priority in self.data.items():
            if curr_min is None or priority < self.data[curr_min]:
                curr_min = value
        del self.data[curr_min]
        return curr_min




