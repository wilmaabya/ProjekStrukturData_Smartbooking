class IntervalNode:
    def __init__(self, start, end):
        self.start = start         
        self.end = end              
        self.max_end = end          
        self.left = None            
        self.right = None           

class IntervalTree:
    def __init__(self):
        self.root = None

    def _insert(self, node, start, end):
        if node is None:
            return IntervalNode(start, end)
        
        if end > node.max_end:
            node.max_end = end
            
        if start < node.start:
            node.left = self._insert(node.left, start, end)
        else:
            node.right = self._insert(node.right, start, end)
            
        return node

    def insert(self, start, end):
        self.root = self._insert(self.root, start, end)

    def _is_overlap(self, start1, end1, start2, end2):
        return start1 < end2 and start2 < end1

    def search_overlap(self, start, end):
        return self._search_overlap(self.root, start, end)

    def _search_overlap(self, node, start, end):
        if node is None:
            return False 

        if self._is_overlap(start, end, node.start, node.end):
            return True

        if node.left is not None and node.left.max_end > start:
            if self._search_overlap(node.left, start, end):
                return True
        
        if node.right is not None:
             return self._search_overlap(node.right, start, end)
        
        return False