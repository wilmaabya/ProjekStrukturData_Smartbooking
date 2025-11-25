class MaxHeap:
    def __init__(self):
        # Index 0 dikosongin biar parent-child gampang dihitung
        self.data = [None]

    def insert(self, item):
        # item berbentuk tuple
        # contoh: (priority, id_booking, tanggal, nama)
        self.data.append(item)
        self._heapify_up(len(self.data) - 1)

    def extract_max(self):
        if len(self.data) <= 1:
            return None
        
        # Kalau cuma satu elemen nyata
        if len(self.data) == 2:
            return self.data.pop()

        root = self.data[1]
        # ambil elemen terakhir ke root
        self.data[1] = self.data.pop()
        self._heapify_down(1)
        return root

    def _heapify_up(self, index):
        # Naikin elemen sampai memenuhi aturan max-heap
        while index > 1:
            parent = index // 2
            if self.data[index][0] > self.data[parent][0]:
                # swap
                self.data[index], self.data[parent] = self.data[parent], self.data[index]
                index = parent
            else:
                break

    def _heapify_down(self, index):
        # Turunin elemen sampai posisi benar
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
