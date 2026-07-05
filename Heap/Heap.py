class MaxHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i): return (i - 1) // 2
    def left_child(self, i): return 2 * i + 1
    def right_child(self, i): return 2 * i + 2

    # FIX (bug #2): the original code compared tingkat_keparahan directly,
    # so two patients with equal severity had an arbitrary (non-FIFO) order
    # -- verified: patients triaged A, B, C at equal severity could come
    # back out as A, C, B. _priority_key adds id_pasien (arrival order) as
    # a tie-breaker: earlier id_pasien wins when severity is equal.
    def _priority_key(self, p):
        return (p.tingkat_keparahan, -p.id_pasien)

    def insert(self, data):
        self.heap.append(data)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, i):
        while i != 0 and self._priority_key(self.heap[self.parent(i)]) < self._priority_key(self.heap[i]):
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)

    def delete_root(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        return root

    def heapify_down(self, i):
        largest = i
        l = self.left_child(i)
        r = self.right_child(i)
        n = len(self.heap)

        if l < n and self._priority_key(self.heap[l]) > self._priority_key(self.heap[largest]):
            largest = l
        if r < n and self._priority_key(self.heap[r]) > self._priority_key(self.heap[largest]):
            largest = r

        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.heapify_down(largest)

    def peek(self):
        return self.heap[0] if self.heap else None

    def display(self):
        if not self.heap:
            print("Tidak ada pasien di antrean dokter (IGD kosong).")
            return
        print("Antrean IGD berdasarkan Prioritas (Max-Heap):")
        for p in self.heap:
            print(f"- {p}")