class IntervalNode:
    def __init__(self, start, end):
        self.start = start
        self.end = end

        # max_end menyimpan nilai terbesar dari subtree ini
        self.max_end = end

        self.left = None
        self.right = None


class IntervalTree:
    def __init__(self):
        self.root = None

    def insert(self, start, end):
        self.root = self._insert(self.root, start, end)

    def _insert(self, node, start, end):
        if node is None:
            return IntervalNode(start, end)

        if start < node.start:
            node.left = self._insert(node.left, start, end)
        else:
            node.right = self._insert(node.right, start, end)

        # Update max_end buat subtree ini
        node.max_end = max(node.max_end, end)
        return node

    def is_conflict(self, start, end):
        return self._is_conflict(self.root, start, end)

    def _is_conflict(self, node, start, end):
        if node is None:
            return False

        # Cek overlap interval:
        # Tidak overlap jika:
        #    end <= node.start   atau   start >= node.end
        if not (end <= node.start or start >= node.end):
            return True

        # Cek subtree kiri jika masih mungkin overlap
        if node.left and node.left.max_end >= start:
            return self._is_conflict(node.left, start, end)

        # Lanjut ke kanan
        return self._is_conflict(node.right, start, end)
