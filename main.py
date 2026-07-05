class Pasien:
    def __init__(self, id_pasien, nama, tingkat_keparahan=0):
        self.id_pasien = id_pasien
        self.nama = nama
        self.tingkat_keparahan = tingkat_keparahan # 1 (Ringan) - 3 (Gawat Darurat)
        self.status = "Menunggu"

    def __str__(self):
        return f"[ID: {self.id_pasien}] {self.nama} (Keparahan: {self.tingkat_keparahan})"

# ==========================================
# 1. QUEUE (Antrean Registrasi Awal - FIFO)
# ==========================================
import typing

class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next: typing.Any = None

class Queue:
    def __init__(self):
        self.front = self.rear = None

    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.rear is None:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    def peek(self):
        return self.front.data if self.front else None

    def display(self):
        if self.front is None:
            print("Antrean registrasi kosong.")
            return
        temp = self.front
        print("Antrean Registrasi:")
        while temp:
            print(f" -> {temp.data.nama}", end="")
            temp = temp.next
        print()

# ==========================================
# 2. AVL TREE (Database Rekam Medis)
# ==========================================
# FIX (bug #1): the original code used a plain BST. Because id_pasien is
# always assigned in increasing order and patients are always triaged in
# FIFO order, every insertion landed on the far right -> the "BST" always
# degenerated into a straight linked list (height == number of nodes,
# every search O(n) instead of O(log n)). An AVL tree rebalances itself
# after every insert so this can't happen, while keeping the exact same
# public interface (insert / search / inorder_traversal / get_height /
# count_nodes) so nothing else in SistemIGD needs to change.
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

# ==========================================
# 3. BINARY HEAP (Max-Heap Prioritas Dokter)
# ==========================================
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

# ==========================================
# 4. STACK (Riwayat Penanganan / Undo)
# ==========================================
class StackNode:
    def __init__(self, data):
        self.data = data
        self.next: typing.Any = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = StackNode(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        popped = self.top.data
        self.top = self.top.next
        return popped

    def display(self):
        if self.top is None:
            print("Riwayat penanganan kosong.")
            return
        temp = self.top
        print("Riwayat Penanganan Terakhir (LIFO):")
        while temp:
            print(f"- {temp.data}")
            temp = temp.next

# ==========================================
# SISTEM UTAMA (Integrasi Bisnis)
# ==========================================
class SistemIGD:
    def __init__(self):
        self.queue_registrasi = Queue()
        self.bst_rekam_medis = BST()
        self.heap_prioritas = MaxHeap()
        self.stack_riwayat = Stack()
        self.auto_id = 100

    def pasien_datang(self, nama):
        # 1. Pasien datang masuk Queue
        pasien_baru = Pasien(self.auto_id, nama)
        self.queue_registrasi.enqueue(pasien_baru)
        print(f"[*] Pasien {nama} masuk antrean registrasi.")
        self.auto_id += 1

    def proses_triage(self, tingkat_keparahan):
        # 2. Perawat memproses antrean (Queue -> BST & Heap)
        pasien = self.queue_registrasi.dequeue()
        if not pasien:
            print("[!] Tidak ada pasien di antrean registrasi.")
            return

        pasien.tingkat_keparahan = tingkat_keparahan

        # Simpan ke BST sebagai database
        self.bst_rekam_medis.insert(pasien)
        # Masukkan ke IGD berdasarkan prioritas (Heap)
        self.heap_prioritas.insert(pasien)

        print(f"[*] Triage Selesai: {pasien.nama} dimasukkan ke IGD dengan prioritas {tingkat_keparahan}.")

    def dokter_tangani_pasien(self):
        # 3. Dokter memanggil pasien prioritas tertinggi (Heap -> Stack)
        pasien = self.heap_prioritas.delete_root()
        if not pasien:
            print("[!] Tidak ada pasien yang menunggu di IGD.")
            return

        pasien.status = "Ditangani"
        self.stack_riwayat.push(pasien)
        print(f"[+] Dokter sedang menangani: {pasien.nama} (Prioritas: {pasien.tingkat_keparahan})")

    def batalkan_penanganan(self):
        # 4. Undo jika dokter salah panggil (Stack -> Heap)
        pasien = self.stack_riwayat.pop()
        if not pasien:
            print("[!] Tidak ada riwayat penanganan untuk dibatalkan.")
            return

        pasien.status = "Menunggu"
        self.heap_prioritas.insert(pasien)
        print(f"[-] Batal penanganan: {pasien.nama} dikembalikan ke antrean IGD.")

# ==========================================
# MENU CLI
# ==========================================
if __name__ == "__main__":
    sistem = SistemIGD()

    while True:
        print("\n=== SISTEM MANAJEMEN IGD RUMAH SAKIT ===")
        print("1. Pasien Baru Datang (Masuk Queue)")
        print("2. Proses Triage Pasien (Queue -> Heap & BST)")
        print("3. Dokter Tangani Pasien (Ambil dari Heap -> Stack)")
        print("4. Batalkan Penanganan Terakhir (Undo dari Stack)")
        print("5. Lihat Semua Antrean (Display Queue & Heap)")
        print("6. Lihat Database Rekam Medis (BST Inorder)")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            nama = input("Nama Pasien: ")
            sistem.pasien_datang(nama)
        elif pilihan == '2':
            if sistem.queue_registrasi.peek():
                print(f"Memproses: {sistem.queue_registrasi.peek().nama}") # type: ignore
                try:
                    keparahan = int(input("Masukkan tingkat keparahan (1-Ringan, 2-Sedang, 3-Gawat): "))
                    sistem.proses_triage(keparahan)
                except ValueError:
                    print("Input harus berupa angka!")
            else:
                print("Antrean registrasi kosong.")
        elif pilihan == '3':
            sistem.dokter_tangani_pasien()
        elif pilihan == '4':
            sistem.batalkan_penanganan()
        elif pilihan == '5':
            print("\n--- STATUS SAAT INI ---")
            sistem.queue_registrasi.display()
            sistem.heap_prioritas.display()
            sistem.stack_riwayat.display()
        elif pilihan == '6':
            print("\n--- DATABASE REKAM MEDIS (BST) ---")
            sistem.bst_rekam_medis.inorder_traversal(sistem.bst_rekam_medis.root)
            print(f"Total Pasien Terdaftar: {sistem.bst_rekam_medis.count_nodes(sistem.bst_rekam_medis.root)}")
        elif pilihan == '0':
            print("Keluar dari sistem. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")