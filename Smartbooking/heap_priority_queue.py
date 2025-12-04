class MaxHeap:
    def __init__(self):
        self.data = [None]

    def insert(self, item):
        self.data.append(item)
        self._heapify_up(len(self.data) - 1)

    def extract_max(self):
        if len(self.data) <= 1:
            return None
        
        if len(self.data) == 2:
            return self.data.pop()

        root = self.data[1]
        self.data[1] = self.data.pop()
        self._heapify_down(1)
        return root

    def _heapify_up(self, index):
        while index > 1:
            parent = index // 2
            if self.data[index][0] > self.data[parent][0]:
                self.data[index], self.data[parent] = self.data[parent], self.data[index]
                index = parent
            else:
                break

    def _heapify_down(self, index):
        while index * 2 < len(self.data):
            left = index * 2
            right = left + 1
            largest = index

            if left < len(self.data) and self.data[left][0] > self.data[largest][0]:
                largest = left

            if right < len(self.data) and self.data[right][0] > self.data[largest][0]:
                largest = right

            if largest != index:
                self.data[index], self.data[largest] = self.data[largest], self.data[index]
                index = largest
            else:
                break
