class MinHeap:
    def __init__(self):
        self.data = []
        
    def isEmpty(self):
        return len(self.data) == 0

    def _parent(self, index):
        return ((index - 1) // 2)
    
    def _leftSide(self, index):
        return (2 * index + 1)

    def _rightSide(self, index):
        return (2 * index + 2)
    
     # ---------- INSERT ----------

    def insert(self, pasien):
        self.data.append(pasien)
        self._heapify_up(len(self.data) - 1)

    def _heapify_up(self, index):
        while index > 0:
            parent_index = self._parent(index)
            if self.data[index].no_rm < self.data[parent_index].no_rm:
                self.data[index], self.data[parent_index] = self.data[parent_index], self.data[index]
                index = parent_index
            else:
                break

     # ---------- DELETE ROOT ----------

    def delete_root(self):
        if self.isEmpty():
            return None
        
        root = self.data[0]
        last_element = self.data.pop()
        
        if not self.isEmpty():
            self.data[0] = last_element
            self._heapify_down(0)
        
        return root
    
    def _heapify_down(self, index):
        n = len(self.data)

        while True:
            left_index = self._leftSide(index)
            right_index = self._rightSide(index)
            small = index

            if left_index < n and self.data[left_index].no_rm < self.data[small].no_rm:
                small = left_index
            if right_index < n and self.data[right_index].no_rm < self.data[small].no_rm:
                small = right_index
            if small != index:
                self.data[index], self.data[small] = self.data[small], self.data[index]
                index = small
            else:
                break

     # ---------- PEEK ----------
    
    def peek(self):
        return self.data[0] if not self.isEmpty() else None
    
    def size(self):
        return len(self.data)
    
    def display(self):
        if self.isEmpty():
            print("Heap is empty || Tumpukan Kosong || Size: 0")
            return
        
        for idx, pasien in enumerate(self.data):
            print(f"Index: {idx} || Data: {pasien} || Size: {self.size()}")

     # ---------- VISUALISASI ----------

    def displayHeap(self):
        if self.isEmpty():
            print("  (Heap kosong)")
            return
        
        n = len(self.data)
        level = 0
        while (2 ** level) - 1 < n:
            level += 1
        
        idx = 0
        lebar_terminal = 60
        for level in range(level):
            jumlah_node_level = min(2 ** level, n - idx)
            label_level = [f"{self.data[idx + i].prioritas}:{self.data[idx + i].nama}"
                           for i in range(jumlah_node_level)]
            baris = " ".join(label_level)
            spasi = max((lebar_terminal - len(baris)) // 2, 0)
            print(" " * spasi + baris)
            idx += jumlah_node_level
        
        print("  (Format label: [prioritas]:[nama pasien], root = paling atas/prioritas tertinggi)")
  



    