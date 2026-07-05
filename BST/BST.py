import typing

class AVLNode:
    def __init__(self, data):
        self.data = data
        self.left: typing.Any = None
        self.right: typing.Any = None
        self.height = 1  # height of this node's own subtree (leaf = 1)

class BST:  # kept the name BST so the rest of the program doesn't need edits
    def __init__(self):
        self.root = None

    # ---------- public API (unchanged signatures) ----------
    def insert(self, data):
        self.root = self._insert_recursive(self.root, data)

    def search(self, id_pasien):
        return self._search_recursive(self.root, id_pasien)

    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            print(f"- {node.data}")
            self.inorder_traversal(node.right)

    def get_height(self, node):
        return self._h(node)

    def count_nodes(self, node):
        if node is None:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    # ---------- AVL internals ----------
    def _h(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._h(node.left) - self._h(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _rotate_right(self, z):
        y = z.left
        z.left = y.right
        y.right = z
        self._update_height(z)
        self._update_height(y)
        return y

    def _rotate_left(self, z):
        y = z.right
        z.right = y.left
        y.left = z
        self._update_height(z)
        self._update_height(y)
        return y

    def _insert_recursive(self, node, data):
        if node is None:
            return AVLNode(data)

        if data.id_pasien < node.data.id_pasien:
            node.left = self._insert_recursive(node.left, data)
        elif data.id_pasien > node.data.id_pasien:
            node.right = self._insert_recursive(node.right, data)
        else:
            return node  # duplicate id_pasien, ignore

        self._update_height(node)
        balance = self._balance_factor(node)

        # Left Left
        if balance > 1 and data.id_pasien < node.left.data.id_pasien:
            return self._rotate_right(node)
        # Right Right
        if balance < -1 and data.id_pasien > node.right.data.id_pasien:
            return self._rotate_left(node)
        # Left Right
        if balance > 1 and data.id_pasien > node.left.data.id_pasien:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right Left
        if balance < -1 and data.id_pasien < node.right.data.id_pasien:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _search_recursive(self, node, id_pasien):
        if node is None or node.data.id_pasien == id_pasien:
            return node
        if node.data.id_pasien < id_pasien:
            return self._search_recursive(node.right, id_pasien)
        return self._search_recursive(node.left, id_pasien)