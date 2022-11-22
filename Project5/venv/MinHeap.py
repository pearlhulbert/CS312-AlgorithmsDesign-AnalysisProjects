import heapq

class MinHeap:
    def __init__(self):
        self._min_heap = []
        self._life_count = 0

    def __next__(self):
        heap_top = self.pop_top()
        return heap_top[2] if heap_top is not None else None

    def __iter__(self):
        return self

    def insert(self, p, o):
        heapq.heappush(self._min_heap, (p, self._life_count, o))
        self._life_count += 1

    def pop_top(self):
        return heapq.heappop(self._min_heap) if len(self._min_heap) > 0 else None