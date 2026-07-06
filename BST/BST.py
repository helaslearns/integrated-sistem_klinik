class NodeBST:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None
        self._size = 0

     # ---------- INSERT ----------

    def insert(self, pasien):
        self.root = self._insert(self.root, pasien)

    def _insert(self, node, pasien):
        if node is None:
            self._size += 1
            return NodeBST(pasien)
        if pasien.no_rm < node.data.no_rm:
            node.left = self._insert(node.left, pasien)
        elif pasien.no_rm > node.data.no_rm:
            node.right = self._insert(node.right, pasien)
        else:
            node.pasien = pasien
        return node

     # ---------- SEARCH ----------

    def search(self, no_rm):
        return self._search(self.root, no_rm)
    
    def _search(self, node, no_rm):
        if node is None:
            return None
        if no_rm == node.data.no_rm:      # sebelumnya node.pasien.no_rm
            return node.data
        elif no_rm < node.data.no_rm:
            return self._search(node.left, no_rm)
        else:
            return self._search(node.right, no_rm)
            
     # ---------- DELETE ----------

    def delete(self, no_rm):
        self.root, deleted = self._delete(self.root, no_rm)
        return deleted

    def _delete(self, node, no_rm):
        if node is None:
            return node, False
 
        deleted = False
        if no_rm < node.pasien.no_rm:
            node.left, deleted = self._delete(node.left, no_rm)
        elif no_rm > node.pasien.no_rm:
            node.right, deleted = self._delete(node.right, no_rm)
        else:
            deleted = True
            # Kasus 1 & 2: node punya <= 1 anak
            if node.left is None:
                self._size -= 1
                return node.right, deleted
            elif node.right is None:
                self._size -= 1
                return node.left, deleted
            # Kasus 3: node punya 2 anak -> cari successor (terkecil di subtree kanan)
            successor = self._min_node(node.right)
            node.pasien = successor.pasien
            node.right, _ = self._delete(node.right, successor.pasien.no_rm)
        return node, deleted
    
    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node
    
     # ---------- TRAVERSAL: INORDER ----------

    def traverseInorder(self):
        hasil = []
        self._inorder(self.root, hasil)
        return hasil
    
    def _inorder(self, node, hasil):
        if node:
            self._inorder(node.left, hasil)
            hasil.append(node.pasien)
            self._inorder(node.right, hasil)
    
    # ---------- HEIGHT ----------

    def height(self):
        return self._height(self.root)
    
    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))
    
     # ---------- NODE COUNT ----------

    def nodeCount(self):
        return self._size
    
    def displayInorder(self):
        data = self.traverseInorder()
        if not data:
            print("BST is empty || BST Kosong || Size: 0")
            return
        for p in data:
            print(f"  RM-{p.no_rm} | {p.nama} | Keluhan: {p.keluhan} | "
                  f"Prioritas: {p.prioritas}")
            
     # ---------- VISUALISASI ----------

    def displayTree(self):
        if self.root is None:
            print("  (Tree kosong)")
            return
        self._display_tree(self.root, "", True)
 
    def _display_tree(self, node, prefix, is_tail):
        if node is None:
            return
        # subtree kanan digambar lebih dulu (muncul di atas)
        self._display_tree(node.right, prefix + ("    " if is_tail else "│   "), False)
        cabang = "└── " if is_tail else "┌── "
        print(f"  {prefix}{cabang}RM-{node.pasien.no_rm} ({node.pasien.nama})")
        # subtree kiri digambar setelahnya (muncul di bawah)
        self._display_tree(node.left, prefix + ("    " if is_tail else "│   "), True)

