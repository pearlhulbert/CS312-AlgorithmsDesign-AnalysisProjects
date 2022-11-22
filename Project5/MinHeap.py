import heapq

class MinHeap:

    def __init__(self):
        self._min_heap = []
        self._life_count = 0
        self.max_length = 0

    def __next__(self):
        # time: pop_top is O(log(n))
        heap_top = self.pop_top()
        return heap_top[2] if heap_top is not None else None

    def __iter__(self):
        return self

    # time: O(log(n))
    def insert(self, p, o):
        # time: O(log(n) for heappush
        self.max_length = len(self._min_heap) if len(self._min_heap) > self.max_length else self.max_length
        heapq.heappush(self._min_heap, (p, self._life_count, o))
        self._life_count += 1

    # time: O(log(n))
    def pop_top(self):
        # time: O(log(n)) for heappop
        return heapq.heappop(self._min_heap) if len(self._min_heap) > 0 else None